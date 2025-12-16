"""
Models for Royal Announcements and Palace News.
"""

from django.db import models
from django.urls import reverse
from django.conf import settings
from cloudinary.models import CloudinaryField


class AnnouncementCategory(models.Model):
    """Categories for announcements."""
    
    name = models.CharField('Category Name', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Description', blank=True)
    color = models.CharField(
        'Badge Color',
        max_length=20,
        default='primary',
        help_text='Bootstrap color class (primary, success, warning, danger, info)'
    )
    
    class Meta:
        verbose_name = 'Announcement Category'
        verbose_name_plural = 'Announcement Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Announcement(models.Model):
    """
    Royal Announcements and Palace News.
    Official communications from the palace.
    """
    
    class Priority(models.TextChoices):
        URGENT = 'urgent', 'Urgent'
        HIGH = 'high', 'High Priority'
        NORMAL = 'normal', 'Normal'
        LOW = 'low', 'Low Priority'
    
    class AnnouncementType(models.TextChoices):
        ROYAL_MESSAGE = 'royal_message', 'Royal Message from Ejeh'
        OFFICIAL = 'official', 'Official Announcement'
        COMMUNIQUE = 'communique', 'Communiqué'
        PRESS_RELEASE = 'press_release', 'Press Release'
        NOTICE = 'notice', 'Public Notice'
        EVENT = 'event', 'Event Announcement'
    
    # Content
    title = models.CharField('Title', max_length=300)
    slug = models.SlugField('Slug', unique=True, max_length=320)
    excerpt = models.TextField('Excerpt', max_length=500, blank=True)
    content = models.TextField('Content')
    
    # Classification
    category = models.ForeignKey(
        AnnouncementCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='announcements'
    )
    announcement_type = models.CharField(
        'Announcement Type',
        max_length=20,
        choices=AnnouncementType.choices,
        default=AnnouncementType.OFFICIAL
    )
    priority = models.CharField(
        'Priority',
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL
    )
    
    # Media
    featured_image = CloudinaryField('Featured Image', blank=True, null=True)
    attachment = CloudinaryField('Attachment (PDF)', blank=True, null=True)
    
    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements'
    )
    
    # Publishing
    is_published = models.BooleanField('Published', default=False)
    is_featured = models.BooleanField('Featured on Homepage', default=False)
    is_pinned = models.BooleanField('Pinned (Always Show First)', default=False)
    publish_date = models.DateTimeField('Publish Date', null=True, blank=True)
    
    # Metrics
    view_count = models.PositiveIntegerField('View Count', default=0)
    
    # Timestamps
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-is_pinned', '-publish_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('announcements:detail', kwargs={'slug': self.slug})
    
    @property
    def priority_badge_class(self):
        """Return Bootstrap badge class based on priority."""
        classes = {
            self.Priority.URGENT: 'danger',
            self.Priority.HIGH: 'warning',
            self.Priority.NORMAL: 'primary',
            self.Priority.LOW: 'secondary',
        }
        return classes.get(self.priority, 'primary')


class RoyalMessage(models.Model):
    """
    Special messages directly from the Ejeh.
    These are highlighted differently from regular announcements.
    """
    
    title = models.CharField('Title', max_length=200)
    message = models.TextField('Message')
    signature_name = models.CharField(
        'Signature Name',
        max_length=200,
        default='His Royal Majesty, The Ejeh of Ankpa'
    )
    
    # Media
    image = CloudinaryField('Image', blank=True, null=True)
    video_url = models.URLField('Video URL', blank=True)
    
    # Status
    is_published = models.BooleanField('Published', default=False)
    is_featured = models.BooleanField('Featured', default=False)
    
    # Timestamps
    message_date = models.DateField('Message Date')
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'Royal Message'
        verbose_name_plural = 'Royal Messages'
        ordering = ['-message_date']
    
    def __str__(self):
        return f"Royal Message: {self.title}"
    
    def get_absolute_url(self):
        return reverse('announcements:royal_message', kwargs={'pk': self.pk})
