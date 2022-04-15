from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.admindocs import urls as docs_urls
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from simpel_pages.sitemaps import CategorySitemap, PageSitemap, SearchSitemap, TagSitemap

sitemaps = {
    "tags": TagSitemap,
    "pages": PageSitemap,
    "categories": CategorySitemap,
    "search": SearchSitemap,
}

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("tinymce/", include("tinymce.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="page_sitemap"),
    path("admin/docs/", include(docs_urls)),
    path("admin/settings/", include("simpel_settings.urls")),
    path("admin/", admin.site.urls),
    path("", include("simpel_pages.urls")),
    prefix_default_language=False,
)
