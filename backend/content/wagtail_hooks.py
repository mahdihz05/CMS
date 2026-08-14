from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem
from wagtail.admin.ui.components import Component
from wagtail.models import Page, Site, WorkflowState
from wagtail.snippets.models import register_snippet

from content.admin_views import (
    BlogPageViewSet, CategoryViewSet, MenuViewSet, ProductPageViewSet,
    SeoRedirectViewSet, StandardPageViewSet, seo_dashboard,
)
from content.models import BlogPage, Category, ContactPage, ProductPage
from seo.models import SeoRedirect


PAGE_VIEWSET = StandardPageViewSet(name="visiona_pages")
POST_VIEWSET = BlogPageViewSet(name="visiona_posts")
PRODUCT_VIEWSET = ProductPageViewSet(name="visiona_products")
CATEGORY_VIEWSET = CategoryViewSet(name="visiona_categories")
MENU_VIEWSET = MenuViewSet(name="visiona_menus")
REDIRECT_VIEWSET = SeoRedirectViewSet(name="visiona_redirects")

register_snippet(CATEGORY_VIEWSET)
register_snippet(MENU_VIEWSET)
register_snippet(REDIRECT_VIEWSET)


@hooks.register("register_admin_viewset")
def register_page_viewsets():
    return [PAGE_VIEWSET, POST_VIEWSET, PRODUCT_VIEWSET]


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("content/css/admin-wordpress.css"))


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script src="{}"></script>', static("content/js/admin-wordpress.js"))


@hooks.register("register_admin_urls")
def register_custom_urls():
    return [path("seo-dashboard/", seo_dashboard, name="visiona_seo_dashboard")]


@hooks.register("construct_main_menu")
def build_persian_menu(request, menu_items):
    originals = {item.name: item for item in menu_items}
    roles = set(request.user.groups.values_list("name", flat=True))
    is_developer = request.user.is_superuser or "Developer" in roles
    can_manage_content = request.user.is_superuser or bool(roles & {"Developer", "Content Editor", "Client / Site Manager", "SEO Specialist"})
    can_manage_seo = request.user.is_superuser or bool(roles & {"Developer", "SEO Specialist", "Client / Site Manager"})
    can_manage_display = request.user.is_superuser or bool(roles & {"Developer", "Client / Site Manager"})
    dashboard = originals.get("wagtailadmin_home")
    if dashboard:
        dashboard.label, dashboard.order = "پیشخوان", 10

    content_menu = Menu(items=[
        MenuItem("برگه‌ها", PAGE_VIEWSET.menu_url, icon_name="doc-full", order=10),
        MenuItem("نوشته‌ها", POST_VIEWSET.menu_url, icon_name="edit", order=20),
    ])
    shop_menu = Menu(items=[
        MenuItem("محصولات", PRODUCT_VIEWSET.menu_url, icon_name="tag", order=10),
        MenuItem("دسته‌بندی محصولات", CATEGORY_VIEWSET.menu_url, icon_name="folder-open-inverse", order=20),
    ])
    media_items = []
    for name, label in (("images", "تصاویر"), ("documents", "اسناد")):
        if name in originals:
            originals[name].label = label
            media_items.append(originals[name])
    seo_items = [
        MenuItem("پیشخوان سئو", reverse("visiona_seo_dashboard"), icon_name="search", order=10),
        MenuItem("تغییر مسیرها", REDIRECT_VIEWSET.menu_url, icon_name="redirect", order=20),
        MenuItem("نقشه سایت", "/api/v1/sitemap.xml", icon_name="site", order=30, attrs={"target": "_blank"}),
    ]
    site = Site.objects.filter(is_default_site=True).first()
    if site:
        seo_items.append(MenuItem("تنظیمات سئو", reverse("wagtailsettings:edit", args=["content", "sitesettings", site.pk]), icon_name="cog", order=40))
    seo_menu = Menu(items=seo_items)
    display_menu = Menu(items=[MenuItem("فهرست‌ها", MENU_VIEWSET.menu_url, icon_name="list-ul")])

    preserved = []
    for name, label, order in (("forms", "فرم‌ها", 70), ("auth", "کاربران", 80), ("settings", "تنظیمات", 90)):
        if name in originals:
            originals[name].label, originals[name].order = label, order
            preserved.append(originals[name])
    if is_developer and "explorer" in originals:
        originals["explorer"].label, originals["explorer"].order = "درخت صفحات (پیشرفته)", 95
        preserved.append(originals["explorer"])

    sections = []
    if can_manage_content:
        sections.extend([
            SubmenuMenuItem("محتوا", content_menu, name="visiona_content", icon_name="doc-full", order=20),
            SubmenuMenuItem("فروشگاه", shop_menu, name="visiona_shop", icon_name="tag", order=30),
            SubmenuMenuItem("رسانه", Menu(items=media_items), name="visiona_media", icon_name="image", order=40),
        ])
    if can_manage_seo:
        sections.append(SubmenuMenuItem("سئو", seo_menu, name="visiona_seo", icon_name="search", order=50))
    if can_manage_display:
        sections.append(SubmenuMenuItem("نمایش", display_menu, name="visiona_display", icon_name="view", order=60))
    menu_items[:] = ([dashboard] if dashboard else []) + sections + preserved


class VisionaSummaryPanel(Component):
    order = 10
    template_name = "content/admin/dashboard.html"

    def __init__(self, request):
        self.request = request

    def get_context_data(self, parent_context=None):
        pages = Page.objects.exclude(depth=1)
        products = ProductPage.objects.all()
        specific_pages = list(pages.specific())
        return {
            "page_count": pages.count(), "post_count": BlogPage.objects.count(),
            "product_count": products.count(), "category_count": Category.objects.count(),
            "form_count": ContactPage.objects.count(),
            "draft_count": pages.filter(live=False).count(),
            "published_count": pages.filter(live=True).count(),
            "scheduled_count": pages.filter(live=False, go_live_at__isnull=False).count(),
            "review_count": WorkflowState.objects.filter(status=WorkflowState.STATUS_IN_PROGRESS).count(),
            "available_count": products.filter(is_available=True).count(),
            "unavailable_count": products.filter(is_available=False).count(),
            "sale_count": products.exclude(discount_price=None).count(),
            "featured_count": products.filter(is_featured=True).count(),
            "seo_issues": sum(1 for p in specific_pages if not getattr(p, "search_description", "")),
            "recent_pages": pages.order_by("-latest_revision_created_at")[:6].specific(),
            "urls": {"pages": PAGE_VIEWSET.menu_url, "posts": POST_VIEWSET.menu_url,
                     "products": PRODUCT_VIEWSET.menu_url, "categories": CATEGORY_VIEWSET.menu_url,
                     "seo": reverse("visiona_seo_dashboard")},
            "can_add_pages": self.request.user.has_perm("wagtailcore.add_page"),
            "can_add_images": self.request.user.has_perm("wagtailimages.add_image"),
        }


@hooks.register("construct_homepage_panels")
def add_summary_panel(request, panels):
    panels.insert(0, VisionaSummaryPanel(request))


@hooks.register("before_publish_page")
def create_slug_redirect(request, page):
    if not page.pk:
        return
    old = Page.objects.filter(pk=page.pk).specific().first()
    if not old or old.slug == page.slug or not old.live:
        return
    parent_url = old.get_parent().url or "/"
    new_path = f"{parent_url.rstrip('/')}/{page.slug}/"
    SeoRedirect.objects.update_or_create(site=old.get_site(), old_path=old.url, defaults={"new_url": new_path, "status_code": 301, "is_active": True})
