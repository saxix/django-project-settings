# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from .models import Setting
from project_settings.forms import SettingsForm
from project_settings.registry import registry
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.contrib.messages import info


def admin_url(model, url, object_id=None):
    """
    Returns the URL for the given model and admin url name.
    """
    opts = model._meta
    url = "admin:%s_%s_%s" % (opts.app_label, opts.object_name.lower(), url)
    args = ()
    if object_id is not None:
        args = (object_id,)
    return reverse(url, args=args)


class SettingAdmin(admin.ModelAdmin):
    change_list_template = 'admin/project_settings/setting/change_list.html'

    def changelist_redirect(self):
        changelist_url = admin_url(Setting, "changelist")
        return HttpResponseRedirect(changelist_url)

    def add_view(self, *args, **kwargs):
        return self.changelist_redirect()

    def change_view(self, *args, **kwargs):
        return self.changelist_redirect()

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        settings_form = SettingsForm(request.POST or None)
        if settings_form.is_valid():
            settings_form.save()
            info(request, _("Settings were successfully updated."))
            return self.changelist_redirect()
        extra_context["settings_form"] = settings_form
        extra_context["title"] = u"%s %s" % (
            _("Change"), force_text(Setting._meta.verbose_name_plural))
        return super(SettingAdmin, self).changelist_view(request,
                                                         extra_context)


admin.site.register(Setting, SettingAdmin)

#
# from __future__ import unicode_literals
#
# from django.contrib import admin
# from django.contrib.messages import info
# from django.http import HttpResponseRedirect
# from django.utils.translation import ugettext_lazy as _
# try:
# from django.utils.encoding import force_text
# except ImportError:
# # Backward compatibility for Py2 and Django < 1.5
# from django.utils.encoding import force_unicode as force_text
#
# from mezzanine.conf.models import Setting
# from mezzanine.conf.forms import SettingsForm
# from mezzanine.utils.urls import admin_url
#
#
# class SettingsAdmin(admin.ModelAdmin):
#     """
#     Admin class for settings model. Redirect add/change views to the list
#     view where a single form is rendered for editing all settings.
#     """
#
#     class Media:
#         css = {"all": ("mezzanine/css/admin/settings.css",)}
#
#     def changelist_redirect(self):
#         changelist_url = admin_url(Setting, "changelist")
#         return HttpResponseRedirect(changelist_url)
#
#     def add_view(self, *args, **kwargs):
#         return self.changelist_redirect()
#
#     def change_view(self, *args, **kwargs):
#         return self.changelist_redirect()
#
#     def changelist_view(self, request, extra_context=None):
#         if extra_context is None:
#             extra_context = {}
#         settings_form = SettingsForm(request.POST or None)
#         if settings_form.is_valid():
#             settings_form.save()
#             info(request, _("Settings were successfully updated."))
#             return self.changelist_redirect()
#         extra_context["settings_form"] = settings_form
#         extra_context["title"] = u"%s %s" % (
#             _("Change"), force_text(Setting._meta.verbose_name_plural))
#         return super(SettingsAdmin, self).changelist_view(request,
#                                                             extra_context)
#
#
# admin.site.register(Setting, SettingsAdmin)
