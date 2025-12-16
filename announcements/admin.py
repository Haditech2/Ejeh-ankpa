"""
Admin configuration for announcements app.
"""

from django.contrib import admin
from .models import Announcement, RoyalMessage, AnnouncementCategory


@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    """Admin for announcement categories."""
    
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """Admin for announcements."""
    
    list_display = [
        'title', 'category', 'announcement_type', 'priority',
        'is_published', 'is_featured', 'is_pinned', 'view_count', 'publish_date'
    ]
    list_filter = [
        'category', 'announcement_type', 'priority',
        'is_published', 'is_featured', 'is_pinned'
    ]
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    raw_id_fields = ['author']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Classification', {
            'fields': ('category', 'announcement_type', 'priority')
        }),
        ('Media', {
            'fields': ('featured_image', 'attachment')
        }),
        ('Publishing', {
            'fields': ('author', 'is_published', 'is_featured', 'is_pinned', 'publish_date')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(RoyalMessage)
class RoyalMessageAdmin(admin.ModelAdmin):
    """Admin for royal messages."""
    
    list_display = ['title', 'message_date', 'is_published', 'is_featured']
    list_filter = ['is_published', 'is_featured']
    search_fields = ['title', 'message']
    date_hierarchy = 'message_date'
