from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sales_engineer.store import JsonStore


class StoreTests(unittest.TestCase):
    def test_round_trip_and_delete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = JsonStore(Path(directory))
            store.save({"id": "abc", "updated_at": "2026-01-01", "name": "Teste"})
            self.assertEqual(store.get("abc")["name"], "Teste")
            self.assertEqual(len(store.list()), 1)
            self.assertTrue(store.delete("abc"))
            self.assertIsNone(store.get("abc"))


if __name__ == "__main__":
    unittest.main()

