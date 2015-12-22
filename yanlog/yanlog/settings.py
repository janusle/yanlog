"""
Django settings for yanlog project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

import cbs
import dj_database_url

cbs.DEFAULT_ENV_PREFIX = 'DJANGO_'


class Base(cbs.BaseSettings):

    SITE_ID = 1
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    FIXTURE_DIRS = [os.path.join(BASE_DIR, 'fixtures'), ]

    ALLOWED_HOSTS = ['127.0.0.1', 'yanle.me']
    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.flatpages',

        # Third party apps
        'disqus',
        'bootstrap3',

        # Local apps
        'common',
        'blog',
        'lettuce.django',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    )

    ROOT_URLCONF = 'yanlog.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    WSGI_APPLICATION = 'yanlog.wsgi.application'
    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

    def DATABASES(self):
        return {
            'default': dj_database_url.parse(self.DEFAULT_DB),
        }

    # Internationalization
    # https://docs.djangoproject.com/en/1.8/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.8/howto/static-files/

    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )

    @cbs.env
    def STATIC_ROOT(self):
        return ''

    @cbs.env
    def DISQUS_API_KEY(self):
        return ''

    @cbs.env
    def DISQUS_WEBSITE_SHORTNAME(self):
        return ''

    @cbs.env
    def DEFAULT_DB(self):
        return 'postgres://localhost/yanlog'

    @cbs.env
    def SECRET_KEY(self):
        return None


class Local(Base):
    """ Settings for local development """

    SECRET_KEY = 'mostm0ux_s!!9pshj0)wpn1#sf+a52kc*t*+jfp6%@088of5!!'

    DEBUG = True

    DEFAULT_DB = 'postgres://dev:dev@localhost:5434/yanlog'

    INSTALLED_APPS = Base.INSTALLED_APPS + (
        'debug_toolbar',
        'django_extensions',
    )


class Test(Base):
    """ Settings for testing env """

    @cbs.env
    def DEFAULT_DB(self):
        # Uses postgres started by docker-compose by default
        return 'postgres://dev:dev@localhost:5434/yanlog'

    SECRET_KEY = 'ul06ndw!fop^owsfzx1x#zh)!%2scv!#!ox1e^9%rrz1&v^bf-'


class Prod(Base):
    """ Settings for production """

    DEBUG = False


MODE = os.environ.get('DJANGO_MODE', 'Local').title()
cbs.apply(MODE, globals())
