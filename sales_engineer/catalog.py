from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# O catálogo é a união dos pacotes de fabricante da skill (packages/<id>/package.json). Um pacote traz
# os produtos, as frentes do documento, as camadas do diagrama e o status (validated | draft).
PACKAGES_DIR = Path(__file__).resolve().parents[1] / "skills" / "akamai-proposal-authoring" / "packages"


def _load_packages() -> dict[str, dict[str, Any]]:
    packages: dict[str, dict[str, Any]] = {}
    for path in sorted(PACKAGES_DIR.glob("*/package.json")):
        package = json.loads(path.read_text(encoding="utf-8"))
        packages[package["id"]] = package
    return packages


PACKAGES = _load_packages()
PRODUCTS: dict[str, dict[str, Any]] = {}
for _package in sorted(PACKAGES.values(), key=lambda p: (p["id"] != "akamai", p["id"])):
    for _product_id, _product in _package["products"].items():
        if _product_id in PRODUCTS:
            raise ValueError(f"produto repetido entre pacotes: {_product_id}")
        PRODUCTS[_product_id] = {**_product, "package": _package["id"], "vendor": _package["vendor"]}
FRONT_GROUPS: dict[str, tuple[str, ...]] = {}
for _package in PACKAGES.values():
    for _group, _members in _package.get("fronts", {}).items():
        FRONT_GROUPS[_group] = FRONT_GROUPS.get(_group, ()) + tuple(_members)


def package_of(product_id: str) -> dict[str, Any] | None:
    product = PRODUCTS.get(product_id)
    return PACKAGES.get(product["package"]) if product else None


def vendors_of(product_ids: list[str]) -> list[str]:
    """Fabricantes dos produtos, na ordem em que aparecem; serviços POPULOS não são fabricante."""
    vendors: list[str] = []
    for product_id in product_ids:
        vendor = PRODUCTS.get(product_id, {}).get("vendor")
        if vendor and vendor != "POPULOS" and vendor not in vendors:
            vendors.append(vendor)
    return vendors


def product_rows(selected: list[str]) -> list[dict]:
    return [{"id": key, **PRODUCTS[key]} for key in selected if key in PRODUCTS]


def recommended_product_ids(decisions: list[dict[str, Any]]) -> list[str]:
    return [
        str(item.get("product_id"))
        for item in decisions
        if item.get("status") == "recommended" and item.get("product_id") in PRODUCTS
    ]
