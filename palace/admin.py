"""
Admin configuration for palace app.
"""

from django.contrib import admin
from .models import (
    EjehProfile, GalleryCategory, GalleryImage,
    HistoryArticle, TraditionalTitle, PalaceInfo
)


@admin.register(EjehProfile)
class EjehProfileAdmin(admin.ModelAdmin):
    """Admin for Ejeh profiles."""
    
    list_display = [
        'full_name', 'title', 'reign_status', 'reign_period',
        'is_active', 'display_order'
    ]
    list_filter = ['reign_status', 'is_active']
    search_fields = ['full_name', 'biography', 'achievements']
    ordering = ['-reign_status', 'display_order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'title', 'royal_title', 'reign_status', 'display_order', 'is_active')
        }),
        ('Images', {
            'fields': ('official_portrait', 'coronation_image')
        }),
        ('Reign Information', {
            'fields': ('reign_start', 'reign_end', 'reign_number')
        }),
        ('Biography', {
            'fields': ('biography', 'early_life', 'achievements', 'legacy', 'motto')
        }),
        ('Personal Details', {
            'fields': ('birth_date', 'birth_place', 'education', 'occupation_before_throne'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('hobbies', 'countries_visited'),
            'classes': ('collapse',)
        }),
        ('Honours', {
            'fields': ('full_title_and_honours',),
            'classes': ('collapse',)
        }),
    )


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    """Admin for gallery categories."""
    
    list_display = ['name', 'slug', 'display_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Admin for gallery images."""
    
    list_display = [
        'title', 'category', 'occasion_type', 'date_taken',
        'is_featured', 'is_published', 'view_count'
    ]
    list_filter = ['category', 'occasion_type', 'is_featured', 'is_published']
    search_fields = ['title', 'caption', 'location']
    date_hierarchy = 'date_taken'
    raw_id_fields = ['related_ejeh']
    
    fieldsets = (
        ('Image', {
            'fields': ('image', 'thumbnail')
        }),
        ('Information', {
            'fields': ('title', 'caption', 'category', 'occasion_type', 'related_ejeh')
        }),
        ('Details', {
            'fields': ('date_taken', 'location', 'photographer')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published')
        }),
    )


@admin.register(HistoryArticle)
class HistoryArticleAdmin(admin.ModelAdmin):
    """Admin for history articles."""
    
    list_display = [
        'title', 'article_type', 'author', 'is_published',
        'is_featured', 'view_count', 'created_at'
    ]
    list_filter = ['article_type', 'is_published', 'is_featured']
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'


@admin.register(TraditionalTitle)
class TraditionalTitleAdmin(admin.ModelAdmin):
    """Admin for traditional titles."""
    
    list_display = ['title_name', 'hierarchy_level', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title_name', 'description']
    ordering = ['hierarchy_level']


@admin.register(PalaceInfo)
class PalaceInfoAdmin(admin.ModelAdmin):
    """Admin for palace information."""
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('palace_name', 'tagline', 'about', 'mission', 'vision')
        }),
        ('Contact', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
        ('Branding', {
            'fields': ('logo', 'banner_image', 'favicon')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not PalaceInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
