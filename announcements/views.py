"""
Views for announcements app.
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q

from .models import Announcement, RoyalMessage, AnnouncementCategory
from .forms import AnnouncementForm, RoyalMessageForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for views that require palace admin access."""
    
    def test_func(self):
        return self.request.user.can_manage_content


# ============== PUBLIC VIEWS ==============

class AnnouncementListView(ListView):
    """List all published announcements."""
    
    model = Announcement
    template_name = 'announcements/list.html'
    context_object_name = 'announcements'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Announcement.objects.filter(is_published=True)
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by type
        announcement_type = self.request.GET.get('type')
        if announcement_type:
            queryset = queryset.filter(announcement_type=announcement_type)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = AnnouncementCategory.objects.all()
        context['announcement_types'] = Announcement.AnnouncementType.choices
        context['pinned_announcements'] = Announcement.objects.filter(
            is_published=True, is_pinned=True
        )[:3]
        context['current_category'] = self.request.GET.get('category', '')
        context['current_type'] = self.request.GET.get('type', '')
        return context


class AnnouncementDetailView(DetailView):
    """Detail view for an announcement."""
    
    model = Announcement
    template_name = 'announcements/detail.html'
    context_object_name = 'announcement'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.can_manage_content:
            return Announcement.objects.all()
        return Announcement.objects.filter(is_published=True)
    
    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_announcements'] = Announcement.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context


class RoyalMessageListView(ListView):
    """List royal messages."""
    
    model = RoyalMessage
    template_name = 'announcements/royal_messages.html'
    context_object_name = 'messages'
    paginate_by = 10
    
    def get_queryset(self):
        return RoyalMessage.objects.filter(is_published=True)


class RoyalMessageDetailView(DetailView):
    """Detail view for a royal message."""
    
    model = RoyalMessage
    template_name = 'announcements/royal_message_detail.html'
    context_object_name = 'royal_message'
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.can_manage_content:
            return RoyalMessage.objects.all()
        return RoyalMessage.objects.filter(is_published=True)


# ============== ADMIN VIEWS ==============

class AnnouncementCreateView(AdminRequiredMixin, CreateView):
    """Create a new announcement."""
    
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/admin/announcement_form.html'
    success_url = reverse_lazy('announcements:list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.is_published and not form.instance.publish_date:
            form.instance.publish_date = timezone.now()
        messages.success(self.request, 'Announcement created successfully.')
        return super().form_valid(form)


class AnnouncementUpdateView(AdminRequiredMixin, UpdateView):
    """Update an announcement."""
    
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/admin/announcement_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def form_valid(self, form):
        messages.success(self.request, 'Announcement updated successfully.')
        return super().form_valid(form)


class AnnouncementDeleteView(AdminRequiredMixin, DeleteView):
    """Delete an announcement."""
    
    model = Announcement
    template_name = 'announcements/admin/announcement_confirm_delete.html'
    success_url = reverse_lazy('announcements:list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Announcement deleted successfully.')
        return super().delete(request, *args, **kwargs)


class RoyalMessageCreateView(AdminRequiredMixin, CreateView):
    """Create a royal message."""
    
    model = RoyalMessage
    form_class = RoyalMessageForm
    template_name = 'announcements/admin/royal_message_form.html'
    success_url = reverse_lazy('announcements:royal_messages')
    
    def form_valid(self, form):
        messages.success(self.request, 'Royal message created successfully.')
        return super().form_valid(form)


class RoyalMessageUpdateView(AdminRequiredMixin, UpdateView):
    """Update a royal message."""
    
    model = RoyalMessage
    form_class = RoyalMessageForm
    template_name = 'announcements/admin/royal_message_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Royal message updated successfully.')
        return super().form_valid(form)


class RoyalMessageDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a royal message."""
    
    model = RoyalMessage
    template_name = 'announcements/admin/royal_message_confirm_delete.html'
    success_url = reverse_lazy('announcements:royal_messages')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Royal message deleted successfully.')
        return super().delete(request, *args, **kwargs)


class AnnouncementManageListView(AdminRequiredMixin, ListView):
    """Admin list view for managing announcements."""
    
    model = Announcement
    template_name = 'announcements/admin/manage_list.html'
    context_object_name = 'announcements'
    paginate_by = 20
    
    def get_queryset(self):
        return Announcement.objects.all().order_by('-created_at')
