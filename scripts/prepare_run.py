"""Prepare one execution folder with exactly what the author receives.

Usage: python scripts/prepare_run.py SOURCE_DIR RUN_DIR --config A|B [--date YYYY-MM-DD] [--mode test|production]
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sales_engineer.case_runner import prepare_run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--config", required=True, choices=["A", "B"])
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--mode", default="test", choices=["test", "production"])
    args = parser.parse_args()
    prepare_run(args.source_dir, args.run_dir, args.date, args.mode, args.config)
    print(f"Execução preparada em {args.run_dir}")


if __name__ == "__main__":
    main()
