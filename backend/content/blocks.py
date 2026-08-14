from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class HeroBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, max_length=80)
    heading = blocks.CharBlock(max_length=140)
    text = blocks.TextBlock(required=False, max_length=360)
    image = ImageBlock(required=False)
    cta_label = blocks.CharBlock(required=False, max_length=40)
    cta_page = blocks.PageChooserBlock(required=False)
    variant = blocks.ChoiceBlock(choices=[("default", "Default"), ("campaign", "Campaign")], default="default")

    class Meta:
        icon = "image"
        label = "Hero"


class ImageTextBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=140)
    text = blocks.RichTextBlock(features=["bold", "italic", "link", "ol", "ul"])
    image = ImageBlock()
    image_side = blocks.ChoiceBlock(choices=[("left", "Left"), ("right", "Right")], default="left")


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=60)
    page = blocks.PageChooserBlock()


class CardsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, max_length=120)
    pages = blocks.ListBlock(blocks.PageChooserBlock(), min_num=1, max_num=12)


class CategoryCardsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, max_length=120)
    categories = blocks.ListBlock(SnippetChooserBlock("content.Category"), min_num=1, max_num=12)


class FeatureBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=80)
    text = blocks.TextBlock(max_length=240)


class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock(max_length=360)
    author = blocks.CharBlock(max_length=80)


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(max_length=160)
    answer = blocks.RichTextBlock(features=["bold", "italic", "link"])


class CTABlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120)
    text = blocks.TextBlock(required=False, max_length=240)
    label = blocks.CharBlock(max_length=60)
    page = blocks.PageChooserBlock()


CONTENT_BLOCKS = [
    ("hero", HeroBlock()),
    ("rich_text", blocks.RichTextBlock(features=["h2", "h3", "bold", "italic", "link", "ol", "ul"])),
    ("image_text", ImageTextBlock()),
    ("product_grid", CardsBlock()),
    ("category_grid", CategoryCardsBlock()),
    ("features", blocks.ListBlock(FeatureBlock(), min_num=1, max_num=6)),
    ("testimonials", blocks.ListBlock(TestimonialBlock(), min_num=1, max_num=8)),
    ("faq", blocks.ListBlock(FAQItemBlock(), min_num=1, max_num=12)),
    ("cta", CTABlock()),
    ("blog_grid", CardsBlock()),
]
