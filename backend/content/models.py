from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from .blocks import CONTENT_BLOCKS
from seo.models import SEOFieldsMixin


class ContentPage(Page, SEOFieldsMixin):
    body = StreamField(CONTENT_BLOCKS, blank=True, use_json_field=True, verbose_name="محتوا")
    content_panels = Page.content_panels + [FieldPanel("body")]
    promote_panels = Page.promote_panels + SEOFieldsMixin.seo_panels

    class Meta:
        abstract = True


class StandardPage(ContentPage):
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    class Meta:
        verbose_name = "برگه"
        verbose_name_plural = "برگه‌ها"


class FormField(AbstractFormField):
    page = ParentalKey("content.ContactPage", on_delete=models.CASCADE, related_name="form_fields")


class ContactPage(SEOFieldsMixin, AbstractEmailForm):
    body = StreamField(CONTENT_BLOCKS, blank=True, use_json_field=True, verbose_name="محتوا")
    thank_you_text = RichTextField("متن پیام موفقیت", default="<p>سپاسگزاریم. به‌زودی با شما تماس می‌گیریم.</p>")
    content_panels = AbstractEmailForm.content_panels + [FieldPanel("body"), InlinePanel("form_fields", label="فیلدهای فرم"), FieldPanel("thank_you_text")]
    promote_panels = Page.promote_panels + SEOFieldsMixin.seo_panels
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    class Meta:
        verbose_name = "فرم تماس"
        verbose_name_plural = "فرم‌های تماس"


class BlogIndexPage(ContentPage):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["content.BlogPage"]

    class Meta:
        verbose_name = "آرشیو نوشته‌ها"
        verbose_name_plural = "آرشیوهای نوشته"


class BlogPage(ContentPage):
    published_date = models.DateField("تاریخ انتشار")
    excerpt = models.CharField("خلاصه", max_length=240)
    author_name = models.CharField("نویسنده", max_length=100, default="تحریریه ویژنا")
    parent_page_types = ["content.BlogIndexPage"]
    subpage_types = []
    content_panels = ContentPage.content_panels + [FieldPanel("published_date"), FieldPanel("excerpt"), FieldPanel("author_name")]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="محتوا"),
        ObjectList(Page.promote_panels + SEOFieldsMixin.seo_panels, heading="سئو و شبکه‌های اجتماعی"),
        ObjectList(Page.settings_panels, heading="تنظیمات پیشرفته"),
    ])

    class Meta:
        verbose_name = "نوشته"
        verbose_name_plural = "نوشته‌ها"

    def save(self, *args, **kwargs):
        self.schema_type = "Article"
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField("نام", max_length=100)
    slug = models.SlugField("نامک لاتین", unique=True, help_text="برای نشانی خوانا از حروف لاتین استفاده کنید.")
    description = models.TextField("توضیحات", blank=True)
    image = models.ForeignKey("wagtailimages.Image", verbose_name="تصویر", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    panels = [FieldPanel("name"), FieldPanel("slug"), FieldPanel("description"), FieldPanel("image")]

    class Meta:
        verbose_name = "دسته‌بندی محصول"
        verbose_name_plural = "دسته‌بندی محصولات"

    def __str__(self):
        return self.name

    def product_count(self):
        return getattr(self, "_product_count", self.products.count())
    product_count.short_description = "تعداد محصول"


class ProductIndexPage(ContentPage):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["content.ProductPage"]

    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاه‌ها"


class ProductPage(ContentPage):
    short_description = models.CharField("توضیح کوتاه", max_length=240)
    description = RichTextField("توضیحات کامل")
    price = models.DecimalField("قیمت (تومان)", max_digits=12, decimal_places=0)
    discount_price = models.DecimalField("قیمت با تخفیف (تومان)", max_digits=12, decimal_places=0, null=True, blank=True)
    sku = models.CharField("شناسه کالا (SKU)", max_length=40, unique=True)
    category = models.ForeignKey(Category, verbose_name="دسته‌بندی", null=True, on_delete=models.SET_NULL, related_name="products")
    product_image = models.ForeignKey("wagtailimages.Image", verbose_name="تصویر محصول", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    is_available = models.BooleanField("موجود است", default=True)
    is_featured = models.BooleanField("محصول ویژه", default=False)
    parent_page_types = ["content.ProductIndexPage"]
    subpage_types = []
    content_panels = ContentPage.content_panels + [
        MultiFieldPanel([FieldPanel("short_description"), FieldPanel("description")], heading="معرفی محصول"),
        MultiFieldPanel([FieldPanel("price"), FieldPanel("discount_price"), FieldPanel("sku"), FieldPanel("category"), FieldPanel("is_available"), FieldPanel("is_featured")], heading="اطلاعات محصول"),
        FieldPanel("product_image"),
    ]
    product_panels = content_panels[len(ContentPage.content_panels):]
    edit_handler = TabbedInterface([
        ObjectList(ContentPage.content_panels, heading="محتوا"),
        ObjectList(product_panels, heading="اطلاعات محصول"),
        ObjectList(Page.promote_panels + SEOFieldsMixin.seo_panels, heading="سئو و شبکه‌های اجتماعی"),
        ObjectList(Page.settings_panels, heading="تنظیمات پیشرفته"),
    ])

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def save(self, *args, **kwargs):
        self.schema_type = "Product"
        super().save(*args, **kwargs)


class Menu(ClusterableModel):
    name = models.CharField("نام فهرست", max_length=80, unique=True)
    slug = models.SlugField("شناسه لاتین", unique=True)
    panels = [FieldPanel("name"), FieldPanel("slug"), InlinePanel("items", label="آیتم‌های فهرست")]

    class Meta:
        verbose_name = "فهرست"
        verbose_name_plural = "فهرست‌ها"

    def __str__(self):
        return self.name


class MenuItem(Orderable):
    menu = ParentalKey(Menu, on_delete=models.CASCADE, related_name="items")
    label = models.CharField("عنوان", max_length=80)
    page = models.ForeignKey(Page, verbose_name="برگه", null=True, blank=True, on_delete=models.CASCADE, related_name="+")
    external_url = models.URLField("نشانی خارجی", blank=True)
    panels = [FieldPanel("label"), FieldPanel("page"), FieldPanel("external_url")]


@register_setting
class SiteSettings(BaseSiteSetting):
    site_name = models.CharField("نام سایت", max_length=100, default="ویژنا")
    logo = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    favicon = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    phone = models.CharField("تلفن", max_length=40, blank=True)
    email = models.EmailField("ایمیل", blank=True)
    address = models.TextField("نشانی", blank=True)
    social_links = models.JSONField("شبکه‌های اجتماعی", default=dict, blank=True)
    default_seo_title = models.CharField("عنوان پیش‌فرض سئو", max_length=70, blank=True)
    default_seo_description = models.CharField("توضیحات پیش‌فرض سئو", max_length=200, blank=True)
    default_og_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    organization_legal_name = models.CharField(max_length=160, blank=True)
    robots_rules = models.TextField(default="User-agent: *\nAllow: /", help_text="Administrator-only. Blocking all production traffic is rejected.")
    panels = [
        MultiFieldPanel([FieldPanel("site_name"), FieldPanel("logo"), FieldPanel("favicon")], heading="هویت برند"),
        MultiFieldPanel([FieldPanel("phone"), FieldPanel("email"), FieldPanel("address"), FieldPanel("social_links")], heading="اطلاعات تماس"),
        MultiFieldPanel([FieldPanel("default_seo_title"), FieldPanel("default_seo_description"), FieldPanel("default_og_image")], heading="پیش‌فرض‌های سئو"),
        FieldPanel("organization_legal_name"), FieldPanel("robots_rules"),
    ]

    def clean(self):
        super().clean()
        compact = "".join(self.robots_rules.lower().split())
        if "user-agent:*" in compact and "disallow:/" in compact and "allow:/" not in compact:
            from django.core.exceptions import ValidationError
            raise ValidationError({"robots_rules": "مسدودکردن کامل سایت مجاز نیست؛ این تغییر باید توسط توسعه‌دهنده انجام شود."})

# Create your models here.
