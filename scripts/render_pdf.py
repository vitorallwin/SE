"""Render an emitted DOCX to PDF (LibreOffice) and page images, for visual QA.

Usage: python scripts/render_pdf.py PROPOSAL.docx [OUT_DIR]
LibreOffice paginates differently from Word. The reference engine for the client is Word; this
render is the portable check that catches layout defects (wrapped headers, unreadable diagrams).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def render(docx: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        # LibreOffice fails on some paths (e.g. a directory named "-x"), so it works on a plain copy.
        source = Path(tmp) / "proposta.docx"
        shutil.copy2(docx, source)
        env = {**os.environ, "HOME": tmp}
        subprocess.run(["soffice", "--headless", f"-env:UserInstallation=file://{tmp}/profile",
                        "--convert-to", "pdf", "--outdir", tmp, str(source)],
                       check=True, capture_output=True, env=env, timeout=240)
        pdf = out_dir / f"{docx.stem}.pdf"
        shutil.copy2(Path(tmp) / "proposta.pdf", pdf)
    import pymupdf

    document = pymupdf.open(pdf)
    for index, page in enumerate(document, start=1):
        page.get_pixmap(dpi=80).save(out_dir / f"{docx.stem}-p{index:02d}.png")
    return pdf


if __name__ == "__main__":
    target = Path(sys.argv[1])
    print(render(target, Path(sys.argv[2]) if len(sys.argv) > 2 else target.parent / "render"))
