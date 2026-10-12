from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Site

from content.models import ProductPage
from seo.models import SeoRedirect
from seo.services import analyze_page, metadata_for


class SEOTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)

    def test_metadata_defaults_and_self_canonical(self):
        page = ProductPage.objects.live().first()
        page.seo_title = ""
        page.canonical_url = ""
        metadata = metadata_for(page)
        self.assertIn(page.title, metadata["title"])
        self.assertEqual(metadata["canonical"], f"http://localhost:3000{page.url}")

    def test_analysis_is_health_indicator(self):
        page = ProductPage.objects.live().first()
        page.search_description = ""
        result = analyze_page(page)
        self.assertLess(result["health"], 100)
        self.assertIn("description_missing", {issue["code"] for issue in result["issues"]})

    def test_redirect_loop_is_rejected(self):
        site = Site.objects.get(is_default_site=True)
        SeoRedirect.objects.create(site=site, old_path="/a/", new_url="/b/")
        redirect = SeoRedirect(site=site, old_path="/b/", new_url="/a/")
        with self.assertRaises(ValidationError):
            redirect.full_clean()

    def test_redirect_path_and_self_target_are_rejected(self):
        site = Site.objects.get(is_default_site=True)
        invalid_path = SeoRedirect(site=site, old_path="old", new_url="/new/")
        with self.assertRaises(ValidationError) as path_error:
            invalid_path.full_clean()
        self.assertIn("old_path", path_error.exception.message_dict)

        self_target = SeoRedirect(site=site, old_path="/same/", new_url="/same/")
        with self.assertRaises(ValidationError) as self_error:
            self_target.full_clean()
        self.assertIn("new_url", self_error.exception.message_dict)
