from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import render
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.models import Page
from wagtail.permissions import page_permission_policy

from .models import BlogPage, Category, Menu, ProductPage, StandardPage
from seo.models import SeoRedirect
from seo.services import analyze_page


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
    roles = set(request.user.groups.values_list("name", flat=True))
    if not (request.user.is_superuser or roles & {"Developer", "SEO Specialist", "Client / Site Manager"}):
        raise PermissionDenied
    editable = page_permission_policy.instances_user_has_permission_for(request.user, "change").exclude(depth=1).specific()
    page_results = []
    all_issues = []
    for page in editable:
        result = analyze_page(page)
        page_results.append({"page": page, **result})
        all_issues.extend(result["issues"])
    issue_codes = [issue["code"] for issue in all_issues]
    return render(request, "content/admin/seo_dashboard.html", {
        "missing_title": issue_codes.count("title_default"),
        "missing_description": issue_codes.count("description_missing"),
        "noindex": issue_codes.count("noindex"),
        "canonical_issues": issue_codes.count("canonical_invalid") + issue_codes.count("canonical_external"),
        "error_count": sum(issue["severity"] == "error" for issue in all_issues),
        "warning_count": sum(issue["severity"] == "warning" for issue in all_issues),
        "average_health": round(sum(item["health"] for item in page_results) / len(page_results)) if page_results else 100,
        "page_results": sorted(page_results, key=lambda item: item["health"]),
        "redirects": SeoRedirect.objects.filter(is_active=True).count(),
    })
