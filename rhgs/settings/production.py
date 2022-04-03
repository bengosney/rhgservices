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

try:
    # Locals
    from .local import *  # noqa
except ImportError:
    pass
