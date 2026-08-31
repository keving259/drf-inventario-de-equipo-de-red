# DRF Inventario de Equipo de Red

API REST construida con **Django REST Framework** para administrar un inventario de dispositivos de red (routers, switches, firewalls, APs, etc.) y sus puertos, con autenticación por token y base de datos **PostgreSQL**.

**Demo en vivo:** [drf-inventario-de-equipo-de-red.onrender.com](https://drf-inventario-de-equipo-de-red.onrender.com)
**Repositorio:** [github.com/keving259/drf-inventario-de-equipo-de-red](https://github.com/keving259/drf-inventario-de-equipo-de-red)

> El servicio está desplegado en el plan gratuito de Render, por lo que si no es utilizado por un tiempo se suspende y la primera petición puede tardar ~30-60 segundos en responder.

![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.18-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-elephant-336791?logo=postgresql&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)

---

## Contenido

- [Características](#-características)
- [Stack tecnológico](#-stack-tecnológico)
- [Modelo de datos](#-modelo-de-datos)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Autenticación](#-autenticación)
- [Instalación local](#-instalación-local)
- [Variables de entorno](#-variables-de-entorno)
- [Despliegue en Render](#-despliegue-en-render)
- [Pruebas con Postman](#-pruebas-con-postman)
- [Estructura del proyecto](#-estructura-del-proyecto)

---

## Características

- CRUD completo de **Dispositivos** de red (routers, switches, firewalls, APs, servidores, etc.)
- CRUD completo de **Puertos** asociados a cada dispositivo
- Autenticación basada en **Token** (login personalizado que devuelve el token del usuario)
- Endpoints protegidos: solo usuarios autenticados pueden crear, leer, actualizar o eliminar recursos
- Panel de administración de Django (`/admin/`)
- Listo para producción: archivos estáticos con **WhiteNoise**, servidor **Gunicorn/Uvicorn** y base de datos **PostgreSQL** vía `DATABASE_URL`

## Stack tecnológico

| Componente           | Tecnología                              |
|----------------------|-----------------------------------------|
| Backend              | Django 6.1 + Django REST Framework 3.18 |
| Base de datos        | PostgreSQL (`psycopg2-binary`)          |
| Autenticación        | Token Authentication (DRF)              |
| Configuración        | `django-environ` (variables `.env`)     |
| Archivos estáticos   | WhiteNoise                              |
| Servidor WSGI/ASGI   | Gunicorn / Uvicorn                      |
| Despliegue           | Render                                  |

## Modelo de datos

### `Dispositivo`

| Campo         | Tipo                          | Descripción                                                                            |
|---------------|-------------------------------|----------------------------------------------------------------------------------------|
| `nombre`      | CharField                     | Nombre identificador del dispositivo                                                   |
| `tipo`        | Choice                        | Router, Switch, Firewall, AP, Servidor, Módem, UPS, NAS, Cámara IP, etc. (20 opciones) |
| `marca`       | CharField                     | Fabricante                                                                             |
| `modelo`      | CharField                     | Modelo del equipo                                                                      |
| `ip_gestion`  | GenericIPAddressField (v4/v6) | IP de gestión del dispositivo                                                          |
| `ubicacion`   | TextField                     | Ubicación física                                                                       |
| `propietario` | ForeignKey → `User`           | Usuario dueño del dispositivo (`related_name='dispositivos'`)                          |

### `Puerto`

| Campo            | Tipo                       | Descripción                                                           |
|------------------|----------------------------|-----------------------------------------------------------------------|
| `dispositivo`    | ForeignKey → `Dispositivo` | Dispositivo al que pertenece (`related_name='puertos'`)               |
| `numero_puerto`  | CharField                  | Identificador del puerto                                              |
| `tipo`           | Choice                     | Fast/Gigabit/10-100G Ethernet, SFP/SFP+/QSFP, Consola, USB, PoE, etc. |
| `velocidad`      | CharField                  | Velocidad del puerto                                                  |
| `estado`         | BooleanField               | Activo / inactivo                                                     |
| `conectado_a`    | CharField (opcional)       | Descripción de a qué está conectado                                   |

## Endpoints de la API

Base URL local: `http://127.0.0.1:8000/api/` · Base URL en producción: `https://drf-inventario-de-equipo-de-red.onrender.com/api/`

| Método   | Endpoint                  | Descripción                         | Auth requerida  |
|----------|---------------------------|-------------------------------------|:---------------:|
| `POST`   | `/api/login/`             | Login, devuelve token de usuario    | No              |
| `GET`    | `/api/dispositivos/`      | Listar dispositivos                 | Sí              |
| `POST`   | `/api/dispositivos/`      | Crear dispositivo                   | Sí              |
| `GET`    | `/api/dispositivos/{id}/` | Obtener un dispositivo              | Sí              |
| `PUT`    | `/api/dispositivos/{id}/` | Actualizar un dispositivo (completo)| Sí              |
| `PATCH`  | `/api/dispositivos/{id}/` | Actualizar un dispositivo (parcial) | Sí              |
| `DELETE` | `/api/dispositivos/{id}/` | Eliminar un dispositivo             | Sí              |
| `GET`    | `/api/puertos/`           | Listar puertos                      | Sí              |
| `POST`   | `/api/puertos/`           | Crear puerto                        | Sí              |
| `GET`    | `/api/puertos/{id}/`      | Obtener un puerto                   | Sí              |
| `PUT`    | `/api/puertos/{id}/`      | Actualizar un puerto (completo)     | Sí              |
| `PATCH`  | `/api/puertos/{id}/`      | Actualizar un puerto (parcial)      | Sí              |
| `DELETE` | `/api/puertos/{id}/`      | Eliminar un puerto                  | Sí              |

También están disponibles `/admin/` (panel de administración de Django) y `/api-auth/` (login/logout navegable de DRF).

## Autenticación

La API usa `TokenAuthentication` (además de `BasicAuthentication` y `SessionAuthentication` para el panel navegable de DRF). Para obtener un token:

```bash
curl -X POST https://drf-inventario-de-equipo-de-red.onrender.com/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "password"}'
```

Respuesta:

```json
{
    "token": "e4a1c2...",
    "user": { "id": 1, "username": "usuario", "email": "..." }
}
```

Luego, incluye el token en cada petición a los endpoints protegidos:

```bash
curl https://drf-inventario-de-equipo-de-red.onrender.com/api/dispositivos/ \
  -H "Authorization: Token e4a1c2..."
```

## Instalación local

### Requisitos previos

- Python 3.11+
- PostgreSQL corriendo localmente (o accesible remotamente)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/keving259/drf-inventario-de-equipo-de-red.git
cd drf-inventario-de-equipo-de-red

# 2. Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear un archivo .env en la raíz del proyecto (ver sección siguiente)

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear un superusuario para poder autenticarte y usar /admin/
python manage.py createsuperuser

# 7. Levantar el servidor de desarrollo
python manage.py runserver
```

La API quedará disponible en `http://127.0.0.1:8000/api/`.

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto (mismo nivel que `manage.py`):

```env
SECRET_KEY=clave-secreta-django
DATABASE_URL=postgres://usuario:password@localhost:5432/nombre_bd
```

| Variable                   | Descripción                                                                                                    |
|----------------------------|----------------------------------------------------------------------------------------------------------------|
| `SECRET_KEY`               | Clave secreta de Django. En desarrollo tiene un valor por defecto inseguro; **cambiar en producción**.         |
| `DATABASE_URL`             | Cadena de conexión a PostgreSQL (formato `postgres://usuario:password@host:puerto/bd`).                        |
| `RENDER`                   | La define Render automáticamente; cuando existe, `DEBUG` pasa a `False` y se exige `sslmode=require` en la BD. |
| `RENDER_EXTERNAL_HOSTNAME` | La define Render automáticamente y se agrega a `ALLOWED_HOSTS`.                                                |

## Despliegue en Render

El proyecto incluye `build.sh`, que Render ejecuta en cada deploy:

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Configuración típica en Render:

1. Crear un **Web Service** apuntando a este repositorio.
2. **Build command:** `./build.sh`
3. **Start command:** `gunicorn network_equipment.wsgi:application`
4. Agregar una base de datos **PostgreSQL** en Render y copiar su `DATABASE_URL` (internal) a las variables de entorno del Web Service.
5. Definir `SECRET_KEY` como variable de entorno.

## Pruebas con Postman

Se probaron todos los endpoints con Postman, cubriendo el login para obtener el token y el flujo completo de CRUD para cada tabla: listar, obtener por id, crear, actualizar y eliminar. Las capturas están en [`docs/screenshots/`](docs/screenshots).

### Login

| Petición           | Captura                                                   |
|--------------------|-----------------------------------------------------------|
| `POST /api/login/` | ![Login - obtener token](docs/screenshots/login-post.png) |

### Dispositivos

| Petición | Captura |
| --- | --- |
| `GET /api/dispositivos/` | ![Listar dispositivos](docs/screenshots/dispositivos-get-list.png) |
| `GET /api/dispositivos/{id}/` | ![Detalle de dispositivo](docs/screenshots/dispositivos-get-detail.png) |
| `POST /api/dispositivos/` | ![Crear dispositivo](docs/screenshots/dispositivos-post.png) |
| `PUT`/`PATCH /api/dispositivos/{id}/` | ![Actualizar dispositivo](docs/screenshots/dispositivos-update.png) |
| `DELETE /api/dispositivos/{id}/` | ![Eliminar dispositivo](docs/screenshots/dispositivos-delete.png) |

### Puertos

| Petición | Captura                                                                           |
| --- | --- |
| `GET /api/puertos/` | ![Listar puertos](docs/screenshots/puertos-get-list.png) |
| `GET /api/puertos/{id}/` | ![Detalle de puerto](docs/screenshots/puertos-get-detail.png) |
| `POST /api/puertos/` | ![Crear puerto](docs/screenshots/puertos-post.png) |
| `PUT`/`PATCH /api/puertos/{id}/` | ![Actualizar puerto](docs/screenshots/puertos-update.png) |
| `DELETE /api/puertos/{id}/` | ![Eliminar puerto](docs/screenshots/puertos-delete.png) |

## Estructura del proyecto

```
drf-inventario-de-equipo-de-red/
├── crud/                      # App principal: modelos, serializers, vistas y API
│   ├── models.py               # Dispositivo y Puerto
│   ├── serializers.py          # DispositivoSerializer, PuertoSerializer, UserSerializer
│   ├── api.py                  # ViewSets (DispositivoViewSet, PuertoViewSet)
│   ├── views.py                # Vista de login + home
│   ├── urls.py                 # Rutas de la app (router + login)
│   ├── admin.py
│   ├── migrations/
│   ├── templates/
│   └── static/
├── network_equipment/          # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── build.sh                    # Script de build para Render
├── requirements.txt
└── manage.py
```
