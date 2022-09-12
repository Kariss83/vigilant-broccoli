from . import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://0a4a8f6ffe4d4bea8331644c949bbe09@o1293076.ingest.sentry.io/6515779",
    integrations=[
        DjangoIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

SECRET_KEY = os.environ["DJANGO_KEY"]
DEBUG = False
ALLOWED_HOSTS = [
    "51.38.234.122",
    "purbeurre.gitgudat.com",
    "www.purbeurre.gitgudat.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",  # on utilise l'adaptateur postgresql
        "NAME": "purbeurre",  # le nom de notre base de données créée précédemment
        "USER": os.environ[
            "DB_USER"
        ],  # attention : remplacez par votre nom d'utilisateur !!
        "PASSWORD": os.environ["DB_PWD"],
        "HOST": "",
        "PORT": "5432",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Purbeurre <root@vps-8351387e.vps.ovh.net>"
