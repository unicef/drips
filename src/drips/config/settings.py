import datetime
import os
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

SETTINGS_DIR = Path(__file__).parent
PACKAGE_DIR = SETTINGS_DIR.parent
DEVELOPMENT_DIR = PACKAGE_DIR.parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

DEBUG = env.bool("DEBUG")

DATABASES = {"default": env.db(default="postgres://postgres:pass@db:5432/postgres")}

INSTALLED_APPS = (
    "drips.apps.core",
    "drips.apps.report_metadata",
    "drips.apps.cost_centers",
    "drips.web",
    "constance",
    "sharepoint_rest_api",
    "unicef_security",
    "unicef_realm",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.admin",
    "django.contrib.humanize",
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "django_celery_beat",
    "django_celery_results",
    "djcelery_email",
    "corsheaders",
    "social_django",
    "admin_extra_buttons",
    "adminactions",
    "rest_framework_social_oauth2",
    "unicef_vision.vision",
    "post_office",
    "unicef_notification",
)

MIDDLEWARE = (
    # 'unicef_security.middleware.HealthCheckMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "unicef_security.middleware.UNICEFSocialAuthExceptionMiddleware",
)

AUTHENTICATION_BACKENDS = (
    "unicef_security.backends.UNICEFAzureADTenantOAuth2Ext",
    "django.contrib.auth.backends.ModelBackend",
)


# path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
MEDIA_ROOT = env("MEDIA_ROOT", default="/tmp/etools/media/")
STATIC_ROOT = env("STATIC_ROOT", default=os.path.join(BASE_DIR, "static"))
MEDIA_URL = "/dm-media/"
STATIC_URL = env("STATIC_URL", default="/static/")
STATICFILES_DIRS = []
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = (
    env("ALLOWED_HOST", default="localhost"),
    "0.0.0.0",
)

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_URL = "/drips/accounts/logout"
LOGOUT_REDIRECT_URL = "/landing/"

# TIME_ZONE = env('TIME_ZONE')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"
ugettext = lambda s: s  # noqa
LANGUAGES = (
    ("es", ugettext("Spanish")),
    ("fr", ugettext("French")),
    ("en", ugettext("English")),
    ("ar", ugettext("Arabic")),
)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
SITE_ID = 1
INTERNAL_IPS = ["127.0.0.1", "localhost"]

USE_I18N = True
USE_TZ = True


CACHES = {
    "default": {
        # 'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/0"),
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake',
#     }
# }


ROOT_URLCONF = "drips.config.urls"
WSGI_APPLICATION = "drips.config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(PACKAGE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                # Already defined Django-related contexts here
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "INFO"},
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

AUTH_USER_MODEL = "unicef_security.User"

HOST = env("HOST", default="http://localhost:8000")

CELERY_ACCEPT_CONTENT = ["pickle", "json", "application/text"]
CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_BROKER_VISIBILITY_VAR = env("CELERY_VISIBILITY_TIMEOUT", default=1800)  # in seconds
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": int(CELERY_BROKER_VISIBILITY_VAR)}
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"
# Sensible settings for celery
CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER", default=False)
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_WORKER_DISABLE_RATE_LIMITS = False
CELERY_TASK_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_RESULT_EXPIRES = 600
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# django-cors-headers: https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = env("CORS_ORIGIN_ALLOW_ALL", default=False)


JWT_AUTH = {
    "JWT_VERIFY": False,  # this requires private key
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LEEWAY": 60,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=30000),
    "JWT_AUDIENCE": None,
    "JWT_ISSUER": None,
    "JWT_ALLOW_REFRESH": False,
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),
    "JWT_AUTH_HEADER_PREFIX": "JWT",
    "JWT_SECRET_KEY": SECRET_KEY,
    "JWT_DECODE_HANDLER": "rest_framework_jwt.utils.jwt_decode_handler",
    # Keys will be set in core.apps.Config.ready()
    "JWT_PUBLIC_KEY": "?",
    # 'JWT_PRIVATE_KEY': wallet.get_private(),
    # 'JWT_PRIVATE_KEY': None,
    "JWT_ALGORITHM": "RS256",
}
SENTRY_DSN = env("SENTRY_DSN", default=None)  # noqa: F405

if SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # by default this is False, must be set to True so the library attaches the request data to the event
        send_default_pii=True,
        integrations=[DjangoIntegration(), CeleryIntegration()],
    )

CONSTANCE_CONFIG = {
    "DEFAULT_GROUP": ("", "drips"),
}

if DEBUG:  # pragma: no cover
    INSTALLED_APPS += ("debug_toolbar",)  # noqa
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)  # noqa
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TEMPLATE_CONTEXT": True,
    }


INSIGHT_URL = env.str("INSIGHT_URL", "http://invalid_vision_url")
INSIGHT_LOGGER_MODEL = "vision.VisionLog"

INSIGHT_SUB_KEY = env.str("INSIGHT_SUB_KEY", "invalid_vision_password")

REALM_TARGET_MODEL = "unicef_realm.BusinessArea"

SHELL_PLUS_PRE_IMPORTS = (("drips.config", "celery"),)

POST_OFFICE = {"DEFAULT_PRIORITY": "now", "BACKENDS": {"default": "djcelery_email.backends.CeleryEmailBackend"}}

DEFAULT_FROM_EMAIL = "drips@unicef.org"
EMAIL_BACKEND = "unicef_notification.backends.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env("EMAIL_PORT", default=25)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env("EMAIL_USE_SSL", default=False)

SOCIAL_AUTH_KEY = env.str("AZURE_CLIENT_ID")
SOCIAL_AUTH_SECRET = env.str("AZURE_CLIENT_SECRET")
SOCIAL_AUTH_TENANT_ID = env.str("AZURE_TENANT")
SOCIAL_AUTH_RESOURCE = "https://graph.microsoft.com/"

SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_SANITIZE_REDIRECTS = False
SOCIAL_AUTH_JSONFIELD_ENABLED = True
POLICY = env("AZURE_B2C_POLICY_NAME", default="B2C_1A_UNICEF_SOCIAL_signup_signin")
SOCIAL_PASSWORD_RESET_POLICY = env("AZURE_B2C_PASS_RESET_POLICY", default="B2C_1_PasswordResetPolicy")
SOCIAL_AUTH_USER_MODEL = "unicef_security.User"

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "unicef_security.graph.get_unicef_user",
    "unicef_security.graph.default_group",
)

USER_FIELDS = ["username", "email", "first_name", "last_name"]

DRIPS_SOURCE_ID = env("DRIPS_SOURCE_ID", default=None)

MATOMO_SITE_TRACKER = env("MATOMO_SITE_TRACKER", default="https://unisitetracker.unicef.io/")
MATOMO_SITE_ID = env("MATOMO_SITE_ID", default=None)
