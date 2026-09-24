from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from docx import Document

from sales_engineer.case_runner import validate_state
from sales_engineer.document_validation import extract_docx_text
from sales_engineer.neutral_template_builder import _product_names_in, build_neutral_template_docx
from sales_engineer.proposal_rules import REQUIRED_DOCUMENT_TEXT_V10, validate_proposal_rules
from tests.test_v7_engine import vertice_latest, vertice_source

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"


def errors_of(proposal: dict) -> str:
    return " | ".join(validate_proposal_rules(proposal, vertice_source()))


def compose(proposal: dict) -> Document:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "p.docx"
        build_neutral_template_docx(proposal, TEMPLATE, output)
        return Document(output)


def trace_rows(document: Document) -> list[list[str]]:
    table = next(t for t in document.tables if t.rows[0].cells[0].text == "Requisito")
    return [[cell.text for cell in row.cells] for row in table.rows]


class ClientFacingTextTests(unittest.TestCase):
    """Auditoria v8.3, itens 2 a 4."""

    def test_fixture_is_clean(self) -> None:
        self.assertEqual(validate_proposal_rules(vertice_latest(), vertice_source()), [])

    def test_catalog_id_never_reaches_the_client(self) -> None:
        proposal = vertice_latest()
        proposal["traceability"][0]["solution"] = "edge_dns com DNSSEC"
        self.assertIn("identificador interno de produto em texto do cliente (edge_dns): traceability.REQ-01", errors_of(proposal))
        # Defesa em profundidade: o compositor também traduz ids na coluna de componente.
        self.assertEqual(_product_names_in("edge_dns + app_api_protector; gtm"), "Edge DNS + App & API Protector; Global Traffic Management")

    def test_matrix_column_shows_acceptance_not_source(self) -> None:
        proposal = vertice_latest()
        rows = trace_rows(compose(proposal))
        self.assertEqual(rows[0], ["Requisito", "Necessidade", "Componente", "Evidência de aceite"])
        criteria = {c["requirement_id"]: c["criterion"] for c in proposal["acceptance_criteria"] if c.get("phase", "committed") == "committed"}
        for row, item in zip(rows[1:], proposal["traceability"]):
            self.assertNotEqual(row[3], item.get("evidence"))
            if item["requirement_id"] in criteria:
                self.assertIn(criteria[item["requirement_id"]], row[3])

    def test_no_template_text_outside_the_case(self) -> None:
        text = extract_docx_text_of(vertice_latest())
        for phrase in ("future state", "segurança de aplicações", "gestão global de tráfego", "Continuidade e desempenho das jornadas digitais"):
            self.assertNotIn(phrase, text)
        self.assertIn("DNS autoritativo resiliente e independente do registrador", text)

    def test_every_new_slot_is_required(self) -> None:
        for key in REQUIRED_DOCUMENT_TEXT_V10:
            proposal = vertice_latest()
            del proposal["document_text"][key]
            self.assertIn(f"document_text.{key} ausente", errors_of(proposal))
        proposal = vertice_latest()
        del proposal["document_text"]["front_titles"]["continuity"]
        self.assertIn("front_titles.continuity ausente", errors_of(proposal))
        proposal = vertice_latest()
        proposal["team_competencies"] = []
        self.assertIn("team_competencies deve ter de 1 a 3", errors_of(proposal))


def extract_docx_text_of(proposal: dict) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "p.docx"
        build_neutral_template_docx(proposal, TEMPLATE, output)
        return extract_docx_text(output)


class SchemaFirstTests(unittest.TestCase):
    """Auditoria v8.3, item 8: o que o validador aceita, o compositor monta."""

    MUTATIONS = [
        ("delivery", "responsibilities", ["texto solto"]),
        ("delivery", "phases", [{"name": "Fase", "weeks": "3 a 4", "objective": "x"}]),
        (None, "dimensioning", [["só", "três", "colunas"]]),
        (None, "sections", {"Resumo executivo": ["x"]}),
        (None, "populos_roles", [["Papel", "Resp"]]),
        (None, "acceptance_criteria", [{"requirement_id": "REQ-01", "phase": "committed", "criterion": 3}]),
        (None, "solution_decisions", [{"product_id": "edge_dns", "status": "recomendado"}]),
        (None, "document_text", {"about_solution": ["lista"]}),
    ]

    def test_shape_errors_are_violations_never_exceptions(self) -> None:
        for parent, key, value in self.MUTATIONS:
            proposal = vertice_latest()
            (proposal[parent] if parent else proposal)[key] = value
            errors = validate_state(proposal, vertice_source())
            self.assertTrue(errors, key)
            self.assertTrue(all(e.startswith("formato (") for e in errors), (key, errors))

    def test_schema_ships_with_the_skill(self) -> None:
        schema = ROOT / "skills" / "akamai-proposal-authoring" / "references" / "state.schema.json"
        self.assertEqual(json.loads(schema.read_text(encoding="utf-8"))["$id"], "populos/proposal-state/v11")


class ProportionalEventPlanTests(unittest.TestCase):
    """Auditoria v8.3, item 5."""

    def test_heavy_readiness_without_traffic_path_product_blocks(self) -> None:
        proposal = vertice_latest()
        proposal["event_readiness"].append({"text": "Sala de crise no início das matrículas;", "phase": proposal["delivery"]["phases"][-1]["name"]})
        self.assertIn("plano de evento desproporcional ao escopo", errors_of(proposal))

    def test_heavy_readiness_is_fine_with_traffic_path_product(self) -> None:
        proposal = vertice_latest()
        proposal["event_readiness"].append({"text": "Sala de crise no início das matrículas;", "phase": proposal["delivery"]["phases"][-1]["name"]})
        next(d for d in proposal["solution_decisions"] if d["product_id"] == "app_api_protector")["status"] = "recommended"
        self.assertNotIn("plano de evento desproporcional", errors_of(proposal))


class StandardConflictTests(unittest.TestCase):
    """Auditoria v8.3, item 7: nas categorias conhecidas, o código obriga a classificar."""

    def _with_client_demand(self, text: str) -> dict:
        proposal = vertice_latest()
        proposal["traceability"].append({"requirement_id": "REQ-99", "requirement": text, "solution": "A definir",
                                         "source": "e-mail", "speakers": ["client"], "hypothesis": False})
        return proposal

    def test_unclassified_demand_blocks(self) -> None:
        proposal = self._with_client_demand("Garantia de 12 meses após o aceite definitivo")
        self.assertIn("sem classificação (standard_conflicts, warranty): REQ-99", errors_of(proposal))

    def test_conflict_needs_a_governance_decision(self) -> None:
        proposal = self._with_client_demand("Tempo de resolução de 30 minutos para incidentes críticos")
        proposal["standard_conflicts"] = [{"category": "sla", "requirement_id": "REQ-99", "status": "conflict", "decision_key": "sla_resolution"}]
        self.assertIn("conflito com padrão POPULOS sem decisão de governança", errors_of(proposal))
        proposal["governance"]["sla_resolution"] = {"state": "populos_internal_decision", "value": None, "source": "TR 7.2"}
        errors = errors_of(proposal)
        self.assertNotIn("sem decisão de governança", errors)
        self.assertIn("decisão interna aberta: sla_resolution", errors)

    def test_compatible_needs_a_reason(self) -> None:
        proposal = self._with_client_demand("Prazo de implantação de 30 dias corridos")
        proposal["standard_conflicts"] = [{"category": "deadline", "requirement_id": "REQ-99", "status": "compatible"}]
        self.assertIn("compatível com padrão POPULOS sem motivo", errors_of(proposal))
        proposal["standard_conflicts"][0]["reason"] = "A estimativa aprovada de 3 a 4 semanas cabe nos 30 dias."
        self.assertNotIn("REQ-99", errors_of(proposal))


class ApprovalQuoteRobustnessTests(unittest.TestCase):
    """Auditoria v8.3: citação de e-mail (>), quebras de linha e espaços não decidem a comparação."""

    def test_email_quoted_approval_matches(self) -> None:
        proposal = vertice_latest()
        warranty = proposal["governance"]["warranty"]
        source = vertice_source() + "\n\n> De: Vitor (dono comercial)\n> Aprovo a Garantia:\n>   " + warranty["value"].replace(" por ", "\n> por ") + "\n"
        warranty["approval_quote"] = "Vitor (dono comercial) Aprovo a Garantia: " + warranty["value"]
        errors = [e for e in validate_proposal_rules(proposal, source) if "warranty" in e]
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
