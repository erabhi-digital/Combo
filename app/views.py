from django.shortcuts import render, redirect , get_object_or_404
from .models import *
from .db_query import *
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse



# Create your views here.





# ---------------- HOME ----------------
def home_view(request):
    context=get_home_context()
    return render(request, 'app/home.html', context)





# ---------------- ABOUT ----------------
def about_view(request):
    context=get_about_context()
    return render(request, 'app/about.html', context)





# ---------------- CONTACT ----------------
def contact_view(request):

    context = get_contact_context()

    try:

        if request.method == "POST":

            name = request.POST.get("name")
            email = request.POST.get("email")
            sub = request.POST.get("sub")
            message = request.POST.get("message")

            # ---------------- Validation ----------------
            if not name or not email or not sub or not message:

                context["error"] = (
                    "Please fill in all required fields."
                )

                return render(
                    request,
                    "app/contact.html",
                    context
                )

            # ---------------- User Info ----------------
            ip = request.META.get("REMOTE_ADDR")
            agent = request.META.get("HTTP_USER_AGENT")

            # ---------------- Save ----------------
            Contact.objects.create(
                name=name,
                email=email,
                sub=sub,
                message=message,
                ip_address=ip,
                user_agent=agent
            )

            context["success"] = (
                "Your message has been sent successfully!"
            )

            return render(
                request,
                "app/contact.html",
                context
            )

    except Exception as e:

        logger.error(f"Contact Form Error: {e}")

        context["error"] = (
            "Something went wrong. Please try again later."
        )

    return render(
        request,
        "app/contact.html",
        context
    )

# ---------------- BLOGS ----------------
def blogs_view(request):
    context=get_blogs_context()
    return render(request, 'app/blogs.html', context)



# ---------------- BLOG DETAILS ----------------
def blog_details_view(request, slug):

    blog = get_object_or_404(Blog, slug=slug)

    related_blogs = Blog.objects.exclude(id=blog.id).order_by("-created_at")[:3]

    return render(request, "app/blog_details.html", {
        "blog": blog,
        "related_blogs": related_blogs
    })


# ---------------- TERMS ----------------
def terms_view(request):
    context=get_terms_context()
    return render(request, 'app/terms.html', context)


# ---------------- PRIVACY ----------------
def privacy_view(request):
    context=get_privacy_context()
    return render(request, 'app/privacy.html', context)


# ---------------- HELP ----------------
def help_view(request):
    return render(request, 'app/help.html')


# ---------------- DISCLAIMER ----------------
def disclaimer_view(request):
    return render(request, 'app/disclaimer.html')


# ---------------- SECURITY ----------------
def security_view(request):
    return render(request, 'app/security.html')


# ---------------- ERROR ----------------
def custom_404_view(request, exception):
    return render(request, "404.html", status=404)





def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))

    lines = [
        "User-Agent: *",
        "Allow: /",
        "",
        "# Block system folders",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /static/",
        "Disallow: /media/",
        "",
        f"Sitemap: {sitemap_url}",
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain")