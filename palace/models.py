"""
Models for Ejeh Ankpa Palace - Profiles, Gallery, History, and Culture.
"""

from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField


class EjehProfile(models.Model):
    """
    Profile model for Past and Present Ejeh of Ankpa.
    Contains biographical information, reign details, and achievements.
    """
    
    class ReignStatus(models.TextChoices):
        PRESENT = 'present', 'Present Ejeh'
        PAST = 'past', 'Past Ejeh'
    
    # Basic Information
    full_name = models.CharField('Full Name', max_length=200)
    title = models.CharField(
        'Royal Title',
        max_length=100,
        default='His Royal Majesty'
    )
    reign_status = models.CharField(
        'Reign Status',
        max_length=10,
        choices=ReignStatus.choices,
        default=ReignStatus.PAST
    )
    
    # Portrait and Images
    official_portrait = CloudinaryField(
        'Official Portrait',
        blank=True,
        null=True
    )
    coronation_image = CloudinaryField(
        'Coronation Image',
        blank=True,
        null=True
    )
    
    # Reign Information
    reign_start = models.DateField('Reign Start Date', null=True, blank=True)
    reign_end = models.DateField('Reign End Date', null=True, blank=True)
    reign_number = models.PositiveIntegerField(
        'Reign Number',
        help_text='Order in succession (e.g., 1st, 2nd, etc.)',
        null=True,
        blank=True
    )
    
    # Biography
    biography = models.TextField('Biography', blank=True)
    early_life = models.TextField('Early Life', blank=True)
    achievements = models.TextField('Achievements & Contributions', blank=True)
    legacy = models.TextField('Legacy', blank=True)
    
    # Additional Details
    birth_date = models.DateField('Date of Birth', null=True, blank=True)
    birth_place = models.CharField('Place of Birth', max_length=200, blank=True)
    education = models.TextField('Education', blank=True)
    occupation_before_throne = models.TextField(
        'Occupation Before Throne',
        blank=True,
        help_text='Professional career before ascending the throne'
    )
    
    # Royal Titles and Honours
    full_title_and_honours = models.TextField(
        'Full Title and Honours',
        blank=True,
        help_text='Complete list of royal titles and honours'
    )
    royal_title = models.CharField(
        'Royal Title Name',
        max_length=100,
        blank=True,
        help_text='E.g., Ejeh Ankpa IV'
    )
    motto = models.TextField('Royal Motto', blank=True)
    hobbies = models.TextField('Hobbies & Interests', blank=True)
    countries_visited = models.TextField('Countries Visited', blank=True)
    
    # Meta
    is_active = models.BooleanField('Active Profile', default=True)
    display_order = models.PositiveIntegerField('Display Order', default=0)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'Ejeh Profile'
        verbose_name_plural = 'Ejeh Profiles'
        ordering = ['-reign_status', 'display_order', '-reign_start']
    
    def __str__(self):
        status = "Present" if self.reign_status == self.ReignStatus.PRESENT else "Past"
        return f"{self.title} {self.full_name} ({status} Ejeh)"
    
    def get_absolute_url(self):
        return reverse('palace:ejeh_detail', kwargs={'pk': self.pk})
    
    @property
    def reign_period(self):
        """Return formatted reign period."""
        if self.reign_start and self.reign_end:
            return f"{self.reign_start.year} - {self.reign_end.year}"
        elif self.reign_start:
            return f"{self.reign_start.year} - Present"
        return "Unknown"
    
    @classmethod
    def get_present_ejeh(cls):
        """Return the current Ejeh profile."""
        return cls.objects.filter(
            reign_status=cls.ReignStatus.PRESENT,
            is_active=True
        ).first()
    
    @classmethod
    def get_past_ejehs(cls):
        """Return all past Ejeh profiles."""
        return cls.objects.filter(
            reign_status=cls.ReignStatus.PAST,
            is_active=True
        ).order_by('-reign_start')


class GalleryCategory(models.Model):
    """Categories for organizing gallery images."""
    
    name = models.CharField('Category Name', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Description', blank=True)
    icon = models.CharField(
        'Icon Class',
        max_length=50,
        blank=True,
        help_text='Bootstrap icon class (e.g., bi-crown)'
    )
    display_order = models.PositiveIntegerField('Display Order', default=0)
    is_active = models.BooleanField('Active', default=True)
    
    class Meta:
        verbose_name = 'Gallery Category'
        verbose_name_plural = 'Gallery Categories'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('palace:gallery_category', kwargs={'slug': self.slug})


class GalleryImage(models.Model):
    """
    Royal Image Gallery for palace occasions and events.
    Stores images of coronations, festivals, ceremonies, and community events.
    """
    
    class OccasionType(models.TextChoices):
        CORONATION = 'coronation', 'Coronation'
        FESTIVAL = 'festival', 'Festival & Ceremony'
        PALACE = 'palace', 'Palace Occasion'
        COMMUNITY = 'community', 'Community Event'
        OFFICIAL = 'official', 'Official Visit'
        CULTURAL = 'cultural', 'Cultural Event'
        OTHER = 'other', 'Other'
    
    # Image
    image = CloudinaryField('Image')
    thumbnail = CloudinaryField('Thumbnail', blank=True, null=True)
    
    # Information
    title = models.CharField('Title', max_length=200)
    caption = models.TextField('Caption', blank=True)
    
    # Classification
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images'
    )
    occasion_type = models.CharField(
        'Occasion Type',
        max_length=20,
        choices=OccasionType.choices,
        default=OccasionType.OTHER
    )
    
    # Related Ejeh (optional)
    related_ejeh = models.ForeignKey(
        EjehProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gallery_images'
    )
    
    # Date and Location
    date_taken = models.DateField('Date Taken', null=True, blank=True)
    location = models.CharField('Location', max_length=200, blank=True)
    
    # Metadata
    photographer = models.CharField('Photographer', max_length=100, blank=True)
    is_featured = models.BooleanField('Featured Image', default=False)
    is_published = models.BooleanField('Published', default=True)
    view_count = models.PositiveIntegerField('View Count', default=0)
    
    # Timestamps
    created_at = models.DateTimeField('Uploaded', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['-date_taken', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('palace:gallery_image', kwargs={'pk': self.pk})


class HistoryArticle(models.Model):
    """
    Historical content about Ankpa Kingdom, traditions, and culture.
    """
    
    class ArticleType(models.TextChoices):
        HISTORY = 'history', 'Kingdom History'
        TRADITION = 'tradition', 'Traditional Practices'
        CULTURE = 'culture', 'Cultural Heritage'
        TITLE = 'title', 'Traditional Titles'
        FESTIVAL = 'festival', 'Festivals'
        LANGUAGE = 'language', 'Language & Arts'
    
    # Content
    title = models.CharField('Title', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    excerpt = models.TextField('Excerpt', max_length=500, blank=True)
    content = models.TextField('Content')
    
    # Media
    featured_image = CloudinaryField('Featured Image', blank=True, null=True)
    video_url = models.URLField('Video URL', blank=True)
    
    # Classification
    article_type = models.CharField(
        'Article Type',
        max_length=20,
        choices=ArticleType.choices,
        default=ArticleType.HISTORY
    )
    
    # Meta
    author = models.CharField('Author', max_length=100, blank=True)
    is_published = models.BooleanField('Published', default=True)
    is_featured = models.BooleanField('Featured', default=False)
    view_count = models.PositiveIntegerField('View Count', default=0)
    
    # Timestamps
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    
    class Meta:
        verbose_name = 'History & Culture Article'
        verbose_name_plural = 'History & Culture Articles'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('palace:history_detail', kwargs={'slug': self.slug})


class TraditionalTitle(models.Model):
    """Traditional titles and hierarchy in the Ankpa Kingdom."""
    
    title_name = models.CharField('Title Name', max_length=100)
    description = models.TextField('Description')
    hierarchy_level = models.PositiveIntegerField(
        'Hierarchy Level',
        help_text='1 = Highest (Ejeh), higher numbers = lower in hierarchy'
    )
    responsibilities = models.TextField('Responsibilities', blank=True)
    requirements = models.TextField('Requirements for Title', blank=True)
    is_active = models.BooleanField('Active Title', default=True)
    
    class Meta:
        verbose_name = 'Traditional Title'
        verbose_name_plural = 'Traditional Titles'
        ordering = ['hierarchy_level', 'title_name']
    
    def __str__(self):
        return self.title_name


class PalaceInfo(models.Model):
    """
    Singleton model for palace general information.
    """
    
    # Palace Information
    palace_name = models.CharField(
        'Palace Name',
        max_length=200,
        default='Ejeh Ankpa Palace'
    )
    tagline = models.CharField(
        'Tagline',
        max_length=300,
        default='The Traditional Institution of the Ejeh of Ankpa'
    )
    about = models.TextField('About the Palace', blank=True)
    mission = models.TextField('Mission Statement', blank=True)
    vision = models.TextField('Vision Statement', blank=True)
    
    # Contact Information
    address = models.TextField('Palace Address', blank=True)
    phone = models.CharField('Phone Number', max_length=20, blank=True)
    email = models.EmailField('Email Address', blank=True)
    
    # Social Media
    facebook_url = models.URLField('Facebook URL', blank=True)
    twitter_url = models.URLField('Twitter URL', blank=True)
    instagram_url = models.URLField('Instagram URL', blank=True)
    youtube_url = models.URLField('YouTube URL', blank=True)
    
    # Branding
    logo = CloudinaryField('Palace Logo', blank=True, null=True)
    banner_image = CloudinaryField('Banner Image', blank=True, null=True)
    favicon = CloudinaryField('Favicon', blank=True, null=True)
    
    # SEO
    meta_description = models.TextField('Meta Description', max_length=160, blank=True)
    meta_keywords = models.CharField('Meta Keywords', max_length=255, blank=True)
    
    class Meta:
        verbose_name = 'Palace Information'
        verbose_name_plural = 'Palace Information'
    
    def __str__(self):
        return self.palace_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
