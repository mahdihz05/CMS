from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from wagtail.models import Page

from content.models import BlogPage, Category, ProductPage, StandardPage


class DemoContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)

    def test_seed_is_idempotent_and_complete(self):
        call_command("seed_demo", verbosity=0)
        self.assertEqual(ProductPage.objects.live().count(), 12)
        self.assertEqual(BlogPage.objects.live().count(), 6)
        self.assertEqual(Category.objects.count(), 4)
        self.assertTrue(Page.objects.filter(slug="about", live=True).exists())
        self.assertTrue(Page.objects.filter(slug="contact", live=True).exists())

    def test_draft_is_not_public(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse

        home = Page.objects.get(slug="home").specific
        draft = StandardPage(title="Hidden draft", slug="hidden-draft", live=False, search_description="A private draft page for test coverage.")
        home.add_child(instance=draft)
        response = self.client.get("/api/v1/pages/resolve/?path=hidden-draft", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 404)
        self.client.force_login(get_user_model().objects.get(username="admin"))
        admin_response = self.client.get(reverse("visiona_pages:index"), {"q": "Hidden draft"})
        self.assertContains(admin_response, "Hidden draft")
        self.assertContains(admin_response, "False")

    def test_seeded_roles_are_separated(self):
        from django.contrib.auth.models import Group
        editor = Group.objects.get(name="Content Editor")
        seo = Group.objects.get(name="SEO Specialist")
        self.assertTrue(editor.permissions.filter(codename="add_image").exists())
        self.assertFalse(editor.permissions.filter(codename="add_seoredirect").exists())
        self.assertTrue(seo.permissions.filter(codename="add_seoredirect").exists())

    def test_admin_dashboard_and_core_sections_render(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse
        from wagtail.models import Site

        self.client.force_login(get_user_model().objects.get(username="admin"))
        urls = [
            reverse("wagtailadmin_home"),
            reverse("wagtailadmin_explore_root"),
            reverse("wagtailimages:index"),
            reverse("wagtaildocs:index"),
            reverse("wagtailforms:index"),
            reverse("wagtailsnippets_seo_seoredirect:list"),
            reverse(
                "wagtailsettings:edit",
                args=["content", "sitesettings", Site.objects.get(is_default_site=True).pk],
            ),
            reverse("wagtailadmin_pages:edit", args=[Page.objects.get(slug="home").pk]),
            reverse("visiona_pages:index"),
            reverse("visiona_posts:index"),
            reverse("visiona_products:index"),
            reverse("visiona_seo_dashboard"),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_admin_is_persian_rtl_and_role_menus_are_scoped(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        from django.test import RequestFactory
        from wagtail.admin.menu import MenuItem
        from content.wagtail_hooks import build_persian_menu

        self.client.force_login(get_user_model().objects.get(username="admin"))
        response = self.client.get("/admin/")
        self.assertContains(response, 'lang="fa"')
        self.assertContains(response, "admin-visiona.css")
        self.assertContains(response, "admin-visiona.js")
        self.assertContains(response, 'data-search-url="/admin/pages/search/"')
        self.assertContains(response, 'data-account-url="/admin/account/"')
        self.assertContains(response, "visiona-brand")
        self.assertContains(response, "ویژونا، مدیریت محتوا")

        expected = {"Content Editor": {"visiona_content", "visiona_shop", "visiona_media"}, "SEO Specialist": {"visiona_content", "visiona_shop", "visiona_media", "visiona_seo"}, "Client / Site Manager": {"visiona_content", "visiona_shop", "visiona_media", "visiona_seo", "visiona_display"}}
        for role, visible in expected.items():
            user = get_user_model().objects.create_user(username=f"menu-{role}", is_staff=True)
            user.groups.add(Group.objects.get(name=role))
            request = RequestFactory().get("/admin/"); request.user = user
            items = [MenuItem("Dashboard", "/admin/", name="wagtailadmin_home")]
            build_persian_menu(request, items)
            names = {item.name for item in items}
            self.assertTrue(visible.issubset(names))
            self.assertNotIn("explorer", names)

    def test_admin_login_uses_visiona_skin_and_real_wagtail_form(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ورود به مدیریت ویژونا")
        self.assertContains(response, "visiona-login-intro")
        self.assertContains(response, "admin-visiona.css")
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, "reset-password")

        invalid = self.client.post("/admin/login/", {"username": "missing", "password": "wrong"})
        self.assertEqual(invalid.status_code, 200)
        self.assertContains(invalid, "messages")

    def test_admin_skin_is_self_hosted_and_has_stitch_tokens(self):
        from django.contrib.staticfiles import finders
        from pathlib import Path

        css_path = Path(finders.find("content/css/admin-visiona.css"))
        css = css_path.read_text(encoding="utf-8")
        self.assertIn("--visiona-sidebar:#172033", css)
        self.assertIn("--visiona-primary:#004ac6", css)
        self.assertIn("../fonts/Vazirmatn-Regular.woff2", css)
        self.assertIn(".sidebar,.sidebar-loading{width:260px}", css)
        self.assertIn("prefers-reduced-motion:reduce", css)
        self.assertNotIn("fonts.googleapis.com", css)
        self.assertNotIn("cdn.tailwindcss.com", css)

    def test_dashboard_uses_real_counts_and_permission_scoped_actions(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        from django.db import connection
        from django.test import RequestFactory
        from django.test.utils import CaptureQueriesContext
        from content.wagtail_hooks import VisionaSummaryPanel

        admin = get_user_model().objects.get(username="admin")
        request = RequestFactory().get("/admin/")
        request.user = admin
        with CaptureQueriesContext(connection) as queries:
            panel_context = VisionaSummaryPanel(request).get_context_data()
            list(panel_context["recent_pages"])
        self.assertLessEqual(len(queries), 35)

        self.client.force_login(admin)
        response = self.client.get("/admin/")
        self.assertContains(response, '<strong>1</strong><span>برگه و صفحه</span>', html=True)
        self.assertContains(response, '<strong>6</strong><span>نوشته</span>', html=True)
        self.assertContains(response, '<strong>12</strong><span>محصول</span>', html=True)
        self.assertContains(response, "صف‌های بازبینی")
        self.assertContains(response, "وضعیت سامانه:")

        seo_user = get_user_model().objects.create_user(username="seo-dashboard", is_staff=True)
        seo_user.groups.add(Group.objects.get(name="SEO Specialist"))
        self.client.force_login(seo_user)
        seo_response = self.client.get("/admin/")
        self.assertNotContains(seo_response, "نوشته جدید")
        self.assertNotContains(seo_response, "محصول جدید")
        self.assertNotContains(seo_response, "وضعیت سامانه:")

        editor = get_user_model().objects.create_user(username="editor-dashboard", is_staff=True)
        editor.groups.add(Group.objects.get(name="Content Editor"))
        self.client.force_login(editor)
        editor_response = self.client.get("/admin/")
        self.assertContains(editor_response, "نوشته جدید")
        self.assertContains(editor_response, "محصول جدید")

    def test_admin_listings_keep_real_search_filters_and_create_routes(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        from django.contrib.staticfiles import finders
        from django.urls import reverse
        from pathlib import Path

        self.client.force_login(get_user_model().objects.get(username="admin"))
        searchable = [
            (reverse("visiona_pages:index"), "درباره", "درباره ویژنا"),
            (reverse("visiona_posts:index"), "پلاریزه", "عدسی پلاریزه"),
            (reverse("visiona_products:index"), "آریا", "آفتابی آریا"),
        ]
        for url, query, expected in searchable:
            with self.subTest(url=url):
                response = self.client.get(url, {"q": query})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected)

        filtered = self.client.get(reverse("visiona_products:index"), {"is_available": "false"})
        self.assertEqual(filtered.status_code, 200)
        self.assertContains(filtered, "آفتابی پلاریزه هور")
        self.assertNotContains(filtered, "آفتابی آریا")
        ordered = self.client.get(reverse("visiona_products:index"), {"ordering": "title", "p": 1})
        self.assertEqual(ordered.status_code, 200)
        self.assertContains(ordered, "data-bulk-action-select-all-checkbox")
        self.assertContains(ordered, "pagination")

        create_urls = {}
        for name in ("visiona_pages:choose_parent", "visiona_posts:choose_parent", "visiona_products:choose_parent"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 302)
                create_urls[name] = response["Location"]
                self.assertEqual(self.client.get(response["Location"]).status_code, 200)

        js_path = Path(finders.find("content/js/admin-visiona.js"))
        js = js_path.read_text(encoding="utf-8")
        self.assertIn("enhanceResponsiveListings", js)
        self.assertIn("dataset.visionaLabel", js)

        seo_user = get_user_model().objects.create_user(username="seo-listings", is_staff=True)
        seo_user.groups.add(Group.objects.get(name="SEO Specialist"))
        self.client.force_login(seo_user)
        self.assertNotEqual(self.client.get(create_urls["visiona_products:choose_parent"]).status_code, 200)

    def test_page_and_product_editors_preserve_wagtail_contracts(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        from django.urls import reverse
        from wagtail.admin.panels import get_edit_handler
        from content.blocks import CONTENT_BLOCKS

        about = StandardPage.objects.get(slug="about")
        product = ProductPage.objects.get(sku="VSN-SUN-001")
        self.client.force_login(get_user_model().objects.get(username="admin"))

        page_response = self.client.get(reverse("wagtailadmin_pages:edit", args=[about.pk]))
        self.assertEqual(page_response.status_code, 200)
        for label in ("محتوا", "سئو و شبکه‌های اجتماعی"):
            self.assertContains(page_response, label)
        block_map = dict(CONTENT_BLOCKS)
        self.assertEqual(block_map["rich_text"].label, "متن غنی")
        self.assertEqual(block_map["hero"].label, "بخش آغازین")
        self.assertEqual(
            [panel.heading for panel in get_edit_handler(StandardPage).children],
            ["محتوا", "سئو و شبکه‌های اجتماعی", "تنظیمات پیشرفته"],
        )
        self.assertContains(page_response, 'data-w-unsaved-confirmation-value="true"')
        self.assertContains(page_response, 'name="action-publish"')

        product_response = self.client.get(reverse("wagtailadmin_pages:edit", args=[product.pk]))
        self.assertEqual(product_response.status_code, 200)
        for label in ("اطلاعات محصول", "شناسه کالا", "قیمت (تومان)", "قیمت با تخفیف", "دسته‌بندی", "تصویر محصول"):
            self.assertContains(product_response, label)
        for field_id in ("id_sku", "id_price", "id_discount_price", "id_category", "id_is_available", "id_is_featured", "id_product_image"):
            self.assertContains(product_response, field_id)

        editor = get_user_model().objects.create_user(username="editor-actions", is_staff=True)
        editor.groups.add(Group.objects.get(name="Content Editor"))
        self.client.force_login(editor)
        editor_response = self.client.get(reverse("wagtailadmin_pages:edit", args=[product.pk]))
        self.assertEqual(editor_response.status_code, 200)
        self.assertContains(editor_response, 'name="action-submit"')
        self.assertNotContains(editor_response, 'name="action-publish"')

    def test_media_library_keeps_real_wagtail_upload_and_metadata(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse
        from wagtail.images import get_image_model

        self.client.force_login(get_user_model().objects.get(username="admin"))
        image_index = self.client.get(reverse("wagtailimages:index"))
        self.assertEqual(image_index.status_code, 200)
        self.assertContains(image_index, "layout-switch-control")
        self.assertContains(image_index, "listing horiz images")
        self.assertEqual(self.client.get(reverse("wagtailimages:add")).status_code, 200)
        self.assertEqual(self.client.get(reverse("wagtaildocs:add_multiple")).status_code, 200)

        image = get_image_model().objects.first()
        edit = self.client.get(reverse("wagtailimages:edit", args=[image.pk]))
        self.assertEqual(edit.status_code, 200)
        for field_id in ("id_title", "id_file", "id_collection", "id_tags", "id_focal_point_x", "id_description"):
            self.assertContains(edit, field_id)

    def test_seo_dashboard_uses_analysis_service_and_is_role_scoped(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        from django.urls import reverse

        url = reverse("visiona_seo_dashboard")
        self.client.force_login(get_user_model().objects.get(username="admin"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "راهنمای فنی داخلی")
        self.assertContains(response, "سلامت میانگین")
        self.assertContains(response, "صفحه‌های نیازمند بهبود")

        editor = get_user_model().objects.create_user(username="editor-no-seo", is_staff=True)
        editor.groups.add(Group.objects.get(name="Content Editor"))
        self.client.force_login(editor)
        self.assertNotEqual(self.client.get(url).status_code, 200)

    def test_published_slug_change_prepares_a_301_redirect(self):
        from django.contrib.auth import get_user_model
        from django.test import RequestFactory
        from content.wagtail_hooks import create_slug_redirect
        from seo.models import SeoRedirect

        product = ProductPage.objects.get(sku="VSN-SUN-001")
        old_url = product.url
        product.slug = "aria-sunglasses-updated"
        request = RequestFactory().post("/admin/")
        request.user = get_user_model().objects.get(username="admin")
        create_slug_redirect(request, product)
        redirect = SeoRedirect.objects.get(old_path=old_url)
        self.assertEqual(redirect.status_code, 301)
        self.assertTrue(redirect.new_url.endswith("/aria-sunglasses-updated/"))

    def test_menus_users_and_workflow_keep_real_models_and_permissions(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group
        from django.core.exceptions import ValidationError
        from django.urls import reverse
        from wagtail.models import Workflow
        from content.models import Menu, MenuItem

        self.assertNotIn("css", {field.name for field in MenuItem._meta.fields})
        invalid = MenuItem(menu=Menu.objects.first(), label="نامعتبر")
        with self.assertRaises(ValidationError):
            invalid.full_clean()

        header = Menu.objects.get(slug="header")
        expected_labels = list(header.items.values_list("label", flat=True))
        api_labels = [item["label"] for item in self.client.get("/api/v1/navigation/", HTTP_HOST="localhost").json()["data"]["header"]]
        self.assertEqual(api_labels, expected_labels)

        workflow = Workflow.objects.get(name="بازبینی محتوا و سئو")
        self.assertEqual(
            list(workflow.workflow_tasks.order_by("sort_order").values_list("task__name", flat=True)),
            ["بازبینی محتوا", "بازبینی سئو"],
        )

        admin = get_user_model().objects.get(username="admin")
        self.client.force_login(admin)
        for url in (reverse("wagtailsnippets_content_menu:list"), reverse("wagtailusers_users:index"), reverse("wagtailusers_groups:index"), reverse("wagtailadmin_reports:workflow"), reverse("wagtailadmin_reports:workflow_tasks")):
            self.assertEqual(self.client.get(url).status_code, 200)

        manager = get_user_model().objects.create_user(username="manager-no-users", is_staff=True)
        manager.groups.add(Group.objects.get(name="Client / Site Manager"))
        self.client.force_login(manager)
        self.assertNotEqual(self.client.get(reverse("wagtailusers_users:index")).status_code, 200)
        self.assertEqual(self.client.get(reverse("wagtailsnippets_content_menu:list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("wagtailsnippets_seo_seoredirect:list")).status_code, 200)

        seo_user = get_user_model().objects.create_user(username="seo-model-access", is_staff=True)
        seo_user.groups.add(Group.objects.get(name="SEO Specialist"))
        self.client.force_login(seo_user)
        self.assertEqual(self.client.get(reverse("wagtailsnippets_content_category:list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("wagtailsnippets_seo_seoredirect:list")).status_code, 200)

    def test_non_stitch_admin_screens_inherit_the_shared_design_system(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse
        from wagtail.models import Page, Site

        self.client.force_login(get_user_model().objects.get(username="admin"))
        blog = BlogPage.objects.first()
        contact = Page.objects.get(slug="contact")
        urls = [
            reverse("wagtailadmin_pages:edit", args=[blog.pk]),
            reverse("wagtailsnippets_content_category:list"),
            reverse("wagtailforms:index"),
            reverse("wagtailforms:list_submissions", args=[contact.pk]),
            reverse("wagtailsettings:edit", args=["content", "sitesettings", Site.objects.get(is_default_site=True).pk]),
            reverse("wagtaildocs:index"),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "admin-visiona.css")

        chooser = self.client.get(reverse("wagtailimages_chooser:choose"))
        self.assertEqual(chooser.status_code, 200)
        self.assertContains(chooser, "w-layout-switch-control")

        error = self.client.get("/admin/route-that-does-not-exist/")
        self.assertEqual(error.status_code, 404)
        self.assertContains(error, "admin-visiona.css", status_code=404)

    def test_demo_reset_preserves_non_demo_and_collision_is_guarded(self):
        from content.models import ProductIndexPage
        shop = ProductIndexPage.objects.get(slug="shop")
        category = Category.objects.first()
        user_product = ProductPage(title="محصول کاربر", slug="user-product", sku="USER-001", short_description="محصولی خارج از داده دمو", description="<p>محتوای کاربر</p>", price=2100000, category=category)
        shop.add_child(instance=user_product); user_product.save_revision().publish()
        call_command("seed_demo", reset_demo=True, verbosity=0)
        self.assertTrue(ProductPage.objects.filter(sku="USER-001").exists())

        demo = ProductPage.objects.get(sku="VSN-SUN-001"); demo.delete()
        collision = ProductPage(title="محتوای کاربر", slug="aria-sunglasses", sku="USER-002", short_description="برخورد کنترل‌شده", description="<p>محتوای کاربر</p>", price=2200000, category=category)
        shop = ProductIndexPage.objects.get(slug="shop"); shop.add_child(instance=collision)
        with self.assertRaises(CommandError):
            call_command("seed_demo", verbosity=0)
