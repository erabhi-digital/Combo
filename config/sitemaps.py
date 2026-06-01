# sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from app.models import Blog, Brand, Category


# Static Pages Sitemap
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
            "contact",
            "blogs",
            "terms",
            "privacy",
            "help",
            "disclaimer",
            "security",
        ]

    def location(self, item):
        return reverse(item)


# Blog Sitemap
class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("blog_details", args=[obj.slug])


# Brand Sitemap
class BrandSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Brand.objects.filter(is_active=True)

    def location(self, obj):
        return f"/brand/{obj.slug}/"


# Category Sitemap
class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, obj):
        return f"/category/{obj.slug}/"