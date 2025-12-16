"""
URL patterns for events app.
"""

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Public views
    path('', views.EventListView.as_view(), name='list'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/events/', views.calendar_events, name='calendar_events'),
    path('festivals/', views.TraditionalFestivalListView.as_view(), name='festivals'),
    path('festival/<slug:slug>/', views.TraditionalFestivalDetailView.as_view(), name='festival_detail'),
    path('<slug:slug>/', views.EventDetailView.as_view(), name='detail'),
    
    # Admin views
    path('admin/manage/', views.EventManageListView.as_view(), name='admin_manage'),
    path('admin/create/', views.EventCreateView.as_view(), name='create'),
    path('admin/<slug:slug>/edit/', views.EventUpdateView.as_view(), name='edit'),
    path('admin/<slug:slug>/delete/', views.EventDeleteView.as_view(), name='delete'),
    
    # Festival admin
    path('admin/festival/create/', views.FestivalCreateView.as_view(), name='festival_create'),
    path('admin/festival/<slug:slug>/edit/', views.FestivalUpdateView.as_view(), name='festival_update'),
    path('admin/festival/<slug:slug>/delete/', views.FestivalDeleteView.as_view(), name='festival_delete'),
]
