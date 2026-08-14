import json
from secrets import compare_digest

from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from wagtail.models import Page, Site

from content.models import ContactPage, Menu, ProductPage, SiteSettings
from seo.models import SEOFieldsMixin, SeoRedirect
from .serializers import serialize_card, serialize_page


def current_site(request):
    return Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()


@require_GET
def page_detail(request):
    site = current_site(request)
    requested_path = "/" + request.GET.get("path", "").strip("/") + ("/" if request.GET.get("path", "").strip("/") else "")
    url_path = site.root_page.url_path + requested_path.lstrip("/")
    page = Page.objects.live().public().filter(url_path=url_path).specific().first()
    if not page:
        raise Http404
    return JsonResponse({"data": serialize_page(page)})


@require_GET
def products(request):
    pages = ProductPage.objects.live().public().select_related("category", "product_image")
    return JsonResponse({"data": [serialize_card(page) for page in pages]})


@require_GET
def navigation(request):
    menus = {}
    for menu in Menu.objects.prefetch_related("items__page"):
        menus[menu.slug] = [{"label": item.label, "url": item.external_url or (item.page.url if item.page else "#")} for item in menu.items.all()]
    return JsonResponse({"data": menus})


@require_GET
def site_settings(request):
    site = current_site(request)
    value = SiteSettings.for_site(site)
    return JsonResponse({"data": {
        "siteName": value.site_name, "phone": value.phone, "email": value.email,
        "address": value.address, "socialLinks": value.social_links,
        "locale": "fa-IR", "direction": "rtl",
        "currency": {"code": "IRT", "label": "تومان", "schemaCode": "IRR", "schemaMultiplier": 10},
    }})


@require_GET
def sitemap(request):
    site = current_site(request)
    rows = []
    for page in Page.objects.live().public().descendant_of(site.root_page, inclusive=True).specific():
        if isinstance(page, SEOFieldsMixin) and page.robots_index and page.sitemap_included and not page.canonical_url:
            rows.append(f"<url><loc>{settings.PUBLIC_SITE_URL}{page.url}</loc><lastmod>{page.last_published_at.date().isoformat() if page.last_published_at else ''}</lastmod><priority>{page.sitemap_priority}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(rows) + "</urlset>"
    return HttpResponse(xml, content_type="application/xml")


@require_GET
def robots(request):
    value = SiteSettings.for_site(current_site(request))
    return HttpResponse(f"{value.robots_rules}\nSitemap: {settings.PUBLIC_SITE_URL}/sitemap.xml\n", content_type="text/plain")


@require_GET
def redirect_lookup(request):
    item = SeoRedirect.objects.filter(site=current_site(request), old_path=request.GET.get("path", ""), is_active=True).first()
    return JsonResponse({"data": {"url": item.new_url, "status": item.status_code} if item else None})


@csrf_exempt
def submit_form(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not compare_digest(request.headers.get("X-Visiona-Form-Secret", ""), settings.FORM_API_SECRET):
        return JsonResponse({"error": "Forbidden"}, status=403)
    if len(request.body) > 32_000:
        return JsonResponse({"error": "Payload too large"}, status=413)
    try:
        payload = json.loads(request.body)
        page = ContactPage.objects.live().public().get(pk=payload.pop("pageId"))
        form = page.get_form(payload)
    except (ValueError, KeyError, ContactPage.DoesNotExist, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid form"}, status=400)
    if not form.is_valid():
        return JsonResponse({"error": "Validation failed", "fields": form.errors.get_json_data()}, status=422)
    page.process_form_submission(form)
    return JsonResponse({"data": {"submitted": True}}, status=201)

# Create your views here.
