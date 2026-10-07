import os
import re

ROOT = "."
EXCLUDES = {".git", "node_modules", ".venv", ".mypy_cache", ".pytest_cache", ".ruff_cache", "out", ".next"}
EXCLUDE_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".lock", ".csv", ".json"} # Exclude json to not break locks, wait, I need to update package.json, signals.schema.json, etc. 
# Better to include json, but exclude lock files specifically.
EXCLUDE_FILES = {"package-lock.json", "uv.lock", "rename.py"}

REPLACEMENTS = [
    (r"Radar Venezuela", "CitedVE"),
    (r"radar-venezuela", "citedve"),
    (r"radarvenezuela\.org", "citedve.vercel.app"),
    (r"VE Radar", "CitedVE"),
    (r"venezuela-radar", "citedve"),
]

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        return # Skip binary files

    new_content = content
    for pattern, repl in REPLACEMENTS:
        new_content = re.sub(pattern, repl, new_content, flags=re.IGNORECASE)
        
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDES]
    for file in files:
        if file in EXCLUDE_FILES or any(file.endswith(ext) for ext in EXCLUDE_EXTS if ext != ".json"):
            continue
        process_file(os.path.join(root, file))
