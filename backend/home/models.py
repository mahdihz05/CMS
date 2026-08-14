from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from content.blocks import CONTENT_BLOCKS
from seo.models import SEOFieldsMixin


class HomePage(Page, SEOFieldsMixin):
    body = StreamField(CONTENT_BLOCKS, blank=True, use_json_field=True, verbose_name="محتوای صفحه اصلی")
    content_panels = Page.content_panels + [FieldPanel("body")]
    promote_panels = Page.promote_panels + SEOFieldsMixin.seo_panels
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["content.StandardPage", "content.ContactPage", "content.BlogIndexPage", "content.ProductIndexPage"]

    class Meta:
        verbose_name = "صفحه اصلی"
        verbose_name_plural = "صفحه‌های اصلی"
