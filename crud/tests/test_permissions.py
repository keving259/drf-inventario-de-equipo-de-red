from ..models import Dispositivo
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase


class DispositivoPermissionsTest(APITestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='admin', password='admin', is_staff=True)
        self.normal_user = User.objects.create_user(username='lector', password='lector', is_staff=False)
        self.list_url = reverse('dispositivos-list')
        
    def test_usuario_no_autenticado(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_usuario_normal(self):
        self.client.force_authenticate(user=self.normal_user)
    
    def test_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
                    'nombre' : "Router",
                    'tipo' : Dispositivo.Tipo.ROUTER,
                    'marca' : 'Cisco',
                    'modelo' : "ISR4321",
                    'ip_gestion' : '192.168.1.1',
                    'ubicacion' : 'Rack 1',
                    'propietario' : self.staff_user.id
                }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_login(self):
        response = self.client.post(reverse('login'), {'username':'admin', 'password':'admin'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response_get = self.client.get(self.list_url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)