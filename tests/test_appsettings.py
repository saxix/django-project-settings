# -*- coding: utf-8 -*-
from django.test.utils import override_settings
from project_settings.models import Setting
from .fixtures import *


def test_default(sett):
    assert sett.VAR1 == 12
    with override_settings(TEST_VAR1=10):
        assert sett.VAR1 == 10
    assert not sett.BOOL


def test_descriptors(sett):
    sett.INT1 = '111'
    assert sett.INT1 == 111

    sett.INT2 = '222'
    assert sett.INT2 == 222

    sett.CHAR1 = 'abc'
    assert sett.CHAR1 == 'abc'

    sett.CHAR2 = 'ghj'
    assert sett.CHAR2 == 'ghj'

    sett.CHAR2 = 'ghj'
    assert sett.CHAR2 == 'ghj'

    sett.BOOL = 1
    assert sett.BOOL

    sett.BOOL = True
    assert sett.BOOL

    sett.BOOL = False
    assert not sett.BOOL


@pytest.mark.django_db
def test_db_values(sett):
    assert sett.EDITABLE == 11
    Setting(prefix='TEST', name='EDITABLE', value=99).save()

    assert sett.EDITABLE == 99


@pytest.mark.django_db
def test_django_settings(django_sett):
    with override_settings(SESSION_EXPIRE_AT_BROWSER_CLOSE=False):
        assert not django_sett.SESSION_EXPIRE_AT_BROWSER_CLOSE

        Setting(prefix='', name='SESSION_EXPIRE_AT_BROWSER_CLOSE', value=1).save()
        assert django_sett.SESSION_EXPIRE_AT_BROWSER_CLOSE





