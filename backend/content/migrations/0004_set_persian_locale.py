from django.db import migrations


def set_persian_locale(apps, schema_editor):
    Locale = apps.get_model("wagtailcore", "Locale")
    UserProfile = apps.get_model("wagtailusers", "UserProfile")
    Locale.objects.filter(language_code__in=["en", "en-us"]).update(language_code="fa")
    UserProfile.objects.all().update(preferred_language="fa")


def restore_english_locale(apps, schema_editor):
    Locale = apps.get_model("wagtailcore", "Locale")
    UserProfile = apps.get_model("wagtailusers", "UserProfile")
    Locale.objects.filter(language_code="fa").update(language_code="en")
    UserProfile.objects.filter(preferred_language="fa").update(preferred_language="en")


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0003_alter_blogindexpage_body_alter_blogpage_body_and_more"),
        ("wagtailcore", "0096_referenceindex_referenceindex_source_object_and_more"),
        ("wagtailusers", "0014_userprofile_contrast"),
    ]

    operations = [migrations.RunPython(set_persian_locale, restore_english_locale)]
