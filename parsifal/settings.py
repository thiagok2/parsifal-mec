# -*- coding: utf-8 -*-
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from unipath import Path
import dj_database_url
from decouple import config, Csv
from mendeley import Mendeley
from django.utils.translation import ugettext_lazy as _

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)

PROJECT_DIR = Path(__file__).parent

DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': dj_database_url.config(
      default = config('DATABASE_URL'))
}

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

ADMINS = (
    ('Ivo Calado', 'ivo.calado@ifal.edu.br'),
)

MANAGERS = ADMINS

LANGUAGES = (
    ('pt-br', _('Portugues')),
    ('en', _('English')),
)

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'pt-br'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = PROJECT_DIR.parent.parent.child('media')
MEDIA_URL = '/media/'
FILE_UPLOAD_TEMP_DIR = '/tmp/'
FILE_UPLOAD_PERMISSIONS = 0644
FILE_UPLOAD_MAX_MEMORY_SIZE = 33554432

STATIC_ROOT = PROJECT_DIR.parent.parent.child('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
    PROJECT_DIR.child('reviews').child('comments').child('static'),
)

SECRET_KEY = config('SECRET_KEY')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'parsifal.urls'

WSGI_APPLICATION = 'parsifal.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',

    'reversion',
    'pagination_bootstrap',

    'parsifal.reviews',
    'parsifal.reviews.comments',
    'parsifal.reviews.planning',
    'parsifal.reviews.conducting',
    'parsifal.reviews.metaanalysis',
    'parsifal.reviews.reporting',
    'parsifal.reviews.settings',
    'parsifal.account_settings',
    'parsifal.activities',
    'parsifal.authentication',
    'parsifal.blog',
    'parsifal.core',
    'parsifal.help',
    'parsifal.library',
    'parsifal.search',
)

LOGIN_URL = '/signin/'
LOGOUT_URL = '/signout/'

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_FILE_PATH = PROJECT_DIR.parent.child('maildumps')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
URL_DEFAULT = config('URL_DEFAULT')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = 'Qeed <noreply@qeed.com.br>'
EMAIL_SUBJECT_PREFIX = '[Qeed] '
SERVER_EMAIL = 'application@parsif.al'

MENDELEY_ID = config('MENDELEY_ID', cast=int)
MENDELEY_SECRET = config('MENDELEY_SECRET')
MENDELEY_REDIRECT_URI = config('MENDELEY_REDIRECT_URI')
MENDELEY = Mendeley(MENDELEY_ID, client_secret=MENDELEY_SECRET, redirect_uri=MENDELEY_REDIRECT_URI)

DROPBOX_APP_KEY = config('DROPBOX_APP_KEY')
DROPBOX_SECRET = config('DROPBOX_SECRET')
DROPBOX_REDIRECT_URI = config('DROPBOX_REDIRECT_URI')

ELSEVIER_API_KEY = config('ELSEVIER_API_KEY')

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/%s/' % u.username,
}

LOCALE_PATHS = (
    PROJECT_DIR.child('locale'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/home/thiago/desenv/log-parsifal.log',
            'when': 'midnight',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'PARSIFAL_LOG': {
            'handlers': ['console', 'mail_admins','file'],
            'level': 'INFO'
        }
    }
}
