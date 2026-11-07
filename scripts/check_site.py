"""Check actual Jekyll HTML for missing local links, fragments and resources."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for attribute in (["href"] if tag in ("a", "link") else ["src"] if tag in ("img", "script", "iframe") else []):
            if attrs.get(attribute):
                self.links.append(attrs[attribute])


def validate(root):
    errors = []
    pages = {p.resolve(): Page(p.read_text(encoding="utf-8")) for p in root.rglob("*.html")}
    if not pages:
        return [f"{root}: no built HTML; run bundle exec jekyll build first"]
    # The production origin is read from the generated CNAME, not hard-coded.
    cname = root / "CNAME"
    host = cname.read_text().strip() if cname.exists() else "local.test"
    origin = f"https://{host}"
    for file, page in pages.items():
        relative = file.relative_to(root).as_posix()
        for link in page.links:
            if "{{" in link or "{%" in link:
                errors.append(f"{relative}: unrendered Liquid: {link}")
                continue
            url = urlsplit(urljoin(f"{origin}/{relative}", link))
            if url.scheme not in ("http", "https") or url.netloc != host:
                continue
            target = (root / unquote(url.path).lstrip("/")).resolve()
            if not target.is_relative_to(root):
                errors.append(f"{relative}: path outside site: {link}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.exists() and not target.suffix:
                target = target.with_suffix(".html")
            if not target.is_file():
                errors.append(f"{relative}: broken local link/resource: {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{relative}: missing fragment: {link}")
    return errors


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
    errors = validate(root)
    print("\n".join(errors) if errors else "Built-site links and resources passed.")
    sys.exit(bool(errors))
