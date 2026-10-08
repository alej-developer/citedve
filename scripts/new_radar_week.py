"""Script interactivo para el flujo de trabajo semanal del analista (Human-in-the-loop).

Uso:
    uv run python scripts/new_radar_week.py --week YYYY-MM-DD
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "radar"
TEMPLATE_PATH = CONTENT_DIR / "_template.md"
SOURCES_PATH = ROOT / "docs" / "SOURCES.md"


def parse_sources_checklist() -> list[str]:
    """Lee docs/SOURCES.md y extrae la lista de URLs estables para revisión humana."""
    urls: list[str] = []
    if not SOURCES_PATH.exists():
        return urls

    content = SOURCES_PATH.read_text(encoding="utf-8")
    for line in content.splitlines():
        if line.startswith("|") and "http" in line:
            # Extraer URL del markdown
            match = re.search(r"<(https?://[^>]+)>", line)
            if match:
                urls.append(match.group(1))
    return urls


def main() -> int:
    parser = argparse.ArgumentParser(description="Inicia el flujo de trabajo de la semana.")
    parser.add_argument("--week", required=True, help="Fecha del lunes de la semana (YYYY-MM-DD)")
    args = parser.parse_args()
    week: str = args.week

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", week):
        print("ERROR: La fecha debe tener el formato YYYY-MM-DD.", file=sys.stderr)
        return 1

    target_md = CONTENT_DIR / f"{week}.md"

    print(f"=== CitedVE - Semana {week} ===")

    # 1. Crear documento desde plantilla
    if not target_md.exists():
        print(f"[*] Creando {target_md.name} desde la plantilla...")
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
        target_md.write_text(template.replace("{WEEK}", week), encoding="utf-8")
    else:
        print(f"[*] El documento {target_md.name} ya existe. Saltando creación.")

    # 2. Imprimir checklist de fuentes
    print("\n[*] Checklist de fuentes (Humano-in-the-loop):")
    print("    Verifique estas fuentes y agregue las señales a data/signals.json:")
    urls = parse_sources_checklist()
    for url in urls:
        print(f"    - [ ] {url}")

    print("\n    (Nota: No usamos scrapers masivos para cumplir con TOS y evitar baneos anti-bot).")

    # 3 & 4. Validar y construir datos
    print("\n[*] Ejecutando validación de señales y derivados (data/*)...")
    try:
        subprocess.run(["uv", "run", "python", "scripts/validate_signals.py"], check=True, cwd=ROOT)
        subprocess.run(["uv", "run", "python", "scripts/build_data.py"], check=True, cwd=ROOT)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] ERROR en la validación o construcción. Código: {e.returncode}")
        return e.returncode

    # 5. Resumen final
    print("\n=== Resumen Operativo ===")
    print("[OK] Markdown inicializado.")
    print("[OK] Señales validadas y derivados reconstruidos.")
    print("\nSiguientes pasos:")
    print(f"  1. Edita {target_md.relative_to(ROOT)} para pulir el contenido.")
    print('  2. git add data/ content/ && git commit -m "feat: radar semanal ' + week + '"')
    print("  3. Abre el PR.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
