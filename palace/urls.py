"""
URL patterns for palace app.
"""

from django.urls import path
from . import views

app_name = 'palace'

urlpatterns = [
    # Home and About
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Ejeh Profiles
    path('ejeh/', views.EjehListView.as_view(), name='ejeh_list'),
    path('ejeh/present/', views.PresentEjehView.as_view(), name='present_ejeh'),
    path('ejeh/past/', views.PastEjehsView.as_view(), name='past_ejehs'),
    path('ejeh/<int:pk>/', views.EjehDetailView.as_view(), name='ejeh_detail'),
    
    # Royal Gallery
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('gallery/category/<slug:slug>/', views.GalleryCategoryView.as_view(), name='gallery_category'),
    path('gallery/image/<int:pk>/', views.GalleryImageDetailView.as_view(), name='gallery_image'),
    
    # History & Culture
    path('history/', views.HistoryListView.as_view(), name='history_list'),
    path('history/<slug:slug>/', views.HistoryDetailView.as_view(), name='history_detail'),
    path('traditional-titles/', views.TraditionalTitlesView.as_view(), name='traditional_titles'),
    
    # Admin - Ejeh Management
    path('manage/ejeh/create/', views.EjehCreateView.as_view(), name='ejeh_create'),
    path('manage/ejeh/<int:pk>/edit/', views.EjehUpdateView.as_view(), name='ejeh_update'),
    path('manage/ejeh/<int:pk>/delete/', views.EjehDeleteView.as_view(), name='ejeh_delete'),
    
    # Admin - Gallery Management
    path('manage/gallery/upload/', views.GalleryUploadView.as_view(), name='gallery_upload'),
    path('manage/gallery/<int:pk>/edit/', views.GalleryImageUpdateView.as_view(), name='gallery_edit'),
    path('manage/gallery/<int:pk>/delete/', views.GalleryImageDeleteView.as_view(), name='gallery_delete'),
    
    # Admin - History Management
    path('manage/history/create/', views.HistoryCreateView.as_view(), name='history_create'),
    path('manage/history/<slug:slug>/edit/', views.HistoryUpdateView.as_view(), name='history_update'),
    path('manage/history/<slug:slug>/delete/', views.HistoryDeleteView.as_view(), name='history_delete'),
    
    # Admin - Palace Settings
    path('manage/settings/', views.PalaceSettingsView.as_view(), name='palace_settings'),
]
