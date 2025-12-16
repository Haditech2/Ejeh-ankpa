"""
Forms for user authentication and registration.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    """Custom login form with styled fields."""
    
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Sign In', css_class='btn btn-primary w-100 mt-3')
        )


class UserRegistrationForm(UserCreationForm):
    """Registration form for community members."""
    
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone_number',
            'village', 'ward', 'password1', 'password2'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+234...'
            }),
            'village': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Village/Community'
            }),
            'ward': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Ward'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Personal Information',
                Row(
                    Column('first_name', css_class='col-md-6'),
                    Column('last_name', css_class='col-md-6'),
                ),
                'email',
                'phone_number',
            ),
            Fieldset(
                'Community Information',
                Row(
                    Column('village', css_class='col-md-6'),
                    Column('ward', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Security',
                'password1',
                'password2',
            ),
            Submit('submit', 'Register as Community Member', css_class='btn btn-primary w-100 mt-3')
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.MEMBER
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for users to update their profile."""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number',
            'profile_image', 'bio', 'village', 'ward'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'phone_number',
            'profile_image',
            'bio',
            Row(
                Column('village', css_class='col-md-6'),
                Column('ward', css_class='col-md-6'),
            ),
            Submit('submit', 'Update Profile', css_class='btn btn-primary mt-3')
        )


class AdminUserForm(forms.ModelForm):
    """Form for admins to manage user roles."""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'role', 'traditional_title', 'is_verified', 'is_active'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Changes'))
