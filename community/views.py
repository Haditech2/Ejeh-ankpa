"""
Views for community app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse

from .models import ContactMessage, PublicFeedback, Newsletter
from .forms import ContactForm, FeedbackForm, NewsletterForm, MessageResponseForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for views that require palace admin access."""
    
    def test_func(self):
        return self.request.user.can_manage_content


# ============== PUBLIC VIEWS ==============

class ContactView(CreateView):
    """Contact the palace page."""
    
    model = ContactMessage
    form_class = ContactForm
    template_name = 'community/contact.html'
    success_url = reverse_lazy('community:contact_success')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Your message has been sent successfully. We will respond as soon as possible.'
        )
        return response


class ContactSuccessView(TemplateView):
    """Contact form success page."""
    
    template_name = 'community/contact_success.html'


class FeedbackCreateView(CreateView):
    """Submit public feedback."""
    
    model = PublicFeedback
    form_class = FeedbackForm
    template_name = 'community/feedback_form.html'
    success_url = reverse_lazy('community:feedback_success')
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        messages.success(
            self.request,
            'Thank you for your feedback! It will be reviewed and published soon.'
        )
        return super().form_valid(form)


class FeedbackSuccessView(TemplateView):
    """Feedback submission success page."""
    
    template_name = 'community/feedback_success.html'


class FeedbackListView(ListView):
    """Display approved public feedback/testimonials."""
    
    model = PublicFeedback
    template_name = 'community/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 12
    
    def get_queryset(self):
        return PublicFeedback.objects.filter(is_approved=True)


def newsletter_subscribe(request):
    """Handle newsletter subscription."""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data.get('name', '')
            
            # Check if already subscribed
            subscriber, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'name': name, 'is_active': True}
            )
            
            if not created and not subscriber.is_active:
                subscriber.is_active = True
                subscriber.unsubscribed_at = None
                subscriber.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for subscribing to our newsletter!'
                })
            
            messages.success(request, 'Thank you for subscribing to our newsletter!')
            return redirect('palace:home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please enter a valid email address.'
                })
    
    return redirect('palace:home')


# ============== ADMIN VIEWS ==============

class MessageListView(AdminRequiredMixin, ListView):
    """Admin view for contact messages."""
    
    model = ContactMessage
    template_name = 'community/admin/message_list.html'
    context_object_name = 'messages_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all()
        
        # Filter by status
        status = self.request.GET.get('status')
        if status == 'unread':
            queryset = queryset.filter(is_read=False)
        elif status == 'read':
            queryset = queryset.filter(is_read=True, is_responded=False)
        elif status == 'responded':
            queryset = queryset.filter(is_responded=True)
        elif status == 'archived':
            queryset = queryset.filter(is_archived=True)
        else:
            queryset = queryset.filter(is_archived=False)
        
        # Filter by type
        message_type = self.request.GET.get('type')
        if message_type:
            queryset = queryset.filter(message_type=message_type)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_types'] = ContactMessage.MessageType.choices
        context['current_status'] = self.request.GET.get('status', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['unread_count'] = ContactMessage.objects.filter(is_read=False).count()
        return context


class MessageDetailView(AdminRequiredMixin, DetailView):
    """Admin view for message detail."""
    
    model = ContactMessage
    template_name = 'community/admin/message_detail.html'
    context_object_name = 'message'
    
    def get_object(self):
        obj = super().get_object()
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=['is_read'])
        return obj


class MessageResponseView(AdminRequiredMixin, UpdateView):
    """Admin view to respond to a message."""
    
    model = ContactMessage
    form_class = MessageResponseForm
    template_name = 'community/admin/message_response.html'
    success_url = reverse_lazy('community:admin_messages')
    
    def form_valid(self, form):
        form.instance.responded_by = self.request.user
        form.instance.responded_at = timezone.now()
        form.instance.is_responded = True
        messages.success(self.request, 'Response saved successfully.')
        return super().form_valid(form)


class FeedbackManageListView(AdminRequiredMixin, ListView):
    """Admin view to manage feedback."""
    
    model = PublicFeedback
    template_name = 'community/admin/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = PublicFeedback.objects.all()
        
        status = self.request.GET.get('status')
        if status == 'pending':
            queryset = queryset.filter(is_approved=False)
        elif status == 'approved':
            queryset = queryset.filter(is_approved=True)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = PublicFeedback.objects.filter(is_approved=False).count()
        context['current_status'] = self.request.GET.get('status', '')
        return context


def approve_feedback(request, pk):
    """Approve a feedback submission."""
    if not request.user.can_manage_content:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('community:admin_feedback')
    
    feedback = get_object_or_404(PublicFeedback, pk=pk)
    feedback.is_approved = True
    feedback.approved_by = request.user
    feedback.approved_at = timezone.now()
    feedback.save()
    
    messages.success(request, 'Feedback approved and published.')
    return redirect('community:admin_feedback')


def reject_feedback(request, pk):
    """Reject/delete a feedback submission."""
    if not request.user.can_manage_content:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('community:admin_feedback')
    
    feedback = get_object_or_404(PublicFeedback, pk=pk)
    feedback.delete()
    
    messages.success(request, 'Feedback rejected and deleted.')
    return redirect('community:admin_feedback')


class NewsletterListView(AdminRequiredMixin, ListView):
    """Admin view for newsletter subscribers."""
    
    model = Newsletter
    template_name = 'community/admin/newsletter_list.html'
    context_object_name = 'subscribers'
    paginate_by = 50
    
    def get_queryset(self):
        return Newsletter.objects.filter(is_active=True)
