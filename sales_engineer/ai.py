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

    def generate_json(self, system: str, payload: dict[str, Any]) -> dict[str, Any]:
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
                    "maxOutputTokens": 16384,
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
