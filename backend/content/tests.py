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
        home = Page.objects.get(slug="home").specific
        draft = StandardPage(title="Hidden draft", slug="hidden-draft", live=False, search_description="A private draft page for test coverage.")
        home.add_child(instance=draft)
        response = self.client.get("/api/v1/pages/resolve/?path=hidden-draft", HTTP_HOST="localhost")
        self.assertEqual(response.status_code, 404)

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
        self.assertContains(response, "admin-wordpress.css")

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
