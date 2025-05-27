"""
Configuración optimizada para Sistema de Reservas - Vistas Quillayquen
Con soporte para plantillas en vistas_quillayquen/templates/
"""

from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent
# settings.py (Django)

# 1. Clave secreta (nunca hardcodear en producción)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())  # ✅ Bien

# 2. Debug (solo True en desarrollo)
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Mejor práctica: controlar por variable de entorno

# 3. Hosts permitidos (seguridad CSRF y Host header validation)
ALLOWED_HOSTS = [
    '.ngrok-free.app',  # Permite cualquier subdominio de ngrok (v3+)
    'localhost',
    '127.0.0.1',
    '[::1]',  # Para IPv6 local
]

# 4. Configuración adicional para ngrok (CSRF y CORS si usas APIs)
if DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'https://*.ngrok-free.app',  # Necesario para forms POST vía ngrok
    ]
    CORS_ALLOW_ALL_ORIGINS = True  # Solo en desarrollo, para APIs
# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vistas_quillayquen',  # Tu aplicación principal
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs
ROOT_URLCONF = 'quillayquen1.urls'

# Configuración de plantillas (MODIFICADO PARA TU ESTRUCTURA)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Vacío porque usaremos APP_DIRS
        'APP_DIRS': True,  # Buscará en app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Base de datos MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Quillayquen1',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
            'init_command': 'SET default_storage_engine=INNODB, collation_connection=utf8mb4_unicode_ci',
            'charset': 'utf8mb4',
        },
    }
}

# Internacionalización
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'vistas_quillayquen/static'),  # Tus archivos estáticos
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Para producción

# Archivos multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración para producción
if not DEBUG:
    ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'