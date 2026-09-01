from .models import Dispositivo, Puerto
from rest_framework import viewsets
from .serializers import DispositivoSerializer, PuertoSerializer
from .permissions import IsStaffOrReadOnly

class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = DispositivoSerializer

class PuertoViewSet(viewsets.ModelViewSet):
    queryset = Puerto.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = PuertoSerializer