from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import Site


class SEOFieldsMixin(models.Model):
    canonical_url = models.URLField("نشانی کانونی", blank=True)
    robots_index = models.BooleanField("اجازه ایندکس", default=True)
    robots_follow = models.BooleanField("دنبال‌کردن پیوندها", default=True)
    og_title = models.CharField("عنوان شبکه‌های اجتماعی", max_length=70, blank=True)
    og_description = models.CharField("توضیحات شبکه‌های اجتماعی", max_length=200, blank=True)
    og_image = models.ForeignKey(get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    sitemap_included = models.BooleanField("نمایش در نقشه سایت", default=True)
    sitemap_priority = models.DecimalField("اولویت در نقشه سایت", max_digits=2, decimal_places=1, default=0.5)
    schema_type = models.CharField(max_length=30, default="WebPage", choices=[("WebPage", "WebPage"), ("Article", "Article"), ("Product", "Product")])
    primary_keyword = models.CharField("کلیدواژه اصلی", max_length=120, blank=True)
    secondary_keywords = models.CharField("کلیدواژه‌های فرعی", max_length=300, blank=True, help_text="با ویرگول جدا کنید")

    seo_panels = [
        MultiFieldPanel([FieldPanel("seo_title"), FieldPanel("search_description"), FieldPanel("canonical_url")], heading="نمایش در نتایج جستجو"),
        MultiFieldPanel([FieldPanel("robots_index"), FieldPanel("robots_follow"), FieldPanel("sitemap_included"), FieldPanel("sitemap_priority")], heading="روبات‌ها و نقشه سایت"),
        MultiFieldPanel([FieldPanel("og_title"), FieldPanel("og_description"), FieldPanel("og_image")], heading="پیش‌نمایش شبکه‌های اجتماعی"),
        MultiFieldPanel([FieldPanel("schema_type"), FieldPanel("primary_keyword"), FieldPanel("secondary_keywords")], heading="اسکیما و کلیدواژه‌ها"),
    ]

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if not 0 <= self.sitemap_priority <= 1:
            raise ValidationError({"sitemap_priority": "اولویت باید بین ۰٫۰ و ۱٫۰ باشد."})


class SeoRedirect(models.Model):
    STATUS_CHOICES = [(301, "301 Permanent"), (302, "302 Temporary"), (307, "307 Temporary"), (308, "308 Permanent")]
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="seo_redirects")
    old_path = models.CharField(max_length=255, help_text="Path beginning with /")
    new_url = models.CharField(max_length=500)
    status_code = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=301)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [FieldPanel("site"), FieldPanel("old_path"), FieldPanel("new_url"), FieldPanel("status_code"), FieldPanel("is_active")]

    class Meta:
        unique_together = [("site", "old_path")]
        ordering = ["old_path"]
        verbose_name = "تغییر مسیر"
        verbose_name_plural = "تغییر مسیرها"

    def __str__(self):
        return f"{self.old_path} → {self.new_url}"

    def clean(self):
        super().clean()
        if not self.old_path.startswith("/"):
            raise ValidationError({"old_path": "مسیر قدیمی باید با / شروع شود."})
        if self.new_url == self.old_path:
            raise ValidationError({"new_url": "تغییر مسیر نمی‌تواند به خودش اشاره کند."})
        target_path = self.new_url.split("?", 1)[0]
        if target_path.startswith("/") and self.site_id:
            seen = {self.old_path}
            while target_path:
                if target_path in seen:
                    raise ValidationError({"new_url": "این تغییر مسیر یک حلقه ایجاد می‌کند."})
                seen.add(target_path)
                target = type(self).objects.filter(site_id=self.site_id, old_path=target_path, is_active=True).exclude(pk=self.pk).first()
                target_path = target.new_url.split("?", 1)[0] if target and target.new_url.startswith("/") else ""
