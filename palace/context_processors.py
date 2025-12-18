"""
Context processor for palace-wide template variables.
"""

from .models import PalaceInfo, EjehProfile


def palace_context(request):
    """Add palace information to all templates."""
    try:
        palace_info = PalaceInfo.get_instance()
    except:
        palace_info = None
    
    try:
        present_ejeh = EjehProfile.get_present_ejeh()
    except:
        present_ejeh = None
    # Resolve safe URLs for media fields to avoid storage/backend errors
    palace_logo_url = None
    palace_favicon_url = None
    if palace_info:
        try:
            if getattr(palace_info, 'logo'):
                palace_logo_url = palace_info.logo.url
        except Exception:
            palace_logo_url = None
        try:
            if getattr(palace_info, 'favicon'):
                palace_favicon_url = palace_info.favicon.url
        except Exception:
            palace_favicon_url = None

    return {
        'palace_info': palace_info,
        'present_ejeh': present_ejeh,
        'palace_logo_url': palace_logo_url,
        'palace_favicon_url': palace_favicon_url,
    }
