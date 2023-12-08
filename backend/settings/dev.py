from backend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: don't include unknown hosts
ALLOWED_HOSTS = [
    "localhost",
    "host.docker.internal",
    "127.0.0.1",
]

# SECURITY WARNING: don't include unknown hosts
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http:\/\/(localhost|host\.docker\.internal|127\.0\.0\.1)\:8080$",
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email Server Configuration
# https://docs.djangoproject.com/en/3.2/topics/email/
# https://docs.djangoproject.com/en/3.2/topics/email/#email-backends

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
