from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL


class Membership(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="membership"
    )

    is_active = models.BooleanField(default=False)

    start_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    plan_name = models.CharField(max_length=50, default="Basic")

    # price pulled from settings
    price = models.IntegerField(default=settings.MEMBERSHIP_PRICE)

    created_at = models.DateTimeField(auto_now_add=True)

    def activate(self):
        """
        Activate or extend membership by 30 days
        """

        now = timezone.now()

        # Extend if active
        if self.expiry_date and self.expiry_date > now:
            self.expiry_date += timedelta(days=30)

        # Start new membership
        else:
            self.start_date = now
            self.expiry_date = now + timedelta(days=30)

        self.is_active = True
        self.save()

    def check_status(self):
        """
        Deactivate membership if expired
        """

        if self.expiry_date and timezone.now() > self.expiry_date:
            self.is_active = False
            self.save()

    def __str__(self):
        return f"{self.user} - {self.plan_name}"


class Payment(models.Model):

    STATUS_CHOICES = [
        ("created", "Created"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.IntegerField(default=settings.MEMBERSHIP_PRICE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created"
    )

    order_id = models.CharField(max_length=200, blank=True)
    payment_id = models.CharField(max_length=200, blank=True)

    razorpay_signature = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"