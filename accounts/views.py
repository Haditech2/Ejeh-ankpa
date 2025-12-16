"""
Views for user authentication and profile management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import User, ChiefProfile
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm


class CustomLoginView(LoginView):
    """Custom login view with styled form."""
    
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('palace:home')
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_full_name()}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    
    next_page = 'palace:home'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """User registration view."""
    
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('palace:home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Registration successful! Please log in with your credentials.'
        )
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    """View user profile."""
    
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile."""
    
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class ChiefListView(ListView):
    """Public view of Council of Chiefs."""
    
    model = ChiefProfile
    template_name = 'accounts/chiefs_list.html'
    context_object_name = 'chiefs'
    
    def get_queryset(self):
        return ChiefProfile.objects.filter(is_active=True).select_related('user')


class ChiefDetailView(DetailView):
    """Detailed view of a chief."""
    
    model = ChiefProfile
    template_name = 'accounts/chief_detail.html'
    context_object_name = 'chief'


class MemberListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """View for admins to see community members."""
    
    model = User
    template_name = 'accounts/members_list.html'
    context_object_name = 'members'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.can_manage_content
    
    def get_queryset(self):
        return User.objects.filter(role=User.Role.MEMBER).order_by('-date_joined')


@login_required
def dashboard_redirect(request):
    """Redirect users to appropriate dashboard based on role."""
    user = request.user
    
    if user.is_palace_admin:
        return redirect('accounts:admin_dashboard')
    elif user.is_chief:
        return redirect('accounts:chief_dashboard')
    else:
        return redirect('accounts:profile')


@login_required
def admin_dashboard(request):
    """Palace administration dashboard."""
    if not request.user.can_manage_content:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('palace:home')
    
    from announcements.models import Announcement
    from events.models import Event
    from community.models import ContactMessage
    from palace.models import GalleryImage
    
    context = {
        'total_users': User.objects.count(),
        'total_members': User.objects.filter(role=User.Role.MEMBER).count(),
        'pending_messages': ContactMessage.objects.filter(is_read=False).count(),
        'upcoming_events': Event.objects.filter(is_published=True).count(),
        'total_announcements': Announcement.objects.count(),
        'total_images': GalleryImage.objects.count(),
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def chief_dashboard(request):
    """Dashboard for Council of Chiefs."""
    if not request.user.is_chief:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('palace:home')
    
    from announcements.models import Announcement
    from events.models import Event
    
    context = {
        'recent_announcements': Announcement.objects.filter(is_published=True)[:5],
        'upcoming_events': Event.objects.filter(is_published=True)[:5],
    }
    
    return render(request, 'accounts/chief_dashboard.html', context)
