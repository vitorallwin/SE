from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class GeminiClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def generate_json(self, system: str, payload: dict[str, Any], max_output_tokens: int = 16384) -> dict[str, Any]:
        if not self.configured:
            raise RuntimeError("GEMINI_API_KEY não configurada")

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{urllib.parse.quote(self.model, safe='')}:generateContent?key="
            f"{urllib.parse.quote(self.api_key, safe='')}"
        )
        prompt = system + "\n\nENTRADA JSON:\n" + json.dumps(payload, ensure_ascii=False)
        invalid_text = ""
        for json_attempt in range(2):
            active_prompt = prompt
            if json_attempt:
                active_prompt = (
                    "Corrija o JSON abaixo. Preserve todo o conteúdo e a estrutura, remova comentários, "
                    "reticências, vírgulas finais e qualquer texto fora do objeto. Responda somente JSON válido.\n\n"
                    + invalid_text
                )
            body = {
                "contents": [{"role": "user", "parts": [{"text": active_prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "responseMimeType": "application/json",
                    "maxOutputTokens": max_output_tokens,
                },
            }
            request = urllib.request.Request(
                url,
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            data = None
            for attempt in range(4):
                try:
                    with urllib.request.urlopen(request, timeout=90) as response:
                        data = json.loads(response.read().decode("utf-8"))
                    break
                except urllib.error.HTTPError as exc:
                    detail = exc.read().decode("utf-8", errors="replace")[:600]
                    if exc.code in {429, 503} and attempt < 3:
                        time.sleep(2 ** (attempt + 1))
                        continue
                    raise RuntimeError(f"Gemini retornou HTTP {exc.code}: {detail}") from exc
                except (urllib.error.URLError, TimeoutError) as exc:
                    if attempt < 3:
                        time.sleep(2 ** (attempt + 1))
                        continue
                    raise RuntimeError(f"Falha ao acessar Gemini: {exc}") from exc

            if data is None:
                raise RuntimeError("Gemini não respondeu após as tentativas configuradas")
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError) as exc:
                raise RuntimeError("Resposta Gemini sem conteúdo utilizável") from exc
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                invalid_text = text
                continue
            if not isinstance(parsed, dict):
                raise RuntimeError("A resposta estruturada do Gemini não é um objeto JSON")
            return parsed
        raise RuntimeError("Gemini retornou JSON inválido mesmo após a etapa de reparo")

    def status(self) -> dict[str, Any]:
        return {
            "configured": self.configured,
            "model": self.model,
            "key_source": "environment" if self.configured else None,
        }


DOTENV_KEYS = {"GEMINI_API_KEY", "GEMINI_MODEL", "ANTHROPIC_API_KEY", "ANTHROPIC_MODEL"}


def load_dotenv(root: Any) -> None:
    """Read the author keys from the git-ignored .env so no key passes through the command line or the browser."""
    from pathlib import Path

    env_file = Path(root) / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        key, _, value = line.partition("=")
        if key.strip() in DOTENV_KEYS and value.strip() and not os.getenv(key.strip()):
            os.environ[key.strip()] = value.strip()


def _json_object(text: str) -> dict[str, Any] | None:
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        return None
    try:
        parsed = json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


class ClaudeClient:
    """Author via the Anthropic Messages API (streamed, since a proposal state is a long answer)."""

    def __init__(self, default_model: str = "") -> None:
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        self.model = os.getenv("ANTHROPIC_MODEL", "").strip() or default_model

    @property
    def configured(self) -> bool:
        return bool(self.api_key and self.model)

    def _stream(self, system: str, user: str, max_output_tokens: int) -> str:
        body = {"model": self.model, "max_tokens": max_output_tokens, "stream": True, "system": system,
                "messages": [{"role": "user", "content": user}]}
        request = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
            method="POST",
        )
        for attempt in range(4):
            try:
                chunks: list[str] = []
                with urllib.request.urlopen(request, timeout=900) as response:
                    for raw in response:
                        line = raw.decode("utf-8").strip()
                        if not line.startswith("data:"):
                            continue
                        event = json.loads(line[5:])
                        if event.get("type") == "content_block_delta" and event["delta"].get("type") == "text_delta":
                            chunks.append(event["delta"]["text"])
                        elif event.get("type") == "error":
                            raise RuntimeError(f"Claude retornou erro: {event.get('error')}")
                return "".join(chunks)
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")[:600]
                if exc.code in {429, 500, 529} and attempt < 3:
                    time.sleep(2 ** (attempt + 2))
                    continue
                raise RuntimeError(f"Claude retornou HTTP {exc.code}: {detail}") from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt < 3:
                    time.sleep(2 ** (attempt + 2))
                    continue
                raise RuntimeError(f"Falha ao acessar Claude: {exc}") from exc
        raise RuntimeError("Claude não respondeu após as tentativas configuradas")

    def generate_json(self, system: str, payload: dict[str, Any], max_output_tokens: int = 16384) -> dict[str, Any]:
        if not self.configured:
            raise RuntimeError("ANTHROPIC_API_KEY não configurada")
        user = "ENTRADA JSON:\n" + json.dumps(payload, ensure_ascii=False)
        text = self._stream(system, user, max_output_tokens)
        parsed = _json_object(text)
        if parsed is None:
            repair = self._stream("Responda somente JSON válido.", "Corrija o JSON abaixo, preservando todo o conteúdo:\n\n" + text, max_output_tokens)
            parsed = _json_object(repair)
        if parsed is None:
            raise RuntimeError("Claude retornou JSON inválido mesmo após a etapa de reparo")
        return parsed

    def status(self) -> dict[str, Any]:
        return {"configured": self.configured, "model": self.model}
