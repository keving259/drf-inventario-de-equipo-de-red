from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Dispositivo, Puerto
from django.core.exceptions import ValidationError
from django.urls import reverse


class DispositivoModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username = 'user',
            password = 'user'
        )
        self.dispositivo = Dispositivo.objects.create(
            nombre = "Router",
            tipo = Dispositivo.Tipo.ROUTER,
            marca = 'Cisco',
            modelo = "ISR4321",
            ip_gestion = '192.168.1.1',
            ubicacion = 'Rack 1',
            propietario = self.user
        )
        
    def test_tipo_choices_display(self):
        self.assertEqual(self.dispositivo.get_tipo_display(), 'Router')
        
    def test_relacion_propietario_dispositivos(self):
        self.assertEqual(self.user.dispositivos.count(), 1)
        self.assertIn(self.dispositivo, self.user.dispositivos.all())
        
    def test_ip_invalida_lanza_error_de_validacion(self):
        dispositivo_invalido = Dispositivo(
            nombre = 'Switch',
            tipo = Dispositivo.Tipo.SWITCH,
            marca = 'TP-Link',
            modelo = 'TL-SG108',
            ip_gestion = '999.999.999.999',
            ubicacion = 'Rack 2',
            propietario = self.user
        )
        with self.assertRaises(ValidationError):
            dispositivo_invalido.full_clean()

class PuertoModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='user', 
            password='user'
        )
        self.dispositivo = Dispositivo.objects.create(
            nombre = 'Switch Core',
            tipo = Dispositivo.Tipo.SWITCH,
            marca = 'Cisco',
            modelo = 'C92OO',
            ip_gestion = '10.0.0.1',
            ubicacion = 'Rack 3',
            propietario = self.user
        )
        self.puerto = Puerto.objects.create(
            dispositivo = self.dispositivo,
            numero_puerto = 'Gi0/1',
            tipo = Puerto.Tipo.ETHERNET_GIGA,
            velocidad = '1000Mbps',
            estado = True
        )
    
    def test_relacion_dispositivo_puertos(self):
        self.assertEqual(self.dispositivo.puertos.count(), 1)
        
    def test_eliminar_dispositivo_elimina_puertos_cascada(self):
        self.dispositivo.delete()
        self.assertEqual(Puerto.objects.count(), 0)
