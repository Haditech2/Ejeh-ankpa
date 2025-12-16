"""
Models for Community Engagement - Contact and Feedback.
"""

from django.db import models
from django.conf import settings


class ContactMessage(models.Model):
    """
    Contact messages from the public.
    Allows visitors to send messages to the palace.
    """
    
    class MessageType(models.TextChoices):
        GENERAL = 'general', 'General Inquiry'
        REQUEST = 'request', 'Request/Appeal'
        FEEDBACK = 'feedback', 'Feedback'
        COMPLAINT = 'complaint', 'Complaint'
        SUGGESTION = 'suggestion', 'Suggestion'
        MEDIA = 'media', 'Media/Press Inquiry'
        OTHER = 'other', 'Other'
    
    class Priority(models.TextChoices):
        HIGH = 'high', 'High Priority'
        NORMAL = 'normal', 'Normal'
        LOW = 'low', 'Low Priority'
    
    # Sender Information
    full_name = models.CharField('Full Name', max_length=200)
    email = models.EmailField('Email Address')
    phone = models.CharField('Phone Number', max_length=20, blank=True)
    
    # Location
    village = models.CharField('Village/Community', max_length=100, blank=True)
    address = models.TextField('Address', blank=True)
    
    # Message
    subject = models.CharField('Subject', max_length=300)
    message_type = models.CharField(
        'Message Type',
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.GENERAL
    )
    message = models.TextField('Message')
    
    # Status
    is_read = models.BooleanField('Read', default=False)
    is_responded = models.BooleanField('Responded', default=False)
    is_archived = models.BooleanField('Archived', default=False)
    priority = models.CharField(
        'Priority',
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL
    )
    
    # Response
    response = models.TextField('Response', blank=True)
    responded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responded_messages'
    )
    responded_at = models.DateTimeField('Responded At', null=True, blank=True)
    
    # Admin notes
    admin_notes = models.TextField('Admin Notes', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField('Received', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.full_name}"
    
    @property
    def status_badge(self):
        """Return status for display."""
        if self.is_archived:
            return 'archived'
        elif self.is_responded:
            return 'responded'
        elif self.is_read:
            return 'read'
        return 'new'


class PublicFeedback(models.Model):
    """
    Public feedback/testimonials that can be displayed on the website.
    These are moderated before being shown publicly.
    """
    
    # Author
    author_name = models.CharField('Author Name', max_length=200)
    author_title = models.CharField(
        'Title/Position',
        max_length=100,
        blank=True,
        help_text='E.g., Community Leader, Elder, etc.'
    )
    author_location = models.CharField('Location', max_length=100, blank=True)
    
    # Content
    content = models.TextField('Feedback Content', max_length=1000)
    
    # Moderation
    is_approved = models.BooleanField('Approved', default=False)
    is_featured = models.BooleanField('Featured', default=False)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_feedback'
    )
    approved_at = models.DateTimeField('Approved At', null=True, blank=True)
    
    # Source
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedback_submissions'
    )
    
    # Timestamps
    created_at = models.DateTimeField('Submitted', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'Public Feedback'
        verbose_name_plural = 'Public Feedback'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback from {self.author_name}"


class Newsletter(models.Model):
    """Newsletter subscription model."""
    
    email = models.EmailField('Email Address', unique=True)
    name = models.CharField('Name', max_length=100, blank=True)
    is_active = models.BooleanField('Active', default=True)
    subscribed_at = models.DateTimeField('Subscribed', auto_now_add=True)
    unsubscribed_at = models.DateTimeField('Unsubscribed', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
