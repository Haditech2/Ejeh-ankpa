"""
URL configuration for Ejeh Ankpa Palace Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    # Ensure browsers requesting `/favicon.ico` get redirected to the
    # static favicon asset (prevents template rendering errors on root requests).
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    path('palace-admin/', admin.site.urls),
    path('', include('palace.urls')),
    path('accounts/', include('accounts.urls')),
    path('announcements/', include('announcements.urls')),
    path('events/', include('events.urls')),
    path('community/', include('community.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = 'Ejeh Ankpa Palace Administration'
admin.site.site_title = 'Ejeh Ankpa Palace'
admin.site.index_title = 'Palace Management Dashboard'
