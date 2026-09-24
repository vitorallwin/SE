from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw

from sales_engineer.document_validation import extract_docx_text
from sales_engineer.feasibility import compute, day_months, paragraph, stabilization_days
from sales_engineer.neutral_template_builder import BOLD_FONTS, REGULAR_FONTS, _font, _wrap, build_neutral_template_docx
from sales_engineer.proposal_rules import validate_proposal_rules
from sales_engineer.violation_codes import code_of
from tests.test_v7_engine import vertice_latest, vertice_source

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"


def errors_of(proposal: dict) -> str:
    return " | ".join(validate_proposal_rules(proposal, vertice_source()))


def expansion_case() -> dict:
    """Números do caso 09 da bateria 2: congelamento em 15/12, licença em até 2 semanas, implantação de 4 a 5."""
    return {
        "proposal_date": "2026-09-24",
        "delivery": {"phases": [{"name": "Implantação", "weeks": [4, 5]}]},
        "critical_events": [{"name": "Lançamento", "kind": "event", "date": "2027-01-15"},
                            {"name": "Congelamento", "kind": "freeze", "date": "2026-12-15"}],
        "event_feasibility": [{"event": "Lançamento", "freeze": "Congelamento", "path": ["licenciamento", "Implantação"],
                               "lead_times": {"licenciamento": {"label": "Liberação da licença", "weeks": [1, 2], "source": "e-mail"}}}],
    }


class EngineDatesTests(unittest.TestCase):
    """N1, N2 e A4: toda data vem do código, com prazo de licença, congelamento e folga."""

    def test_expansion_deadline_is_the_audited_one(self) -> None:
        result = compute(expansion_case())[0]
        self.assertEqual(str(result.start_deadline), "2026-10-27")  # 15/12 − 5 semanas − 2 semanas
        self.assertEqual(result.classification, "fits")
        self.assertEqual((str(result.end_earliest), str(result.end_latest)), ("2026-10-29", "2026-11-12"))

    def test_license_lead_time_is_part_of_the_window(self) -> None:
        without_license = expansion_case()
        feasibility = without_license["event_feasibility"][0]
        feasibility["path"], feasibility["lead_times"] = ["Implantação"], {}
        self.assertEqual(str(compute(without_license)[0].start_deadline), "2026-11-10")
        self.assertEqual(str(compute(expansion_case())[0].start_deadline), "2026-10-27")

    def test_declared_lead_time_must_be_on_the_path(self) -> None:
        proposal = expansion_case()
        proposal["event_feasibility"][0]["path"] = ["Implantação"]
        self.assertIn("prazo declarado fora do caminho até o evento: licenciamento", compute(proposal)[0].errors[0])

    def test_approved_stabilization_buffer_moves_the_deadline(self) -> None:
        proposal = expansion_case()
        proposal["governance"] = {"stabilization_buffer": {"state": "commitment", "value": "5 dias úteis de estabilização"}}
        self.assertEqual(stabilization_days(proposal), 7)
        self.assertEqual(str(compute(proposal)[0].start_deadline), "2026-10-20")

    def test_no_default_buffer_becomes_a_caveat(self) -> None:
        result = compute(expansion_case())[0]
        self.assertIn("não há folga de estabilização aprovada", " ".join(result.caveats))

    def test_unknown_freeze_date_is_conditional_with_caveat(self) -> None:
        result = compute(vertice_latest())[0]
        self.assertEqual(result.classification, "conditional")
        self.assertIn("não foi informada", " ".join(result.caveats))
        self.assertEqual(str(result.step_deadlines["Ativação das licenças Edge DNS"]), "2026-12-14")

    def test_same_inputs_same_dates(self) -> None:
        texts = {paragraph(compute(deepcopy(expansion_case()))[0]) for _ in range(3)}
        self.assertEqual(len(texts), 1)

    def test_author_date_without_origin_blocks(self) -> None:
        proposal = vertice_latest()
        summary = next(s for s in proposal["sections"] if s["title"].casefold() == "resumo executivo")
        summary["paragraphs"].append("O término ficaria entre 15/10/2026 e 22/10/2026.")
        errors = errors_of(proposal)
        self.assertIn("data 15/10 em texto do cliente sem origem", errors)
        self.assertIn("data 22/10 em texto do cliente sem origem", errors)

    def test_source_and_engine_dates_are_allowed(self) -> None:
        proposal = vertice_latest()
        summary = next(s for s in proposal["sections"] if s["title"].casefold() == "resumo executivo")
        summary["paragraphs"].append("As matrículas começam em 11 de janeiro, e as licenças precisam estar ativas até 14/12/2026.")
        self.assertEqual(validate_proposal_rules(proposal, vertice_source()), [])

    def test_engine_paragraph_reaches_the_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "p.docx"
            build_neutral_template_docx(vertice_latest(), TEMPLATE, output)
            text = extract_docx_text(output)
        self.assertIn('Prazo limite para a etapa "Ativação das licenças Edge DNS": 14/12/2026', text)

    def test_written_dates_are_recognized(self) -> None:
        self.assertEqual(day_months("1º de março, 2026-12-15 e 11/01"), {(1, 3), (15, 12), (11, 1)})


class PhaseScopeTests(unittest.TestCase):
    """A2 e N3: SLA e itens de prontidão declaram a fase ou opção a que pertencem."""

    def test_readiness_item_needs_a_phase(self) -> None:
        proposal = vertice_latest()
        proposal["event_readiness"][0]["phase"] = "Fase inexistente"
        self.assertIn("item de prontidão sem fase ou opção válida", errors_of(proposal))

    def test_readiness_is_rendered_with_its_phase(self) -> None:
        proposal = vertice_latest()
        item = proposal["event_readiness"][0]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "p.docx"
            build_neutral_template_docx(proposal, TEMPLATE, output)
            self.assertIn(f"{item['phase']}: {item['text']}", extract_docx_text(output))

    def test_sla_scope_is_rendered(self) -> None:
        proposal = vertice_latest()
        last = proposal["delivery"]["phases"][-1]["name"]
        approved = deepcopy(proposal["governance"]["warranty"])
        approved.update({"value": [last], "approved_value": [last], "applies_to_phases": [last]})
        proposal["governance"]["sla_applicability"] = approved
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "p.docx"
            proposal["governance"]["engagement_type"]["value"] = "implementation"
            build_neutral_template_docx(proposal, TEMPLATE, output)
            self.assertIn(f"aplica-se somente a: {last}", extract_docx_text(output))


class OptionalRangeTests(unittest.TestCase):
    """A3: a faixa de uma onda opcional pode ser escrita como foi aprovada."""

    def test_optional_wave_range_is_accepted(self) -> None:
        proposal = vertice_latest()
        proposal["optional_phase"] = {"title": "Fase 2", "waves": [{"id": "fase-2", "name": "Fase 2", "components": [], "weeks": [6, 8]}]}
        proposal["document_text"]["schedule_sequence"] += " A Fase 2, opcional, leva de 6 a 8 semanas."
        self.assertNotIn("diverge da soma das fases", errors_of(proposal))


class ClientClarificationTests(unittest.TestCase):
    """N4: contradição no documento do cliente é pedido de esclarecimento, não decisão da POPULOS."""

    def test_clarification_needs_the_question(self) -> None:
        proposal = vertice_latest()
        proposal["traceability"].append({"requirement_id": "REQ-99", "requirement": "Prazo de implantação de 30 dias corridos (item 5.2) e 60 dias (item 9.1)",
                                         "solution": "A esclarecer", "source": "TR", "speakers": ["input_document"], "hypothesis": False})
        proposal["standard_conflicts"] = [{"category": "deadline", "requirement_id": "REQ-99", "status": "client_clarification",
                                           "clarification_question": "Qual prazo prevalece: 30 dias (5.2) ou 60 dias (9.1)?"}]
        self.assertIn("contradição do cliente sem pedido de esclarecimento", errors_of(proposal))
        proposal["open_questions"].append("Qual prazo prevalece: 30 dias (5.2) ou 60 dias (9.1)?")
        self.assertNotIn("REQ-99", errors_of(proposal))


class InstitutionalStandardsTests(unittest.TestCase):
    """A1: o autor enxerga os valores da tabela institucional, versionados com o template."""

    def test_skill_carries_the_template_sla_values(self) -> None:
        from scripts.export_institutional_standards import TARGET, institutional_standards
        self.assertEqual(json.loads(TARGET.read_text(encoding="utf-8")), institutional_standards())
        severities = {s["severity"]: (s["response"], s["resolution"]) for s in institutional_standards()["sla"]["severities"]}
        self.assertEqual(severities["ALTA"], ("Até 1 hora", "Até 4 horas"))
        self.assertEqual(severities["MÉDIA"], ("Até 2 horas", "Até 8 horas"))


class DiagramWrapTests(unittest.TestCase):
    """V1: rótulo longo quebra a linha em vez de encolher até ficar ilegível."""

    def test_long_label_wraps_at_readable_size(self) -> None:
        draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        label = "Datacenter próprio (principal) e nuvem pública (contingência automática)"
        font = _font(REGULAR_FONTS, 24)
        lines = _wrap(draw, label, font, 330)
        self.assertLessEqual(len(lines), 3)
        self.assertTrue(all(draw.textbbox((0, 0), line, font=font)[2] <= 330 for line in lines))

    def test_diagram_labels_are_length_limited(self) -> None:
        proposal = vertice_latest()
        proposal["document_text"]["diagram_origins"] = "x" * 81
        self.assertIn("formato (document_text.diagram_origins)", errors_of(proposal))


class ViolationCodeTests(unittest.TestCase):
    """N5: códigos estáveis para agregar violações por execução."""

    def test_codes(self) -> None:
        self.assertEqual(code_of("decisão interna aberta: warranty"), "DECISAO-ABERTA")
        self.assertEqual(code_of("data 15/10 em texto do cliente sem origem no insumo nem no cálculo do motor: sections"), "DATA-SEM-ORIGEM")
        self.assertEqual(code_of("GATE sem_catalogo: pedido fora do catálogo"), "GATE-CATALOGO")
        self.assertEqual(code_of("formato (x): y"), "FORMATO")


if __name__ == "__main__":
    unittest.main()
