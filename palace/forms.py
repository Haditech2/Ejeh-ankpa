"""
Forms for palace app.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column

from .models import EjehProfile, GalleryImage, GalleryCategory, HistoryArticle, PalaceInfo


class EjehProfileForm(forms.ModelForm):
    """Form for creating/editing Ejeh profiles."""
    
    class Meta:
        model = EjehProfile
        fields = [
            'full_name', 'title', 'reign_status', 'official_portrait',
            'coronation_image', 'reign_start', 'reign_end', 'reign_number',
            'biography', 'early_life', 'achievements', 'legacy',
            'birth_date', 'birth_place', 'education', 'occupation_before_throne',
            'full_title_and_honours', 'is_active', 'display_order'
        ]
        widgets = {
            'reign_start': forms.DateInput(attrs={'type': 'date'}),
            'reign_end': forms.DateInput(attrs={'type': 'date'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'biography': forms.Textarea(attrs={'rows': 5}),
            'achievements': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Save Profile'))


class GalleryImageForm(forms.ModelForm):
    """Form for uploading gallery images."""
    
    class Meta:
        model = GalleryImage
        fields = [
            'image', 'title', 'caption', 'category', 'occasion_type',
            'related_ejeh', 'date_taken', 'location', 'photographer',
            'is_featured', 'is_published'
        ]
        widgets = {
            'date_taken': forms.DateInput(attrs={'type': 'date'}),
            'caption': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Upload Image'))


class GalleryCategoryForm(forms.ModelForm):
    """Form for gallery categories."""
    
    class Meta:
        model = GalleryCategory
        fields = ['name', 'slug', 'description', 'icon', 'display_order', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Category'))


class HistoryArticleForm(forms.ModelForm):
    """Form for history and culture articles."""
    
    class Meta:
        model = HistoryArticle
        fields = [
            'title', 'slug', 'excerpt', 'content', 'featured_image',
            'video_url', 'article_type', 'author', 'is_published', 'is_featured'
        ]
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Save Article'))


class PalaceInfoForm(forms.ModelForm):
    """Form for palace settings."""
    
    class Meta:
        model = PalaceInfo
        fields = '__all__'
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
            'mission': forms.Textarea(attrs={'rows': 3}),
            'vision': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Save Settings'))
