import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import User
from .utils import send_otp_email

logger = logging.getLogger(__name__)


# =====================================================
# REGISTER
# =====================================================
def register_view(request):

    context = {}

    try:
        if request.method == "POST":

            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if not all([username, email, password]):
                context["error"] = "All fields are required."
                return render(request, "accounts/register.html", context)

            if User.objects.filter(email=email).exists():
                context["error"] = "Email already exists."
                return render(request, "accounts/register.html", context)

            if User.objects.filter(username=username).exists():
                context["error"] = "Username already exists."
                return render(request, "accounts/register.html", context)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            otp = user.generate_otp("register")
            send_otp_email(email, otp, purpose="verify")

            request.session["email"] = email
            request.session["otp_purpose"] = "register"

            return redirect("verify_otp")

    except Exception as e:
        logger.exception(f"Register Error: {e}")
        context["error"] = "Something went wrong"

    return render(request, "accounts/register.html", context)


# =====================================================
# LOGIN
# =====================================================
def login_view(request):

    context = {}

    try:
        if request.method == "POST":

            email = request.POST.get("email")
            password = request.POST.get("password")

            if not email or not password:
                context["error"] = "All fields are required."
                return render(request, "accounts/login.html", context)

            user = authenticate(request, email=email, password=password)

            if not user:
                context["error"] = "Invalid email or password."
                return render(request, "accounts/login.html", context)

            if not user.is_verified:
                request.session["email"] = email
                request.session["otp_purpose"] = "register"
                return redirect("verify_otp")

            login(request, user)
            return redirect("home")

    except Exception as e:
        logger.exception(f"Login Error: {e}")
        context["error"] = "Login failed"

    return render(request, "accounts/login.html", context)


# =====================================================
# VERIFY OTP
# =====================================================
def verify_otp_view(request):

    context = {}

    try:

        email = request.session.get("email")
        purpose = request.session.get("otp_purpose")

        if not email or not purpose:
            return redirect("register")

        user = get_object_or_404(User, email=email)

        if request.method == "POST":

            otp = request.POST.get("otp")

            if user.otp_is_valid(otp, purpose):

                user.clear_otp()

                if purpose == "register":
                    user.is_verified = True
                    user.save()

                    request.session.pop("otp_purpose", None)

                    login(request, user)
                    return redirect("home")

                elif purpose == "reset":
                    request.session["otp_verified"] = True
                    request.session.pop("otp_purpose", None)
                    return redirect("password_reset_new")

            context["error"] = "Invalid or expired OTP"

    except Exception as e:
        logger.exception(f"OTP Verify Error: {e}")
        context["error"] = "Verification failed"

    return render(request, "accounts/verify_otp.html", context)


# =====================================================
# RESEND OTP
# =====================================================
def resend_otp_view(request):

    context = {}

    try:

        email = request.session.get("email")
        purpose = request.session.get("otp_purpose")

        if not email or not purpose:
            return redirect("register")

        user = get_object_or_404(User, email=email)

        if user.otp_created_at:
            diff = timezone.now() - user.otp_created_at

            if diff.total_seconds() < 60:
                context["error"] = "Wait 1 minute before resending OTP"
                return render(request, "accounts/verify_otp.html", context)

        otp = user.generate_otp(purpose)
        send_otp_email(email, otp, purpose=purpose)

        context["success"] = "OTP resent successfully"

    except Exception as e:
        logger.exception(f"Resend OTP Error: {e}")
        context["error"] = "Failed to resend OTP"

    return render(request, "accounts/verify_otp.html", context)


# =====================================================
# PASSWORD RESET REQUEST
# =====================================================
def password_reset_request(request):

    context = {}

    try:

        if request.method == "POST":

            email = request.POST.get("email")

            if not email:
                context["error"] = "Email is required."
                return render(request, "accounts/password_reset_email.html", context)

            user = User.objects.filter(email=email).first()

            if not user:
                context["error"] = "No account found."
                return render(request, "accounts/password_reset_email.html", context)

            otp = user.generate_otp("reset")
            send_otp_email(email, otp, purpose="reset")

            request.session["email"] = email
            request.session["otp_purpose"] = "reset"

            return redirect("verify_otp")

    except Exception as e:
        logger.exception(f"Password Reset Request Error: {e}")
        context["error"] = "Something went wrong"

    return render(request, "accounts/password_reset_email.html", context)


# =====================================================
# NEW PASSWORD SET
# =====================================================
def password_reset_new(request):

    context = {}

    try:

        email = request.session.get("email")
        otp_verified = request.session.get("otp_verified")

        if not email or not otp_verified:
            return redirect("password_reset")

        user = get_object_or_404(User, email=email)

        if request.method == "POST":

            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not new_password or not confirm_password:
                context["error"] = "All fields are required."
                return render(request, "accounts/password_reset_new.html", context)

            if new_password != confirm_password:
                context["error"] = "Passwords do not match."
                return render(request, "accounts/password_reset_new.html", context)

            user.set_password(new_password)
            user.clear_otp()
            user.save()

            request.session.flush()

            return redirect("login")

    except Exception as e:
        logger.exception(f"Password Reset Error: {e}")
        context["error"] = "Password reset failed"

    return render(request, "accounts/password_reset_new.html", context)


# =====================================================
# LOGOUT
# =====================================================
@login_required
def logout_view(request):

    try:
        logout(request)
        return redirect("login")

    except Exception as e:
        logger.exception(f"Logout Error: {e}")
        return redirect("login")