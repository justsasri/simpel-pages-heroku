import dj_database_url
import django_heroku

from .base import *  # NOQA
from .base import env

USE_TLS = env("USE_TLS", bool, True)
DEBUG = env("DEBUG", bool, False)
DOMAIN = env("DOMAIN", str, default="localhost")
ALLOW_WILD_CARD = env("ALLOW_WILD_CARD", bool, default=False)
SECRET_KEY = env("SECRET_KEY", str, default="django-insecure")

ALLOWED_HOSTS = [
    "www.%s" % DOMAIN,
    DOMAIN,
    env("DIGITAL_OCEAN_IP_ADDRESS", str, default="127.0.0.1"),
]

if ALLOW_WILD_CARD:
    ALLOWED_HOSTS += [".%s" % DOMAIN]

STORAGE_TYPE = env("STORAGE_TYPE", None)

if STORAGE_TYPE == "cloudinary":
    CLOUDINARY_CLOUD_NAME = env("CLOUDINARY_CLOUD_NAME", str, default="")
    CLOUDINARY_API_KEY = env("CLOUDINARY_API_KEY", str, default="")
    CLOUDINARY_API_SECRET = env("CLOUDINARY_API_SECRET", str, default="")
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
        "API_KEY": CLOUDINARY_API_KEY,
        "API_SECRET": CLOUDINARY_API_SECRET,
    }
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
elif STORAGE_TYPE == "whitenoise":
    MIDDLEWARE += [  # NOQA
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES["default"] = dj_database_url.config(conn_max_age=600)  # NOQA

DEPLOYMENT_ENV = env("DEPLOYMENT_ENV", str, default="docker")

if DEPLOYMENT_ENV == "heroku":
    django_heroku.settings(locals())
