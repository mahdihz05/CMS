from django.urls import path

from . import views

urlpatterns = [
    path("pages/resolve/", views.page_detail, name="api-page-detail"),
    path("products/", views.products, name="api-products"),
    path("navigation/", views.navigation, name="api-navigation"),
    path("site-settings/", views.site_settings, name="api-site-settings"),
    path("redirects/resolve/", views.redirect_lookup, name="api-redirect"),
    path("forms/submit/", views.submit_form, name="api-form-submit"),
    path("sitemap.xml", views.sitemap, name="api-sitemap"),
    path("robots.txt", views.robots, name="api-robots"),
]
