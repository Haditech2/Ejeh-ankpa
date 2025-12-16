"""
Admin configuration for events app.
"""

from django.contrib import admin
from .models import Event, EventCategory, TraditionalFestival


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    """Admin for event categories."""
    
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin for events."""
    
    list_display = [
        'title', 'category', 'event_type', 'start_date', 'venue',
        'is_published', 'is_featured', 'is_cancelled'
    ]
    list_filter = [
        'category', 'event_type', 'recurrence',
        'is_published', 'is_featured', 'is_cancelled'
    ]
    search_fields = ['title', 'description', 'venue']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Classification', {
            'fields': ('category', 'event_type')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date', 'is_all_day', 'recurrence')
        }),
        ('Location', {
            'fields': ('venue', 'address', 'map_url')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Additional Details', {
            'fields': ('dress_code', 'special_instructions', 'contact_info'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured', 'is_cancelled')
        }),
    )


@admin.register(TraditionalFestival)
class TraditionalFestivalAdmin(admin.ModelAdmin):
    """Admin for traditional festivals."""
    
    list_display = ['name', 'month_name', 'duration_days', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'typical_month']
    search_fields = ['name', 'description', 'history']
    prepopulated_fields = {'slug': ('name',)}
