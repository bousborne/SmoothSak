"""Check the static publication directory without installing dependencies."""

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


SITE_ROOT = Path(__file__).resolve().parents[1] / "smoothsak.com" / "html"


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "src" in attrs:
            self.references.append(attrs["src"])
        if tag == "link" and "href" in attrs:
            self.references.append(attrs["href"])


class StaticSiteTests(unittest.TestCase):
    def check_reference(self, reference, source):
        parsed = urlsplit(reference)
        if parsed.netloc or parsed.scheme:
            self.assertIn(parsed.scheme, ("https", "data"), reference)
            return
        if not parsed.path:
            return
        base = SITE_ROOT if parsed.path.startswith("/") else source.parent
        target = (base / unquote(parsed.path.lstrip("/"))).resolve()
        self.assertTrue(target.is_relative_to(SITE_ROOT.resolve()), reference)
        self.assertTrue(target.is_file(), f"{source.name}: missing {reference}")

    def test_html_assets(self):
        source = SITE_ROOT / "index.html"
        parser = AssetParser()
        parser.feed(source.read_text())
        self.assertTrue(parser.references)
        for reference in parser.references:
            with self.subTest(reference=reference):
                self.check_reference(reference, source)

    def test_css_assets(self):
        for source in SITE_ROOT.glob("css/*.css"):
            for reference in re.findall(r"url\(\s*([^)]*?)\s*\)", source.read_text()):
                with self.subTest(source=source.name, reference=reference):
                    self.check_reference(reference.strip("\"'"), source)


if __name__ == "__main__":
    unittest.main()
