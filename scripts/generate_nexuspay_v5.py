from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sales_engineer.demo_case_nexuspay_v5 import build_nexuspay_v5
from sales_engineer.neutral_template_builder import build_neutral_template_docx
from sales_engineer.proposal_rules import validate_proposal_rules


SOURCE = ROOT / "data" / "proposals" / "20260923-e54ccb6.json"
STATE = ROOT / "data" / "proposals" / "nexuspay-competitive-v5.json"
OUTPUT = ROOT / "data" / "generated" / "POPULOS-Proposta-Tecnica-NexusPay-Competitiva-v5.docx"
REPORT = ROOT / "data" / "generated" / "NexusPay-v5-relatorio-cobertura.md"
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"

# Decisões válidas somente para o caso NexusPay (opportunity_id nexuspay-2026-09).
# Nunca reutilizar como padrão global nem como exemplo few-shot.
CASE_DECISIONS = {
    "engagement_type": {
        "state": "commitment",
        "value": "phased",
        "source": "decisão de teste do caso NexusPay (24/09/2026): Fase 1 assessment e desenho contratada; Fase 2 implantação opcional. Confirmar com o dono comercial.",
    },
    "phase1_estimate": {
        "state": "commitment",
        "value": "4 a 6 semanas (Assessment 2 a 3; Desenho 2 a 3)",
        "source": "decisão de teste do caso NexusPay (24/09/2026). Confirmar com o arquiteto responsável.",
    },
    "warranty": {
        "state": "commitment",
        "value": "A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final.",
        "source": "decisão do caso NexusPay informada pelo responsável (teste)",
    },
    "license_supply": {
        "state": "commitment",
        "value": "As licenças e subscrições Akamai da Fase 2 serão fornecidas pela POPULOS por meio de revenda autorizada e deverão estar ativas antes da configuração.",
        "source": "decisão do caso NexusPay informada pelo responsável (teste)",
    },
}
ESTIMATE_OWNER = "Arquiteto responsável POPULOS (decisão de teste do caso)"


def coverage_report(proposal: dict, errors: list[str]) -> str:
    lines = [
        "# NexusPay V5 — relatório de cobertura insumo → proposta",
        "",
        f"- Código: `{proposal['code']}`",
        f"- Regras: v{proposal['rules_version']}",
        f"- Resultado das regras de estado: {'aprovado, 0 violações' if not errors else f'{len(errors)} violação(ões)'}",
        "",
        "## Decisões do caso (escopo: somente NexusPay)",
        "",
        "| Decisão | Valor | Origem |",
        "|---|---|---|",
    ]
    for key, decision in proposal["governance"].items():
        lines.append(f"| {key} | {decision.get('value')} | {decision.get('source')} |")
    lines += ["", "## Cobertura do insumo", "", "| Referência | Trecho | Status | Destino |", "|---|---|---|---|"]
    for entry in proposal["source_coverage"]:
        destination = ", ".join(entry.get("targets", [])) or entry.get("reason", "")
        lines.append(f"| {entry['ref']} | {entry['statement']} | {entry['status']} | {destination} |")
    lines += ["", "## Números ditos pelo cliente", "", "| Referência | Número | Destino |", "|---|---|---|"]
    for number in proposal["client_numbers"]:
        lines.append(f"| {number['ref']} | {number['quote']} | {number['destination']} |")
    lines += ["", "## Requisitos e origem", "", "| REQ | Requisito | Origem |", "|---|---|---|"]
    for item in proposal["traceability"]:
        lines.append(f"| {item['requirement_id']} | {item['requirement']} | {item['source']} |")
    lines += ["", "## Estimativas", ""]
    for estimate in proposal["estimates"]:
        lines.append(f"- {estimate['item']}: {estimate['value']} — responsável: {estimate['owner']}")
    if errors:
        lines += ["", "## Violações", ""] + [f"- {error}" for error in errors]
    return "\n".join(lines) + "\n"


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    proposal = build_nexuspay_v5(source)
    proposal["governance"].update(CASE_DECISIONS)
    for estimate in proposal["estimates"]:
        estimate["owner"] = ESTIMATE_OWNER
    proposal.setdefault("ai_generation", {})["human_content_edits"] = "transformação determinística V5"
    proposal["document_manifest"] = None
    errors = validate_proposal_rules(proposal)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(coverage_report(proposal, errors), encoding="utf-8")
    STATE.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
    build_neutral_template_docx(proposal, TEMPLATE, OUTPUT)
    print(f"Estado: {STATE}")
    print(f"DOCX: {OUTPUT}")
    print(f"Relatório: {REPORT}")


if __name__ == "__main__":
    main()
