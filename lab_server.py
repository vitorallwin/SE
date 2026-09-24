"""Bancada de testes do motor v11: python lab_server.py  →  http://127.0.0.1:8765

Local tool: it listens on 127.0.0.1 only. Author keys stay in the git-ignored .env; the browser never sees them.
"""
from __future__ import annotations

import json
import mimetypes
import os
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from sales_engineer import lab

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "lab"
MAX_BODY = 25 * 1024 * 1024


class Handler(BaseHTTPRequestHandler):
    server_version = "Bancada/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def do_GET(self) -> None:
        self._dispatch("GET")

    def do_POST(self) -> None:
        self._dispatch("POST")

    def _dispatch(self, method: str) -> None:
        try:
            path = urlparse(self.path).path
            if method == "GET" and not path.startswith("/api/"):
                return self._static(path)
            self._api(method, path)
        except lab.LabError as exc:
            self._json({"error": str(exc)}, exc.status)
        except Exception as exc:  # noqa: BLE001
            self._json({"error": f"{type(exc).__name__}: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _api(self, method: str, path: str) -> None:
        routes = [
            ("GET", r"/api/status", lambda: lab.status()),
            ("GET", r"/api/runs", lambda: lab.list_runs()),
            ("POST", r"/api/runs", lambda: lab.create_run(self._body())),
            ("GET", r"/api/runs/([a-z0-9-]+)", lambda r: lab.detail(r)),
            ("POST", r"/api/runs/([a-z0-9-]+)/attempts", lambda r: lab.submit_state(r, self._body().get("state", ""))),
            ("POST", r"/api/runs/([a-z0-9-]+)/author", lambda r: lab.start_author(r, self._body().get("engine", ""))),
            ("POST", r"/api/runs/([a-z0-9-]+)/complement", lambda r: lab.complement_run(r, self._body().get("text", ""))),
            ("POST", r"/api/runs/([a-z0-9-]+)/pdf", lambda r: lab.render_pdf(r)),
            ("POST", r"/api/keys", lambda: lab.set_key(**{k: v for k, v in self._body().items() if k in {"provider", "key", "base_url", "model"}})),
        ]
        for verb, pattern, handler in routes:
            match = re.fullmatch(pattern, path)
            if verb == method and match:
                return self._json(handler(*match.groups()))
        match = re.fullmatch(r"/api/runs/([a-z0-9-]+)/files/(.+)", path)
        if method == "GET" and match:
            return self._file(lab.file_path(match.group(1), unquote(match.group(2))))
        raise lab.LabError("rota inexistente", 404)

    def _body(self) -> dict[str, Any]:
        # Só a própria página pode escrever: JSON (força preflight em outra origem) e Origin local, quando houver.
        if not (self.headers.get("Content-Type") or "").startswith("application/json"):
            raise lab.LabError("Content-Type deve ser application/json", 415)
        origin = self.headers.get("Origin")
        if origin and urlparse(origin).hostname not in {"127.0.0.1", "localhost"}:
            raise lab.LabError("origem não permitida", 403)
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            raise lab.LabError("requisição grande demais", 413)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError as exc:
            raise lab.LabError("corpo não é JSON") from exc
        if not isinstance(body, dict):
            raise lab.LabError("corpo deve ser um objeto")
        return body

    def _static(self, path: str) -> None:
        target = (STATIC / (path.lstrip("/") or "index.html")).resolve()
        if STATIC.resolve() not in target.parents or not target.is_file():
            target = STATIC / "index.html"
        self._file(target, download=False)

    def _file(self, target: Path, download: bool = True) -> None:
        data = target.read_bytes()
        kind = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if target.suffix in {".md", ".json"}:
            kind += "; charset=utf-8" if kind.startswith("text") or kind.endswith("json") else ""
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        if download and target.suffix in {".docx", ".pdf", ".json", ".md"}:
            self.send_header("Content-Disposition", f'attachment; filename="{target.name}"')
        self.end_headers()
        self.wfile.write(data)

    def _json(self, payload: Any, status: int = HTTPStatus.OK) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    port = int(os.getenv("LAB_PORT", "8765"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Bancada em http://127.0.0.1:{port}  (Ctrl+C encerra)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
