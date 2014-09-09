# -*- coding: utf-8 -*-
import pytest
from project_settings.conf import ProjectSettings, IntegerValue, StringValue, ListValue, BoolValue


@pytest.fixture
@pytest.mark.django_db
def sett():
    class Sett(ProjectSettings):
        defaults = {
            'INT1': IntegerValue(11),
            'INT2': 22,
            'VAR1': 12,
            'CHAR1': StringValue('z'),
            'CHAR2': 'z',
            'LIST': [1, 2, 3],
            'BOOL': True,
            'EDITABLE': IntegerValue(11, True)
        }

    return Sett('TEST')


@pytest.fixture
def django_sett():
    class Sett(ProjectSettings):
        defaults = {
            'DEBUG': False,
            'SESSION_EXPIRE_AT_BROWSER_CLOSE': BoolValue(True, True),
            'INTERNAL_IPS': ListValue(["127.0.0.1"], True),
            'CHAR1': StringValue('z', True),
            'EDITABLE': IntegerValue(11, True)
        }

    return Sett('')
