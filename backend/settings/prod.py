from .base import *
import os

# ---------------------------------------------------------
# PRODUCTION MODE
# ---------------------------------------------------------
DEBUG = False

ALLOWED_HOSTS = [
    "*",   # You can restrict this later to your domain
]

# ---------------------------------------------------------
# DATABASE — AWS RDS PostgreSQL
# ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


# ---------------------------------------------------------
# STATIC FILES — Whitenoise for production
# ---------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# ---------------------------------------------------------
# SECURITY HEADERS
# ---------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# If your load balancer terminates SSL, keep this False.
SECURE_SSL_REDIRECT = False

# ---------------------------------------------------------
# ALLOWED CORS HEADERS (optional)
# ---------------------------------------------------------
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
