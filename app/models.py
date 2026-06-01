from django.db import models, transaction
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# =========================================================
# ABSTRACT BASE MODEL
# Common reusable fields
# =========================================================
class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    class Meta:
        abstract = True


# =========================================================
# ICON MODEL
# Stores icon classes (FontAwesome / Bootstrap Icons)
# =========================================================
class Icon(BaseModel):
    name = models.CharField(
        max_length=100,
        db_index=True
    )

    class_name = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.class_name}"


# =========================================================
# PAGE KEY MODEL
# Used to identify website pages dynamically
# =========================================================
class PageKey(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return self.name


# =========================================================
# IMAGE LIBRARY MODEL
# Central image storage used across the website
# =========================================================
class Image(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.image:
            valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]

            if not any(
                self.image.name.lower().endswith(ext)
                for ext in valid_extensions
            ):
                raise ValidationError(
                    "Only JPG, JPEG, PNG, and WEBP files are allowed."
                )

    def __str__(self):
        return self.name


# =========================================================
# SITE SETTINGS
# Controls global site settings like logo and favicon
# =========================================================
class SiteSettings(models.Model):
    site_name = models.CharField(
        max_length=200,
        db_index=True
    )

    logo = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        related_name="site_logo"
    )

    favicon = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        related_name="site_favicon"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.site_name


# =========================================================
# NAVBAR MODEL
# Dynamic navigation menu managed from admin
# =========================================================
class Nav(BaseModel):
    name = models.CharField(
        max_length=100,
        db_index=True
    )

    url = models.CharField(
        max_length=200,
        blank=True
    )

    icon = models.ForeignKey(
        Icon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nav_icons"
    )

    order = models.PositiveIntegerField(
        default=0,
        db_index=True
    )

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["order", "is_active"]),
        ]

    def __str__(self):
        return self.name


# =========================================================
# HERO SECTION
# Controls hero banners for different pages
# =========================================================
class Hero(BaseModel):
    badge_label = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=200,
        db_index=True
    )

    sub_title = models.TextField(
        blank=True,
        null=True
    )

    page_key = models.ForeignKey(
        PageKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="heroes",
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]

        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

        indexes = [
            models.Index(fields=["page_key", "is_active"]),
            models.Index(fields=["created_at", "is_active"]),
        ]

    def __str__(self):
        return self.title


# =========================================================
# BRAND MODEL
# Stores product brands
# =========================================================
class Brand(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    compatible = models.CharField(
        max_length=100,
        blank=True
    )

    slug = models.SlugField(
        max_length=120,
        null=True,
        blank=True,
        unique=True,
        db_index=True
    )

    order = models.PositiveIntegerField(
        default=0,
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug", "is_active"]),
        ]

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1

        while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# CATEGORY MODEL
# Product categories
# =========================================================
class Category(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    slug = models.SlugField(
        max_length=120,
        blank=True,
        null=True,
        unique=True,
        db_index=True
    )

    order = models.PositiveIntegerField(
        default=0,
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug", "is_active"]),
        ]

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1

        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================
# COMBO MODEL
# Stores compatible product combinations
# =========================================================
class Combo(BaseModel):
    main_model = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    compatible_model = models.TextField(
        blank=True,
        null=True
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="combo_brands",
        db_index=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="combo_categories",
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["main_model"]),
            models.Index(fields=["brand", "category"]),
            models.Index(fields=["brand", "is_active"]),
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["created_at", "is_active"]),
        ]

    def __str__(self):
        return self.main_model


# =========================================================
# BLOG MODEL
# For storing blog posts
# =========================================================
class Blog(BaseModel):
    title = models.CharField(
        max_length=200,
        db_index=True
    )

    description = models.TextField()

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        db_index=True
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_images"
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["slug", "is_active"]),
            models.Index(fields=["created_at", "is_active"]),
        ]

    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# =========================================================
# ABOUT SECTION
# Story / Vision / Mission
# =========================================================
class About(BaseModel):
    ABOUT_CHOICES = [
        ("story", "Story"),
        ("vision", "Vision"),
        ("mission", "Mission"),
    ]

    title = models.CharField(
        max_length=100,
        db_index=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="abouts",
        db_index=True
    )

    about = models.CharField(
        max_length=100,
        choices=ABOUT_CHOICES,
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["about", "is_active"]),
            models.Index(fields=["created_at", "is_active"]),
        ]

    def __str__(self):
        return self.title


# =========================================================
# TEAM MEMBERS
# =========================================================
class Team(BaseModel):
    name = models.CharField(
        max_length=150,
        db_index=True
    )

    role = models.CharField(
        max_length=150,
        blank=True,
        db_index=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_images"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        db_index=True
    )

    whatsapp = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["role", "is_active"]),
            models.Index(fields=["created_at", "is_active"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.role}"


# =========================================================
# CONTACT FORM SUBMISSIONS
# =========================================================
class Contact(BaseModel):
    name = models.CharField(
        max_length=100,
        db_index=True
    )

    email = models.EmailField(
        db_index=True
    )

    sub = models.CharField(
        max_length=100,
        db_index=True
    )

    message = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        db_index=True
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["email", "created_at"]),
            models.Index(fields=["created_at", "is_active"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.email}"


# =========================================================
# PRIVACY POLICY & TERMS
# =========================================================
class PrivacyTerms(BaseModel):
    PT_CHOICES = [
        ("privacy", "Privacy"),
        ("terms", "Terms"),
    ]

    title = models.CharField(
        max_length=100,
        db_index=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    privacy_or_terms = models.CharField(
        max_length=100,
        choices=PT_CHOICES,
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["privacy_or_terms", "is_active"]),
            models.Index(fields=["created_at", "is_active"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.privacy_or_terms}"