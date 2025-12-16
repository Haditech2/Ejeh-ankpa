"""
Views for Ejeh Ankpa Palace main app.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from .models import (
    EjehProfile, GalleryImage, GalleryCategory,
    HistoryArticle, TraditionalTitle, PalaceInfo
)
from .forms import (
    EjehProfileForm, GalleryImageForm, GalleryCategoryForm,
    HistoryArticleForm, PalaceInfoForm
)


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for views that require palace admin access."""
    
    def test_func(self):
        return self.request.user.can_manage_content


# ============== HOME PAGE ==============

class HomeView(TemplateView):
    """Palace homepage."""
    
    template_name = 'palace/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import here to avoid circular imports
        from announcements.models import Announcement
        from events.models import Event
        
        context['present_ejeh'] = EjehProfile.get_present_ejeh()
        context['featured_images'] = GalleryImage.objects.filter(
            is_published=True, is_featured=True
        )[:6]
        context['recent_announcements'] = Announcement.objects.filter(
            is_published=True
        )[:3]
        context['upcoming_events'] = Event.objects.filter(
            is_published=True
        ).order_by('start_date')[:4]
        context['featured_articles'] = HistoryArticle.objects.filter(
            is_published=True, is_featured=True
        )[:3]
        
        return context


class AboutView(TemplateView):
    """About the palace page."""
    
    template_name = 'palace/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['palace_info'] = PalaceInfo.get_instance()
        context['traditional_titles'] = TraditionalTitle.objects.filter(is_active=True)
        return context


# ============== EJEH PROFILES ==============

class EjehListView(ListView):
    """List all Ejeh profiles (past and present)."""
    
    model = EjehProfile
    template_name = 'palace/ejeh_list.html'
    context_object_name = 'ejehs'
    
    def get_queryset(self):
        return EjehProfile.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['present_ejeh'] = EjehProfile.get_present_ejeh()
        context['past_ejehs'] = EjehProfile.get_past_ejehs()
        return context


class EjehDetailView(DetailView):
    """Detail view for an Ejeh profile."""
    
    model = EjehProfile
    template_name = 'palace/ejeh_detail.html'
    context_object_name = 'ejeh'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related gallery images
        context['gallery_images'] = GalleryImage.objects.filter(
            related_ejeh=self.object, is_published=True
        )[:8]
        return context


class PresentEjehView(DetailView):
    """View for the present Ejeh."""
    
    model = EjehProfile
    template_name = 'palace/present_ejeh.html'
    context_object_name = 'ejeh'
    
    def get_object(self):
        return get_object_or_404(
            EjehProfile,
            reign_status=EjehProfile.ReignStatus.PRESENT,
            is_active=True
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images'] = GalleryImage.objects.filter(
            related_ejeh=self.object, is_published=True
        )[:8]
        return context


class PastEjehsView(ListView):
    """List past Ejeh profiles."""
    
    model = EjehProfile
    template_name = 'palace/past_ejehs.html'
    context_object_name = 'past_ejehs'
    
    def get_queryset(self):
        return EjehProfile.get_past_ejehs()


# ============== ROYAL GALLERY ==============

class GalleryView(ListView):
    """Main gallery view."""
    
    model = GalleryImage
    template_name = 'palace/gallery.html'
    context_object_name = 'images'
    paginate_by = 24
    
    def get_queryset(self):
        queryset = GalleryImage.objects.filter(is_published=True)
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by occasion type
        occasion = self.request.GET.get('occasion')
        if occasion:
            queryset = queryset.filter(occasion_type=occasion)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(caption__icontains=search) |
                Q(location__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GalleryCategory.objects.filter(is_active=True)
        context['occasion_types'] = GalleryImage.OccasionType.choices
        context['current_category'] = self.request.GET.get('category', '')
        context['current_occasion'] = self.request.GET.get('occasion', '')
        return context


class GalleryCategoryView(ListView):
    """Gallery filtered by category."""
    
    model = GalleryImage
    template_name = 'palace/gallery_category.html'
    context_object_name = 'images'
    paginate_by = 24
    
    def get_queryset(self):
        self.category = get_object_or_404(GalleryCategory, slug=self.kwargs['slug'])
        return GalleryImage.objects.filter(
            category=self.category, is_published=True
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = GalleryCategory.objects.filter(is_active=True)
        return context


class GalleryImageDetailView(DetailView):
    """Detail view for a gallery image."""
    
    model = GalleryImage
    template_name = 'palace/gallery_image.html'
    context_object_name = 'image'
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related images
        context['related_images'] = GalleryImage.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(pk=self.object.pk)[:4]
        return context


# ============== HISTORY & CULTURE ==============

class HistoryListView(ListView):
    """List history and culture articles."""
    
    model = HistoryArticle
    template_name = 'palace/history_list.html'
    context_object_name = 'articles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = HistoryArticle.objects.filter(is_published=True)
        
        # Filter by type
        article_type = self.request.GET.get('type')
        if article_type:
            queryset = queryset.filter(article_type=article_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_types'] = HistoryArticle.ArticleType.choices
        context['current_type'] = self.request.GET.get('type', '')
        return context


class HistoryDetailView(DetailView):
    """Detail view for a history article."""
    
    model = HistoryArticle
    template_name = 'palace/history_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_articles'] = HistoryArticle.objects.filter(
            is_published=True,
            article_type=self.object.article_type
        ).exclude(pk=self.object.pk)[:3]
        return context


class TraditionalTitlesView(ListView):
    """List traditional titles."""
    
    model = TraditionalTitle
    template_name = 'palace/traditional_titles.html'
    context_object_name = 'titles'
    
    def get_queryset(self):
        return TraditionalTitle.objects.filter(is_active=True)


# ============== ADMIN VIEWS ==============

class EjehCreateView(AdminRequiredMixin, CreateView):
    """Create a new Ejeh profile."""
    
    model = EjehProfile
    form_class = EjehProfileForm
    template_name = 'palace/admin/ejeh_form.html'
    success_url = reverse_lazy('palace:ejeh_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ejeh profile created successfully.')
        return super().form_valid(form)


class EjehUpdateView(AdminRequiredMixin, UpdateView):
    """Update an Ejeh profile."""
    
    model = EjehProfile
    form_class = EjehProfileForm
    template_name = 'palace/admin/ejeh_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Ejeh profile updated successfully.')
        return super().form_valid(form)


class EjehDeleteView(AdminRequiredMixin, DeleteView):
    """Delete an Ejeh profile."""
    
    model = EjehProfile
    template_name = 'palace/admin/ejeh_confirm_delete.html'
    success_url = reverse_lazy('palace:ejeh_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ejeh profile deleted successfully.')
        return super().delete(request, *args, **kwargs)


class GalleryUploadView(AdminRequiredMixin, CreateView):
    """Upload a new gallery image."""
    
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'palace/admin/gallery_upload.html'
    success_url = reverse_lazy('palace:gallery')
    
    def form_valid(self, form):
        messages.success(self.request, 'Image uploaded successfully.')
        return super().form_valid(form)


class GalleryImageUpdateView(AdminRequiredMixin, UpdateView):
    """Update a gallery image."""
    
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'palace/admin/gallery_upload.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Image updated successfully.')
        return super().form_valid(form)


class GalleryImageDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a gallery image."""
    
    model = GalleryImage
    template_name = 'palace/admin/gallery_confirm_delete.html'
    success_url = reverse_lazy('palace:gallery')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Image deleted successfully.')
        return super().delete(request, *args, **kwargs)


class HistoryCreateView(AdminRequiredMixin, CreateView):
    """Create a history article."""
    
    model = HistoryArticle
    form_class = HistoryArticleForm
    template_name = 'palace/admin/history_form.html'
    success_url = reverse_lazy('palace:history_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Article created successfully.')
        return super().form_valid(form)


class HistoryUpdateView(AdminRequiredMixin, UpdateView):
    """Update a history article."""
    
    model = HistoryArticle
    form_class = HistoryArticleForm
    template_name = 'palace/admin/history_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Article updated successfully.')
        return super().form_valid(form)


class HistoryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a history article."""
    
    model = HistoryArticle
    template_name = 'palace/admin/history_confirm_delete.html'
    success_url = reverse_lazy('palace:history_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Article deleted successfully.')
        return super().delete(request, *args, **kwargs)


class PalaceSettingsView(AdminRequiredMixin, UpdateView):
    """Update palace settings."""
    
    model = PalaceInfo
    form_class = PalaceInfoForm
    template_name = 'palace/admin/palace_settings.html'
    success_url = reverse_lazy('accounts:admin_dashboard')
    
    def get_object(self):
        return PalaceInfo.get_instance()
    
    def form_valid(self, form):
        messages.success(self.request, 'Palace settings updated successfully.')
        return super().form_valid(form)
