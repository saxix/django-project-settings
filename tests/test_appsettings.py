# -*- coding: utf-8 -*-
import mock
from django.test.utils import override_settings
from django.conf import settings as django_settings
from project_settings.conf import settings
from project_settings.models import Setting
from .fixtures import *  # noqa
from project_settings.utils import register_setting

@pytest.mark.django_db
def test_register_not_editable():
    register_setting('TEST1', 10)
    assert settings.TEST1 == 10
    assert not Setting.objects.filter(name='TEST1').exists()


@pytest.mark.django_db
def test_register_editable():
    register_setting('TEST2', 12, editable=True)
    assert settings.TEST2 == 12
    assert Setting.objects.filter(name='TEST2').exists()


@pytest.mark.django_db
def test_register_load_value():
    with mock.patch('project_settings.conf.settings._loaded', False):
        register_setting('TEST_EDITABLE1', 12, editable=True)
        Setting(prefix='', name='TEST_EDITABLE1', value=99).save()
        assert settings.TEST_EDITABLE1 == 99


@pytest.mark.django_db
def test_default(sett):
    assert sett.EDITABLE2 == 11  # sanity check
    with override_settings(TEST_EDITABLE2=10):
        assert sett.EDITABLE2 == 10
        Setting(prefix='', name='TEST_EDITABLE2', value=99).save()
        del django_settings.TEST_EDITABLE2
        assert sett.EDITABLE2 == 99
