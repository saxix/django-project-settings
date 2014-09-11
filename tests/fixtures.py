# -*- coding: utf-8 -*-
import pytest
from project_settings.conf import ProjectSettings
from project_settings.values import IntegerValue, StringValue, ListValue, BoolValue
from project_settings.conf import settings
from django.test.signals import setting_changed


def clear_cache(*a, **kw):
    settings._editable_cache={}
    settings._loaded=False


@pytest.fixture
@pytest.mark.django_db
def sett():
    class Sett(ProjectSettings):
        defaults = {
            'INT1': IntegerValue(11),
            # 'INT2': 22,
            'VAR1': 12,
            'CHAR1': StringValue('z'),
            # 'CHAR2': 'z',
            # 'LIST': [1, 2, 3],
            'BOOL': True,
            'EDITABLE1': IntegerValue(11, True),
            'EDITABLE2': IntegerValue(11, True),
        }

    return Sett('TEST')


@pytest.fixture
def django_sett():
    setting_changed.connect(clear_cache)

    class Sett(ProjectSettings):
        defaults = {
            'DEBUG': False,
            'SESSION_EXPIRE_AT_BROWSER_CLOSE': BoolValue(True, True),
            'INTERNAL_IPS': ListValue(["127.0.0.1"], True),
            'CHAR1': StringValue('z', True),
            'EDITABLE': IntegerValue(11, True)
        }

    return Sett('')
