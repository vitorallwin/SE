"""Create an isolated workspace for one execution: engine, skill, brief and a single case.

Usage: python scripts/make_workspace.py SOURCE_DIR WORKSPACE --config A|B [--date YYYY-MM-DD] [--mode test|production] [--sealed]
The author works with the workspace as its working directory; its execution folder is WORKSPACE/execucao.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sales_engineer.case_runner import make_workspace


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--config", required=True, choices=["A", "B"])
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--mode", default="test", choices=["test", "production"])
    parser.add_argument("--sealed", action="store_true", help="sem código do motor no workspace")
    args = parser.parse_args()
    run_dir = make_workspace(args.workspace, args.source_dir, args.date, args.mode, args.config, sealed=args.sealed)
    print(f"Workspace pronto: {args.workspace} (execução em {run_dir})")


if __name__ == "__main__":
    main()
