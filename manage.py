#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # --- Bloque agregado para crear superusuario desde users_data.json ---
    try:
        import django
        django.setup()

        from django.contrib.auth import get_user_model
        from django.core.management import call_command

        User = get_user_model()

        if not User.objects.filter(is_superuser=True).exists():
            print("⚠️  No hay superusuario. Cargando desde users_data.json...")
            call_command('loaddata', 'fixtures/users_data.json')
            print("✅ Superusuario importado correctamente.")
    except Exception as e:
        print(f"❌ Error al intentar cargar el superusuario: {e}")
    # -----------------------------------------------------------------------

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
