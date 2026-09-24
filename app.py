from __future__ import annotations

import json
import mimetypes
import os
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from sales_engineer.service import ProposalService

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
SERVICE = ProposalService(ROOT)


class ApiError(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


class Handler(BaseHTTPRequestHandler):
    server_version = "SalesEngineerV2/2.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        message = fmt % args
        if "key=" in message.lower():
            message = message.split("?", 1)[0]
        print(f"[{self.log_date_time_string()}] {message}")

    def do_GET(self) -> None:
        try:
            self._get()
        except Exception as exc:
            self._handle_error(exc)

    def do_POST(self) -> None:
        try:
            self._post()
        except Exception as exc:
            self._handle_error(exc)

    def do_PATCH(self) -> None:
        try:
            self._patch()
        except Exception as exc:
            self._handle_error(exc)

    def do_DELETE(self) -> None:
        try:
            self._delete()
        except Exception as exc:
            self._handle_error(exc)

    def _get(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/health":
            return self._json({"status": "ok", "version": "2.0", "ai": SERVICE.ai.status()})
        if path == "/api/proposals":
            return self._json({"items": SERVICE.list()})
        match = re.fullmatch(r"/api/proposals/([a-zA-Z0-9-]+)", path)
        if match:
            proposal = SERVICE.get(match.group(1))
            if proposal is None:
                raise ApiError(404, "Proposta não encontrada")
            return self._json(proposal)
        match = re.fullmatch(r"/api/proposals/([a-zA-Z0-9-]+)/docx", path)
        if match:
            proposal, output = SERVICE.generate_docx(match.group(1))
            return self._file(output, proposal["document"]["filename"])
        return self._static(path)

    def _post(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        payload = self._body()
        if path == "/api/proposals":
            return self._json(SERVICE.create(payload), status=201)
        if path == "/api/demo/ai":
            return self._json(SERVICE.create_ai_demo(), status=201)
        match = re.fullmatch(r"/api/proposals/([a-zA-Z0-9-]+)/run", path)
        if match:
            through = parse_qs(parsed.query).get("through", [None])[0]
            return self._json(SERVICE.run(match.group(1), through=through))
        match = re.fullmatch(r"/api/proposals/([a-zA-Z0-9-]+)/approve", path)
        if match:
            return self._json(SERVICE.approve(match.group(1), str(payload.get("approver", ""))))
        match = re.fullmatch(r"/api/proposals/([a-zA-Z0-9-]+)/generate", path)
        if match:
            proposal, _ = SERVICE.generate_docx(match.group(1))
            return self._json(proposal)
        raise ApiError(404, "Rota não encontrada")

    def _patch(self) -> None:
        match = re.fullmatch(r"/api/proposals/([a-zA-Z0-9-]+)", urlparse(self.path).path)
        if not match:
            raise ApiError(404, "Rota não encontrada")
        self._json(SERVICE.update(match.group(1), self._body()))

    def _delete(self) -> None:
        match = re.fullmatch(r"/api/proposals/([a-zA-Z0-9-]+)", urlparse(self.path).path)
        if not match:
            raise ApiError(404, "Rota não encontrada")
        if not SERVICE.delete(match.group(1)):
            raise ApiError(404, "Proposta não encontrada")
        self.send_response(204)
        self.end_headers()

    def _body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 2_000_000:
            raise ApiError(413, "Conteúdo maior que 2 MB")
        if not length:
            return {}
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ApiError(400, "JSON inválido") from exc
        if not isinstance(data, dict):
            raise ApiError(400, "O corpo precisa ser um objeto JSON")
        return data

    def _json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: Path, download_name: str) -> None:
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        self.send_header("Content-Disposition", f'attachment; filename="{download_name}"')
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _static(self, url_path: str) -> None:
        relative = "index.html" if url_path in {"", "/"} else url_path.lstrip("/")
        candidate = (WEB / relative).resolve()
        if WEB.resolve() not in candidate.parents and candidate != WEB.resolve():
            raise ApiError(403, "Acesso negado")
        if not candidate.exists() or not candidate.is_file():
            candidate = WEB / "index.html"
        body = candidate.read_bytes()
        mime = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime + ("; charset=utf-8" if mime.startswith("text/") or mime == "application/javascript" else ""))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _handle_error(self, exc: Exception) -> None:
        if isinstance(exc, ApiError):
            return self._json({"error": exc.message}, exc.status)
        if isinstance(exc, KeyError):
            return self._json({"error": str(exc).strip("'")}, 404)
        if isinstance(exc, ValueError):
            return self._json({"error": str(exc)}, 400)
        print(f"Erro: {type(exc).__name__}: {exc}")
        self._json({"error": "Erro interno ao processar a solicitação"}, 500)


def seed_demo() -> None:
    if SERVICE.list():
        return
    demo = SERVICE.create({
        "client_name": "Aurora Varejo S.A.",
        "opportunity": "Proteção de aplicações e DNS autoritativo",
        "owner": "Equipe Sales Engineering",
        "products": ["app_api_protector", "edge_dns", "bot_manager"],
        "transcript": "O cliente deseja proteger o portal de vendas e as APIs públicas. Precisa reduzir indisponibilidade causada por ataques e integrar eventos ao SIEM. A implantação deve ocorrer em fases, começando pelos domínios críticos.",
        "requirements": "Proteger aplicações e APIs contra ataques web e DDoS; manter DNS autoritativo altamente disponível; integrar eventos de segurança ao SIEM; implantar em ondas com homologação; registrar evidências dos testes",
        "scope": "Discovery técnico, desenho, configuração de políticas, onboarding de domínios, integração SIEM, homologação assistida e transferência de conhecimento.",
        "assumptions": "A Aurora fornecerá acessos e contatos técnicos. Mudanças em produção ocorrerão em janela aprovada. O escopo comercial prevalece sobre estimativas desta proposta técnica.",
    })
    SERVICE.store.save(SERVICE.pipeline.run(demo, through="commercial_qa"))


def main() -> None:
    seed_demo()
    port = int(os.getenv("SALES_ENGINEER_PORT", "8010"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Sales Engineer AI V2 em http://localhost:{port}")
    print("Gemini configurado." if SERVICE.ai.configured else "Modo demonstração ativo; defina GEMINI_API_KEY para usar Gemini.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
