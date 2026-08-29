from .models import Dispositivo, Puerto
from rest_framework import viewsets, permissions
from .serializers import DispositivoSerializer, PuertoSerializer

class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DispositivoSerializer

class PuertoViewSet(viewsets.ModelViewSet):
    queryset = Puerto.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PuertoSerializer