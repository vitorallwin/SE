from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any


class JsonStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            proposals = []
            for path in self.root.glob("*.json"):
                try:
                    proposals.append(json.loads(path.read_text(encoding="utf-8")))
                except (OSError, json.JSONDecodeError):
                    continue
            return sorted(proposals, key=lambda item: item.get("updated_at", ""), reverse=True)

    def get(self, proposal_id: str) -> dict[str, Any] | None:
        path = self.root / f"{proposal_id}.json"
        if not path.exists():
            return None
        with self._lock:
            return json.loads(path.read_text(encoding="utf-8"))

    def save(self, proposal: dict[str, Any]) -> dict[str, Any]:
        path = self.root / f"{proposal['id']}.json"
        temp = path.with_suffix(".tmp")
        with self._lock:
            temp.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
            temp.replace(path)
        return proposal

    def delete(self, proposal_id: str) -> bool:
        path = self.root / f"{proposal_id}.json"
        with self._lock:
            if not path.exists():
                return False
            path.unlink()
            return True

