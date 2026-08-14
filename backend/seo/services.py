from dataclasses import asdict, dataclass
from urllib.parse import urlparse

from django.conf import settings


@dataclass(frozen=True)
class SEOIssue:
    code: str
    severity: str
    message: str


def metadata_for(page):
    site_name = page.get_site().site_name or "ویژنا"
    title = page.seo_title.strip() or f"{page.title} | {site_name}"
    description = page.search_description.strip()
    canonical = page.canonical_url.strip() or f"{settings.PUBLIC_SITE_URL}{page.url}"
    return {
        "title": title,
        "description": description,
        "canonical": canonical,
        "robots": f"{'index' if page.robots_index else 'noindex'},{'follow' if page.robots_follow else 'nofollow'}",
        "openGraph": {"title": page.og_title or title, "description": page.og_description or description, "image": image_payload(page.og_image)},
    }


def image_payload(image, spec="width-1600|format-webp"):
    if not image:
        return None
    rendition = image.get_rendition(spec)
    return {"url": rendition.url, "width": rendition.width, "height": rendition.height, "alt": getattr(image, "alt_text", "") or image.title}


def analyze_page(page):
    meta = metadata_for(page)
    issues = []
    if not page.seo_title:
        issues.append(SEOIssue("title_default", "warning", "عنوان سئو از مقدار پیش‌فرض سایت استفاده می‌کند."))
    elif not 30 <= len(page.seo_title) <= 60:
        issues.append(SEOIssue("title_length", "warning", "طول عنوان سئو خارج از بازه پیشنهادی ۳۰ تا ۶۰ نویسه است."))
    if not page.search_description:
        issues.append(SEOIssue("description_missing", "error", "توضیحات متا وارد نشده است."))
    elif not 70 <= len(page.search_description) <= 160:
        issues.append(SEOIssue("description_length", "warning", "طول توضیحات متا خارج از بازه پیشنهادی ۷۰ تا ۱۶۰ نویسه است."))
    if page.canonical_url and not urlparse(page.canonical_url).scheme:
        issues.append(SEOIssue("canonical_invalid", "error", "نشانی کانونی باید کامل و مطلق باشد."))
    elif page.canonical_url and urlparse(page.canonical_url).netloc != urlparse(settings.PUBLIC_SITE_URL).netloc:
        issues.append(SEOIssue("canonical_external", "warning", "نشانی کانونی به دامنه دیگری اشاره می‌کند؛ آن را بررسی کنید."))
    if not page.robots_index:
        issues.append(SEOIssue("noindex", "warning", "این صفحه از ایندکس موتورهای جستجو خارج شده است."))
    keyword = page.primary_keyword.casefold().strip()
    if keyword and keyword not in page.title.casefold():
        issues.append(SEOIssue("keyword_title", "warning", "کلیدواژه اصلی در عنوان صفحه نیست."))
    body_text = str(getattr(page, "body", "")).casefold()
    if keyword and keyword not in body_text:
        issues.append(SEOIssue("keyword_body", "warning", "کلیدواژه اصلی در محتوای صفحه نیست."))
    if keyword and body_text.count(keyword) > max(5, len(body_text.split()) // 40):
        issues.append(SEOIssue("keyword_stuffing", "warning", "ممکن است کلیدواژه اصلی بیش از اندازه تکرار شده باشد."))
    if body_text.count("<h1") > 0:
        issues.append(SEOIssue("multiple_h1", "warning", "محتوا علاوه بر عنوان صفحه یک H1 دیگر دارد."))
    return {"health": max(0, 100 - sum(25 if x.severity == "error" else 10 for x in issues)), "issues": [asdict(x) for x in issues], "metadata": meta}
