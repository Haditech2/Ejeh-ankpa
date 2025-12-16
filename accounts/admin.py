"""
Admin configuration for accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ChiefProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    
    list_display = [
        'email', 'first_name', 'last_name', 'role',
        'traditional_title', 'is_verified', 'is_active', 'date_joined'
    ]
    list_filter = ['role', 'is_verified', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name', 'traditional_title']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_image', 'bio')
        }),
        ('Role & Title', {
            'fields': ('role', 'traditional_title')
        }),
        ('Community', {
            'fields': ('village', 'ward')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2',
                'role', 'is_staff', 'is_active'
            ),
        }),
    )


@admin.register(ChiefProfile)
class ChiefProfileAdmin(admin.ModelAdmin):
    """Admin interface for ChiefProfile model."""
    
    list_display = ['title', 'user', 'domain', 'installation_date', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'user__first_name', 'user__last_name', 'domain']
    ordering = ['order', 'title']
    raw_id_fields = ['user']
