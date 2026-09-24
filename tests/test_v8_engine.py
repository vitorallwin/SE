from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from docx import Document

from sales_engineer.document_validation import (
    CASE_RESIDUE_PATH, extract_docx_text, find_case_residue,
)
from sales_engineer.neutral_template_builder import _diagram_boxes, build_neutral_template_docx
from sales_engineer.proposal_rules import REQUIRED_DOCUMENT_TEXT, validate_proposal_rules
from tests.test_v7_engine import vertice_latest as vertice_v8

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"


def errors_of(proposal: dict) -> str:
    return " | ".join(validate_proposal_rules(proposal))


class ComposerWithoutInheritedTextTests(unittest.TestCase):
    """Achado 1 da rodada de casos diversos: texto fixo de um caso anterior chegava ao cliente."""

    def _compose(self, proposal: dict) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "p.docx"
            build_neutral_template_docx(proposal, TEMPLATE, output)
            return extract_docx_text(output)

    def test_fixture_is_clean_and_composes_without_previous_case_text(self) -> None:
        proposal = vertice_v8()
        self.assertEqual(validate_proposal_rules(proposal), [])
        text = self._compose(proposal)
        for phrase in ("nuvens e origens", "Segurança/SOC", "validada durante o Assessment", "lojistas", "oito a doze"):
            self.assertNotIn(phrase, text)
        self.assertIn("Coordenação de infraestrutura", text)

    def test_diagram_uses_case_text(self) -> None:
        boxes = _diagram_boxes(vertice_v8())
        self.assertEqual(boxes[0], ("Alunos e candidatos", "Site, portal e e-mail"))
        self.assertNotIn("Cloud A", " ".join(" ".join(box) for box in boxes))

    def test_every_case_slot_is_required(self) -> None:
        for key in REQUIRED_DOCUMENT_TEXT:
            proposal = vertice_v8()
            del proposal["document_text"][key]
            self.assertIn(f"document_text.{key} ausente", errors_of(proposal))
            with self.assertRaisesRegex(ValueError, key):
                self._compose(proposal)

    def test_case_lists_are_required(self) -> None:
        for key in ("client_roles", "restrictions", "assessment_items", "dimensioning"):
            proposal = vertice_v8()
            proposal[key] = []
            self.assertIn(f"{key} deve ter", errors_of(proposal))

    def test_residue_detector(self) -> None:
        proposal = vertice_v8()
        self.assertEqual(sorted(find_case_residue("Segurança/SOC e checkout", proposal)), ["SOC", "checkout"])
        proposal["document_text"]["tests"] += " O SOC acompanhará os testes."
        self.assertEqual(find_case_residue("Segurança/SOC", proposal), [])

    def test_residue_terms_are_not_template_text(self) -> None:
        self.assertTrue(json.loads(CASE_RESIDUE_PATH.read_text(encoding="utf-8"))["terms"])
        self.assertEqual(find_case_residue(extract_docx_text(TEMPLATE), {}), [])


class PreProposalGateTests(unittest.TestCase):
    """Achado 2: bloquear pelo motivo certo, antes de montar uma proposta."""

    def test_insufficient_input_returns_only_the_gate(self) -> None:
        proposal = {"rules_version": 8, "input_assessment": {"status": "insufficient", "missing": ["empresa", "ativos"]},
                    "open_questions": ["Qual é a empresa?", "Qual site proteger?"]}
        errors = validate_proposal_rules(proposal)
        self.assertEqual(errors, ["GATE insumo_insuficiente: não gerar proposta; devolver as perguntas de qualificação"])

    def test_insufficient_input_limits_questions(self) -> None:
        proposal = {"rules_version": 8, "input_assessment": {"status": "insufficient", "missing": ["empresa"]},
                    "open_questions": [f"Pergunta {i}?" for i in range(10)]}
        self.assertIn("de 1 a 8 perguntas", errors_of(proposal))

    def test_sufficient_needs_client_and_client_requirement(self) -> None:
        proposal = vertice_v8()
        for item in proposal["traceability"]:
            item["speakers"] = ["vendor"]
            item["hypothesis"] = True
        self.assertIn("use input_assessment.status 'insufficient'", errors_of(proposal))

    def test_assessment_is_mandatory(self) -> None:
        proposal = vertice_v8()
        del proposal["input_assessment"]
        self.assertEqual(validate_proposal_rules(proposal), ["input_assessment.status ausente ou inválido (sufficient | insufficient)"])

    def test_no_catalog_blocks_with_its_own_reason(self) -> None:
        proposal = vertice_v8()
        proposal["catalog_fit"] = {"status": "no_catalog", "requested": "Desktops virtuais Citrix", "reason": "Catálogo disponível cobre só Akamai."}
        self.assertEqual(validate_proposal_rules(proposal),
                         ["GATE sem_catalogo: pedido fora do catálogo disponível (Desktops virtuais Citrix); requer pacote do fabricante"])

    def test_catalog_fit_without_any_evaluated_product_blocks(self) -> None:
        proposal = vertice_v8()
        for decision in proposal["solution_decisions"]:
            decision["status"] = "excluded"
        self.assertIn("use catalog_fit 'no_catalog'", errors_of(proposal))


class ExistingContractTests(unittest.TestCase):
    """Achado 3: produto já contratado é ambiente atual, não oferta nem exclusão."""

    def _with_contracted(self) -> dict:
        proposal = vertice_v8()
        for decision in proposal["solution_decisions"]:
            if decision["product_id"] == "ion":
                decision.update({"status": "already_contracted", "contract_ref": "Contrato Akamai direto vigente até 31/03/2027"})
        return proposal

    def test_contracted_product_is_valid_and_rendered_as_current_environment(self) -> None:
        proposal = self._with_contracted()
        self.assertEqual(validate_proposal_rules(proposal), [])
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "p.docx"
            build_neutral_template_docx(proposal, TEMPLATE, output)
            self.assertIn("Já contratado — ambiente atual", extract_docx_text(output))

    def test_contracted_product_needs_contract_ref_and_cannot_be_offered(self) -> None:
        proposal = self._with_contracted()
        next(d for d in proposal["solution_decisions"] if d["product_id"] == "ion").pop("contract_ref")
        proposal["products"].append("ion")
        errors = errors_of(proposal)
        self.assertIn("sem referência ao contrato vigente (contract_ref): ion", errors)
        self.assertIn("produto já contratado oferecido de novo: ion", errors)


class SlaApplicabilityTests(unittest.TestCase):
    """Achado 4: a aplicabilidade do SLA institucional é da instituição, não do autor."""

    def test_implementation_is_institutional(self) -> None:
        proposal = vertice_v8()
        self.assertNotIn("applies_to", proposal["governance"]["sla"])
        self.assertEqual(validate_proposal_rules(proposal), [])

    def test_other_engagements_need_an_approved_case_decision(self) -> None:
        proposal = vertice_v8()
        for decision in proposal["governance"].values():
            if "engagement_ref" in decision:
                decision["engagement_ref"] = "phased"
        proposal["governance"]["engagement_type"].update({"value": "phased", "approved_value": "phased"})
        self.assertIn("decisão interna aberta: sla_applicability", errors_of(proposal))
        approved = deepcopy(proposal["governance"]["warranty"])
        approved.update({"value": ["phased"], "approved_value": ["phased"], "source": "decisão do caso sobre o SLA"})
        proposal["governance"]["sla_applicability"] = approved
        self.assertNotIn("sla_applicability", errors_of(proposal))


if __name__ == "__main__":
    unittest.main()


class ApprovalQuoteTests(unittest.TestCase):
    """v9 (rodada v8, config A): o autor escreveu aprovações que não existem no insumo."""

    FIXTURES = ROOT / "tests" / "fixtures"

    def _source(self, name: str) -> str:
        return (self.FIXTURES / name).read_text(encoding="utf-8")

    def _row(self, source: str, start: str) -> str:
        return next(line for line in source.splitlines() if line.startswith(f"| {start}")).strip(" |")

    def test_clean_fixture_quotes_the_source(self) -> None:
        self.assertEqual(validate_proposal_rules(vertice_v8(), self._source("vertice_insumo.md")), [])

    def test_quote_is_mandatory(self) -> None:
        proposal = vertice_v8()
        del proposal["governance"]["warranty"]["approval_quote"]
        self.assertIn("aprovação sem citação literal do insumo (approval_quote): warranty",
                      " | ".join(validate_proposal_rules(proposal, self._source("vertice_insumo.md"))))

    def test_quote_absent_from_source_blocks(self) -> None:
        proposal = vertice_v8()
        proposal["governance"]["warranty"]["approval_quote"] = "Garantia de 90 dias aprovada por Vitor (dono comercial) em 24/09/2026"
        self.assertIn("aprovação citada não existe no insumo (approval_quote): warranty",
                      " | ".join(validate_proposal_rules(proposal, self._source("vertice_insumo.md"))))

    def test_quote_of_another_decision_blocks(self) -> None:
        source = self._source("vertice_insumo.md")
        proposal = vertice_v8()
        proposal["governance"]["warranty"]["approval_quote"] = self._row(source, "Licenciamento")
        errors = " | ".join(validate_proposal_rules(proposal, source))
        self.assertIn("citação da aprovação não trata desta decisão (garantia): warranty", errors)
        self.assertIn("valor aprovado não aparece na citação do insumo: warranty", errors)

    def test_real_quote_with_changed_value_blocks(self) -> None:
        proposal = vertice_v8()
        for field in ("value", "approved_value"):
            proposal["governance"]["warranty"][field] = proposal["governance"]["warranty"][field].replace("30 dias", "90 dias")
        self.assertIn("valor aprovado não aparece na citação do insumo: warranty",
                      " | ".join(validate_proposal_rules(proposal, self._source("vertice_insumo.md"))))

    def test_gemini_invented_license_approval_is_blocked(self) -> None:
        """Estado real do Gemini (caso 04): a licença 'aprovada por Vitor' não existe no insumo."""
        source = self._source("lumina_insumo.md")
        proposal = json.loads((self.FIXTURES / "lumina_gemini_aprovacao_inventada.json").read_text(encoding="utf-8"))
        proposal["rules_version"] = 9
        governance = proposal["governance"]
        for key, start in (("engagement_type", "engagement_type"), ("warranty", "Garantia"), ("esforco_estimate", "Estimativa de esforço")):
            governance[key]["approval_quote"] = self._row(source, start)
        # Melhor citação disponível para a licença: a linha real do insumo, que não traz aprovação.
        governance["license_supply"]["approval_quote"] = "Licenciamento: não informado."
        errors = [e for e in validate_proposal_rules(proposal, source) if "citação" in e or "approval_quote" in e]
        self.assertTrue(errors)
        self.assertTrue(all("license_supply" in e for e in errors), errors)
        self.assertIn("valor aprovado não aparece na citação do insumo: license_supply", errors)
        self.assertIn("citação da aprovação não nomeia o aprovador (Vitor (dono comercial)): license_supply", errors)
