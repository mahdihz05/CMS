# چک‌لیست بازطراحی پنل مدیریت Visiona براساس Stitch

مرجع طراحی: `stitch_visiona_cms_admin_interface.zip`

این چک‌لیست فقط زمانی تیک می‌خورد که هر بخش هم از نظر بصری با مرجع Stitch تطبیق داده شده باشد و هم رفتار واقعی Wagtail، مجوزها، Draft، Revision، Preview و Workflow را حفظ کند.

## وضعیت و قواعد اجرا

- [x] بررسی `DESIGN.md` و استخراج رنگ‌ها، تایپوگرافی، فاصله‌ها و Breakpointها
- [x] بررسی بصری ۱۰ صفحه دسکتاپ و ۳ صفحه موبایل
- [x] تطبیق اولیه طرح با پنل فعلی Wagtail و قابلیت‌های موجود
- [x] تعیین موارد خارج از دامنه و ناسازگاری‌های طرح
- [ ] ثبت تصاویر Baseline از پنل فعلی پیش از شروع تغییرات
- [x] به‌روزرسانی قرارداد بصری پنل در `docs/admin-visual-contract.md`

قواعد ثابت:

- HTML و Tailwind CDN تولیدشده توسط Stitch مستقیماً وارد پروژه نمی‌شود؛ طرح با Template، CSS و JavaScript محدود Wagtail بازسازی می‌شود.
- Vazirmatn به‌صورت Self-hosted باقی می‌ماند و فونت یا آیکن از Google CDN بارگیری نمی‌شود.
- دکمه‌ها و عملیات باید به Actionهای واقعی Wagtail متصل باشند؛ کنترل نمایشی و بی‌عمل ساخته نمی‌شود.
- «سفارش‌ها»، «مشتریان»، Checkout و موجودی عددی از طرح محصولات حذف می‌شوند؛ کاتالوگ فعلی فقط Site Extension نمونه است.
- دکمه عمومی «ذخیره تغییرات» فقط در صفحه‌ای نمایش داده می‌شود که Action واقعی ذخیره دارد.
- تمام عنوان Blockها و متن‌های رابط فارسی می‌شوند و CMS هیچ کنترل CSS، رنگ، فاصله یا JavaScript به ویرایشگر نمی‌دهد.
- وضعیت‌ها فقط با رنگ منتقل نمی‌شوند و تمام Focus stateها، Labelها و کنتراست باید قابل دسترس باشند.

## مرحله ۱ — Design System و پوسته مشترک

- [x] تبدیل توکن‌های Stitch به CSS variables پایدار برای رنگ، تایپوگرافی، فاصله، Radius و Elevation
- [x] پیاده‌سازی فونت Vazirmatn با وزن‌ها و Line-heightهای تعریف‌شده
- [x] بازطراحی سایدبار RTL با عرض ۲۶۰ پیکسل، گروه‌بندی فعلی و Active state صحیح
- [x] بازطراحی Header شامل Breadcrumb بومی Wagtail، جست‌وجو، Preview و پروفایل؛ اعلان تا وجود منبع واقعی عمداً حذف است
- [x] حفظ نمایش منو براساس نقش‌های Administrator، Developer، SEO، Editor و Site Manager
- [x] پیاده‌سازی Button، Input، Select، Badge، Table، Card، Alert، Modal و Drawer مشترک
- [x] بازطراحی صفحه ورود مطابق `desktop_8` با خطا، Focus، فراموشی رمز و حالت موبایل
- [x] حذف وابستگی ظاهری قبلی WordPress بدون دست‌زدن به رفتار داخلی Wagtail

معیار پذیرش مرحله ۱:

- [ ] پوسته در عرض‌های ۱۴۴۰، ۱۰۲۴، ۷۶۸ و ۳۹۰ پیکسل بدون هم‌پوشانی نمایش داده شود
- [ ] هیچ محتوایی زیر سایدبار قرار نگیرد و جهت آیکن‌ها در RTL درست باشد
- [x] منو و Login برای نقش‌های آزموده‌شده بدون خطای Template رندر شوند
- [ ] بررسی Keyboard navigation، Focus visible، Contrast و Reduced motion انجام شود

## مرحله ۲ — پیشخوان

- [x] بازسازی پیشخوان براساس `desktop_10` و `mobile_1`
- [x] اتصال کارت‌های منتشرشده، پیش‌نویس، در انتظار بررسی و زمان‌بندی‌شده به داده واقعی
- [x] نمایش صف Content Review و SEO Review با لینک و مجوز صحیح
- [x] بازطراحی وضعیت SEO، فعالیت‌های اخیر و عملیات سریع
- [x] نمایش خلاصه کاتالوگ فقط با داده‌های موجود: کل محصولات، موجود/ناموجود، تخفیف‌دار و ویژه
- [x] نمایش اعلان وضعیت سیستم فقط برای Administrator و Developer
- [x] حذف آمار ساختگی، درصد رشد ساختگی، نظرات و موجودی عددی غیرواقعی

معیار پذیرش مرحله ۲:

- [x] اعداد و لینک‌های داشبورد با Queryهای واقعی تطبیق داشته باشند
- [x] نقش‌های فاقد مجوز Action غیرمجاز نبینند
- [x] تعداد Queryها نسبت به Baseline کنترل و از N+1 جلوگیری شود
- [ ] دسکتاپ و موبایل با تصاویر مرجع مقایسه بصری شوند

## مرحله ۳ — فهرست‌های محتوا و کاتالوگ

- [x] بازطراحی فهرست برگه‌ها براساس `desktop_9` و `mobile_2`
- [x] تعمیم همان الگو به نوشته‌ها و فرم‌ها با ستون‌ها و Actionهای واقعی هر مدل
- [x] بازطراحی فهرست محصولات براساس `desktop_3` بدون سفارش، مشتری و موجودی عددی
- [x] هماهنگ‌سازی دسته‌بندی محصولات، منوها و Redirectها با Table و Filter مشترک
- [x] اتصال جست‌وجو، فیلتر، مرتب‌سازی، صفحه‌بندی، Bulk selection و Create action به ViewSetهای Wagtail
- [x] نمایش وضعیت انتشار و SEO با متن، آیکن و Badge قابل دسترس
- [x] تبدیل جدول‌های موبایل به Cardهای خوانا بدون حذف Action یا وضعیت مهم
- [x] افزودن Empty، Loading، Error و Permission-denied state قابل اجرا

معیار پذیرش مرحله ۳:

- [x] Search، Filter، Pagination و Create-parent routing واقعاً کار کنند
- [x] Draft در API عمومی ظاهر نشود و وضعیت آن در Admin درست نمایش داده شود
- [x] ستون‌ها و Actionها براساس مجوز کاربر محدود شوند
- [ ] هیچ ستون یا ردیفی پشت سایدبار یا خارج Viewport قرار نگیرد

## مرحله ۴ — ویرایشگر برگه و محصول

- [x] بازطراحی ویرایشگر برگه براساس `desktop_4` و `mobile_3`
- [x] حفظ Tabهای «محتوا»، «سئو و شبکه‌های اجتماعی» و «تنظیمات پیشرفته»
- [x] بازطراحی StreamField Blockها با عنوان فارسی، Collapse، Reorder، Duplicate و Delete موجود در Wagtail
- [x] پوشش Hero، متن غنی، تصویر و متن، ویژگی‌ها، نظرات، FAQ، CTA و Gridهای کنترل‌شده
- [x] بازطراحی پنل انتشار با Save draft، Preview، Submit for review، Schedule و Publish براساس مجوز
- [x] حفظ Autosave، Revision history، Locking، Workflow و هشدار Unsaved changes
- [x] اعمال همان Design System روی ویرایشگر محصول و گروه «اطلاعات محصول»
- [x] حفظ SKU، دسته‌بندی، قیمت تومان، تخفیف، تصویر، موجود/ناموجود و ویژه بدون افزودن Commerce
- [x] اصلاح تجربه موبایل با Action bar پایینی بدون پنهان‌کردن هشدار یا خطای Validation

معیار پذیرش مرحله ۴:

- [ ] ساخت، ویرایش، Preview، Draft، Submit for review، Publish و Schedule آزمایش شوند
- [ ] Reorder و حذف Block باعث ازبین‌رفتن داده یا ناسازگاری Schema نشود
- [ ] کاربر بدون مجوز Publish دکمه انتشار نبیند و نتواند URL آن را دور بزند
- [ ] Desktop و Mobile با تصاویر Stitch مقایسه و اختلاف‌های عمده ثبت و رفع شوند

## مرحله ۵ — رسانه

- [x] بازطراحی کتابخانه رسانه براساس `desktop_6` با Grid/List و صفحه جزئیات واقعی Wagtail به‌جای Drawer نمایشی
- [x] حفظ Upload، Collection، Search، Filter و انتخاب تصویر Wagtail
- [x] نمایش ابعاد، حجم، نوع فایل، Alt text، Caption، Focal point و محل‌های استفاده در حد قابلیت واقعی Wagtail
- [x] جایگزینی فایل و عملیات مخرب فقط با مجوز و تأیید مناسب انجام شود
- [x] حذف پشتیبانی نمایشی ویدئو یا ویژگی‌هایی که Backend فعلی ارائه نمی‌کند

معیار پذیرش مرحله ۵:

- [ ] Upload تصویر و سند، ویرایش Alt، Rendition و انتخاب تصویر داخل Block آزمایش شوند
- [ ] رسانه خصوصی یا Draft از مسیر عمومی نشت نکند
- [ ] Grid و Detail drawer در دسکتاپ و موبایل قابل استفاده باشند

## مرحله ۶ — SEO و Redirect

- [x] بازطراحی پیشخوان SEO براساس `desktop_5`
- [x] اتصال سلامت کلی، عنوان/توضیح ناقص، noindex، canonical و sitemap به تحلیل واقعی موجود
- [x] حفظ توضیح صریح «راهنمای قطعی داخلی است و امتیاز رتبه گوگل نیست»
- [x] بازطراحی Live SERP و Social preview در فرم ویرایش
- [x] بازطراحی Redirectها براساس `desktop_7` با Search، Filter و Status badge
- [x] نمایش خطای حلقه Redirect، Self redirect و مسیر نامعتبر نزدیک فیلد مربوطه
- [x] حفظ ۳۰۱، ۳۰۲، ۳۰۷ و ۳۰۸ و Redirect خودکار تغییر Slug

معیار پذیرش مرحله ۶:

- [x] نتایج Dashboard با `seo.services` و داده صفحه تطبیق داشته باشند
- [x] Validation حلقه و Redirect به خود با تست Backend پوشش داده شود
- [x] Metadata، canonical، robots، sitemap و JSON-LD عمومی بدون Regression باقی بمانند

## مرحله ۷ — منوها، کاربران و Workflow

- [x] بازطراحی مدیریت منو براساس `desktop_2`
- [x] حذف فیلد «کلاس CSS دلخواه» نمایش‌داده‌شده در Stitch برای حفظ جدایی محتوا و طراحی
- [x] اتصال افزودن صفحه/لینک خارجی، Reorder، حذف و ذخیره به مدل Menu فعلی
- [x] بازطراحی کاربران و نقش‌ها براساس `desktop_1` با استفاده از Permissionهای واقعی Wagtail
- [x] نمایش تصویری Workflow موجود بدون ساخت نقش یا مرحله نمایشی
- [x] محدودسازی تغییر مجوزهای حساس به Administrator/Developer

معیار پذیرش مرحله ۷:

- [x] ترتیب منو پس از ذخیره در API Navigation منعکس شود
- [ ] Content Review و SEO Review از ابتدا تا انتها آزمایش شوند
- [x] تست‌های Role visibility و Permission isolation پاس شوند

## مرحله ۸ — صفحات فاقد مرجع مستقیم Stitch

- [x] تعمیم Design System به نوشته‌ها و ویرایشگر مقاله
- [x] تعمیم Design System به دسته‌بندی محصولات
- [x] تعمیم Design System به فرم‌ها و Submissionها با رعایت حساسیت داده
- [x] تعمیم Design System به تنظیمات سایت و SEO
- [x] تعمیم Design System به اسناد، انتخاب‌گرهای Modal و صفحات خطا
- [x] هماهنگ‌سازی حالت‌های Empty، Loading، Error، Success، Disabled و Permission denied

## مرحله ۹ — اعتبارسنجی نهایی

- [x] اجرای کامل تست‌های Backend و Migration drift check
- [x] اجرای تست‌های Admin برای Dashboard، ViewSetها، نقش‌ها، Workflow، Draft و Redirect
- [x] اجرای Frontend lint، TypeScript و Production build برای اطمینان از عدم Regression عمومی
- [x] Smoke test احراز هویت‌شده تمام مسیرهای Admin اصلی
- [x] Smoke test Storefront، API، Sitemap، Robots، تصاویر و فرم تماس
- [ ] بررسی بصری صفحه‌به‌صفحه در ۱۴۴۰ و ۳۹۰ پیکسل و مقایسه با Stitch
- [ ] بررسی WCAG AA، Keyboard، Focus، Screen-reader labels و Reduced motion
- [x] بررسی تعداد Queryها و نبود JavaScript یا Dependency غیرضروری
- [x] به‌روزرسانی README، ممیزی نهایی، برنامه پروژه و `AGENTS.md` فقط برای تصمیم‌های پایدار
- [x] ثبت محدودیت‌های باقیمانده و روش Rollback

## تعریف پایان کار

- [ ] تمام مراحل بالا با شواهد تست و مقایسه بصری تیک خورده باشند
- [x] هیچ قابلیت موجود Wagtail یا قرارداد `/api/v1` شکسته نشده باشد
- [ ] Draft isolation، Permission، Revision، Preview و Workflow حفظ شده باشند
- [ ] پنل در دسکتاپ و موبایل به Design System Stitch وفادار و قابل استفاده باشد
- [x] هیچ قابلیت خارج از دامنه مانند Commerce، Visual Builder یا کد دلخواه وارد CMS نشده باشد
