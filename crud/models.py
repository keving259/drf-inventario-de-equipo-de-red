from django.db import models
from django.conf import settings

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=200)
    
    class Tipo(models.TextChoices):
        ROUTER = 'RT', 'Router'
        SWITCH = 'SW', 'Switch'
        FIREWALL = 'FW', 'Firewall'
        PUNTO_ACCESO = 'AP', 'Punto de acceso (AP)'
        CONTROLADOR_WLAN = 'WC', 'Controlador WLAN'
        SERVIDOR = 'SV', 'Servidor'
        MODEM = 'MD', 'Módem'
        HUB = 'HB', 'Hub'
        BRIDGE = 'BR', 'Bridge'
        BALANCEADOR = 'LB', 'Balanceador de carga'
        GATEWAY = 'GW', 'Gateway'
        REPETIDOR = 'RP', 'Repetidor'
        IDS_IPS = 'IP', 'IDS/IPS'
        UPS = 'UP', 'UPS'
        NAS = 'NA', 'NAS'
        IMPRESORA = 'IM', 'Impresora de red'
        CAMARA_IP = 'CM', 'Cámar IP'
        TELEFONO_IP = 'TP', 'Teléfono IP'
        ESTACION_TRABAJO = 'ET', 'Estación de trabajo'
        PATCH_PANEL = 'PP', 'Patch panel'
        OTRO = 'OT', 'Otro'
        
    tipo = models.CharField(max_length=4, choices=Tipo.choices)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=200)
    ip_gestion = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    ubicacion = models.TextField(max_length=300)
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dispositivos'
    )

class Puerto(models.Model):
    dispositivo = models.ForeignKey(
        Dispositivo,
        on_delete = models.CASCADE,
        related_name = 'puertos'
    )
    numero_puerto = models.CharField(max_length=15)
    
    class Tipo(models.TextChoices):
        ETHERNET_FAST = 'FE', 'Fast Ethernet (10/100)'
        ETHERNET_GIGA = 'GE', 'Gigabit Ethernet (1G)'
        ETHERNET_10G = '10G', '10 Gigabit Ethernet'
        ETHERNET_25G = '25G', '25 Gigabit Ethernet'
        ETHERNET_40G = '40G', '40 Gigabit Ethernet'
        ETHERNET_100G = '100G', '100 Gigabit Ethernet'
        FIBRA_SFP = 'SFP', 'Fibra SFP'
        FIBRA_SFP_PLUS = 'SFP+', 'Fibra SFP+'
        FIBRA_QSFP = 'QSFP', 'Fibra QSFP'
        CONSOLA = 'CON', 'Consola (RJ45/RS232)'
        USB = 'USB', 'USB'
        SERIAL = 'SER', 'Serial'
        MANAGEMENT = 'MGT', 'Puerto de gestión'
        POE = 'POE', 'PoE'
        OTRO = 'OT', 'Otro'
        
    tipo = models.CharField(max_length=4, choices=Tipo.choices)
    velocidad = models.CharField(max_length=20)
    estado = models.BooleanField()
    conectado_a = models.CharField(max_length=500, blank=True, null=True)