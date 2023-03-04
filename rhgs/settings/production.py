# Standard Library
import os

# Third Party
import dj_database_url

# Locals
from .base import *  # noqa

DEBUG = False

env = os.environ.copy()

# It's a GOOD idea to lock this down.
ALLOWED_HOSTS = ["*"]

DATABASES["default"] = dj_database_url.config()  # noqa

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECRET_KEY = env["SECRET_KEY"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_CSS_HASHING_METHOD = "content"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


HONEYBADGER = {"API_KEY": env["HONEYBADGER_API_KEY"]}

MIDDLEWARE += [  # noqa
    "honeybadger.contrib.DjangoHoneybadgerMiddleware",
]

WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("SMTP_HOST")
EMAIL_HOST_USER = os.environ.get("SMTP_USER")
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASS")
EMAIL_PORT = os.environ.get("SMTP_PORT")
EMAIL_USE_TLS = True


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default",
    },
    "renditions": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "renditions",
    },
}

if "REDIS_URL" in os.environ:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.environ.get("REDIS_URL"),
        },
        "renditions": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.environ.get("REDIS_URL"),
        },
    }


try:
    # Locals
    from .local import *  # noqa
except ImportError:
    pass
