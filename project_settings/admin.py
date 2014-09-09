# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Setting


class SettingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Setting, SettingAdmin)
