# -*- coding: utf-8 -*-
#
from editable_settings.conf import AppSettings
from django.conf import settings as django_settings


conf = AppSettings('')


def register_setting(name=None, label=None, editable=False, description=None,
                     default=None, choices=None, descriptor=None):
    if hasattr(django_settings, name):
        editable = False
    if label is None:
        label = name.replace("_", " ").title()

    conf.defaults[name] = descriptor(default=default,
                                     choices=choices,
                                     editable=editable,
                                     label=label,
                                     descriptor=descriptor)
    setattr(django_settings, name, default)
