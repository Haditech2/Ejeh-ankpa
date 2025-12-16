"""
URL patterns for announcements app.
"""

from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    # Public views
    path('', views.AnnouncementListView.as_view(), name='list'),
    path('detail/<slug:slug>/', views.AnnouncementDetailView.as_view(), name='detail'),
    path('royal-messages/', views.RoyalMessageListView.as_view(), name='royal_messages'),
    path('royal-message/<int:pk>/', views.RoyalMessageDetailView.as_view(), name='royal_message'),
    
    # Admin views
    path('admin/manage/', views.AnnouncementManageListView.as_view(), name='admin_manage'),
    path('admin/create/', views.AnnouncementCreateView.as_view(), name='create'),
    path('admin/<slug:slug>/edit/', views.AnnouncementUpdateView.as_view(), name='edit'),
    path('admin/<slug:slug>/delete/', views.AnnouncementDeleteView.as_view(), name='delete'),
    
    # Royal message admin
    path('admin/royal-message/create/', views.RoyalMessageCreateView.as_view(), name='royal_message_create'),
    path('admin/royal-message/<int:pk>/edit/', views.RoyalMessageUpdateView.as_view(), name='royal_message_update'),
    path('admin/royal-message/<int:pk>/delete/', views.RoyalMessageDeleteView.as_view(), name='royal_message_delete'),
]
