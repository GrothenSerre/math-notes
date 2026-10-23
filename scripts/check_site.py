"""Check rendered internal links and byte-for-byte preservation of downloads."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import posixpath

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
BASE_PATH = "/math-notes/"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        key = "href" if tag in ("a", "link") else "src" if tag in ("script", "img") else None
        if key and attr.get(key):
            self.links.append(attr[key])


def digest(path):
    return hashlib.sha256(path.read_bytes()).digest()


def check():
    if not (SITE / "index.html").is_file():
        raise SystemExit("Run quarto render before checking the site.")
    problems = []
    html_files = list(SITE.rglob("*.html"))
    checked = 0
    for html in html_files:
        parser = LinkParser()
        parser.feed(html.read_text(encoding="utf-8"))
        for raw in parser.links:
            url = urlsplit(raw)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if path.startswith(BASE_PATH):
                path = path[len(BASE_PATH):]
                target = SITE / path
            elif path.startswith("/"):
                target = SITE / path.lstrip("/")
            else:
                target = html.parent / path
            target = Path(posixpath.normpath(str(target)))
            if target.is_dir():
                target = target / "index.html"
            checked += 1
            if not target.is_file():
                problems.append(f"{html.relative_to(SITE)}: {raw}")

    documents = json.loads((ROOT / "_generated/documents.yml").read_text(encoding="utf-8"))
    for item in documents:
        relative = item["path"].lstrip("/")
        source, published = ROOT / relative, SITE / relative
        if not published.is_file() or digest(source) != digest(published):
            problems.append(f"Missing or changed download: {relative}")
    if problems:
        raise SystemExit("Broken site references:\n" + "\n".join(problems))
    print(f"Verified {len(html_files)} pages, {checked} internal references, and {len(documents)} unchanged downloads.")


if __name__ == "__main__":
    check()
