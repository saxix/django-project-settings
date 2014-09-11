SECRET_KEY = '1111'
TIME_ZONE = 'Europe/Rome'
USE_TZ = True
DEBUG = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SITE_ID = 1
INTERNAL_IPS = ("127.0.0.1",)

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        # "NAME": ":memory:",
        "NAME": "aaa.sqlite",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = ''
MEDIA_URL = STATIC_URL + "media/"
MEDIA_ROOT = ''
# Package/module name to import the root urlpatterns from for the project.
# ROOT_URLCONF = "%s.site.urls" % PROJECT_DIRNAME


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.contenttypes",
    "project_settings",
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    # "django.core.context_processors.debug",
    # "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    # "django.core.context_processors.tz",
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
)
#
# TEST_INT = 1
# TEST_CHAR = 'a'
# TEST_BOOL = False
