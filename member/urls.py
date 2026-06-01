from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path("buy/", views.create_order, name="create_order"),
    path("verify/", views.verify_payment, name="verify_payment"),
    path("webhook/", views.razorpay_webhook, name="webhook"),
]