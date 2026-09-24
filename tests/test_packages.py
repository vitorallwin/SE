from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from sales_engineer.catalog import FRONT_GROUPS, PACKAGES, PACKAGES_DIR, PRODUCTS
from sales_engineer.document_validation import extract_docx_text
from sales_engineer.neutral_template_builder import build_neutral_template_docx
from sales_engineer.proposal_rules import validate_proposal_rules

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"


def telecom() -> dict:
    return json.loads((FIXTURES / "packages_telecom_teste.json").read_text(encoding="utf-8"))


def source() -> str:
    return (FIXTURES / "packages_telecom_insumo.md").read_text(encoding="utf-8")


def errors_of(proposal: dict) -> str:
    return " | ".join(validate_proposal_rules(proposal, source()))


class PackageCatalogTests(unittest.TestCase):
    """O catálogo é a união dos pacotes de fabricante; cada pacote é autocontido."""

    def test_packages_are_complete(self) -> None:
        self.assertEqual(set(PACKAGES), {"akamai", "sentinelone", "fortinet", "veeam", "populos_services"})
        for package_id, package in PACKAGES.items():
            self.assertTrue((PACKAGES_DIR / package_id / "gating.md").exists(), package_id)
            self.assertIn(package["status"], {"validated", "draft"})
            for members in package["fronts"].values():
                self.assertTrue(set(members) <= set(package["products"]), package_id)
            for product_id, product in package["products"].items():
                self.assertTrue(product["name"] and product["summary"] and product["capabilities"], product_id)
                self.assertEqual(PRODUCTS[product_id]["vendor"], package["vendor"])

    def test_akamai_stays_validated_and_new_packages_are_drafts(self) -> None:
        self.assertEqual(PACKAGES["akamai"]["status"], "validated")
        self.assertEqual({p for p, pkg in PACKAGES.items() if pkg["status"] == "draft"}, {"sentinelone", "fortinet", "veeam", "populos_services"})
        self.assertIn("endpoint", FRONT_GROUPS)


class MultiVendorProposalTests(unittest.TestCase):
    """Proposta de endpoint + sustentação: emite em teste, com o fabricante e os termos de suporte no documento."""

    def test_emits_with_vendor_and_support_terms(self) -> None:
        proposal = telecom()
        self.assertEqual(validate_proposal_rules(proposal, source()), [])
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "p.docx"
            build_neutral_template_docx(proposal, TEMPLATE, output)
            text = extract_docx_text(output)
        self.assertIn("Sobre a SentinelOne", text)
        self.assertIn("Parceria POPULOS e SentinelOne", text)
        self.assertIn("4.2 Componentes e posição na proposta", text)
        self.assertIn("A sustentação segue os termos aprovados para esta proposta: atendimento em dias úteis", text)
        self.assertNotIn("NOC 24x7", text)
        self.assertNotIn("Akamai", text)
        self.assertNotIn("serviços de borda", text)

    def test_draft_package_blocks_production(self) -> None:
        proposal = telecom()
        proposal["data_mode"] = "production"
        self.assertIn("pacote sentinelone em rascunho", errors_of(proposal))

    def test_continuous_service_needs_approved_support_terms(self) -> None:
        proposal = telecom()
        proposal["governance"]["support_terms"] = {"state": "populos_internal_decision", "value": None, "source": "sem decisão"}
        errors = validate_proposal_rules(proposal, source())
        self.assertEqual([e for e in errors if "support_terms" in e], ["decisão interna aberta: support_terms"])
        del proposal["governance"]["support_terms"]
        self.assertIn("decisão interna aberta: support_terms (exigida por", errors_of(proposal))

    def test_support_quote_must_be_literal(self) -> None:
        proposal = telecom()
        proposal["governance"]["support_terms"]["approval_quote"] = "Mariana Costa aprova suporte 24x7 com resposta em 1 hora para tudo."
        self.assertIn("support_terms", errors_of(proposal))

    def test_at_most_three_fronts(self) -> None:
        proposal = telecom()
        for product_id in ("veeam_vbr", "edge_dns"):
            proposal["solution_decisions"].append({"product_id": product_id, "status": "recommended", "requirement_ids": ["REQ-05"],
                                                   "rationale": "teste", "client_summary": "teste", "capabilities": ["x"]})
        proposal["solution_decisions"] = [d for d in proposal["solution_decisions"] if not (d["product_id"] == "veeam_vbr" and d["status"] == "already_contracted")]
        self.assertIn("o template comporta 3", errors_of(proposal))

    def test_legacy_about_akamai_slot_still_accepted(self) -> None:
        proposal = telecom()
        proposal["document_text"]["about_akamai"] = proposal["document_text"].pop("about_vendor")
        self.assertNotIn("about_vendor", errors_of(proposal))


if __name__ == "__main__":
    unittest.main()
