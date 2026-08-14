from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.models import Page

from .models import BlogPage, Category, Menu, ProductPage, StandardPage
from seo.models import SeoRedirect


class StandardPageViewSet(PageListingViewSet):
    model = StandardPage
    name = "visiona_pages"
    icon = "doc-full"
    menu_label = "برگه‌ها"
    list_display = ["title", "owner", "live", "latest_revision_created_at"]
    search_fields = ["title", "slug", "search_description"]
    list_filter = ["live"]
    ordering = ["-latest_revision_created_at"]


class BlogPageViewSet(PageListingViewSet):
    model = BlogPage
    name = "visiona_posts"
    icon = "edit"
    menu_label = "نوشته‌ها"
    list_display = ["title", "author_name", "published_date", "live", "latest_revision_created_at"]
    search_fields = ["title", "excerpt", "author_name", "primary_keyword"]
    list_filter = ["live", "published_date"]
    ordering = ["-published_date"]


class ProductPageViewSet(PageListingViewSet):
    model = ProductPage
    name = "visiona_products"
    icon = "tag"
    menu_label = "محصولات"
    list_display = ["title", "sku", "category", "price", "discount_price", "is_available", "is_featured", "live"]
    search_fields = ["title", "sku", "short_description", "primary_keyword"]
    list_filter = ["live", "is_available", "is_featured", "category"]
    ordering = ["-latest_revision_created_at"]


class CategoryViewSet(SnippetViewSet):
    model = Category
    icon = "tag"
    menu_label = "دسته‌بندی محصولات"
    menu_name = "visiona_categories"
    list_display = ["name", "slug", "product_count"]
    search_fields = ["name", "slug", "description"]
    ordering = ["name"]

    def get_queryset(self, request):
        return Category.objects.annotate(_product_count=Count("products"))

class MenuViewSet(SnippetViewSet):
    model = Menu
    icon = "list-ul"
    menu_label = "فهرست‌ها"
    menu_name = "visiona_menus"
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]


class SeoRedirectViewSet(SnippetViewSet):
    model = SeoRedirect
    icon = "redirect"
    menu_label = "تغییر مسیرها"
    menu_name = "visiona_redirects"
    list_display = ["old_path", "new_url", "status_code", "is_active", "created_at"]
    list_filter = ["status_code", "is_active"]
    search_fields = ["old_path", "new_url"]


@login_required
def seo_dashboard(request):
    pages = Page.objects.exclude(depth=1).specific()
    missing_title = sum(1 for page in pages if not getattr(page, "seo_title", ""))
    missing_description = sum(1 for page in pages if not getattr(page, "search_description", ""))
    noindex = sum(1 for page in pages if hasattr(page, "robots_index") and not page.robots_index)
    return render(request, "content/admin/seo_dashboard.html", {
        "missing_title": missing_title,
        "missing_description": missing_description,
        "noindex": noindex,
        "redirects": SeoRedirect.objects.filter(is_active=True).count(),
    })
