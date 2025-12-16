"""
Views for events app.
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
import json

from .models import Event, EventCategory, TraditionalFestival
from .forms import EventForm, TraditionalFestivalForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for views that require palace admin access."""
    
    def test_func(self):
        return self.request.user.can_manage_content


# ============== PUBLIC VIEWS ==============

class EventListView(ListView):
    """List upcoming events."""
    
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Event.objects.filter(
            is_published=True,
            is_cancelled=False
        )
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by type
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Filter by time frame
        time_frame = self.request.GET.get('time', 'upcoming')
        now = timezone.now()
        
        if time_frame == 'upcoming':
            queryset = queryset.filter(start_date__gte=now)
        elif time_frame == 'past':
            queryset = queryset.filter(start_date__lt=now)
        elif time_frame == 'today':
            queryset = queryset.filter(start_date__date=now.date())
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(venue__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        context['event_types'] = Event.EventType.choices
        context['current_category'] = self.request.GET.get('category', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_time'] = self.request.GET.get('time', 'upcoming')
        
        # Featured events
        context['featured_events'] = Event.objects.filter(
            is_published=True,
            is_featured=True,
            is_cancelled=False,
            start_date__gte=timezone.now()
        )[:3]
        
        return context


class EventDetailView(DetailView):
    """Detail view for an event."""
    
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.can_manage_content:
            return Event.objects.all()
        return Event.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related events
        context['related_events'] = Event.objects.filter(
            is_published=True,
            is_cancelled=False,
            category=self.object.category,
            start_date__gte=timezone.now()
        ).exclude(pk=self.object.pk)[:3]
        return context


class CalendarView(TemplateView):
    """Calendar view of events."""
    
    template_name = 'events/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get events for calendar
        events = Event.objects.filter(
            is_published=True,
            is_cancelled=False
        ).values(
            'id', 'title', 'slug', 'start_date', 'end_date',
            'is_all_day', 'venue', 'category__color'
        )
        
        # Format for FullCalendar
        calendar_events = []
        for event in events:
            calendar_events.append({
                'id': event['id'],
                'title': event['title'],
                'start': event['start_date'].isoformat(),
                'end': event['end_date'].isoformat() if event['end_date'] else None,
                'allDay': event['is_all_day'],
                'url': f"/events/{event['slug']}/",
                'backgroundColor': event['category__color'] or '#8B4513',
                'extendedProps': {
                    'venue': event['venue']
                }
            })
        
        context['calendar_events'] = json.dumps(calendar_events)
        context['categories'] = EventCategory.objects.all()
        
        return context


class TraditionalFestivalListView(ListView):
    """List traditional festivals."""
    
    model = TraditionalFestival
    template_name = 'events/festivals.html'
    context_object_name = 'festivals'
    
    def get_queryset(self):
        return TraditionalFestival.objects.filter(is_active=True)


class TraditionalFestivalDetailView(DetailView):
    """Detail view for a traditional festival."""
    
    model = TraditionalFestival
    template_name = 'events/festival_detail.html'
    context_object_name = 'festival'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


# ============== ADMIN VIEWS ==============

class EventCreateView(AdminRequiredMixin, CreateView):
    """Create a new event."""
    
    model = Event
    form_class = EventForm
    template_name = 'events/admin/event_form.html'
    success_url = reverse_lazy('events:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Event created successfully.')
        return super().form_valid(form)


class EventUpdateView(AdminRequiredMixin, UpdateView):
    """Update an event."""
    
    model = Event
    form_class = EventForm
    template_name = 'events/admin/event_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully.')
        return super().form_valid(form)


class EventDeleteView(AdminRequiredMixin, DeleteView):
    """Delete an event."""
    
    model = Event
    template_name = 'events/admin/event_confirm_delete.html'
    success_url = reverse_lazy('events:list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Event deleted successfully.')
        return super().delete(request, *args, **kwargs)


class FestivalCreateView(AdminRequiredMixin, CreateView):
    """Create a traditional festival."""
    
    model = TraditionalFestival
    form_class = TraditionalFestivalForm
    template_name = 'events/admin/festival_form.html'
    success_url = reverse_lazy('events:festivals')
    
    def form_valid(self, form):
        messages.success(self.request, 'Festival created successfully.')
        return super().form_valid(form)


class FestivalUpdateView(AdminRequiredMixin, UpdateView):
    """Update a traditional festival."""
    
    model = TraditionalFestival
    form_class = TraditionalFestivalForm
    template_name = 'events/admin/festival_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def form_valid(self, form):
        messages.success(self.request, 'Festival updated successfully.')
        return super().form_valid(form)


class FestivalDeleteView(AdminRequiredMixin, DeleteView):
    """Delete a traditional festival."""
    
    model = TraditionalFestival
    template_name = 'events/admin/festival_confirm_delete.html'
    success_url = reverse_lazy('events:festivals')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Festival deleted successfully.')
        return super().delete(request, *args, **kwargs)


class EventManageListView(AdminRequiredMixin, ListView):
    """Admin list view for managing events."""
    
    model = Event
    template_name = 'events/admin/manage_list.html'
    context_object_name = 'events'
    paginate_by = 20
    
    def get_queryset(self):
        return Event.objects.all().order_by('-start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = Event.EventType.choices
        return context


def calendar_events(request):
    """API endpoint for calendar events (JSON)."""
    events = Event.objects.filter(
        is_published=True,
        is_cancelled=False
    )
    
    event_data = []
    for event in events:
        color_map = {
            'ceremony': '#8B4513',
            'festival': '#228B22',
            'meeting': '#17a2b8',
            'celebration': '#ffc107',
            'other': '#6c757d',
        }
        event_data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat() if event.end_date else None,
            'allDay': event.is_all_day,
            'url': event.get_absolute_url(),
            'backgroundColor': color_map.get(event.event_type, '#8B4513'),
            'extendedProps': {
                'venue': event.venue,
                'eventType': event.get_event_type_display(),
                'time': event.start_date.strftime('%I:%M %p') if not event.is_all_day else None,
                'description': event.description[:100] + '...' if len(event.description) > 100 else event.description,
            }
        })
    
    return JsonResponse(event_data, safe=False)
