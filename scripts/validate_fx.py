"""Valida `data/fx/observations.json` contra el esquema FX y las reglas de integridad.

Uso:  uv run python scripts/validate_fx.py
Sale con código 1 si hay errores.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "schema" / "fx_observations.schema.json"
OBSERVATIONS_PATH = ROOT / "data" / "fx" / "observations.json"

FX_ALLOWED_HOSTS = frozenset({"www.bcv.org.ve", "www.usdt.com.ve", "web.archive.org"})
DISCARDED_HOSTS = frozenset(
    {
        "binance.com",
        "bybit.com",
        "monitordedivisavenezuela.com",
        "exchangemonitor.net",
        "criptoya.com",
        "pitbullchain.com",
        "yadio.io",
        "eldorado.io",
    }
)
AFFILIATE_NAMES = frozenset({"ref", "aff", "referral", "affiliate"})

KIND_BY_INDICATOR = {
    "tasa_oficial_bcv": frozenset({"banco_central"}),
    "tasa_informativa_banco": frozenset({"banco", "agregado_fuente"}),
    "p2p_referencia": frozenset({"mercado_p2p"}),
}
UNIT_BY_INDICATOR = {
    "tasa_oficial_bcv": "VES/USD",
    "tasa_informativa_banco": "VES/USD",
    "p2p_referencia": "VES/USDT",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _host(url: str) -> str:
    return urlparse(url).hostname or ""


def _discarded(url: str) -> bool:
    lowered = url.lower()
    return any(domain in lowered for domain in DISCARDED_HOSTS)


def _affiliate(url: str) -> bool:
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    return any(name in AFFILIATE_NAMES or name.startswith("utm_") for name in query)


def _path_is_root(url: str) -> bool:
    path = urlparse(url).path
    return path in ("", "/")


def _parse_published(text: str) -> Decimal:
    cleaned = text.strip().replace(" ", "").replace("\u00a0", "")
    plain = r"[0-9]+(?:[.,][0-9]+)?"
    grouped = r"[0-9]{1,3}(?:[.,][0-9]{3})+(?:[.,][0-9]+)?"
    if not re.fullmatch(f"{plain}|{grouped}", cleaned):
        raise InvalidOperation(text)
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")
    return Decimal(cleaned)


def _values_match(value: float, published: str) -> bool:
    try:
        parsed = _parse_published(published)
    except (InvalidOperation, ValueError):
        return False
    exponent = parsed.as_tuple().exponent
    places = -exponent if isinstance(exponent, int) and exponent < 0 else 0
    quantum = Decimal(1).scaleb(-places)
    got = Decimal(str(value)).quantize(quantum)
    return got == parsed


def _expected_edition_id(cutoff: date) -> str:
    iso = cutoff.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _check_url(errors: list[str], label: str, url: str) -> None:
    host = _host(url)
    if host not in FX_ALLOWED_HOSTS:
        errors.append(f"integridad: {label}: dominio no permitido '{host}'")
    if _discarded(url):
        errors.append(f"integridad: {label}: dominio descartado")
    if "/bapi/" in url or url.rstrip("/").endswith("/bapi"):
        errors.append(f"integridad: {label}: /bapi/ está vetado")
    if _affiliate(url):
        errors.append(f"integridad: {label}: parámetro de afiliado")
    if _path_is_root(url):
        errors.append(f"integridad: {label}: la URL no puede ser la raíz del dominio")


def _edition_rules(
    errors: list[str],
    edition: dict[str, Any],
    rows: list[dict[str, Any]],
    today: date,
) -> None:
    eid = edition["id"]
    cutoff = date.fromisoformat(edition["cutoff_date"])
    if cutoff.weekday() != 4:
        errors.append(f"integridad: '{eid}': el corte {cutoff.isoformat()} no es viernes")
    if edition["id"] != _expected_edition_id(cutoff):
        errors.append(f"integridad: '{eid}': el id no es la semana ISO de {cutoff.isoformat()}")
    if cutoff > today:
        errors.append(f"integridad: '{eid}': el corte {cutoff.isoformat()} es posterior a hoy")

    published = [row for row in rows if row["status"] == "published"]
    for row in rows:
        label = f"'{row['id']}'"
        as_of = date.fromisoformat(row["as_of_date"])
        if as_of > cutoff:
            errors.append(f"integridad: {label}: as_of_date posterior al corte")
        accessed = datetime.fromisoformat(row["source"]["accessed_at"])
        if accessed.date() < as_of:
            errors.append(f"integridad: {label}: accessed_at anterior a as_of_date")
        if not _values_match(row["value"], row["value_as_published"]):
            errors.append(f"integridad: {label}: value no coincide con value_as_published")

        expected_id = (
            f"fx-{row['edition']}-{row['indicator']}-{row['institution']['id']}-{row['side']}"
        )
        if row["id"] != expected_id:
            errors.append(f"integridad: {label}: el id no sigue el patrón de la fila")

        indicator = row["indicator"]
        if row["institution"]["kind"] not in KIND_BY_INDICATOR[indicator]:
            errors.append(f"integridad: {label}: kind no corresponde al indicador")
        if row["unit"] != UNIT_BY_INDICATOR[indicator]:
            errors.append(f"integridad: {label}: unidad no corresponde al indicador")
        _check_url(errors, f"{label} url", row["source"]["url"])
        archive = row["source"].get("archive_url")
        if archive:
            _check_url(errors, f"{label} archive_url", archive)

        if indicator == "tasa_oficial_bcv":
            if row["date_basis"] != "fecha_operacion":
                errors.append(f"integridad: {label}: la tasa oficial usa fecha de operación")
            if row.get("operation_date") != row["as_of_date"]:
                errors.append(f"integridad: {label}: as_of_date debe ser la fecha de operación")
        if indicator == "p2p_referencia" and row["date_basis"] != "captura_archivada":
            errors.append(f"integridad: {label}: P2P usa captura_archivada")
        if (
            indicator == "p2p_referencia"
            and row["status"] == "published"
            and not row["source"].get("upstream_id")
        ):
            errors.append(f"integridad: {label}: P2P publicado exige upstream_id")

    _pair_notes(errors, published)
    _unique_slots(errors, published)

    if edition["status"] != "published":
        return

    officials = [row for row in published if row["indicator"] == "tasa_oficial_bcv"]
    for side in ("compra", "venta"):
        count = sum(1 for row in officials if row["side"] == side)
        if count != 1:
            errors.append(f"integridad: '{eid}': hace falta exactamente 1 tasa oficial de {side}")

    banks = {
        row["institution"]["id"]
        for row in published
        if row["indicator"] == "tasa_informativa_banco" and row["institution"]["kind"] == "banco"
    }
    if len(banks) < 3:
        errors.append(f"integridad: '{eid}': hacen falta al menos 3 bancos (hay {len(banks)})")

    p2p = [row for row in published if row["indicator"] == "p2p_referencia"]
    if edition["p2p_status"] == "sin_dato":
        if p2p:
            errors.append(f"integridad: '{eid}': sin_dato no admite observaciones P2P publicadas")
        return
    _p2p_independence(errors, eid, p2p)


def _pair_notes(errors: list[str], published: list[dict[str, Any]]) -> None:
    by_key: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = {}
    for row in published:
        key = (row["edition"], row["indicator"], row["institution"]["id"])
        by_key.setdefault(key, {})[row["side"]] = row
    for sides in by_key.values():
        compra = sides.get("compra")
        venta = sides.get("venta")
        if compra and venta and compra["value"] > venta["value"] and not compra.get("notes"):
            errors.append(
                f"integridad: '{compra['id']}': compra > venta exige notes "
                "(así lo publica la fuente)"
            )


def _unique_slots(errors: list[str], published: list[dict[str, Any]]) -> None:
    seen: set[tuple[str, str, str, str]] = set()
    for row in published:
        slot = (row["edition"], row["indicator"], row["institution"]["id"], row["side"])
        if slot in seen:
            errors.append(f"integridad: '{row['id']}' repite indicador, institución y lado")
        seen.add(slot)


def _p2p_independence(errors: list[str], eid: str, rows: list[dict[str, Any]]) -> None:
    by_side: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_side.setdefault(row["side"], []).append(row)
    if not by_side:
        errors.append(f"integridad: '{eid}': p2p_status publicado exige al menos un lado P2P")
        return
    for side, group in by_side.items():
        upstreams = [row["source"].get("upstream_id") for row in group]
        if any(item is None for item in upstreams):
            continue
        if len(upstreams) != len(set(upstreams)):
            errors.append(f"integridad: '{eid}': P2P {side} repite upstream_id")
        if len(set(upstreams)) < 2:
            errors.append(
                f"integridad: '{eid}': P2P {side} necesita al menos 2 upstream_id distintos"
            )


def collect_errors(
    observations_path: Path = OBSERVATIONS_PATH,
    schema_path: Path = SCHEMA_PATH,
    today: date | None = None,
) -> list[str]:
    errors: list[str] = []
    document = load_json(observations_path)
    validator = Draft202012Validator(load_json(schema_path))
    for err in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path)):
        location = "/".join(str(part) for part in err.absolute_path) or "<raíz>"
        errors.append(f"schema: {location}: {err.message}")
    if errors:
        return errors

    clock = today or datetime.now(UTC).date()
    editions = {edition["id"]: edition for edition in document["editions"]}
    if len(editions) != len(document["editions"]):
        errors.append("integridad: id de edición duplicado")

    seen: set[str] = set()
    grouped: dict[str, list[dict[str, Any]]] = {eid: [] for eid in editions}
    for row in document["observations"]:
        rid = row["id"]
        if rid in seen:
            errors.append(f"integridad: id duplicado '{rid}'")
        seen.add(rid)
        edition_id = row["edition"]
        if edition_id not in editions:
            errors.append(f"integridad: '{rid}' cita la edición inexistente '{edition_id}'")
            continue
        grouped[edition_id].append(row)

    for edition in document["editions"]:
        _edition_rules(errors, edition, grouped.get(edition["id"], []), clock)
    return errors


def main() -> int:
    if not OBSERVATIONS_PATH.exists():
        print(f"ERROR no existe {OBSERVATIONS_PATH}", file=sys.stderr)
        return 1
    errors = collect_errors()
    if errors:
        print(f"ERROR {len(errors)} error(es) en data/fx/observations.json", file=sys.stderr)
        for line in errors:
            print(f"  - {line}", file=sys.stderr)
        return 1
    count = len(load_json(OBSERVATIONS_PATH)["observations"])
    print(f"OK data/fx/observations.json válido ({count} observaciones)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
