import six
from datetime import datetime, date
from django.forms import NumberInput, TextInput, DateInput, CheckboxInput, PasswordInput
from django.test.signals import setting_changed
from .models import Setting
from django.conf import settings as django_settings


class Value(object):
    def __init__(self, default, editable=False,
                 label=None,
                 description=None,
                 choices=None):
        self._default = default
        self._name = None
        self._prefix = None
        self._editable = editable
        self._description = description
        self._choices = choices
        self._label = label

    def __get__(self, instance, owner):
        value = instance.defaults[self._name]
        if self._editable:
            try:
                value = Setting.objects.get(prefix=instance.prefix, name=self._name).value
            except:
                value = getattr(django_settings, self._name, value)
        else:
            value = getattr(django_settings, self._name, value)

        return self.func(value)

    def __set__(self, instance, value):
        if value is None:
            instance.defaults[self._name] = None
        else:
            instance.defaults[self._name] = self.func(value)


class IntegerValue(Value):
    widget = NumberInput
    func = int


class StringValue(Value):
    widget = TextInput
    func = unicode


class PasswordValue(Value):
    widget = PasswordInput
    func = unicode


class TextValue(Value):
    widget = TextInput
    func = unicode


class ListValue(Value):
    widget = TextInput
    func = list


class DateValue(Value):
    widget = DateInput
    func = datetime.strptime


class BoolValue(Value):
    widget = CheckboxInput
    func = bool


default_mapping = (((bool,), BoolValue),
                   ((list, tuple), ListValue),
                   ((six.string_types,), StringValue),
                   ((datetime, date), DateValue),
                   ((int, long), IntegerValue),
)


class SettingsBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(SettingsBase, cls).__new__

        for k, v in attrs['defaults'].items():
            for types, descriptor in default_mapping:
                if isinstance(v, types):
                    v = descriptor(v)
                    v._name = k
                    break
            else:
                if isinstance(v, Value):
                    v._name = k
                    attrs['defaults'][k] = v._default

            attrs[k] = v
        return super_new(cls, name, bases, attrs)


class ProjectSettings(six.with_metaclass(SettingsBase)):
    """
    Class to manage application related settings
    How to use:

    >>> from django.conf import settings
    >>> settings.APP_OVERRIDE = 'overridden'
    >>> settings.MYAPP_CALLBACK = 100
    >>> class MySettings(ProjectSettings):
    ...     defaults = {'ENTRY1': 'abc', 'ENTRY2': 123, 'OVERRIDE': None, 'CALLBACK':10}
    ...     def set_CALLBACK(self, value):
    ...         setattr(self, 'CALLBACK', value*2)

    >>> conf = MySettings("APP")
    >>> conf.ENTRY1
    'abc'
    >>> conf.OVERRIDE
    'overridden'

    >>> conf = MySettings("MYAPP")
    >>> conf.ENTRY2
    123
    >>> conf = MySettings("MYAPP")
    >>> conf.CALLBACK
    200

    """
    defaults = {}

    def __init__(self, prefix):
        """
        Loads our settings from django.conf.settings, applying defaults for any
        that are omitted.
        """
        self.prefix = prefix
        from django.conf import settings

        for name, default in six.iteritems(self.defaults):
            full_name = self.get_full_name(name)
            value = getattr(settings, full_name, default)
            self._set_attr(full_name, value)
        setting_changed.connect(self._handler)

    def get_full_name(self, name):
        if self.prefix:
            return (self.prefix + '_' + name).upper()
        return name.upper()

    def _set_attr(self, full_name, value):
        if self.prefix:
            full_name = full_name[len(self.prefix) + 1:]

        setattr(self, full_name, value)
        # setattr(django_settings, full_name, value)

    def _handler(self, sender, setting, value, **kwargs):
        if setting.startswith(self.prefix):
            self._set_attr(setting, value)
