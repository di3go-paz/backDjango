import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()


from django.contrib.auth import get_user_model
User = get_user_model()


if not User.objects.filter(username=os.environ.get('SUPERUSER_USERNAME')).exists():
    User.objects.create_superuser(
        os.environ.get('SUPERUSER_USERNAME'),
        os.environ.get('SUPERUSER_EMAIL'),
        os.environ.get('SUPERUSER_PASSWORD')
    )
    print("Superusuario creado!")