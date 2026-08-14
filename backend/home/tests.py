from django.test import TestCase

from home.models import HomePage


class HomePageTests(TestCase):
    fixtures = []

    def test_home_model_has_seo_fields(self):
        fields = {field.name for field in HomePage._meta.fields}
        self.assertTrue({"canonical_url", "robots_index", "og_title", "sitemap_included"} <= fields)
