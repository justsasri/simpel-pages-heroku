import os
from urllib.parse import urlparse

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SIMPEL_PAGE_MODEL = "simpel_pages.Page"
SIMPEL_PAGE_SITE_MODEL = "simpel_pages.RootPage"

SITE_ID = 1

SITE_NAME = env("SITE_NAME", str, default="example")

BASE_URL = env("BASE_URL", str, default="http://127.0.0.1:8000")

PAGE_CACHE_TIMEOUT = env("PAGE_CACHE_TIMEOUT", int, default=0)

INSTALLED_APPS = [
    "haystack",
    "apps.auth",
    "simpel_pages",
    "simpel_themes",
    "simpel_settings",
    "mptt",
    "filer",
    "tinymce",
    "django_rq",
    "polymorphic",
    "easy_thumbnails",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]


ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.auth.contexts.settings_export",
            ],
        },
    },
]


WSGI_APPLICATION = "server.wsgi.application"

COMMENTS_APP = "django_comments_xtd"
COMMENTS_XTD_MODEL = "simpel_discuss.models.Threat"
COMMENTS_XTD_FORM_CLASS = "simpel_discuss.forms.ThreatForm"
#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = b"Timendi causa est nescire. " b"Aequam memento rebus in arduis servare mentem."

# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = "webmaster@example.com"
COMMENTS_XTD_MAX_THREAD_LEVEL = 1  # default is 0
COMMENTS_XTD_LIST_ORDER = ("-thread_id", "order")  # default is ('thread_id', 'order')

# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = "helpdesk@example.com"

COMMENTS_XTD_APP_MODEL_OPTIONS = {
    "default": {
        "allow_flagging": True,
        "allow_feedback": True,
        "show_feedback": True,
        "who_can_post": "users",  # Valid values: 'all', users'
    }
}

# ------------------------------------------------------------------------------
# DATABASE
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# ------------------------------------------------------------------------------
# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = "authentication.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


######################################################
# SESSION & CACHE
######################################################

REDIS_URL = env("REDIS_URL", str, "redis://:habibie099secret@127.0.0.1:6379/0")

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 15  # Logout if inactive for 15 minutes
SESSION_SAVE_EVERY_REQUEST = True

if REDIS_URL:
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    SESSION_CACHE_ALIAS = "default"
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        },
    }
######################################################
# QUEUES
######################################################

REDIS_SSL = env("REDIS_SSL", bool, False)
RQ_DATABASE = 1
RQ_URL = urlparse(REDIS_URL)

RQ_QUEUES = {
    "default": {
        "HOST": RQ_URL.hostname,
        "USERNAME": RQ_URL.username,
        "PASSWORD": RQ_URL.password,
        "PORT": RQ_URL.port,
        "DB": RQ_DATABASE,
        "SSL": bool(REDIS_SSL),
        "SSL_CERT_REQS": None,
    },
}

# -----------------------------------------------------------------
# INTERNATIONALIZATION
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# -----------------------------------------------------------------

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("id", "Indonesia"),
    ("en", "English (United States)"),
]

# -----------------------------------------------------------------
# STATICFILE & STORAGE
# -----------------------------------------------------------------

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "/media/"

# -----------------------------------------------------------------
# CACHE
# -----------------------------------------------------------------

REDIS_URL = env("REDIS_URL", str, default=None)
SESSION_ENGINE = "django.contrib.sessions.backends.db"

if REDIS_URL:
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        },
    }


# SENTRY

SENTRY_DSN = env("SENTRY_DSN", str, default="")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

FAVICON_URL = "/favicon.ico"

SETTINGS_EXPORT = [
    "PAGE_CACHE_TIMEOUT",
    "BASE_URL",
    "SITE_NAME",
    "FAVICON_URL",
]

SETTINGS_EXPORT_VARIABLE_NAME = "django_settings"

TAGGIT_CASE_INSENSITIVE = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 300,
    "menubar": False,
    "plugins": "advlist, autolink, lists, link, image, charmap, print, preview, anchor, table,"
    "searchreplace, visualblocks, code, fullscreen, insertdatetime , media, table, paste,"
    "code, help, wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist indent table image| "
    "removeformat code help",
}

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(BASE_DIR, "search"),
        "STORAGE": "file",
        "POST_LIMIT": 128 * 1024 * 1024,
        "INCLUDE_SPELLING": True,
        "BATCH_SIZE": 100,
        # 'EXCLUDED_INDEXES': ['thirdpartyapp.search_indexes.BarIndex'],
    },
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": True},
}
