from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('blogs/', blogs_view, name='blogs'),
    path('blog-details/<slug:slug>/', blog_details_view, name='blog_details'),
    path('terms/', terms_view, name='terms'),
    path('privacy/', privacy_view, name='privacy'),
    path('help/', help_view, name='help'),
    path('disclaimer/', disclaimer_view, name='disclaimer'),
    path('security/', security_view, name='security'),
    path("robots.txt", robots_txt, name="robots_txt"),
]


