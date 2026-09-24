from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from datetime import date
from pathlib import Path

from scripts.generate_nexuspay_v5 import CASE_DECISIONS as V5_DECISIONS
from scripts.generate_nexuspay_v6 import CASE_DECISIONS, ESTIMATE_OWNER
from sales_engineer.demo_case_nexuspay_v6 import build_nexuspay_v6
from sales_engineer.document_validation import extract_docx_text
from sales_engineer.neutral_template_builder import build_neutral_template_docx
from sales_engineer.proposal_rules import phase_window, validate_proposal_rules


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"
SOURCE = ROOT / "data" / "proposals" / "20260923-e54ccb6.json"


def resolved_v6() -> dict:
    proposal = build_nexuspay_v6(json.loads(SOURCE.read_text(encoding="utf-8")))
    proposal["governance"].update(deepcopy(CASE_DECISIONS))
    for estimate in proposal["estimates"]:
        estimate["owner"] = ESTIMATE_OWNER
    return proposal


class V6RulesTests(unittest.TestCase):
    def assertViolation(self, proposal: dict, fragment: str) -> None:
        errors = validate_proposal_rules(proposal)
        self.assertTrue(any(fragment in error for error in errors), f"esperado '{fragment}' em {errors}")

    def test_resolved_v6_state_has_no_violations(self) -> None:
        self.assertEqual(validate_proposal_rules(resolved_v6()), [])

    # Decisões aprovadas, sem edição e presas ao engajamento
    def test_v5_style_decisions_do_not_pass_v6(self) -> None:
        proposal = resolved_v6()
        proposal["governance"].update(deepcopy(V5_DECISIONS))
        self.assertViolation(proposal, "decisão sem aprovador e data: engagement_type")
        self.assertViolation(proposal, "decisão com origem pendente de confirmação: phase1_estimate")

    def test_edited_decision_text_blocks(self) -> None:
        proposal = resolved_v6()
        proposal["governance"]["license_supply"]["value"] = "As licenças da Fase 2 serão fornecidas pela POPULOS."
        self.assertViolation(proposal, "texto da decisão difere do valor aprovado: license_supply")

    def test_engagement_change_invalidates_dependent_decisions(self) -> None:
        proposal = resolved_v6()
        proposal["governance"]["engagement_type"].update({"value": "implementation", "approved_value": "implementation"})
        self.assertViolation(proposal, "decisão tomada para outro engajamento (phased ≠ implementation): warranty")

    def test_sla_must_be_applicable_to_engagement(self) -> None:
        proposal = resolved_v6()
        proposal["governance"]["sla"]["applies_to"] = ["implementation"]
        self.assertViolation(proposal, "SLA não declarado aplicável ao engajamento phased")

    # Proveniência por falante
    def test_vendor_only_requirement_must_be_hypothesis(self) -> None:
        proposal = resolved_v6()
        proposal["traceability"][2]["speakers"] = ["vendor"]
        self.assertViolation(proposal, "só na fala do fabricante sem marcação de hipótese: REQ-03")
        proposal["traceability"][2]["hypothesis"] = True
        self.assertEqual(validate_proposal_rules(proposal), [])

    def test_speakers_are_derived_from_transcript(self) -> None:
        by_id = {item["requirement_id"]: item["speakers"] for item in resolved_v6()["traceability"]}
        self.assertEqual(by_id["REQ-03"], ["client", "input_document", "vendor"])
        self.assertEqual(by_id["REQ-08"], ["client"])

    # Limite de escopo × entregas contratadas
    def test_committed_criteria_cannot_require_forbidden_actions(self) -> None:
        proposal = resolved_v6()
        proposal["acceptance_criteria"][0]["criterion"] += " Reversão testável."
        self.assertViolation(proposal, "ação proibida pelo limite de escopo ('testável')")

    # Viabilidade da Black Friday calculada agora
    def test_phase_window_arithmetic(self) -> None:
        earliest, latest = phase_window(date(2026, 9, 24), [{"weeks": [3, 4]}, {"weeks": [3, 4]}])
        self.assertEqual((earliest, latest), (date(2026, 11, 5), date(2026, 11, 19)))

    def test_declared_window_must_match_calculation(self) -> None:
        proposal = resolved_v6()
        proposal["event_feasibility"][0]["phase1_end_latest"] = "2026-11-05"
        self.assertViolation(proposal, "janela da Fase 1 declarada diverge do cálculo")

    def test_summary_must_declare_event_feasibility(self) -> None:
        proposal = resolved_v6()
        proposal["sections"][0]["paragraphs"].pop()
        self.assertViolation(proposal, "sumário não declara a viabilidade do evento")

    def test_phase1_after_event_forces_does_not_fit(self) -> None:
        proposal = resolved_v6()
        proposal["event_feasibility"][0]["classification"] = "partially_fits"
        proposal["critical_events"][0]["date"] = "2026-11-01"
        self.assertViolation(proposal, "a viabilidade não é 'não cabe'")

    def test_event_without_date_needs_question(self) -> None:
        proposal = resolved_v6()
        proposal["critical_events"][1].pop("pending_question")
        self.assertViolation(proposal, "evento sem data e sem pergunta pendente: Pix Day")

    # Trilha rápida
    def test_fast_track_declares_production_change_and_freeze(self) -> None:
        proposal = resolved_v6()
        proposal["fast_track"].update({"production_change": False, "deadline_reference": "event", "controls": ["janela"], "first_question": ""})
        proposal["fast_track"]["components"].append("prolexic")
        errors = " ".join(validate_proposal_rules(proposal))
        for fragment in ("mudança em produção", "antes do congelamento", "controle próprio: reversão", "hostnames", "não pode prometer Prolexic"):
            self.assertIn(fragment, errors)


class V6DocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.directory = tempfile.TemporaryDirectory()
        output = Path(cls.directory.name) / "v6.docx"
        build_neutral_template_docx(resolved_v6(), TEMPLATE, output)
        cls.text = extract_docx_text(output)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.directory.cleanup()

    def test_supply_box_states_phase1_needs_no_licenses_and_keeps_approved_text(self) -> None:
        self.assertIn("A Fase 1 é exclusivamente de serviços e não requer licenças Akamai.", self.text)
        self.assertIn(CASE_DECISIONS["license_supply"]["value"], self.text)

    def test_fast_track_and_black_friday_declared(self) -> None:
        self.assertIn("6.4 Trilha rápida opcional", self.text)
        self.assertIn("Entrar na borda Akamai já é uma mudança em produção", self.text)
        self.assertIn("termina entre 05/11 e 19/11", self.text)

    def test_contradictions_removed(self) -> None:
        for term in ("sob carga e geografia definidas", "reversão testável", "4 a 6", "quatro a seis"):
            self.assertNotIn(term, self.text)
        self.assertIn("contas comprometidas ou fraude após o login", self.text)


if __name__ == "__main__":
    unittest.main()
