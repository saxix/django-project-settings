# -*- coding: utf-8 -*-
#
from django.conf import settings as django_settings
from project_settings.registry import registry
from project_settings.values import default_mapping, get_descriptor


def register_setting(name=None, default=None, editable=False, descriptor=None,
                     label=None, description=None, prefix=None, choices=None):
    from project_settings.models import Setting

    if hasattr(django_settings, name):
        editable = False
        default = getattr(django_settings, name)

    if label is None:
        label = name.replace("_", " ").title()
    if descriptor is None:
        descriptor = get_descriptor(default)

    if editable:
        Setting.objects.get_or_create(name=name, value=default, prefix=prefix or '')

    registry[name] = {"name": name, "label": label, "editable": editable,
                      "description": description, "default": default,
                      "choices": choices, "descriptor": descriptor}


def merge_settings():
    from .conf import settings

    for setting, value in settings:
        setattr(django_settings, setting, value)

#
# def load_project_settings(settings):
# from project_settings.conf import settings
#
