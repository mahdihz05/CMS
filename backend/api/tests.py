from django.core.management import call_command
from django.test import TestCase
import json


class PublicAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)

    def get(self, path):
        return self.client.get(path, HTTP_HOST="localhost")

    def test_home_and_product_page_api(self):
        home = self.get("/api/v1/pages/resolve/")
        self.assertEqual(home.status_code, 200)
        self.assertEqual(home.json()["data"]["title"], "ویژنا؛ فروشگاه تخصصی عینک")
        product = self.get("/api/v1/pages/resolve/?path=shop/aria-sunglasses")
        self.assertEqual(product.status_code, 200)
        data = product.json()["data"]
        self.assertEqual(data["product"]["sku"], "VSN-SUN-001")
        self.assertEqual(data["product"]["priceToman"], "3490000")
        self.assertEqual(data["schemas"][0]["@type"], "Product")
        self.assertEqual(data["schemas"][0]["offers"]["priceCurrency"], "IRR")
        self.assertEqual(data["schemas"][0]["offers"]["price"], "31900000")
        self.assertIn("canonical", data["metadata"])

    def test_navigation_settings_sitemap_and_robots(self):
        self.assertIn("header", self.get("/api/v1/navigation/").json()["data"])
        settings = self.get("/api/v1/site-settings/").json()["data"]
        self.assertEqual(settings["siteName"], "ویژنا")
        self.assertEqual(settings["locale"], "fa-IR")
        self.assertEqual(settings["direction"], "rtl")
        sitemap = self.get("/api/v1/sitemap.xml")
        self.assertContains(sitemap, "shop/aria-sunglasses", status_code=200)
        robots = self.get("/api/v1/robots.txt")
        self.assertContains(robots, "Sitemap:", status_code=200)

    def test_redirect_statuses_are_exposed(self):
        from seo.models import SeoRedirect
        from wagtail.models import Site
        SeoRedirect.objects.create(site=Site.objects.get(is_default_site=True), old_path="/old/", new_url="/shop/", status_code=308)
        data = self.get("/api/v1/redirects/resolve/?path=/old/").json()["data"]
        self.assertEqual(data, {"url": "/shop/", "status": 308})

    def test_contact_form_requires_server_secret_and_stores_submission(self):
        from content.models import ContactPage
        from wagtail.contrib.forms.models import FormSubmission
        page = ContactPage.objects.live().get()
        payload = {"pageId": page.id}
        for field in page.get_form_fields():
            payload[field.clean_name] = "demo@example.com" if field.field_type == "email" else "پیام آزمایشی"
        denied = self.client.post("/api/v1/forms/submit/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(denied.status_code, 403)
        accepted = self.client.post("/api/v1/forms/submit/", data=json.dumps(payload), content_type="application/json", HTTP_X_VISIONA_FORM_SECRET="unsafe-development-form-secret")
        self.assertEqual(accepted.status_code, 201)
        self.assertEqual(FormSubmission.objects.filter(page=page).count(), 1)
