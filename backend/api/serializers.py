from datetime import date, datetime
from decimal import Decimal

from django.conf import settings
from wagtail.models import Page

from content.models import BlogIndexPage, BlogPage, Category, ContactPage, ProductIndexPage, ProductPage, StandardPage
from home.models import HomePage
from seo.services import analyze_page, image_payload, metadata_for


def stream_value(value):
    if hasattr(value, "get_rendition"):
        return image_payload(value)
    if isinstance(value, Page):
        return serialize_card(value.specific)
    if isinstance(value, Category):
        return {"id": value.id, "name": value.name, "slug": value.slug, "description": value.description, "image": image_payload(value.image)}
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if hasattr(value, "source"):
        return str(value)
    if isinstance(value, dict):
        return {key: stream_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)) or hasattr(value, "bound_blocks"):
        return [stream_value(item.value if hasattr(item, "value") else item) for item in value]
    return value


def blocks_for(page):
    return [{"id": block.id, "type": block.block_type, "value": stream_value(block.value)} for block in getattr(page, "body", [])]


def schema_for(page, metadata):
    base = {"@context": "https://schema.org", "@type": page.schema_type, "name": page.title, "url": metadata["canonical"]}
    crumbs = [{"@type": "ListItem", "position": index + 1, "name": ancestor.title, "item": f"{settings.PUBLIC_SITE_URL}{ancestor.url}"} for index, ancestor in enumerate(page.get_ancestors().live().specific()[1:])]
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": page.title, "item": metadata["canonical"]})
    schemas = [base, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}]
    if isinstance(page, BlogPage):
        base.update({"@type": "Article", "datePublished": page.published_date.isoformat(), "author": {"@type": "Person", "name": page.author_name}, "description": page.excerpt})
    if isinstance(page, ProductPage):
        schema_price_rial = (page.discount_price or page.price) * 10
        base.update({"@type": "Product", "sku": page.sku, "description": page.short_description, "image": image_payload(page.product_image), "offers": {"@type": "Offer", "priceCurrency": "IRR", "price": str(schema_price_rial), "availability": "https://schema.org/InStock" if page.is_available else "https://schema.org/OutOfStock", "url": metadata["canonical"]}})
    return schemas


def serialize_page(page):
    page = page.specific
    metadata = metadata_for(page)
    payload = {
        "id": page.id, "type": page._meta.label_lower, "title": page.title,
        "slug": page.slug, "url": page.url, "lastPublishedAt": page.last_published_at.isoformat() if page.last_published_at else None,
        "metadata": metadata, "seoAnalysis": analyze_page(page), "blocks": blocks_for(page),
    }
    if isinstance(page, ProductIndexPage):
        payload["products"] = [serialize_card(p.specific) for p in page.get_children().live().public()]
    elif isinstance(page, BlogIndexPage):
        payload["posts"] = [serialize_card(p.specific) for p in page.get_children().live().public()]
    elif isinstance(page, ProductPage):
        payload["product"] = {"sku": page.sku, "shortDescription": page.short_description, "description": str(page.description), "priceToman": str(page.price), "discountPriceToman": str(page.discount_price) if page.discount_price else None, "available": page.is_available, "featured": page.is_featured, "category": page.category.name if page.category else None, "image": image_payload(page.product_image)}
    elif isinstance(page, BlogPage):
        payload["article"] = {"date": page.published_date.isoformat(), "excerpt": page.excerpt, "author": page.author_name}
    elif isinstance(page, ContactPage):
        payload["form"] = {"pageId": page.id, "fields": [{"name": field.clean_name, "label": field.label, "type": field.field_type, "required": field.required} for field in page.get_form_fields()]}
    payload["schemas"] = schema_for(page, metadata)
    return payload


def serialize_card(page):
    data = {"id": page.id, "title": page.title, "url": page.url, "description": page.search_description}
    if isinstance(page, ProductPage):
        data.update({"priceToman": str(page.discount_price or page.price), "originalPriceToman": str(page.price), "image": image_payload(page.product_image), "category": page.category.name if page.category else None})
    if isinstance(page, BlogPage):
        data.update({"date": page.published_date.isoformat(), "excerpt": page.excerpt})
    return data
