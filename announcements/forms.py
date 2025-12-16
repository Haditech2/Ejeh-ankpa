"""
Forms for announcements app.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column

from .models import Announcement, RoyalMessage, AnnouncementCategory


class AnnouncementForm(forms.ModelForm):
    """Form for creating/editing announcements."""
    
    class Meta:
        model = Announcement
        fields = [
            'title', 'slug', 'excerpt', 'content', 'category',
            'announcement_type', 'priority', 'featured_image', 'attachment',
            'is_published', 'is_featured', 'is_pinned', 'publish_date'
        ]
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 10}),
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Content',
                'title',
                'slug',
                'excerpt',
                'content',
            ),
            Fieldset(
                'Classification',
                Row(
                    Column('category', css_class='col-md-4'),
                    Column('announcement_type', css_class='col-md-4'),
                    Column('priority', css_class='col-md-4'),
                ),
            ),
            Fieldset(
                'Media',
                Row(
                    Column('featured_image', css_class='col-md-6'),
                    Column('attachment', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Publishing Options',
                Row(
                    Column('is_published', css_class='col-md-4'),
                    Column('is_featured', css_class='col-md-4'),
                    Column('is_pinned', css_class='col-md-4'),
                ),
                'publish_date',
            ),
            Submit('submit', 'Save Announcement', css_class='btn btn-primary')
        )


class RoyalMessageForm(forms.ModelForm):
    """Form for royal messages."""
    
    class Meta:
        model = RoyalMessage
        fields = [
            'title', 'message', 'signature_name', 'image',
            'video_url', 'is_published', 'is_featured', 'message_date'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 8}),
            'message_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Save Royal Message'))


class AnnouncementCategoryForm(forms.ModelForm):
    """Form for announcement categories."""
    
    class Meta:
        model = AnnouncementCategory
        fields = ['name', 'slug', 'description', 'color']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Category'))
