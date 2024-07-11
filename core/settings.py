"""
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import environ
import sys

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ENV_PATH = os.environ.get("ENV_PATH", f"{BASE_DIR.parent}/envs/.env.local")
# now load the contents of the defined .env file
env = environ.Env()
if os.path.exists(ENV_PATH):
    print(f"loading ENV vars from {ENV_PATH}")
    environ.Env.read_env(ENV_PATH)
else:
    print("NO ENV_PATH found!")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", "default_key-this_is_insecure_and_should_be_changed")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = env.str("ALLOWED_HOSTS", "127.0.0.1").split(",")
INTERNAL_IPS = env.str("INTERNAL_IPS", "127.0.0.1").split(",")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "auditlog",
    "debug_toolbar",
    "django_extensions",
    "django_filters",
    "djangoaddicts.hostutils",
    "djangoaddicts.pygwalker",
    "djangoaddicts.signalcontrol",
    "drf_spectacular",
    "handyhelpers",
    "userextensions",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_filters",
    # project apps
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "handyhelpers.middleware.RequireLoginMiddleware",
    "userextensions.middleware.UserRecentsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "handyhelpers.context_processors.get_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env.str("DB_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "TEST_NAME": env.str("DB_TEST_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": env.str("DB_USER", "core"),
        "PASSWORD": env.str("DB_PASSWORD", "core"),
        "HOST": env.str("DB_HOST", "localhost"),
        "PORT": env.str("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(str(BASE_DIR), "staticroot")
STATIC_URL = "/static/"

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (os.path.join(str(BASE_DIR), "core/static"),)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


BASE_TEMPLATE = "base.htm"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/userextensions/user_login_redirect"
LOGIN_REDIRECT_URL_DEFAULT = "/"
SESSION_COOKIE_AGE = env.int("SESSION_COOKIE_AGE", 28800)
SKIP_FIXED_URL_LIST = ["/userextensions/list_recents/", "/userextensions/user_login_redirect/", "/"]
REQUIRED_LOGIN_IGNORE_PATHS = [
    "/accounts/login/",
    "/accounts/logout/",
    "/logout",
    "/admin/",
    "/admin/login/",
    "/handyhelpers/live",
    "/handyhelpers/ready",
    "/handyhelpers/starttime",
    "/handyhelpers/uptime",
]


# logging configuration
LOG_PATH = env.str('LOG_PATH', os.path.join(BASE_DIR, 'django_logs'))
DEFAULT_LOG_LEVEL = env.str('DEFAULT_LOG_LEVEL', 'INFO')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
    print(f'INFO: created log path: {LOG_PATH}')
else:
    print(f'INFO: using log path: {LOG_PATH}')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s",
            'datefmt': "%Y/%b/%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(str(LOG_PATH), 'django.log'),
            'maxBytes': 1024 * 1024 * 15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'user': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(str(LOG_PATH), 'user.log'),
            'maxBytes': 1024 * 1024 * 15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': DEFAULT_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },

    },
    'loggers': {
        'django': {
            'handlers': ['django', 'console'],
            'level': 'INFO',
        },
        'user': {
            'handlers': ['user', 'console'],
            'level': 'INFO',
        },
        '': {
            'handlers': ['console'],
            'level': DEFAULT_LOG_LEVEL,
        }
    },
}


# drf configuration
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ) if DEBUG else ("rest_framework.authentication.TokenAuthentication", ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "drf_excel.renderers.XLSXRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": env.int("DRF_PAGE_SIZE", 100),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "{{ project_name }} APIs",
    "DESCRIPTION": "RESTful APIs for {{ project_name }}",
    "VERSION": "1.0.0",
}

PROJECT_NAME = "{{ project_name }}"
PROJECT_DESCRIPTION = """{{ project_name }} is a super awesome project powered, in part, by amazing code provided by DjangoAddicts."""
PROJECT_VERSION = env.str("PROJECT_VERSION", "")
PROJECT_SOURCE = "https://github.com/djangoaddicts"

PYGWALKER_THEME = "light"
SESSION_COOKIE_SECURE = True
