from rest_framework import serializers
from .models import Dispositivo, Puerto
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = ('nombre', 'tipo', 'marca', 'modelo', 'ip_gestion', 'ubicacion', 'propietario')

class PuertoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puerto
        fields = ('dispositivo', 'numero_puerto', 'tipo', 'velocidad', 'estado', 'conectado_a')
