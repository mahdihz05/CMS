from datetime import date, timedelta
from pathlib import Path

from django.contrib.auth.models import Group, Permission, User
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from wagtail.images import get_image_model
from wagtail.models import Collection, GroupApprovalTask, GroupPagePermission, Page, Site, Workflow, WorkflowPage, WorkflowTask

from content.models import BlogIndexPage, BlogPage, Category, ContactPage, FormField, Menu, MenuItem, ProductIndexPage, ProductPage, SiteSettings, StandardPage
from home.models import HomePage


CATEGORIES = [
    ("عینک آفتابی", "sunglasses", "عینک‌های آفتابی با محافظت UV برای استفاده روزمره"),
    ("فریم طبی", "optical-frames", "فریم‌های سبک و خوش‌فرم برای عدسی طبی"),
    ("عینک بلوکات", "blue-light-glasses", "عینک مناسب کار طولانی با نمایشگر"),
    ("عینک ورزشی", "sport-glasses", "فریم‌های مقاوم و پایدار برای حرکت و ورزش"),
]

PRODUCTS = [
    ("آفتابی آریا", "aria-sunglasses", "VSN-SUN-001", "sunglasses", 3490000, 3190000, True, True, "12720210"),
    ("آفتابی ساحل", "sahel-sunglasses", "VSN-SUN-002", "sunglasses", 4290000, None, True, True, "12352237"),
    ("آفتابی کلاسیک مهر", "mehr-classic-sunglasses", "VSN-SUN-003", "sunglasses", 2890000, 2490000, True, False, "1499477"),
    ("آفتابی پلاریزه هور", "hoor-polarized-sunglasses", "VSN-SUN-004", "sunglasses", 5890000, None, False, True, "5677349"),
    ("فریم طبی رستا", "rasta-optical-frame", "VSN-OPT-001", "optical-frames", 3790000, None, True, True, "4936933"),
    ("فریم تیتانیوم ماهور", "mahoor-titanium-frame", "VSN-OPT-002", "optical-frames", 8900000, 8190000, True, True, "28938431"),
    ("فریم سبک نیلا", "nila-light-frame", "VSN-OPT-003", "optical-frames", 3190000, None, True, False, "11199907"),
    ("فریم گرد ویدا", "vida-round-frame", "VSN-OPT-004", "optical-frames", 4590000, None, False, False, "8360292"),
    ("بلوکات کارا", "kara-blue-light", "VSN-BLU-001", "blue-light-glasses", 2590000, 2290000, True, True, "5752246"),
    ("بلوکات سپهر", "sepehr-blue-light", "VSN-BLU-002", "blue-light-glasses", 3990000, None, True, False, "29538700"),
    ("ورزشی تندر", "tondar-sport-glasses", "VSN-SPT-001", "sport-glasses", 6790000, 6190000, True, True, "5201996"),
    ("ورزشی اوج", "owj-sport-glasses", "VSN-SPT-002", "sport-glasses", 5390000, None, False, False, "5766170"),
]

POSTS = [
    ("راهنمای انتخاب فریم براساس فرم صورت", "choose-frame-for-face-shape", "با چند معیار ساده، فریمی هماهنگ با فرم صورت و استایل خود انتخاب کنید."),
    ("عدسی پلاریزه چیست و چه زمانی لازم است؟", "polarized-lenses-guide", "تفاوت عدسی پلاریزه با عدسی معمولی و کاربرد آن در رانندگی و فضای باز."),
    ("عینک بلوکات؛ انتخاب درست برای کار با نمایشگر", "blue-light-glasses-guide", "نکاتی برای انتخاب عینک مناسب ساعات طولانی کار با لپ‌تاپ و موبایل."),
    ("چطور از عینک خود نگهداری کنیم؟", "eyewear-care-guide", "روش درست شست‌وشو، خشک‌کردن و نگهداری فریم و عدسی."),
    ("راهنمای اندازه فریم و پل بینی", "frame-size-and-bridge-guide", "اعداد روی دسته عینک چه معنایی دارند و چطور اندازه مناسب را پیدا کنیم."),
    ("عینک آفتابی مناسب رانندگی", "driving-sunglasses-guide", "ویژگی‌های مهم عینک آفتابی برای دید بهتر و آسایش بیشتر هنگام رانندگی."),
]

LEGACY_PRODUCT_SKUS = {"AVI-001", "CLB-002", "MTF-003", "RVS-004", "BLG-005", "SPS-006", "PAF-007", "POL-008"}
LEGACY_POST_SLUGS = {"how-to-choose-frames-for-everyday-comfort", "polarized-lenses-explained", "caring-for-acetate-and-titanium-frames"}
LEGACY_IMAGE_TITLES = {"Aviator Sunglasses", "Classic Black Frame", "Minimal Titanium Frame", "Round Vintage Sunglasses", "Blue Light Glasses", "Sport Sunglasses", "Premium Acetate Frame", "Polarized Sunglasses"}


class Command(BaseCommand):
    help = "ایجاد امن و تکرارپذیر محتوای نمایشی فارسی ویژنا"

    def add_arguments(self, parser):
        parser.add_argument("--admin-password", default="admin")
        parser.add_argument("--reset-demo", action="store_true", help="فقط رکوردهای شناخته‌شده دموی ویژنا را جایگزین می‌کند")

    @transaction.atomic
    def handle(self, *args, **options):
        root = Page.get_first_root_node()
        home = HomePage.objects.first()
        if not home:
            home = HomePage(title="ویژنا", slug="home")
            root.add_child(instance=home)
        site, _ = Site.objects.update_or_create(is_default_site=True, defaults={"hostname": "localhost", "port": 8000, "site_name": "ویژنا", "root_page": home})
        shop = self.page(home, ProductIndexPage, "فروشگاه", "shop", "فروشگاه عینک ویژنا", "خرید عینک آفتابی، فریم طبی، بلوکات و ورزشی ویژنا")
        blog = self.page(home, BlogIndexPage, "مجله ویژنا", "blog", "مجله عینک و سلامت دید ویژنا", "راهنماهای کاربردی انتخاب و نگهداری عینک")

        if options["reset_demo"]:
            self.reset_known_demo(shop, blog)
            # Page.delete() updates the persisted parent counters. Refresh the
            # parent instances before treebeard uses them for new children.
            shop.refresh_from_db()
            blog.refresh_from_db()
        self.assert_no_collisions(shop)

        home.title, home.slug = "ویژنا؛ فروشگاه تخصصی عینک", "home"
        home.seo_title = "ویژنا | عینک آفتابی، طبی و بلوکات"
        home.search_description = "مجموعه‌ای منتخب از عینک‌های آفتابی، فریم طبی، بلوکات و ورزشی با طراحی مدرن."

        value = SiteSettings.for_site(site)
        value.site_name = "ویژنا"; value.phone = "۰۲۱-۸۸۷۷۶۶۵۵"; value.email = "hello@visiona.ir"
        value.address = "تهران، خیابان میرداماد، پلاک ۱۲۴"; value.social_links = {"instagram": "https://instagram.com/visiona.ir"}
        value.default_seo_title = "ویژنا | فروشگاه تخصصی عینک"; value.default_seo_description = "انتخاب و خرید عینک با راهنمای تخصصی ویژنا"
        value.organization_legal_name = "فروشگاه اینترنتی ویژنا"; value.save()

        category_map = {}
        for name, slug, description in CATEGORIES:
            obj, created = Category.objects.get_or_create(slug=slug, defaults={"name": name, "description": description})
            if not created:
                obj.name, obj.description = name, description; obj.save(update_fields=["name", "description"])
            category_map[slug] = obj

        images = {row[8]: self.image(row[0], row[8], index) for index, row in enumerate(PRODUCTS)}
        for category_slug, image_id in (("sunglasses", "12720210"), ("optical-frames", "4936933"), ("blue-light-glasses", "5752246"), ("sport-glasses", "5201996")):
            category_map[category_slug].image = images[image_id]
            category_map[category_slug].save(update_fields=["image"])
        for index, (title, slug, sku, category_slug, price, discount, available, featured, image_id) in enumerate(PRODUCTS):
            description = f"{title} با طراحی متعادل، فریم خوش‌ساخت و نشیمن راحت، برای استفاده روزمره انتخابی مطمئن است."
            defaults = {"title": title, "slug": slug, "short_description": description, "description": f"<p>{description}</p><p>این محصول با کنترل کیفیت ویژنا و راهنمای انتخاب سایز عرضه می‌شود.</p>", "price": price, "discount_price": discount, "sku": sku, "category": category_map[category_slug], "product_image": images[image_id], "is_available": available, "is_featured": featured, "seo_title": f"{title} | ویژنا", "search_description": f"مشخصات، قیمت و تصاویر {title} از مجموعه عینک ویژنا.", "primary_keyword": title}
            product = ProductPage.objects.child_of(shop).filter(slug=slug).first()
            if not product:
                product = ProductPage(**defaults); shop.add_child(instance=product)
            else:
                for key, item in defaults.items(): setattr(product, key, item)
            product.save_revision().publish()

        for index, (title, slug, excerpt) in enumerate(POSTS):
            post = BlogPage.objects.child_of(blog).filter(slug=slug).first()
            defaults = {"title": title, "slug": slug, "published_date": date.today() - timedelta(days=index * 8), "excerpt": excerpt, "author_name": "تحریریه ویژنا", "search_description": excerpt, "seo_title": f"{title} | مجله ویژنا", "primary_keyword": title.split("؛")[0], "body": [("rich_text", f"<h2>{title}</h2><p>{excerpt}</p><p>در انتخاب عینک، تناسب اندازه، کیفیت ساخت و نوع استفاده روزانه را هم‌زمان در نظر بگیرید. کارشناسان ویژنا برای انتخاب دقیق‌تر همراه شما هستند.</p>")]}
            if not post:
                post = BlogPage(**defaults); blog.add_child(instance=post)
            else:
                for key, item in defaults.items(): setattr(post, key, item)
            post.save_revision().publish()

        about = self.page(home, StandardPage, "درباره ویژنا", "about", "درباره ویژنا", "ویژنا؛ انتخاب دقیق‌تر برای دیدی روشن‌تر")
        old_contact = Page.objects.child_of(home).filter(slug="contact").specific().first()
        if old_contact and not isinstance(old_contact, ContactPage):
            if old_contact.slug not in {"contact"}: raise CommandError("برخورد محتوای کاربر با صفحه تماس")
            old_contact.delete()
        contact = self.page(home, ContactPage, "تماس با ما", "contact", "تماس با ویژنا", "برای راهنمایی انتخاب عینک با ویژنا تماس بگیرید")
        about.body = [("rich_text", "<h2>دید روشن، انتخاب دقیق</h2><p>ویژنا با تمرکز بر طراحی کاربردی، کیفیت ساخت و راهنمایی صادقانه شکل گرفته است.</p>")]
        contact.body = [("rich_text", "<h2>با ما در ارتباط باشید</h2><p>برای راهنمایی انتخاب محصول، پیام خود را ارسال کنید.</p>")]
        contact.from_address = "website@visiona.ir"; contact.to_address = "hello@visiona.ir"; contact.subject = "پیام جدید از سایت ویژنا"; contact.thank_you_text = "<p>پیام شما ثبت شد. به‌زودی با شما تماس می‌گیریم.</p>"
        if not contact.form_fields.exists():
            for order, (label, field_type) in enumerate([("نام و نام خانوادگی", "singleline"), ("ایمیل", "email"), ("پیام", "multiline")]): FormField.objects.create(page=contact, label=label, field_type=field_type, required=True, sort_order=order)
        about.save_revision().publish(); contact.save_revision().publish()

        featured = list(ProductPage.objects.child_of(shop).live().filter(is_featured=True)[:6])
        articles = list(BlogPage.objects.child_of(blog).live().order_by("-published_date")[:3])
        home.body = [
            ("hero", {"eyebrow": "کالکشن تازه ویژنا", "heading": "دنیا را با سبک خودت ببین", "text": "عینک‌هایی خوش‌ساخت برای دید بهتر و استفاده راحت در تمام روز.", "image": images["12720210"], "cta_label": "مشاهده محصولات", "cta_page": shop, "variant": "campaign"}),
            ("category_grid", {"heading": "عینک مناسب خودت را پیدا کن", "categories": list(category_map.values())}),
            ("product_grid", {"heading": "محصولات ویژه", "pages": featured}),
            ("features", [{"title": "انتخاب تخصصی", "text": "راهنمایی برای انتخاب اندازه و فرم مناسب"}, {"title": "کیفیت قابل اعتماد", "text": "متریال سبک و بادوام برای استفاده روزمره"}, {"title": "محافظت از چشم", "text": "گزینه‌های UV، پلاریزه و بلوکات"}]),
            ("image_text", {"heading": "کالکشن جدید؛ سبک‌تر و دقیق‌تر", "text": "<p>فرم‌های متعادل و رنگ‌های کاربردی برای استایل روزمره.</p>", "image": images["28938431"], "image_side": "left"}),
            ("testimonials", [{"quote": "فریم خیلی سبک بود و راهنمای انتخاب سایز واقعاً کمکم کرد.", "author": "سارا، مشتری ویژنا"}, {"quote": "بسته‌بندی خوب و توضیحات محصول دقیق بود.", "author": "آرمان، مشتری ویژنا"}]),
            ("blog_grid", {"heading": "راهنمای انتخاب و نگهداری عینک", "pages": articles}),
            ("cta", {"heading": "برای انتخاب عینک نیاز به راهنمایی دارید؟", "text": "کارشناسان ویژنا پاسخگوی شما هستند.", "label": "تماس با ویژنا", "page": contact}),
        ]
        home.save_revision().publish()
        self.menu("header", "فهرست اصلی", [("خانه", home), ("فروشگاه", shop), ("مجله", blog), ("درباره ما", about), ("تماس با ما", contact)])
        self.menu("footer", "فهرست پایین سایت", [("فروشگاه", shop), ("مجله", blog), ("تماس با ما", contact)])
        self.roles(options["admin_password"])
        self.stdout.write(self.style.SUCCESS("Visiona Persian demo ready: 12 products, 4 categories, 6 posts."))

    def assert_no_collisions(self, shop):
        demo_skus = {row[2] for row in PRODUCTS} | LEGACY_PRODUCT_SKUS
        for _, slug, sku, *_ in PRODUCTS:
            collision = Page.objects.child_of(shop).filter(slug=slug).specific().first()
            if collision and (not isinstance(collision, ProductPage) or collision.sku not in demo_skus): raise CommandError(f"نامک {slug} متعلق به محتوای Demo نیست؛ عملیات متوقف شد.")
            sku_collision = ProductPage.objects.filter(sku=sku).exclude(path__startswith=shop.path).first()
            if sku_collision: raise CommandError(f"SKU {sku} بیرون از فروشگاه Demo وجود دارد؛ عملیات متوقف شد.")

    def reset_known_demo(self, shop, blog):
        demo_skus = {row[2] for row in PRODUCTS} | LEGACY_PRODUCT_SKUS
        # Page uses treebeard's materialised path tree. Deleting a page queryset
        # bypasses its tree-aware delete implementation and can leave numchild
        # inconsistent, so reset each known demo page through Page.delete().
        demo_products = list(ProductPage.objects.child_of(shop).filter(sku__in=demo_skus))
        demo_posts = list(BlogPage.objects.child_of(blog).filter(slug__in=({row[1] for row in POSTS} | LEGACY_POST_SLUGS)))
        for page in [*demo_products, *demo_posts]:
            page.delete()
        get_image_model().objects.filter(title__in=LEGACY_IMAGE_TITLES).delete()
        get_image_model().objects.filter(collection__name="تصاویر دموی ویژنا", title__in={row[0] for row in PRODUCTS}).delete()
        Category.objects.filter(slug__in={"optical", "computer-glasses"}, products__isnull=True).delete()

    def page(self, parent, cls, title, slug, seo_title, description):
        page = cls.objects.child_of(parent).filter(slug=slug).first()
        if not page:
            collision = Page.objects.child_of(parent).filter(slug=slug).first()
            if collision: raise CommandError(f"نامک {slug} با محتوای غیر Demo برخورد دارد.")
            page = cls(title=title, slug=slug); parent.add_child(instance=page)
        page.title, page.seo_title, page.search_description = title, seo_title, description
        page.save_revision().publish(); return page

    def image(self, title, pexels_id, index):
        model = get_image_model(); marker = f"pexels-{pexels_id}.webp"
        existing = model.objects.filter(collection__name="تصاویر دموی ویژنا", title=title).first()
        collection = Collection.objects.filter(name="تصاویر دموی ویژنا").first()
        if not collection: collection = Collection.get_first_root_node().add_child(name="تصاویر دموی ویژنا")
        if existing:
            existing.title, existing.collection = title, collection; existing.save(update_fields=["title", "collection"]); return existing
        asset = Path(__file__).resolve().parents[2] / "seed_assets" / marker
        if not asset.exists(): raise CommandError(f"فایل تصویر محلی موجود نیست: {asset}")
        with asset.open("rb") as handle:
            return model.objects.create(title=title, collection=collection, file=ImageFile(handle, name=marker))

    def menu(self, slug, name, items):
        menu, _ = Menu.objects.get_or_create(slug=slug, defaults={"name": name}); menu.name = name; menu.save(update_fields=["name"]); menu.items.all().delete()
        for order, (label, page) in enumerate(items): MenuItem.objects.create(menu=menu, label=label, page=page, sort_order=order)

    def roles(self, password):
        groups = {name: Group.objects.get_or_create(name=name)[0] for name in ["Developer", "SEO Specialist", "Content Editor", "Client / Site Manager"]}
        editor_permissions = Permission.objects.filter(codename__in=["access_admin", "add_page", "change_page", "add_image", "change_image", "add_document", "change_document"])
        category_permissions = Permission.objects.filter(content_type__app_label="content", content_type__model="category", codename__in=["add_category", "change_category", "delete_category", "view_category"])
        menu_permissions = Permission.objects.filter(content_type__app_label="content", content_type__model="menu", codename__in=["add_menu", "change_menu", "delete_menu", "view_menu"])
        redirect_permissions = Permission.objects.filter(content_type__app_label="seo", content_type__model="seoredirect")
        groups["Content Editor"].permissions.set(editor_permissions | category_permissions)
        groups["Client / Site Manager"].permissions.set(editor_permissions | category_permissions | menu_permissions | redirect_permissions)
        seo_base = Permission.objects.filter(Q(codename="access_admin") | Q(content_type__app_label="wagtailcore", codename="change_page"))
        category_view = category_permissions.filter(codename="view_category")
        groups["SEO Specialist"].permissions.set(seo_base | category_view | redirect_permissions)
        groups["Developer"].permissions.set(Permission.objects.all())
        home = HomePage.objects.first(); page_perms = {p.codename: p for p in Permission.objects.filter(content_type__app_label="wagtailcore", codename__in=["add_page", "change_page", "publish_page", "lock_page", "unlock_page"])}
        mapping = {"Content Editor": ["add_page", "change_page"], "SEO Specialist": ["change_page"], "Client / Site Manager": ["add_page", "change_page", "publish_page"], "Developer": list(page_perms)}
        GroupPagePermission.objects.filter(page=home, group__in=groups.values()).delete()
        for group_name, codenames in mapping.items():
            for codename in codenames:
                if codename in page_perms: GroupPagePermission.objects.create(group=groups[group_name], page=home, permission=page_perms[codename])
        workflow, _ = Workflow.objects.get_or_create(name="بازبینی محتوا و سئو"); workflow.workflow_tasks.all().delete()
        for order, (name, group_name) in enumerate([("بازبینی محتوا", "Client / Site Manager"), ("بازبینی سئو", "SEO Specialist")]):
            task = GroupApprovalTask.objects.filter(name=name).first() or GroupApprovalTask.objects.create(name=name); task.groups.set([groups[group_name]]); WorkflowTask.objects.create(workflow=workflow, task=task, sort_order=order)
        WorkflowPage.objects.update_or_create(page=home, defaults={"workflow": workflow})
        admin, created = User.objects.get_or_create(username="admin", defaults={"email": "admin@visiona.local", "is_staff": True, "is_superuser": True})
        if created: admin.set_password(password); admin.save()
