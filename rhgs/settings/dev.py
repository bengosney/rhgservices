# Locals
from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-peuw@-)h##f#v54u2sr*n(jcsue35+y4!bn&^**)(qnkf1h%$0"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    # Locals
    from .local import *  # noqa
except ImportError:
    pass
