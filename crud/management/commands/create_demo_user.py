import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = (
        'Crea (o actualiza la contraseña de) un usuario de solo lectura para la '
        'demo publica, a partir de las variables de entorno DEMO_USER_USERNAME, '
        'DEMO_USER_EMAIL y DEMO_USER_PASSWORD.'
    )
    
    def handle(self, *args, **options):
        username = os.environ.get('DEMO_USER_USERNAME')
        password = os.environ.get('DEMO_USER_PASSWORD')
        email = os.environ.get('DEMO_USER_EMAIL', '')
        
        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'DEMO_USER_USERNAME / DEMO_USER_PASSWORD no definidas, se omite'
                )
            )
            return
        
        user, created = User.objects.get_or_create(
            username = username, defaults={'email': email}
        )
        user.email = email
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        
        accion = 'creado' if created else 'actualizado'
        self.stdout.write(self.style.SUCCESS(f'Usuario de solo lectura "{username}" {accion}'))