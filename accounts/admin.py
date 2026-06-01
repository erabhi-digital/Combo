from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from unfold.admin import ModelAdmin


class UserAdmin(BaseUserAdmin, ModelAdmin):

    model = User

    # Columns visible in admin list page
    list_display = (
        'email',
        'username',
        'is_verified',
        'is_staff',
        'is_active'
    )

    list_filter = (
        'is_verified',
        'is_staff',
        'is_active'
    )

    search_fields = (
        'email',
        'username',
    )

    ordering = ('email',)

    # Edit user page
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),

        ('Personal Info', {
            'fields': (
                'username',
            )
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_verified',
            )
        }),

        ('OTP Info', {
            'fields': (
                'otp',
                'otp_type',
                'otp_created_at'
            )
        }),

        ('Important Dates', {
            'fields': ('last_login',)
        }),
    )

    # Create user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
            ),
        }),
    )


admin.site.register(User, UserAdmin)