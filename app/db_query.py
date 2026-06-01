from .models import *
from django.utils import timezone
from django.core.cache import cache
from django.db.models import Prefetch

import logging
logger = logging.getLogger(__name__)



def get_lower(string):
    try:
        return string.lower()
    except Exception as e:
        logger.error(f"Lower Function Error: {e}")
        return ""

# =========================================================
# OPTIMIZED HOME CONTEXT
# PERFORMANCE IMPROVED VERSION
# =========================================================

def get_home_context():

    try:

        # =================================================
        # CACHE KEY
        # =================================================
        cache_key = "home_page_context"

        # =================================================
        # GET CACHE
        # =================================================
        context = cache.get(cache_key)

        if context:
            return context

        # =================================================
        # HERO QUERY
        # =================================================
        hero = (
            Hero.objects
            .select_related("page_key")
            .only(
                "id",
                "title",
                "sub_title",
                "badge_label",
                "page_key__name",
                "is_active"
            )
            .filter(
                page_key__name=get_lower("home"),
                is_active=True
            )
            .first()
        )

        # =================================================
        # BRANDS QUERY
        # =================================================
        brands = list(
            Brand.objects
            .only(
                "id",
                "name",
                "compatible",
                "slug",
                "order"
            )
            .filter(
                is_active=True
            )
            .order_by("order")
        )

        # =================================================
        # CATEGORY QUERY
        # =================================================
        categories = list(
            Category.objects
            .only(
                "id",
                "name",
                "slug",
                "order"
            )
            .filter(
                is_active=True
            )
            .order_by("order")
        )

        # =================================================
        # BLOG QUERY
        # =================================================
        blogs = list(
            Blog.objects
            .select_related("image")
            .only(
                "id",
                "title",
                "slug",
                "description",
                "created_at",
                "image__image"
            )
            .order_by("-created_at")[:3]
        )

        # =================================================
        # CONTEXT
        # =================================================
        context = {
            "hero": hero,
            "brands": brands,
            "categories": categories,
            "blogs": blogs,
        }

        # =================================================
        # CACHE CONTEXT
        # =================================================
        cache.set(
            cache_key,
            context,
            timeout=60 * 30
        )

        return context

    except Exception as error:

        logger.error(
            f"Home Context Error: {str(error)}"
        )

        # =================================================
        # SAFE FALLBACK
        # =================================================
        return {
            "hero": None,
            "brands": [],
            "categories": [],
            "blogs": [],
        }







# ---------------- ABOUT (OPTIMIZED) ----------------
def get_about_context():

    try:
        cache_key = "about_page_context"

        # ================================
        # CACHE CHECK
        # ================================
        context = cache.get(cache_key)
        if context:
            return context

        # ================================
        # HERO (optimized)
        # ================================
        hero = (
            Hero.objects
            .select_related("page_key")
            .only(
                "id",
                "title",
                "sub_title",
                "badge_label",
                "page_key__name",
                "is_active",
            )
            .filter(
                page_key__name=get_lower("about"),
                is_active=True
            )
            .first()
        )

        # ================================
        # ABOUT DATA (SINGLE QUERY)
        # instead of 3 queries
        # ================================
        about_qs = {
            obj.about: obj
            for obj in About.objects.filter(
                is_active=True
            ).only(
                "id",
                "about",
                "title",
                "description",
                "image"
            )
        }

        story = about_qs.get("story")
        vision = about_qs.get("vision")
        mission = about_qs.get("mission")

        # ================================
        # TEAM (optimized)
        # ================================
        teams = list(
            Team.objects
            .select_related("image")
            .only(
                "id",
                "name",
                "role",
                "bio",
                "image__image"
            )
            .filter(is_active=True)
        )

        # ================================
        # FINAL CONTEXT
        # ================================
        context = {
            "hero": hero,
            "story": story,
            "vision": vision,
            "mission": mission,
            "teams": teams
        }

        # ================================
        # CACHE RESULT (30 min)
        # ================================
        cache.set(cache_key, context, 60 * 30)

        return context

    except Exception as e:

        logger.error(f"About Context Error: {e}")

        return {
            "hero": None,
            "story": None,
            "vision": None,
            "mission": None,
            "teams": [],
        }





# ---------------- CONTACT ----------------
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


def get_contact_context():

    try:
        cache_key = "contact_page_context"

        # ==============================
        # CACHE CHECK
        # ==============================
        context = cache.get(cache_key)
        if context:
            return context

        # ==============================
        # HERO QUERY (OPTIMIZED)
        # ==============================
        hero = (
            Hero.objects
            .select_related("page_key")
            .only(
                "id",
                "title",
                "sub_title",
                "badge_label",
                "page_key__name",
                "is_active",
            )
            .filter(
                page_key__name=get_lower("contact"),
                is_active=True
            )
            .first()
        )

        # ==============================
        # BUILD CONTEXT
        # ==============================
        context = {
            "hero": hero
        }

        # ==============================
        # CACHE (30 min)
        # ==============================
        cache.set(cache_key, context, 60 * 30)

        return context

    except Exception as e:

        logger.error(f"Contact Context Error: {e}")

        return {
            "hero": None,
        }
        
        

# ---------------- BLOGS ----------------

def get_blogs_context():

    try:
        cache_key = "blogs_page_context"

        # =========================
        # CACHE CHECK
        # =========================
        context = cache.get(cache_key)
        if context:
            return context

        # =========================
        # HERO QUERY (OPTIMIZED)
        # =========================
        hero = (
            Hero.objects
            .select_related("page_key")
            .only(
                "id",
                "title",
                "sub_title",
                "badge_label",
                "page_key__name",
                "is_active",
            )
            .filter(
                page_key__name=get_lower("blogs"),
                is_active=True
            )
            .first()
        )

        # =========================
        # BLOGS QUERY (OPTIMIZED)
        # LIMIT ADDED (CRITICAL FIX)
        # =========================
        blogs = list(
            Blog.objects
            .select_related("image")
            .only(
                "id",
                "title",
                "slug",
                "description",
                "created_at",
                "image__image"
            )
            .order_by("-created_at")[:9]   # important improvement
        )

        # =========================
        # CONTEXT
        # =========================
        context = {
            "hero": hero,
            "blogs": blogs
        }

        # =========================
        # CACHE (30 min)
        # =========================
        cache.set(cache_key, context, 60 * 30)

        return context

    except Exception as e:

        logger.error(f"Blogs Context Error: {e}")

        return {
            "hero": None,
            "blogs": [],
        }




# ---------------- TERMS ----------------

def get_terms_context():

    try:
        cache_key = "terms_page_context"

        # =========================
        # CACHE CHECK
        # =========================
        context = cache.get(cache_key)
        if context:
            return context

        # =========================
        # HERO (optimized)
        # =========================
        hero = (
            Hero.objects
            .select_related("page_key")
            .only(
                "id",
                "title",
                "sub_title",
                "badge_label",
                "page_key__name",
                "is_active",
            )
            .filter(
                page_key__name=get_lower("terms"),
                is_active=True
            )
            .first()
        )

        # =========================
        # TERMS (optimized)
        # =========================
        terms = list(
            PrivacyTerms.objects
            .only(
                "id",
                "title",
                "description",
                "privacy_or_terms",
                "is_active",
            )
            .filter(
                privacy_or_terms="terms",
                is_active=True
            )
            .order_by("id")  # or "order" if exists
        )

        # =========================
        # CONTEXT
        # =========================
        context = {
            "hero": hero,
            "terms": terms,
            "today": timezone.now(),
        }

        # =========================
        # CACHE (1 hour recommended)
        # =========================
        cache.set(
            cache_key,
            context,
            60 * 60
        )

        return context

    except Exception as e:

        logger.error(f"Terms Context Error: {e}")

        return {
            "hero": None,
            "terms": [],
            "today": timezone.now(),
        }








# ---------------- PRIVACY ----------------
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def get_privacy_context():

    try:
        cache_key = "privacy_page_context"

        # =========================
        # CACHE CHECK
        # =========================
        context = cache.get(cache_key)
        if context:
            return context

        # =========================
        # HERO QUERY (OPTIMIZED)
        # =========================
        hero = (
            Hero.objects
            .select_related("page_key")
            .only(
                "id",
                "title",
                "sub_title",
                "badge_label",
                "page_key__name",
                "is_active",
            )
            .filter(
                page_key__name=get_lower("privacy"),
                is_active=True
            )
            .first()
        )

        # =========================
        # PRIVACY POLICIES (OPTIMIZED)
        # =========================
        policies = list(
            PrivacyTerms.objects
            .only(
                "id",
                "title",
                "description",
                "privacy_or_terms",
                "is_active",
            )
            .filter(
                privacy_or_terms="privacy",
                is_active=True
            )
            .order_by("id")
        )

        # =========================
        # CONTEXT
        # =========================
        context = {
            "hero": hero,
            "policies": policies,
            "today": timezone.now(),
        }

        # =========================
        # CACHE (1 hour)
        # =========================
        cache.set(context, cache_key, 60 * 60)

        return context

    except Exception as e:

        logger.error(f"Privacy Context Error: {e}")

        return {
            "hero": None,
            "policies": [],
            "today": timezone.now(),
        }