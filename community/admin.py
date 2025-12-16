"""
Admin configuration for community app.
"""

from django.contrib import admin
from .models import ContactMessage, PublicFeedback, Newsletter


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin for contact messages."""
    
    list_display = [
        'subject', 'full_name', 'email', 'message_type',
        'is_read', 'is_responded', 'is_archived', 'created_at'
    ]
    list_filter = ['message_type', 'is_read', 'is_responded', 'is_archived', 'priority']
    search_fields = ['subject', 'full_name', 'email', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = [
        'full_name', 'email', 'phone', 'village', 'address',
        'subject', 'message_type', 'message', 'created_at'
    ]
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('full_name', 'email', 'phone', 'village', 'address')
        }),
        ('Message', {
            'fields': ('subject', 'message_type', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read', 'is_responded', 'is_archived', 'priority')
        }),
        ('Response', {
            'fields': ('response', 'responded_by', 'responded_at', 'admin_notes')
        }),
    )


@admin.register(PublicFeedback)
class PublicFeedbackAdmin(admin.ModelAdmin):
    """Admin for public feedback."""
    
    list_display = [
        'author_name', 'author_location', 'is_approved',
        'is_featured', 'created_at'
    ]
    list_filter = ['is_approved', 'is_featured']
    search_fields = ['author_name', 'content']
    date_hierarchy = 'created_at'
    
    actions = ['approve_feedback', 'feature_feedback']
    
    def approve_feedback(self, request, queryset):
        queryset.update(is_approved=True, approved_by=request.user)
    approve_feedback.short_description = "Approve selected feedback"
    
    def feature_feedback(self, request, queryset):
        queryset.update(is_featured=True)
    feature_feedback.short_description = "Feature selected feedback"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin for newsletter subscribers."""
    
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active']
    search_fields = ['email', 'name']
    date_hierarchy = 'subscribed_at'
