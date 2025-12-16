"""
Models for Events and Ceremonial Calendar.
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone
from cloudinary.models import CloudinaryField


class EventCategory(models.Model):
    """Categories for events."""
    
    name = models.CharField('Category Name', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Description', blank=True)
    color = models.CharField(
        'Calendar Color',
        max_length=20,
        default='#8B4513',
        help_text='Hex color code for calendar display'
    )
    icon = models.CharField('Icon Class', max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Event Category'
        verbose_name_plural = 'Event Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Events and ceremonial occasions.
    Includes traditional festivals, palace meetings, and special occasions.
    """
    
    class EventType(models.TextChoices):
        FESTIVAL = 'festival', 'Traditional Festival'
        CEREMONY = 'ceremony', 'Ceremony'
        MEETING = 'meeting', 'Palace Meeting'
        CELEBRATION = 'celebration', 'Celebration'
        MEMORIAL = 'memorial', 'Memorial'
        OFFICIAL = 'official', 'Official Event'
        COMMUNITY = 'community', 'Community Event'
        OTHER = 'other', 'Other'
    
    class RecurrenceType(models.TextChoices):
        NONE = 'none', 'One-time Event'
        ANNUAL = 'annual', 'Annual'
        MONTHLY = 'monthly', 'Monthly'
        WEEKLY = 'weekly', 'Weekly'
    
    # Basic Information
    title = models.CharField('Event Title', max_length=200)
    slug = models.SlugField('Slug', unique=True, max_length=220)
    description = models.TextField('Description')
    short_description = models.TextField('Short Description', max_length=300, blank=True)
    
    # Classification
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    event_type = models.CharField(
        'Event Type',
        max_length=20,
        choices=EventType.choices,
        default=EventType.OTHER
    )
    
    # Date and Time
    start_date = models.DateTimeField('Start Date & Time')
    end_date = models.DateTimeField('End Date & Time', null=True, blank=True)
    is_all_day = models.BooleanField('All Day Event', default=False)
    
    # Recurrence
    recurrence = models.CharField(
        'Recurrence',
        max_length=10,
        choices=RecurrenceType.choices,
        default=RecurrenceType.NONE
    )
    
    # Location
    venue = models.CharField('Venue', max_length=200)
    address = models.TextField('Full Address', blank=True)
    map_url = models.URLField('Map URL', blank=True)
    
    # Media
    featured_image = CloudinaryField('Featured Image', blank=True, null=True)
    
    # Additional Details
    dress_code = models.CharField('Dress Code', max_length=200, blank=True)
    special_instructions = models.TextField('Special Instructions', blank=True)
    contact_info = models.TextField('Contact Information', blank=True)
    
    # Status
    is_published = models.BooleanField('Published', default=False)
    is_featured = models.BooleanField('Featured Event', default=False)
    is_cancelled = models.BooleanField('Cancelled', default=False)
    
    # Timestamps
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['start_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})
    
    @property
    def is_upcoming(self):
        """Check if event is in the future."""
        return self.start_date > timezone.now()
    
    @property
    def is_ongoing(self):
        """Check if event is currently happening."""
        now = timezone.now()
        if self.end_date:
            return self.start_date <= now <= self.end_date
        return self.start_date.date() == now.date()
    
    @property
    def is_past(self):
        """Check if event has ended."""
        if self.end_date:
            return self.end_date < timezone.now()
        return self.start_date < timezone.now()
    
    @property
    def days_until(self):
        """Return days until event starts."""
        if self.is_upcoming:
            delta = self.start_date - timezone.now()
            return delta.days
        return 0
    
    @property
    def duration(self):
        """Return event duration in hours."""
        if self.end_date:
            delta = self.end_date - self.start_date
            return delta.total_seconds() / 3600
        return None


class TraditionalFestival(models.Model):
    """
    Traditional festivals of Ankpa Kingdom.
    These are recurring cultural events with historical significance.
    """
    
    name = models.CharField('Festival Name', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Description')
    history = models.TextField('History & Significance', blank=True)
    
    # Timing
    typical_month = models.PositiveIntegerField(
        'Typical Month',
        choices=[(i, i) for i in range(1, 13)],
        null=True,
        blank=True,
        help_text='Month when this festival typically occurs'
    )
    duration_days = models.PositiveIntegerField('Duration (Days)', default=1)
    
    # Media
    featured_image = CloudinaryField('Featured Image', blank=True, null=True)
    
    # Activities
    activities = models.TextField('Activities & Rituals', blank=True)
    traditional_attire = models.TextField('Traditional Attire', blank=True)
    food_and_drinks = models.TextField('Traditional Food & Drinks', blank=True)
    
    # Status
    is_active = models.BooleanField('Still Celebrated', default=True)
    is_featured = models.BooleanField('Featured Festival', default=False)
    
    # Timestamps
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'Traditional Festival'
        verbose_name_plural = 'Traditional Festivals'
        ordering = ['typical_month', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('events:festival_detail', kwargs={'slug': self.slug})
    
    @property
    def month_name(self):
        """Return the month name."""
        import calendar
        if self.typical_month:
            return calendar.month_name[self.typical_month]
        return 'Various'
