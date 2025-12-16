"""
URL patterns for accounts app.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    
    # Dashboards
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/chief/', views.chief_dashboard, name='chief_dashboard'),
    
    # Chiefs
    path('chiefs/', views.ChiefListView.as_view(), name='chiefs_list'),
    path('chiefs/<int:pk>/', views.ChiefDetailView.as_view(), name='chief_detail'),
    
    # Members (admin only)
    path('members/', views.MemberListView.as_view(), name='members_list'),
]
