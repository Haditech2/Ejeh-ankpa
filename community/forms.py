"""
Forms for community app.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML

from .models import ContactMessage, PublicFeedback, Newsletter


class ContactForm(forms.ModelForm):
    """Public contact form."""
    
    class Meta:
        model = ContactMessage
        fields = [
            'full_name', 'email', 'phone', 'village',
            'subject', 'message_type', 'message'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+234...'
            }),
            'village': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Village/Community'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your message'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your message here...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('phone', css_class='col-md-6'),
                Column('village', css_class='col-md-6'),
            ),
            Row(
                Column('subject', css_class='col-md-8'),
                Column('message_type', css_class='col-md-4'),
            ),
            'message',
            Submit('submit', 'Send Message', css_class='btn btn-primary btn-lg')
        )


class FeedbackForm(forms.ModelForm):
    """Form for submitting public feedback."""
    
    class Meta:
        model = PublicFeedback
        fields = ['author_name', 'author_title', 'author_location', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'author_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Title/Position (optional)'
            }),
            'author_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Location'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your feedback or testimonial...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('author_name', css_class='col-md-6'),
                Column('author_location', css_class='col-md-6'),
            ),
            'author_title',
            'content',
            HTML('<p class="text-muted small mb-3">Your feedback will be reviewed before being published.</p>'),
            Submit('submit', 'Submit Feedback', css_class='btn btn-primary')
        )


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form."""
    
    class Meta:
        model = Newsletter
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-md-8'),
                Column('name', css_class='col-md-4'),
            ),
            Submit('submit', 'Subscribe', css_class='btn btn-primary')
        )


class MessageResponseForm(forms.ModelForm):
    """Form for admin to respond to messages."""
    
    class Meta:
        model = ContactMessage
        fields = ['response', 'priority', 'admin_notes', 'is_read', 'is_responded', 'is_archived']
        widgets = {
            'response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Type your response here...'
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Internal notes (not visible to sender)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save & Send Response'))
