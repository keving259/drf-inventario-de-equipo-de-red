from rest_framework import routers
from .api import DispositivoViewSet, PuertoViewSet
from django.urls import path
from . import views

router = routers.DefaultRouter()

router.register('dispositivos', DispositivoViewSet, 'dispositivos')
router.register('puertos', PuertoViewSet, 'puertos')

urlpatterns = [
    path('login/', views.login, name='login'),
] + router.urls