import os


def pytest_configure(config):
    from django.conf import settings

    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    # django.setup()
