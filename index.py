"""
Vercel Python entrypoint for the Ejeh Ankpa Django project.

Vercel looks for a top-level `app` variable which is a WSGI/ASGI application.
We simply re-export the Django WSGI application from `ejeh_palace.wsgi`.
"""

from ejeh_palace.wsgi import application

# Vercel expects `app` for WSGI/ASGI applications
app = application


