from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random


# ==========================
# USER MANAGER
# ==========================
class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError("Email is required")

        if not username:
            raise ValueError("Username is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user


    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email=email,
            username=username,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)

        return user
# ==========================
# USER MODEL
# ==========================
class User(AbstractBaseUser, PermissionsMixin):

    # Core Fields
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # OTP Type Choices
    OTP_TYPE_CHOICES = (
        ('register', 'Register'),
        ('reset', 'Reset Password'),
    )

    # OTP Fields
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_type = models.CharField(max_length=10, choices=OTP_TYPE_CHOICES, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


    # ==========================
    # OTP GENERATE
    # ==========================
    def generate_otp(self, otp_type):
        self.otp = str(random.randint(100000, 999999))
        self.otp_type = otp_type
        self.otp_created_at = timezone.now()
        self.save(update_fields=['otp', 'otp_type', 'otp_created_at'])
        return self.otp


    # ==========================
    # OTP VALIDATE
    # ==========================
    def otp_is_valid(self, otp, otp_type):
        if not self.otp or not self.otp_created_at:
            return False

        if self.otp != otp:
            return False

        if self.otp_type != otp_type:
            return False

        # Expiry: 5 minutes
        diff = timezone.now() - self.otp_created_at
        return diff.total_seconds() <= 300


    # ==========================
    # CLEAR OTP (after use)
    # ==========================
    def clear_otp(self):
        self.otp = None
        self.otp_type = None
        self.otp_created_at = None
        self.save(update_fields=['otp', 'otp_type', 'otp_created_at'])