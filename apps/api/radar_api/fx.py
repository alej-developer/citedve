"""Cálculos puros del panel de tasas. No lee la red ni escribe datos."""

from __future__ import annotations

import json
import math
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

NOTICE = "Foto semanal, no cotización en vivo. Información, no asesoramiento."
FRESHNESS_MAX_DAYS = 8
SCHEMA_VERSION = "0.1.0"
P2P_SIDE_PREFERENCE = ("compra", "venta", "referencia")


def gap_label(official: float, parallel: float) -> str:
    """Porcentaje (paralelo − oficial) / oficial, con el mismo texto que `toFixed(1)`."""
    if not math.isfinite(official) or not math.isfinite(parallel) or official <= 0 or parallel <= 0:
        return "n/d"
    percent = ((parallel - official) / official) * 100
    return f"{_js_to_fixed(percent, 1)}%"


def median(values: list[float]) -> float | None:
    if not _usable(values):
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def p2p_bounds(values: list[float]) -> tuple[float, float] | None:
    if not _usable(values):
        return None
    return min(values), max(values)


def bank_dispersion(rows: list[dict[str, Any]], side: str) -> dict[str, float | int] | None:
    """Mínimo, máximo y amplitud de bancos. No incluye agregados ni dice qué banco es."""
    values = [
        float(row["value"])
        for row in rows
        if row["indicator"] == "tasa_informativa_banco"
        and row["side"] == side
        and row["status"] == "published"
        and row["institution"]["kind"] == "banco"
        and isinstance(row["value"], (int, float))
        and math.isfinite(float(row["value"]))
        and float(row["value"]) > 0
    ]
    if not values:
        return None
    low = min(values)
    high = max(values)
    return {"min": low, "max": high, "amplitud": high - low, "n": len(values)}


def render_published_latest(document: dict[str, Any]) -> str:
    chosen, banner = _select_edition(document["editions"])
    if chosen is None:
        payload: dict[str, Any] = _empty_payload()
        if banner:
            payload["retracted_banner"] = banner
        return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    rows = [row for row in document["observations"] if row["edition"] == chosen["id"]]
    official = {
        "compra": _official_side(rows, "compra"),
        "venta": _official_side(rows, "venta"),
    }
    banks = _bank_rows(rows)
    p2p = _p2p_block(chosen, rows)
    venta = official["venta"]
    official_value = None if venta is None else venta.get("value")
    gaps = None
    if p2p["estado"] == "publicado" and isinstance(official_value, (int, float)):
        gaps = _gaps(float(official_value), p2p)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "edition": {
            "id": chosen["id"],
            "cutoff_date": chosen["cutoff_date"],
            "status": "published",
            "p2p_status": chosen["p2p_status"],
            "notes": chosen.get("notes"),
        },
        "notice": NOTICE,
        "freshness_max_days": FRESHNESS_MAX_DAYS,
        "retracted_banner": banner,
        "official": official,
        "banks": banks,
        "dispersion": {
            "compra": bank_dispersion(rows, "compra"),
            "venta": bank_dispersion(rows, "venta"),
        },
        "p2p": p2p,
        "gaps": gaps,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _js_to_fixed(value: float, digits: int) -> str:
    sign = "-" if value < 0 else ""
    quantum = Decimal(1).scaleb(-digits)
    rounded = Decimal(repr(abs(value))).quantize(quantum, rounding=ROUND_HALF_UP)
    return f"{sign}{rounded:.{digits}f}"


def _usable(values: list[float]) -> bool:
    return len(values) >= 2 and all(math.isfinite(item) and item > 0 for item in values)


def _empty_payload() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "edition": None,
        "notice": NOTICE,
        "freshness_max_days": FRESHNESS_MAX_DAYS,
    }


def _select_edition(
    editions: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, str | None]:
    ordered = sorted(editions, key=lambda edition: (edition["cutoff_date"], edition["id"]))
    published = [edition for edition in ordered if edition["status"] == "published"]
    chosen = published[-1] if published else None
    if chosen is None:
        retracted = [edition for edition in ordered if edition["status"] == "retracted"]
    else:
        retracted = [
            edition
            for edition in ordered
            if edition["status"] == "retracted" and edition["cutoff_date"] > chosen["cutoff_date"]
        ]
    banner = None
    if retracted:
        last = retracted[-1]
        reason = last.get("retraction_reason") or ""
        banner = f"La edición {last['id']} se retiró: {reason}".rstrip()
    return chosen, banner


def _hide(row: dict[str, Any]) -> bool:
    return str(row["status"]) != "published"


def _side_view(row: dict[str, Any]) -> dict[str, Any]:
    hidden = _hide(row)
    source = row["source"]
    return {
        "status": row["status"],
        "as_of_date": row["as_of_date"],
        "date_basis": row["date_basis"],
        "operation_date": row.get("operation_date"),
        "unit": row["unit"],
        "value": None if hidden else row["value"],
        "value_as_published": None if hidden else row["value_as_published"],
        "notes": row.get("notes"),
        "retraction_reason": row.get("retraction_reason"),
        "source": {
            "name": source["name"],
            "url": source["url"],
            "locator": source.get("locator"),
            "accessed_at": source["accessed_at"],
            "archive_url": source.get("archive_url"),
            "publisher_id": source["publisher_id"],
            "upstream_id": source.get("upstream_id"),
        },
    }


def _official_side(rows: list[dict[str, Any]], side: str) -> dict[str, Any] | None:
    matches = [
        row for row in rows if row["indicator"] == "tasa_oficial_bcv" and row["side"] == side
    ]
    if not matches:
        return None
    return _side_view(matches[0])


def _bank_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row["indicator"] != "tasa_informativa_banco":
            continue
        if row["side"] not in {"compra", "venta"}:
            continue
        institution = row["institution"]
        item = grouped.setdefault(
            institution["id"],
            {"institution": institution, "compra": None, "venta": None},
        )
        item[row["side"]] = _side_view(row)
    ordered = sorted(
        grouped.values(),
        key=lambda item: (
            item["institution"]["kind"] == "agregado_fuente",
            str(item["institution"]["name"]).casefold(),
            item["institution"]["id"],
        ),
    )
    for item in ordered:
        compra = item["compra"]
        venta = item["venta"]
        discrepancia = False
        if (
            isinstance(compra, dict)
            and isinstance(venta, dict)
            and compra["status"] == "published"
            and venta["status"] == "published"
            and compra["value"] is not None
            and venta["value"] is not None
            and float(compra["value"]) > float(venta["value"])
        ):
            discrepancia = True
        item["discrepancia"] = discrepancia
    return ordered


def _p2p_block(edition: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    if edition["p2p_status"] != "publicado":
        return {"estado": "sin_dato"}
    published = [
        row for row in rows if row["indicator"] == "p2p_referencia" and row["status"] == "published"
    ]
    side, group = _choose_p2p_side(published)
    if side is None:
        return {"estado": "sin_dato"}
    values = [float(row["value"]) for row in group]
    bounds = p2p_bounds(values)
    mid = median(values)
    if bounds is None or mid is None:
        return {"estado": "sin_dato"}
    low, high = bounds
    publishers = {row["source"]["publisher_id"] for row in group}
    fuentes = [
        {
            "name": row["source"]["name"],
            "url": row["source"]["url"],
            "archive_url": row["source"].get("archive_url"),
            "upstream_id": row["source"].get("upstream_id"),
            "publisher_id": row["source"]["publisher_id"],
            "value": row["value"],
            "accessed_at": row["source"]["accessed_at"],
        }
        for row in sorted(group, key=lambda row: str(row["source"]["name"]).casefold())
    ]
    return {
        "estado": "publicado",
        "side": side,
        "unit": "VES/USDT",
        "min": low,
        "max": high,
        "mediana": mid,
        "n_fuentes": len({row["source"].get("upstream_id") for row in group}),
        "n_editores": len(publishers),
        "limitacion_editor_unico": len(publishers) == 1,
        "fuentes": fuentes,
    }


def _choose_p2p_side(
    rows: list[dict[str, Any]],
) -> tuple[str | None, list[dict[str, Any]]]:
    for side in P2P_SIDE_PREFERENCE:
        group = [row for row in rows if row["side"] == side]
        upstreams = {row["source"].get("upstream_id") for row in group}
        upstreams.discard(None)
        if len(upstreams) >= 2 and len(upstreams) == len(group):
            return side, group
    return None, []


def _gaps(official: float, p2p: dict[str, Any]) -> list[dict[str, Any]]:
    side = str(p2p["side"])
    points = (
        ("P2P mín.", float(p2p["min"])),
        ("P2P máx.", float(p2p["max"])),
        ("P2P mediana", float(p2p["mediana"])),
    )
    return [
        {
            "label": label,
            "side": side,
            "official_label": "BCV",
            "official": official,
            "parallel_label": label,
            "parallel": parallel,
            "text": gap_label(official, parallel),
        }
        for label, parallel in points
    ]
