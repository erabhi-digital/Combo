from django.core.cache import cache

from .models import Nav


def navbar(request):

    try:
        # =========================================
        # CACHE KEY
        # =========================================
        cache_key = "navbar_items"

        # =========================================
        # GET FROM CACHE
        # =========================================
        nav_items = cache.get(cache_key)

        # =========================================
        # DATABASE QUERY IF CACHE MISS
        # =========================================
        if nav_items is None:

            nav_items = list(
                Nav.objects.filter(
                    is_active=True
                )
                .only("name", "url", "order")
                .order_by("order")
            )

            # Cache for 1 hour
            cache.set(
                cache_key,
                nav_items,
                timeout=60 * 60
            )

        # =========================================
        # FALLBACK IF EMPTY
        # =========================================
        if not nav_items:

            nav_items = [
                {"name": "Home", "url": "home"},
                {"name": "Blogs", "url": "blogs"},
                {"name": "About", "url": "about"},
                {"name": "Contact", "url": "contact"},
            ]

    except Exception as error:

        print(f"Navbar Context Error: {error}")

        nav_items = [
            {"name": "Home", "url": "home"},
            {"name": "Blogs", "url": "blogs"},
            {"name": "About", "url": "about"},
            {"name": "Contact", "url": "contact"},
        ]

    return {
        "nav_items": nav_items
    }