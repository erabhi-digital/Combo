from django.contrib import admin
from django.utils.html import format_html
from .models import *
from unfold.admin import ModelAdmin

# =========================================================
# ADMIN BRANDING
# =========================================================

admin.site.site_header = "XyzCombo Admin"
admin.site.site_title = "XyzCombo Panel"
admin.site.index_title = "Welcome to Dashboard"


# =========================================================
# GLOBAL ADMIN BASE
# Reusable admin optimizations
# =========================================================

class BaseAdmin(ModelAdmin):
    readonly_fields = ("created_at",)

    list_per_page = 25

    date_hierarchy = "created_at"

    save_on_top = True


# =========================================================
# ICON
# =========================================================

@admin.register(Icon)
class IconAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "name",
        "class_name",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "class_name",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    list_editable = (
        "is_active",
    )

    ordering = ("-created_at",)


# =========================================================
# PAGE KEY
# =========================================================

@admin.register(PageKey)
class PageKeyAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    ordering = ("-created_at",)


# =========================================================
# IMAGE
# =========================================================

@admin.register(Image)
class ImageAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "name",
        "preview",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    list_editable = (
        "is_active",
    )

    ordering = ("-created_at",)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:5px;" />',
                obj.image.url
            )
        return "-"

    preview.short_description = "Preview"


# =========================================================
# SITE SETTINGS
# =========================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "site_name",
        "logo_preview",
        "favicon_preview",
        "created_at",
    )

    search_fields = (
        "site_name",
    )

    autocomplete_fields = (
        "logo",
        "favicon",
    )

    ordering = ("-created_at",)

    def logo_preview(self, obj):
        if obj.logo and obj.logo.image:
            return format_html(
                '<img src="{}" width="40" />',
                obj.logo.image.url
            )
        return "-"

    logo_preview.short_description = "Logo"

    def favicon_preview(self, obj):
        if obj.favicon and obj.favicon.image:
            return format_html(
                '<img src="{}" width="25" />',
                obj.favicon.image.url
            )
        return "-"

    favicon_preview.short_description = "Favicon"


# =========================================================
# NAVBAR
# =========================================================

@admin.register(Nav)
class NavAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "name",
        "url",
        "icon",
        "order",
        "is_active",
    )

    search_fields = (
        "name",
        "url",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    autocomplete_fields = (
        "icon",
    )

    ordering = ("order",)


# =========================================================
# HERO
# =========================================================

@admin.register(Hero)
class HeroAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "badge_label",
        "title",
        "page_key",
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "sub_title",
    )

    list_filter = (
        "page_key",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    autocomplete_fields = (
        "page_key",
    )

    ordering = ("-created_at",)


# =========================================================
# BRAND
# =========================================================

@admin.register(Brand)
class BrandAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "name",
        "slug",
        "compatible",
        "order",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
        "compatible",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_filter = (
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = ("order",)


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "name",
        "slug",
        "order",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_filter = (
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = ("order",)


# =========================================================
# COMBO
# =========================================================

@admin.register(Combo)
class ComboAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "main_model",
        "brand",
        "category",
        "is_active",
        "created_at",
    )

    search_fields = (
        "main_model",
        "compatible_model",
    )

    list_filter = (
        "brand",
        "category",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    autocomplete_fields = (
        "brand",
        "category",
    )

    ordering = ("-created_at",)


# =========================================================
# BLOG
# =========================================================

@admin.register(Blog)
class BlogAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "title",
        "slug",
        "image_preview",
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "slug",
        "description",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    list_editable = (
        "is_active",
    )

    autocomplete_fields = (
        "image",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    ordering = ("-created_at",)

    def image_preview(self, obj):
        if obj.image and obj.image.image:
            return format_html(
                '<img src="{}" width="50" />',
                obj.image.image.url
            )
        return "-"

    image_preview.short_description = "Image"


# =========================================================
# ABOUT
# =========================================================

@admin.register(About)
class AboutAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "title",
        "about",
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "about",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    autocomplete_fields = (
        "image",
    )

    ordering = ("-created_at",)


# =========================================================
# TEAM
# =========================================================

@admin.register(Team)
class TeamAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "name",
        "role",
        "email",
        "phone",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "role",
        "email",
    )

    list_filter = (
        "role",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    autocomplete_fields = (
        "image",
    )

    ordering = ("-created_at",)


# =========================================================
# CONTACT
# =========================================================

@admin.register(Contact)
class ContactAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "name",
        "email",
        "sub",
        "created_at",
        "is_active",
    )

    search_fields = (
        "name",
        "email",
        "sub",
        "message",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    readonly_fields = (
        "ip_address",
        "user_agent",
        "created_at",
    )

    list_editable = (
        "is_active",
    )

    ordering = ("-created_at",)


# =========================================================
# PRIVACY TERMS
# =========================================================

@admin.register(PrivacyTerms)
class PrivacyTermsAdmin(BaseAdmin,ModelAdmin):
    list_display = (
        "title",
        "privacy_or_terms",
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "privacy_or_terms",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    ordering = ("-created_at",)