"""Configuration A: the author is a single Gemini call per attempt, under the same brief, skill,
validator and iteration limit as configuration B.

Usage: python scripts/author_with_gemini.py RUN_DIR   (run scripts/prepare_run.py first)
Requires GEMINI_API_KEY in the environment; GEMINI_MODEL overrides the model.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sales_engineer.ai import GeminiClient, load_dotenv
from sales_engineer.case_runner import author_loop


def main() -> int:
    load_dotenv(ROOT)
    run_dir = Path(sys.argv[1])
    log = author_loop(run_dir, GeminiClient())
    shutil.copy2(run_dir / "author_run.json", run_dir / "gemini_run.json")
    print(json.dumps(log, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
