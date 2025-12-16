"""
User models for Ejeh Ankpa Palace Platform.
Implements role-based user system for traditional institution.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from cloudinary.models import CloudinaryField


class UserManager(BaseUserManager):
    """Custom user manager for the palace platform."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.EJEH)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with role-based access for the Ejeh Ankpa Palace.
    
    Roles:
    - EJEH: Traditional Ruler / Super Admin
    - PALACE_ADMIN: Palace Administrators
    - CHIEF: Council of Chiefs
    - MEMBER: Registered Community Members
    - VISITOR: Public Visitors (read-only)
    """
    
    class Role(models.TextChoices):
        EJEH = 'ejeh', 'Ejeh (Traditional Ruler)'
        PALACE_ADMIN = 'palace_admin', 'Palace Administrator'
        CHIEF = 'chief', 'Council of Chiefs'
        MEMBER = 'member', 'Community Member'
        VISITOR = 'visitor', 'Public Visitor'
    
    username = None
    email = models.EmailField('Email Address', unique=True)
    
    # Personal Information
    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100)
    phone_number = models.CharField('Phone Number', max_length=20, blank=True)
    
    # Profile
    profile_image = CloudinaryField('Profile Image', blank=True, null=True)
    bio = models.TextField('Biography', blank=True)
    
    # Role and Title
    role = models.CharField(
        'Role',
        max_length=20,
        choices=Role.choices,
        default=Role.VISITOR
    )
    traditional_title = models.CharField(
        'Traditional Title',
        max_length=100,
        blank=True,
        help_text='E.g., Chief, Elder, etc.'
    )
    
    # Community Information
    village = models.CharField('Village/Community', max_length=100, blank=True)
    ward = models.CharField('Ward', max_length=100, blank=True)
    
    # Status
    is_verified = models.BooleanField('Verified Member', default=False)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    last_updated = models.DateTimeField('Last Updated', auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        if self.traditional_title:
            return f"{self.traditional_title} {self.get_full_name()}"
        return self.get_full_name() or self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name
    
    @property
    def is_ejeh(self):
        return self.role == self.Role.EJEH
    
    @property
    def is_palace_admin(self):
        return self.role in [self.Role.EJEH, self.Role.PALACE_ADMIN]
    
    @property
    def is_chief(self):
        return self.role in [self.Role.EJEH, self.Role.PALACE_ADMIN, self.Role.CHIEF]
    
    @property
    def is_community_member(self):
        return self.role in [self.Role.EJEH, self.Role.PALACE_ADMIN, self.Role.CHIEF, self.Role.MEMBER]
    
    @property
    def can_manage_content(self):
        """Check if user can manage palace content."""
        return self.role in [self.Role.EJEH, self.Role.PALACE_ADMIN]
    
    @property
    def can_moderate(self):
        """Check if user can moderate community content."""
        return self.role in [self.Role.EJEH, self.Role.PALACE_ADMIN, self.Role.CHIEF]


class ChiefProfile(models.Model):
    """Extended profile for Council of Chiefs members."""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='chief_profile'
    )
    title = models.CharField('Chieftaincy Title', max_length=100)
    domain = models.CharField('Domain/Area of Authority', max_length=200, blank=True)
    installation_date = models.DateField('Installation Date', null=True, blank=True)
    is_active = models.BooleanField('Active Chief', default=True)
    order = models.PositiveIntegerField('Display Order', default=0)
    
    class Meta:
        verbose_name = 'Chief Profile'
        verbose_name_plural = 'Chief Profiles'
        ordering = ['order', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"
