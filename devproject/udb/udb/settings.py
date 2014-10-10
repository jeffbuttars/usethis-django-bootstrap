# Django settings for udb project.

import os
import sys
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_NAME = 'timehook'


# Are we in a test run?
IN_TESTING = 'test' in sys.argv

# Find out what the full path of the directory this
# settings file is in. This is the first step to making
# this settings file portable by having it automatically
# adapt to it's location on the file system
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Project version for tracking state of the project
# "YYYYMMDDpp" pp == pathc number for multiple versions
# in one day. Usually, pp is 00
PROJECT_NAME = 'udb'
_log_dir = os.getenv('DJANGO_LOG_DIR',
                     '/tmp/' + PROJECT_NAME)
if not os.path.exists(_log_dir):
    try:
        os.makedirs(_log_dir)
    except OSError:
        _log_dir = '/tmp/' + PROJECT_NAME + str(os.geteuid())
        if not os.path.exists(_log_dir):
            os.makedirs(_log_dir)

# By default we'll assume a production environment,
# which means no DEBUG by default. Here we check the
# shell environment to to see if the DJANGO_JBC_DEV
# variable is set. If it is, we turn on debugging.
#
# For instance, on your development machine you probably
# want it to be debug mode by default. In that case, add this
# to your ~/.bashrc file(without the quotes):
# 'export DJANGO_DEBUG=yes'
DEBUG = False
if os.getenv('DJANGO_DEBUG', ''):
    DEBUG = True

# Override the environment and explicity set DEBUG
# here if you wish to do that

if DEBUG:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!! Setting DEBUG = True !!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# We set up TEMPLATE_DEBUG to be the same as the DEBUG
# DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Set the root domain name for the project.
# this will act as the default domain for certain setings.
DOMAIN_NAME = 'usethisdjango.com'
STATIC_DOMAIN_NAME = 'static.usethisdjango.com'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

if DOMAIN_NAME == 'example.com':
    raise Exception(
        "You need set the DOMAIN_NAME variable in your settings.py")

if DEBUG:
    DOMAIN_NAME = PROJECT_NAME
else:
    print("Running in Production Mode")
    ALLOWED_HOSTS = [DOMAIN_NAME, STATIC_DOMAIN_NAME] + ALLOWED_HOSTS


ADMINS = (('Jeff Buttars', 'jeff@jeffbuttars.com'),
          )

# Mailer setup
# EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', '')
# EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', '')
# EMAIL_PORT = os.getenv('DJANGO_EMAIL_PORT', '')
# # The e-mail address Django will use to send FROM
# SERVER_EMAIL = os.getenv('DJANGO_EMAIL_SEND_FROM', EMAIL_HOST_USER)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Boise'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'
if DEBUG:
    STATIC_URL = '/static/'


# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '%sadmin/' % (STATIC_URL)

# Additional locations of static files
 # STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
# )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x+oyqezpi*0)subh(-3!%-3vt8mtp5+mc-huzi1o)-$7@v0@f)'

from django.conf import global_settings
# List of callables that know how to import templates from various sources.
# By default, we wrapp all loaders in the cached loader. This is a
# production scenario, and it's fast!
# During DEBUG, each template is re-constructed for each rendering.

if not DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader',
         global_settings.TEMPLATE_LOADERS),
    )

# Add custom context processors here.
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.contrib.auth.context_processors.auth",
    'usethis_bootstrap.context_processor.bootstrap_urls',
)


# MIDDLEWARE_CLASSES = (
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
# ) + global_settings.MIDDLEWARE_CLASSES
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'

# TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
# )

LOGIN_REDIRECT_URL = "/"

# APPEND_SLASH=True
JQUERY_VER = '2.0.3'
BOOTSTRAP_SETTINGS = {
    'use_cdn': False,
    # 'themes_dir': os.path.join(SITE_ROOT, 'bootstrap', 'static', 'themes'),
    'theme': 'simplex',
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'usethis_bootstrap',
    'sample',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s %(levelname)s:%(process)s '
                       '%(filename)s:%(lineno)s %(module)s::'
                       '%(funcName)s() %(message)s'),
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_all': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': _log_dir + '/django.log',
        },
    },
    'loggers': {

        'django': {
            'handlers': ['console', 'file_all'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },

        'django.request': {
            'handlers': ['mail_admins', 'console', 'file_all'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': True,
        },
        'django.debug': {
            'handlers': ['console', 'file_all'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        PROJECT_NAME: {
            'handlers': ['console', 'file_all'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        }
    }
}
