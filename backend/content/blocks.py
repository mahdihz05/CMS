from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class HeroBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(label="پیش‌عنوان", required=False, max_length=80)
    heading = blocks.CharBlock(label="عنوان", max_length=140)
    text = blocks.TextBlock(label="متن", required=False, max_length=360)
    image = ImageBlock(label="تصویر", required=False)
    cta_label = blocks.CharBlock(label="متن دکمه", required=False, max_length=40)
    cta_page = blocks.PageChooserBlock(label="صفحه مقصد", required=False)
    variant = blocks.ChoiceBlock(label="نوع نمایش", choices=[("default", "پیش‌فرض"), ("campaign", "کمپین")], default="default")

    class Meta:
        icon = "image"
        label = "بخش آغازین"


class ImageTextBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="عنوان", max_length=140)
    text = blocks.RichTextBlock(label="متن", features=["bold", "italic", "link", "ol", "ul"])
    image = ImageBlock(label="تصویر")
    image_side = blocks.ChoiceBlock(label="جای تصویر", choices=[("left", "چپ"), ("right", "راست")], default="left")

    class Meta:
        label = "تصویر و متن"


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(label="عنوان پیوند", max_length=60)
    page = blocks.PageChooserBlock(label="صفحه مقصد")

    class Meta:
        label = "پیوند"


class CardsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="عنوان", required=False, max_length=120)
    pages = blocks.ListBlock(blocks.PageChooserBlock(label="صفحه"), label="صفحه‌ها", min_num=1, max_num=12)

    class Meta:
        label = "شبکه کارت‌ها"


class CategoryCardsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="عنوان", required=False, max_length=120)
    categories = blocks.ListBlock(SnippetChooserBlock("content.Category", label="دسته‌بندی"), label="دسته‌بندی‌ها", min_num=1, max_num=12)

    class Meta:
        label = "شبکه دسته‌بندی‌ها"


class FeatureBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="عنوان", max_length=80)
    text = blocks.TextBlock(label="متن", max_length=240)

    class Meta:
        label = "ویژگی"


class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock(label="نقل‌قول", max_length=360)
    author = blocks.CharBlock(label="نام گوینده", max_length=80)

    class Meta:
        label = "نظر مشتری"


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(label="پرسش", max_length=160)
    answer = blocks.RichTextBlock(label="پاسخ", features=["bold", "italic", "link"])

    class Meta:
        label = "پرسش و پاسخ"


class CTABlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="عنوان", max_length=120)
    text = blocks.TextBlock(label="متن", required=False, max_length=240)
    label = blocks.CharBlock(label="متن دکمه", max_length=60)
    page = blocks.PageChooserBlock(label="صفحه مقصد")

    class Meta:
        label = "دعوت به اقدام"


CONTENT_BLOCKS = [
    ("hero", HeroBlock()),
    ("rich_text", blocks.RichTextBlock(label="متن غنی", features=["h2", "h3", "bold", "italic", "link", "ol", "ul"])),
    ("image_text", ImageTextBlock()),
    ("product_grid", CardsBlock(label="شبکه محصولات")),
    ("category_grid", CategoryCardsBlock()),
    ("features", blocks.ListBlock(FeatureBlock(), label="ویژگی‌ها", min_num=1, max_num=6)),
    ("testimonials", blocks.ListBlock(TestimonialBlock(), label="نظر مشتریان", min_num=1, max_num=8)),
    ("faq", blocks.ListBlock(FAQItemBlock(), label="پرسش‌های پرتکرار", min_num=1, max_num=12)),
    ("cta", CTABlock()),
    ("blog_grid", CardsBlock(label="شبکه نوشته‌ها")),
]
