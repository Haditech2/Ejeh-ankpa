"""
Forms for events app.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column

from .models import Event, EventCategory, TraditionalFestival


class EventForm(forms.ModelForm):
    """Form for creating/editing events."""
    
    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'description', 'short_description',
            'category', 'event_type', 'start_date', 'end_date', 'is_all_day',
            'recurrence', 'venue', 'address', 'map_url', 'featured_image',
            'dress_code', 'special_instructions', 'contact_info',
            'is_published', 'is_featured', 'is_cancelled'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'special_instructions': forms.Textarea(attrs={'rows': 3}),
            'contact_info': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Basic Information',
                'title',
                'slug',
                'short_description',
                'description',
            ),
            Fieldset(
                'Classification',
                Row(
                    Column('category', css_class='col-md-6'),
                    Column('event_type', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Date & Time',
                Row(
                    Column('start_date', css_class='col-md-4'),
                    Column('end_date', css_class='col-md-4'),
                    Column('is_all_day', css_class='col-md-4'),
                ),
                'recurrence',
            ),
            Fieldset(
                'Location',
                'venue',
                'address',
                'map_url',
            ),
            Fieldset(
                'Media & Details',
                'featured_image',
                'dress_code',
                'special_instructions',
                'contact_info',
            ),
            Fieldset(
                'Publishing',
                Row(
                    Column('is_published', css_class='col-md-4'),
                    Column('is_featured', css_class='col-md-4'),
                    Column('is_cancelled', css_class='col-md-4'),
                ),
            ),
            Submit('submit', 'Save Event', css_class='btn btn-primary')
        )


class EventCategoryForm(forms.ModelForm):
    """Form for event categories."""
    
    class Meta:
        model = EventCategory
        fields = ['name', 'slug', 'description', 'color', 'icon']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Category'))


class TraditionalFestivalForm(forms.ModelForm):
    """Form for traditional festivals."""
    
    class Meta:
        model = TraditionalFestival
        fields = [
            'name', 'slug', 'description', 'history', 'typical_month',
            'duration_days', 'featured_image', 'activities', 'traditional_attire',
            'food_and_drinks', 'is_active', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'history': forms.Textarea(attrs={'rows': 4}),
            'activities': forms.Textarea(attrs={'rows': 3}),
            'traditional_attire': forms.Textarea(attrs={'rows': 2}),
            'food_and_drinks': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Save Festival'))
