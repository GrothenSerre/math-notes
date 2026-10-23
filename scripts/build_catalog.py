"""Generate Quarto listings from the existing archive and uploaded files.

Uses only Python's standard library. Run automatically before `quarto render`.
Optional title/category overrides live in _data/documents.json.
"""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "_generated"


def human_size(size):
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{max(1, round(size / 1024))} KB"


def build():
    metadata = json.loads((ROOT / "_data/documents.json").read_text(encoding="utf-8"))
    paths = set()
    for relative in metadata:
        path = ROOT / relative
        if path.is_file() and not path.is_symlink():
            paths.add(path)
    # New uploads need no manual index entry.
    for folder in ("documents/files", "mathematics/files"):
        for path in (ROOT / folder).rglob("*"):
            if path.is_file() and not path.is_symlink() and not any(
                part.startswith(".") for part in path.relative_to(ROOT / folder).parts
            ):
                paths.add(path)

    documents = []
    mathematics = []
    for path in sorted(paths):
        relative = path.relative_to(ROOT).as_posix()
        overrides = metadata.get(relative, {})
        is_math = relative.startswith("mathematics/files/") or (
            relative in metadata and not relative.startswith("documents/")
            and overrides.get("kind") != "CV"
        )
        item = {
            "title": re.sub(r"[_-]+", " ", path.stem).strip(),
            "description": "",
            "categories": ["Mathematics" if is_math else "Documents"],
            "kind": "Note" if is_math else "Document",
            "year": "",
            **overrides,
            "path": "/" + relative,
            "filetype": path.suffix.lstrip(".").upper() or "FILE",
            "size": human_size(path.stat().st_size),
        }
        documents.append(item)
        # The theses have their own HTML introduction pages in mathematics/notes.
        if is_math and overrides.get("kind") not in ("Master's thesis", "Bachelor's thesis"):
            mathematics.append(item)

    GENERATED.mkdir(exist_ok=True)
    for name, items in (("documents", documents), ("mathematics", mathematics)):
        # JSON is a valid YAML subset and avoids a Python package dependency.
        (GENERATED / f"{name}.yml").write_text(
            json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"Catalogued {len(documents)} downloadable files.")


if __name__ == "__main__":
    build()
