"""Exercise the user-facing checks against small, real site directories."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContentCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = {
            "name": "Test Person", "email": "person@example.com",
            "avatar": "/images/photo.png", "updated_on": "2026-11-07",
            "degree": {"en": "PhD", "zh": "博士"},
            "current": {"employer": "Example", "employer_url": "https://example.com",
                        "role": {"en": "Engineer", "zh": "工程师"},
                        "since": "2021.07", "summary": {"en": "Research", "zh": "研究"}},
            "links": [],
        }
        self.put("_data/profile.yml", json.dumps(self.profile))
        self.put("_config.yml", 'url: https://example.com\nbaseurl: ""\n')
        self.put("CNAME", "example.com\n")
        self.put("_data/navigation.yml", 'main:\n  - title: Home\n    url: /\n')
        self.put("_pages/about.md", '---\ntitle: Home\npermalink: /\n---\nHello\n')
        self.put("images/photo.png", "test image")
        self.put("_publications/paper.md", '---\ntitle: Real paper\npermalink: /paper/\nyear: 2021\ncategory: manuscripts\nvenue: Journal\ncitation: A citation\nselected: true\n---\nAbstract\n')

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_check(self):
        return subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts/check_content.py"), str(self.root)],
                              text=True, capture_output=True, encoding="utf-8")

    def test_valid_content_passes(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_email_is_explained(self):
        del self.profile["email"]
        self.put("_data/profile.yml", json.dumps(self.profile))
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("profile.yml: email", result.stdout)

    def test_invalid_calendar_date_is_rejected(self):
        self.profile["updated_on"] = "2026-02-30"
        self.put("_data/profile.yml", json.dumps(self.profile))
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("updated_on", result.stdout)

    def test_missing_avatar_is_rejected(self):
        (self.root / "images/photo.png").unlink()
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("images/photo.png", result.stdout)

    def test_duplicate_output_route_is_rejected(self):
        self.put("_pages/duplicate.md", '---\ntitle: Duplicate\npermalink: /paper/\n---\n')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate route", result.stdout)

    def test_unsafe_contact_url_is_rejected(self):
        self.profile["links"] = [{"label": "Link", "url": "javascript:alert(1)"}]
        self.put("_data/profile.yml", json.dumps(self.profile))
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("https://", result.stdout)

    def test_equivalent_html_output_routes_are_rejected(self):
        self.put("_pages/one.md", '---\ntitle: One\npermalink: /same-name\n---\n')
        self.put("_pages/two.md", '---\ntitle: Two\npermalink: /same-name.html\n---\n')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate route", result.stdout)

    def test_malformed_contact_url_has_a_field_error(self):
        self.profile["links"] = [{"label": "Link", "url": "https://[bad.example/paper"}]
        self.put("_data/profile.yml", json.dumps(self.profile))
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("profile.yml: links.url", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_malformed_site_url_has_a_field_error(self):
        self.put("_config.yml", 'url: "https://[bad.example"\n')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("_config.yml: url", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


class BuiltSiteCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "index.html").write_text('<html><title>Home</title><a href="/cv/#education">CV</a></html>')
        (self.root / "cv").mkdir()
        (self.root / "cv/index.html").write_text('<html><title>CV</title><h2 id="education">Education</h2></html>')

    def check(self):
        return subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts/check_site.py"), str(self.root)],
                              text=True, capture_output=True, encoding="utf-8")

    def test_existing_internal_page_and_fragment_pass(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_internal_page_fails(self):
        (self.root / "cv/index.html").unlink()
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("/cv/#education", result.stdout)

    def test_missing_fragment_fails(self):
        (self.root / "cv/index.html").write_text('<html><title>CV</title></html>')
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("education", result.stdout)


if __name__ == "__main__":
    unittest.main()
