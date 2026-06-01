from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('resend-otp/', resend_otp_view, name='resend_otp'),
    path('login/', login_view, name='login'),
    path('logout/',logout_view,name="logout"),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-new/', password_reset_new, name='password_reset_new'),
]