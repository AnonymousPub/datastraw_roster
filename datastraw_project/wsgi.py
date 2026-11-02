import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datastraw_project.settings')

try:
    call_command('migrate')
    call_command('seed_data') # Seeds your sample data automatically
except Exception as e:
    print(f"Startup error: {e}")

application = get_wsgi_application()