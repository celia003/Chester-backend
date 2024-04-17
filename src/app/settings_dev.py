from .settings_base import *
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(BASE_DIR, '.env_dev')
load_dotenv(dotenv_path)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  os.getenv('DB_NAME'),
        'USER':  os.getenv('DB_USER'),
        'HOST':  os.getenv('DB_HOST'),
        'PORT':  os.getenv('DB_PORT'),
        'PASSWORD': os.getenv('DB_PASSWORD')
    }
}

# Application definition

INSTALLED_APPS += [
    'silk',
]

APP_NAME = os.getenv('APP_NAME')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')

URL_BASE = os.getenv('URL_BASE')

AVOID_2FA = os.getenv("AVOID_2FA", 'False').lower() in ('true', '1', 't')

TOKEN_EXPIRED_AFTER_SECONDS = 60 * 60
TOKEN_RECREATED_AFTER_SECONDS = 10 * 60

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

AUTH_PASSWORD_RESET_TOKEN_GENERATOR = 'app.management.views.CustomPasswordResetTokenGenerator'

NOGAS_RNA = NOGASRestNotificationApi(
                service_endpoint=os.getenv('NOGAS_SERVICE_ENDPOINT'),
                connection_keystore_path=os.getenv('NOGAS_CERT_PATH'),
                connection_keystore_password=os.getenv('NOGAS_PSWD'),
                connection_keystore_type="PKCS12",
)
