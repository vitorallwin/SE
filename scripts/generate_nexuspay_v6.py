from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.generate_nexuspay_v5 import coverage_report
from sales_engineer.demo_case_nexuspay_v6 import build_nexuspay_v6
from sales_engineer.neutral_template_builder import build_neutral_template_docx
from sales_engineer.proposal_rules import validate_proposal_rules


SOURCE = ROOT / "data" / "proposals" / "20260923-e54ccb6.json"
STATE = ROOT / "data" / "proposals" / "nexuspay-competitive-v6.json"
OUTPUT = ROOT / "data" / "generated" / "POPULOS-Proposta-Tecnica-NexusPay-Competitiva-v6.docx"
REPORT = ROOT / "data" / "generated" / "NexusPay-v6-relatorio-cobertura.md"
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"

APPROVER = "Vitor (responsável comercial) — dado de teste"
APPROVED_AT = "2026-09-24"
ENGAGEMENT = "phased"


def _decision(value: str, source: str, **extra) -> dict:
    return {"state": "commitment", "value": value, "approved_value": value, "source": source,
            "approved_by": APPROVER, "approved_at": APPROVED_AT, "engagement_ref": ENGAGEMENT, **extra}


# Decisões válidas somente para o caso NexusPay (opportunity_id nexuspay-2026-09), aprovadas como dado de teste.
# Mudar o engajamento ou editar um valor invalida a decisão e bloqueia a emissão.
CASE_DECISIONS = {
    "engagement_type": _decision("phased", "Fase 1 assessment e desenho contratada; Fase 2 implantação opcional. Aprovado ao seguir para a V6."),
    "phase1_estimate": _decision("6 a 8 semanas (Assessment 3 a 4; Desenho 3 a 4)", "revisada após o crescimento do escopo para 13 itens; escolhida pelo responsável"),
    "warranty": _decision("A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final.", "aplicável à Fase 1 conforme resposta do responsável"),
    "license_supply": _decision("As licenças e subscrições Akamai serão fornecidas pela POPULOS por meio de revenda autorizada e deverão estar ativas antes da configuração.", "decisão original do caso, sem alteração de texto"),
    "sla": _decision("tabela institucional do template POPULOS", "populos_standard; aplicabilidade ao engajamento em fases confirmada pelo responsável", applies_to=["phased", "implementation"]),
}
ESTIMATE_OWNER = APPROVER


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    proposal = build_nexuspay_v6(source)
    proposal["governance"].update(CASE_DECISIONS)
    for estimate in proposal["estimates"]:
        estimate["owner"] = ESTIMATE_OWNER
    proposal.setdefault("ai_generation", {})["human_content_edits"] = "transformação determinística V6"
    proposal["document_manifest"] = None
    errors = validate_proposal_rules(proposal)
    report = coverage_report(proposal, errors).replace("NexusPay V5", "NexusPay V6")
    feasibility = proposal["event_feasibility"][0]
    report += (
        "\n## Viabilidade de eventos críticos\n\n"
        f"- {feasibility['event']}: Fase 1 termina entre {feasibility['phase1_end_earliest']} e {feasibility['phase1_end_latest']}"
        f" (início em {feasibility['reference_date']}). Classificação pela Fase 2: {feasibility['classification']}. {feasibility['reason']}\n"
        "- Pix Day: data não informada; pergunta pendente.\n"
        "\n## Proveniência por falante\n\n| REQ | Falantes |\n|---|---|\n"
        + "".join(f"| {item['requirement_id']} | {', '.join(item['speakers'])} |\n" for item in proposal["traceability"])
        + "\n## Perguntas abertas\n\n" + "".join(f"- {question}\n" for question in proposal["open_questions"])
    )
    REPORT.write_text(report, encoding="utf-8")
    STATE.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
    build_neutral_template_docx(proposal, TEMPLATE, OUTPUT)
    print(f"Estado: {STATE}")
    print(f"DOCX: {OUTPUT}")
    print(f"Relatório: {REPORT}")


if __name__ == "__main__":
    main()
