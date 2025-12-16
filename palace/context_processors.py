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
    
    return {
        'palace_info': palace_info,
        'present_ejeh': present_ejeh,
    }
