# Locals
from rhgs.settings.base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-peuw@-)h##f#v54u2sr*n(jcsue35+y4!bn&^**)(qnkf1h%$0"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += [  # noqa
    "debug_toolbar",
    "debugtools",
    "localimages",
    "django_browser_reload",
]

MIDDLEWARE += [  # noqa
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": True,
    "root": {
        "level": "DEBUG",
    },
}

CSP_DEFAULT_SRC = None
CSP_STYLE_SRC = None
CSP_FONT_SRC = None
CSP_IMG_SRC = None

try:
    # Locals
    from rhgs.settings.local import *  # noqa
except ImportError:
    pass
