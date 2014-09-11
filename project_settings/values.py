# -*- coding: utf-8 -*-
from django import forms
import six
from datetime import datetime, date
from django.forms import NumberInput, TextInput, DateInput, CheckboxInput, PasswordInput
from .models import Setting
from django.conf import settings as django_settings


class Value(forms.Field):
    def __init__(self, default, editable=False,
                 label=None,
                 prefix=None,
                 name=None,
                 description=None,
                 choices=None):
        self.default = default
        self.name = name
        self.prefix = prefix
        self.editable = editable
        self.description = description
        self.choices = choices
        self.label = label
        # if isinstance(self.formfield, forms.Field):
        #     self.formfield = self.formfield
        # else:
        self.formfield = self.formfield()

    def validate(self, value):
        return self.formfield.validate(value)

class IntegerValue(Value):
    formfield = forms.IntegerField
    # func = int


class StringValue(Value):
    formfield = forms.CharField
    # func = unicode


class PasswordValue(Value):
    formfield = forms.PasswordInput
    # func = unicode


class TextValue(Value):
    widget = TextInput
    func = unicode


class ListValue(Value):
    formfield = forms.CharField
    func = list


class DateValue(Value):
    formfield = forms.DateField


class BoolValue(Value):
    formfield = forms.BooleanField


class ClassValue(Value):
    formfield = forms.BooleanField


default_mapping = (((bool,), BoolValue),
                   ((list, tuple), ListValue),
                   ((six.string_types,), StringValue),
                   ((datetime, date), DateValue),
                   ((int, long), IntegerValue),)


def get_descriptor(value):
    if isinstance(value, Value):
        return value
    for types, descriptor in default_mapping:
        if isinstance(value, types):
            return descriptor(value)
