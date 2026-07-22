#!/usr/bin/env python3
"""Dependency-free structural checks for the PRIMO static site."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.landmarks = set()
        self.title = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if value := attributes.get("id"):
            assert value not in self.ids, f"Duplicate id: {value}"
            self.ids.add(value)
        if tag == "a":
            self.links.append(attributes.get("href", ""))
        if tag == "img":
            self.images.append(attributes)
        if tag in {"header", "main", "footer", "nav"}:
            self.landmarks.add(tag)
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title.append(data)


def main():
    required = [
        "index.html",
        "styles.css",
        "script.js",
        "assets/primo-logo.png",
        "assets/primo-banner.png",
        "assets/favicon.svg",
        ".github/workflows/pages.yml",
    ]
    for relative in required:
        path = ROOT / relative
        assert path.exists() and (path.stat().st_size > 0 or path.name == ".nojekyll"), f"Missing/empty: {relative}"

    html = (ROOT / "index.html").read_text()
    parser = SiteParser()
    parser.feed(html)

    assert set(["header", "main", "footer", "nav"]).issubset(parser.landmarks)
    assert "PRIMO" in "".join(parser.title)
    assert {"top", "mission", "benchmark", "publication", "participate"}.issubset(parser.ids)

    for image in parser.images:
        assert image.get("alt"), f"Image lacks alt text: {image}"
        source = image.get("src", "")
        assert source and (ROOT / source).exists(), f"Missing image source: {source}"
        assert image.get("width") and image.get("height"), f"Image lacks dimensions: {source}"

    for href in parser.links:
        assert href and href != "#", "Empty or fake link found"
        parsed = urlparse(href)
        if href.startswith("#"):
            assert href[1:] in parser.ids, f"Broken fragment: {href}"
        elif not parsed.scheme:
            target = href.split("#", 1)[0]
            assert (ROOT / target).exists(), f"Broken internal link: {href}"
        else:
            assert parsed.scheme in {"https", "mailto"}, f"Unsafe link scheme: {href}"

    assert "Coming soon" in html
    assert "href=\"#\"" not in html
    print(f"PASS: {len(parser.ids)} ids, {len(parser.links)} links, {len(parser.images)} image(s), all structural checks passed")


if __name__ == "__main__":
    main()
