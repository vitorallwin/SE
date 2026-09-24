from __future__ import annotations

import base64
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

from sales_engineer import lab
from sales_engineer.violation_codes import code_of

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class BenchTests(unittest.TestCase):
    """Bancada: o mesmo fluxo das rodadas (tentativas, limite, veredito), sem regra própria."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        patcher = mock.patch.object(lab, "RUNS", Path(self.tmp.name))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)
        insumo = base64.b64encode((FIXTURES / "vertice_insumo.md").read_bytes()).decode()
        self.run_id = lab.create_run({"name": "Vértice", "proposal_date": "2026-09-24",
                                      "files": [{"name": "insumo.md", "content": insumo}]})["id"]
        self.state = json.loads((FIXTURES / "vertice_v11.json").read_text(encoding="utf-8"))

    def test_clean_state_is_emitted(self) -> None:
        run = lab.submit_state(self.run_id, json.dumps(self.state))
        self.assertEqual(run["verdict"]["key"], "emitted")
        self.assertTrue(any(f["path"].endswith(".docx") for f in run["files"]))
        self.assertEqual(run["pending"]["feasibility"][0]["classification"], "conditional")

    def test_violations_carry_codes_and_the_limit_holds(self) -> None:
        broken = deepcopy(self.state)
        broken["sections"][0]["paragraphs"].append("Conclusão prevista para 15/10/2026.")
        run = lab.submit_state(self.run_id, json.dumps(broken))
        self.assertEqual(run["verdict"]["key"], "violations")
        self.assertIn("DATA-SEM-ORIGEM", {item["code"] for item in run["attempt_log"][0]["items"]})
        lab.submit_state(self.run_id, "{")
        run = lab.submit_state(self.run_id, "{")
        self.assertEqual(run["verdict"]["key"], "failed")
        self.assertFalse(run["pending"]["readable"])
        with self.assertRaises(lab.LabError):
            lab.submit_state(self.run_id, json.dumps(self.state))

    def test_complement_creates_a_new_run_with_the_note(self) -> None:
        child = lab.complement_run(self.run_id, "De: Diretoria\nAprovo garantia de 30 dias.")
        self.assertNotEqual(child["id"], self.run_id)
        self.assertEqual(child["parent"], self.run_id)
        self.assertIn("Aprovo garantia de 30 dias.", child["insumo"])
        self.assertEqual(child["attempts"], 0)

    def test_files_stay_inside_the_run(self) -> None:
        with self.assertRaises(lab.LabError):
            lab.file_path(self.run_id, "../../engine_config.json")
        with self.assertRaises(lab.LabError):
            lab.detail("../x")

    def test_legitimate_block_is_not_an_author_failure(self) -> None:
        attempt = {"codes": ["DECISAO-ABERTA"], "errors_count": 1}
        self.assertEqual(lab.verdict([attempt], 3, False)["key"], "blocked")
        self.assertEqual(code_of("JSON inválido: x"), "JSON-INVALIDO")


class DotenvTests(unittest.TestCase):
    """Chave do .env escrita no Windows: BOM do Bloco de Notas, aspas e variável antiga da máquina."""

    def test_notepad_env_with_quotes_wins_over_machine_variable(self) -> None:
        import os

        from sales_engineer.ai import explain_key_error, key_source, load_dotenv

        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"GEMINI_API_KEY": "antiga"}, clear=False):
            (Path(tmp) / ".env").write_bytes('\ufeffGEMINI_API_KEY="nova-chave"\nexport ANTHROPIC_API_KEY = \'outra\'\n'.encode("utf-8"))
            load_dotenv(tmp)
            self.assertEqual(os.environ["GEMINI_API_KEY"], "nova-chave")
            self.assertEqual(os.environ["ANTHROPIC_API_KEY"], "outra")
            self.assertEqual(key_source("GEMINI_API_KEY"), ".env")
            message = explain_key_error("Gemini", 400, '{"reason": "API_KEY_INVALID"}')
            self.assertIn("recusou a chave (origem: .env)", message)
            self.assertNotIn("nova-chave", message)


    def test_key_from_the_bench_goes_to_env_without_bom_or_quotes(self) -> None:
        import os

        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {}, clear=False), \
                mock.patch.object(lab, "ROOT", Path(tmp)), mock.patch.object(lab, "check_key", return_value={"ok": True, "message": "ok"}):
            env = Path(tmp) / ".env"
            env.write_bytes("\ufeffGEMINI_API_KEY=\nOUTRA=1\n".encode("utf-8"))
            result = lab.set_key("gemini", ' "AIzaSyExemploExemploExemploExemplo123" ')
            text = env.read_bytes().decode("utf-8")
            self.assertFalse(text.startswith("\ufeff"))
            self.assertIn("OUTRA=1", text)
            self.assertEqual(text.count("GEMINI_API_KEY"), 1)
            self.assertIn("GEMINI_API_KEY=AIzaSyExemploExemploExemploExemplo123\n", text)
            self.assertEqual(result["length"], len("AIzaSyExemploExemploExemploExemplo123"))
            self.assertNotIn("AIzaSy", json.dumps(result))
            with self.assertRaises(lab.LabError):
                lab.set_key("gemini", "curta")
            self.assertEqual(lab.set_key("gemini", "")["length"], result["length"])  # vazio mantém a chave atual
            with self.assertRaises(lab.LabError):
                lab.set_key("local", "", "https://servidor/v1", "populos")  # sem chave local ainda


class LocalAITests(unittest.TestCase):
    """IA local compatível com OpenAI: mesmo loop de autor, validador e limite."""

    def serve(self, handler_cls):
        import threading
        from http.server import ThreadingHTTPServer

        server = ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        return f"http://127.0.0.1:{server.server_port}/v1"

    def test_local_author_emits_through_the_same_loop(self) -> None:
        import os
        from http.server import BaseHTTPRequestHandler

        from sales_engineer.ai import OpenAICompatClient
        from sales_engineer.case_runner import author_loop, prepare_run

        state_text = (FIXTURES / "vertice_v11.json").read_text(encoding="utf-8")
        seen: list[dict] = []

        class Fake(BaseHTTPRequestHandler):
            def log_message(self, *args):  # noqa: D401
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                seen.append({"auth": self.headers.get("Authorization"), **body})
                if "response_format" in body:  # servidor que não aceita response_format
                    self.send_response(400); self.end_headers(); self.wfile.write(b'{"error":"response_format"}'); return
                reply = {"choices": [{"finish_reason": "stop", "message": {"content": "```json\n" + state_text + "\n```"}}]}
                data = json.dumps(reply).encode()
                self.send_response(200); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

        base = self.serve(Fake)
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {
                "LOCAL_AI_BASE_URL": base, "LOCAL_AI_API_KEY": "chave-de-teste", "LOCAL_AI_MODEL": "populos"}):
            source = Path(tmp) / "fonte"
            source.mkdir()
            (source / "insumo.md").write_bytes((FIXTURES / "vertice_insumo.md").read_bytes())
            run_dir = Path(tmp) / "run"
            prepare_run(source, run_dir, "2026-09-24", "test", "B")
            log = author_loop(run_dir, OpenAICompatClient())
            attempts = json.loads((run_dir / "attempts.json").read_text(encoding="utf-8"))["attempts"]
        self.assertEqual(attempts[0]["composition"]["status"], "emitted", attempts[0]["errors"])
        self.assertEqual(log["model"], "populos")
        self.assertEqual(seen[-1]["auth"], "Bearer chave-de-teste")
        self.assertEqual(seen[-1]["model"], "populos")
        self.assertNotIn("response_format", seen[-1])

    def test_rejected_local_key_is_explained(self) -> None:
        import os
        from http.server import BaseHTTPRequestHandler

        from sales_engineer.ai import OpenAICompatClient

        class Deny(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(401); self.end_headers(); self.wfile.write(b'{"error":{"type":"authentication_error"}}')

        base = self.serve(Deny)
        with mock.patch.dict(os.environ, {"LOCAL_AI_BASE_URL": base, "LOCAL_AI_API_KEY": "x" * 30, "LOCAL_AI_MODEL": "populos"}):
            with self.assertRaises(RuntimeError) as ctx:
                OpenAICompatClient().generate_json("s", {"a": 1})
        self.assertIn("IA local recusou a chave", str(ctx.exception))
        self.assertIn("LOCAL_AI_API_KEY", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
