import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ejeh_palace.settings')
try:
	application = get_wsgi_application()
except Exception as e:
	# Print traceback so Vercel build logs include the real import error
	import sys, traceback
	print("WSGI application import failed:", file=sys.stderr)
	traceback.print_exc()
	raise

# Expose common name Vercel looks for for WSGI apps
app = application
