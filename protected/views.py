from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from app.models import Combo
from member.models import Membership
from member.decorators import membership_required
import logging

logger = logging.getLogger(__name__)


# ----------------------------
# BRAND / COMBO DETAIL VIEW
# ----------------------------
@login_required
@membership_required
def combo_detail_view(request, slug):

    try:
        brand_slug = slug

        combos = (
            Combo.objects
            .select_related("brand", "category")
            .filter(
                brand__slug__iexact=brand_slug,
                category__name__iexact="combo",
                is_active=True
            )
            .values(
                "main_model",
                "compatible_model"
            )
            .order_by("-created_at")
        )

        context = {
            "brand": brand_slug,
            "combos": combos
        }

        return render(
            request,
            "protected/combo_detail.html",
            context
        )

    except Exception as e:
        logger.error(f"Combo Detail View Error: {e}")

        return render(
            request,
            "protected/combo_detail.html",
            {
                "brand": slug,
                "combos": [],
            }
        )


# ----------------------------
# CATEGORY DETAIL VIEW
# ----------------------------
@login_required
@membership_required
def category_detail_view(request, slug):

    try:
        category_slug = slug

        combos = (
            Combo.objects
            .select_related("brand", "category")
            .filter(
                category__slug__iexact=category_slug,
                is_active=True
            )
            .values(
                "main_model",
                "compatible_model"
            )
            .order_by("-created_at")
        )

        context = {
            "category": category_slug,
            "combos": combos
        }

        return render(
            request,
            "protected/category_detail.html",
            context
        )

    except Exception as e:
        logger.error(f"Category Detail View Error: {e}")

        return render(
            request,
            "protected/category_detail.html",
            {
                "category": slug,
                "combos": [],
            }
        )


# ----------------------------
# PROFILE VIEW
# ----------------------------
@login_required
def profile_view(request):

    try:
        user = request.user

        membership = (
            Membership.objects
            .filter(user=user)
            .only(
                "plan_name",
                "is_active",
                "start_date",
                "expiry_date"
            )
            .first()
        )

        context = {
            "user": user,
            "membership": membership,
            "now": timezone.now()
        }

        return render(
            request,
            "protected/profile.html",
            context
        )

    except Exception as e:
        logger.error(f"Profile View Error: {e}")

        return render(
            request,
            "protected/profile.html",
            {
                "user": request.user,
                "membership": None,
                "now": timezone.now(),
            }
        )