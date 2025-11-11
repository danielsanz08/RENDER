import os
from pathlib import Path

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔹 Clave secreta y modo debug
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-insegura-para-desarrollo')
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.8']



# 🔹 Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps propias
    'libreria',
    'backup',
    

    # Terceros
    'django_extensions',
    'widget_tweaks',
]

# 🔹 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # útil si luego haces deploy
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔹 Configuración principal
ROOT_URLCONF = 'sistema.urls'
# Backup configuration
BACKUP_ROOT = os.path.join(BASE_DIR, 'backups')

# Asegúrate de que el directorio exista
if not os.path.exists(BACKUP_ROOT):
    os.makedirs(BACKUP_ROOT)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'sistema.wsgi.application'

# 🔹 Base de datos local (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'render',  # nombre de tu BD local
        'USER': 'root',
        'PASSWORD': 'Miclavesegura2025¡', 
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        },
    }
}

# 🔹 Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🔹 Internacionalización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 🔹 Archivos estáticos y media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 🔹 Tipo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔹 Autenticación personalizada
AUTHENTICATION_BACKENDS = [
    'libreria.backends.NameBackend',
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_USER_MODEL = 'libreria.CustomUser'

# 🔹 Redirecciones login/logout
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login_view'
LOGIN_URL = 'libreria:login'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 600  # La sesión expira después de 10 minutos
SESSION_SAVE_EVERY_REQUEST = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_TIMEOUT = 30  # 30 segundos
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "gestorccd@gmail.com"
EMAIL_HOST_PASSWORD = "utdf dxyn btiz dgjv"  # tu contraseña de aplicación
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
PASSWORD_RESET_TIMEOUT = 300  # 5 minutos

# 🔹 Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# 🔹 Sesiones y sitio
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SITE_NAME = 'hedybed'
