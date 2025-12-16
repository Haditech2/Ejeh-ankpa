"""
URL patterns for community app.
"""

from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Public views
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
    path('feedback/', views.FeedbackListView.as_view(), name='feedback_list'),
    path('feedback/submit/', views.FeedbackCreateView.as_view(), name='feedback_submit'),
    path('feedback/success/', views.FeedbackSuccessView.as_view(), name='feedback_success'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Admin views
    path('admin/messages/', views.MessageListView.as_view(), name='admin_messages'),
    path('admin/messages/<int:pk>/', views.MessageDetailView.as_view(), name='admin_message_detail'),
    path('admin/messages/<int:pk>/reply/', views.MessageResponseView.as_view(), name='admin_message_reply'),
    path('admin/feedback/', views.FeedbackManageListView.as_view(), name='admin_feedback'),
    path('admin/feedback/<int:pk>/approve/', views.approve_feedback, name='approve_feedback'),
    path('admin/feedback/<int:pk>/reject/', views.reject_feedback, name='reject_feedback'),
    path('admin/newsletter/', views.NewsletterListView.as_view(), name='admin_newsletter'),
]
