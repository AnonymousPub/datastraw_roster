import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datastraw_project.settings')

# Automatically run migrations on startup for cloud deployment
try:
    call_command('migrate')
except Exception as e:
    print(f"Migration error: {e}")

application = get_wsgi_application()