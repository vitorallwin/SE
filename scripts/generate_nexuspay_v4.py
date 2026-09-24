from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sales_engineer.demo_case_nexuspay_v2 import build_nexuspay_v2
from sales_engineer.neutral_template_builder import build_neutral_template_docx


SOURCE = ROOT / "data" / "proposals" / "20260923-e54ccb6.json"
STATE = ROOT / "data" / "proposals" / "nexuspay-competitive-v4.json"
OUTPUT = ROOT / "data" / "generated" / "POPULOS-Proposta-Tecnica-NexusPay-Competitiva-v4.docx"
TEMPLATE = ROOT / "assets" / "proposal_neutral_template.docx"


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    proposal = build_nexuspay_v2(source)
    proposal["code"] = "PT-2609-NXP4"
    proposal["governance"]["warranty"] = {
        "state": "commitment",
        "value": "A POPULOS corrigirá defeitos diretamente atribuíveis aos serviços executados por 90 dias corridos após o aceite final.",
        "source": "decisão aprovada para o caso NexusPay",
    }
    proposal["governance"]["license_supply"] = {
        "state": "commitment",
        "value": "As licenças e subscrições Akamai serão fornecidas pela POPULOS por meio de revenda autorizada e deverão estar ativas antes da configuração.",
        "source": "decisão aprovada para o caso NexusPay",
    }
    proposal.setdefault("ai_generation", {})["human_content_edits"] = "transformação determinística V4"
    proposal["document_manifest"] = None
    STATE.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
    build_neutral_template_docx(proposal, TEMPLATE, OUTPUT)
    print(f"Estado: {STATE}")
    print(f"DOCX: {OUTPUT}")


if __name__ == "__main__":
    main()
