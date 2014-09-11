# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Setting
from project_settings.registry import registry


class SettingAdmin(admin.ModelAdmin):
    change_list_template = 'admin/project_settings/setting/change_list.html'

    def changelist_view(self, request, extra_context=None):
        context = extra_context or {}
        context['registry'] = registry
        return super(SettingAdmin, self).changelist_view(request, context)


admin.site.register(Setting, SettingAdmin)
