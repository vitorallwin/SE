"""Submit one authoring attempt: validate, log it as passN, and compose when clean.

Usage: python scripts/validate_attempt.py RUN_DIR STATE.json
Exit codes: 0 clean and composed, 1 rule violations, 2 composer blocked, 4 iteration limit reached.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sales_engineer.case_runner import record_attempt


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 64
    result = record_attempt(Path(sys.argv[1]), Path(sys.argv[2]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] == "limit_reached":
        return 4
    if result["status"] == "violations":
        return 1
    return 0 if result.get("composition", {}).get("status") == "emitted" else 2


if __name__ == "__main__":
    sys.exit(main())
