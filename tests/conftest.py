import os

from django.conf import settings
from oscar.defaults import OSCAR_SETTINGS
from oscar import OSCAR_MAIN_TEMPLATE_DIR, get_core_apps
from stores import OSCAR_STORES_MAIN_TEMPLATE_DIR


ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
location = lambda x: os.path.join(ROOT_DIR, x)
GEOIP_PATH = location('sandbox/geoip')
GEOIP_COUNTRY = location('sandbox/geoip/GeoIP.dat')
GEOIP_CITY = location('sandbox/geoip/GeoIPCity.dat')


def pytest_configure():
    location = lambda x: os.path.join(
        os.path.dirname(os.path.realpath(__file__)), x)

    test_settings = OSCAR_SETTINGS.copy()
    test_settings.update(dict(
        DATABASES={
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'oscar_stores',
                'USER': 'sample_role',
                'PASSWORD': 'sample_password',
                'HOST': '127.0.0.1',
                'PORT': 5432,
            }
        },
        SITE_ID=1,
        MEDIA_ROOT=location('public/media'),
        MEDIA_URL='/media/',
        STATIC_URL='/static/',
        STATICFILES_DIRS=(location('static/'),),
        STATIC_ROOT=location('public'),
        STATICFILES_FINDERS=(
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'oscar.apps.basket.middleware.BasketMiddleware',
        ),
        ROOT_URLCONF='sandbox.sandbox.urls',
        TEMPLATES=[
            {
                # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
                'DIRS': [
                    location('templates'),
                    OSCAR_STORES_MAIN_TEMPLATE_DIR,
                    OSCAR_MAIN_TEMPLATE_DIR
                ],
                'OPTIONS': {
                    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
                    # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
                    'loaders': [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ],
                    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        # Oscar specific
                        'oscar.apps.search.context_processors.search_form',
                        'oscar.apps.promotions.context_processors.promotions',
                        'oscar.apps.checkout.context_processors.checkout',
                        'oscar.core.context_processors.metadata',
                        'oscar.apps.customer.notifications.context_processors.notifications',
                    ],
                },
            },
        ],
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'django.contrib.gis',
            'django.contrib.flatpages',
            'compressor',
            'widget_tweaks',
        ] + get_core_apps() + [
            'stores',
        ],
        AUTHENTICATION_BACKENDS=(
            'oscar.apps.customer.auth_backends.Emailbackend',
            'django.contrib.auth.backends.ModelBackend',
        ),
        LOGIN_REDIRECT_URL='/accounts/',
        APPEND_SLASH=True,
        HAYSTACK_CONNECTIONS={
            'default': {
                'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
            },
        },
        GEOIP_PATH = GEOIP_PATH,
        GEOIP_COUNTRY = GEOIP_COUNTRY,
        GEOIP_CITY = GEOIP_CITY,
        COMPRESS_ENABLED=False,
        TEST_RUNNER='django.test.runner.DiscoverRunner',
    ))
    settings.configure(**test_settings)
