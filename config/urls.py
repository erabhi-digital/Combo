
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# urls.py

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, BlogSitemap, BrandSitemap, CategorySitemap

sitemaps = {
    "static": StaticViewSitemap,
    "blogs": BlogSitemap,
    "brands": BrandSitemap,
    "categories": CategorySitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('auth/', include('accounts.urls')),
    path('memberships/', include('member.urls')),
    path('protected/', include('protected.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

]
handler404 = 'app.views.custom_404_view'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
