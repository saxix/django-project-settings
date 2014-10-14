from __future__ import unicode_literals
import six
from _warnings import warn
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings as django_settings
from project_settings.registry import registry
from project_settings.values import default_mapping, get_descriptor
# from mezzanine.conf import register_setting


@python_2_unicode_compatible
class Options(object):
    def __init__(self):
        self.descriptors = {}

    def __str__(self):
        return "Options"


class Settings(object):
    """
    An object that provides settings via dynamic attribute access.

    Settings that are registered as editable will be stored in the
    database once the site settings form in the admin is first saved.
    When these values are accessed via this settings object, *all*
    database stored settings get retrieved from the database.

    When accessing uneditable settings their default values are used,
    unless they've been given a value in the project's settings.py
    module.

    The settings object also provides access to Django settings via
    ``django.conf.settings``, in order to provide a consistent method
    of access for all settings.
    """

    def __init__(self, prefix=""):
        """
        The ``_loaded`` attribute is a flag for defining whether
        editable settings have been loaded from the database. It
        defaults to ``True`` here to avoid errors when the DB table
        is first created. It's then set to ``False`` whenever the
        ``use_editable`` method is called, which should be called
        before using editable settings in the database.
        ``_editable_cache`` is the dict that stores the editable
        settings once they're loaded from the database, the first
        time an editable setting is accessed.
        """
        self._loaded = True
        if prefix:
            self._prefix = '%s_' % prefix
        else:
            self._prefix = ""
        self._editable_cache = {}

    def use_editable(self):
        """
        Empty the editable settings cache and set the loaded flag to
        ``False`` so that settings will be loaded from the DB on next
        access. If the conf app is not installed then set the loaded
        flag to ``True`` in order to bypass DB lookup entirely.
        """
        self._loaded = 'project_settings' not in getattr(self, "INSTALLED_APPS")
        self._editable_cache = {}

    def _load(self):
        """
        Load settings from the database into cache. Delete any settings from
        the database that are no longer registered, and emit a warning if
        there are settings that are defined in settings.py and the database.
        """
        from project_settings.models import Setting

        removed_settings = []
        conflicting_settings = []
        for setting_obj in Setting.objects.all():
            try:
                registry[setting_obj.name]
            except KeyError:
                # Setting in DB isn't registered (removed from code),
                # so add to removal list and skip remaining handling.
                removed_settings.append(setting_obj.name)
                continue

            # Convert DB value to correct type.
            descriptor = registry[setting_obj.name]["descriptor"]
            force_editable = registry[setting_obj.name]["force_editable"]
            # type_fn = self.TYPE_FUNCTIONS.get(setting_type, setting_type)
            type_fn = descriptor.formfield.to_python
            try:
                setting_value = type_fn(setting_obj.value)
            except ValueError:
                # Shouldn't occur, but just a safeguard
                # for if the db value somehow ended up as
                # an invalid type.
                setting_value = registry[setting_obj.name]["default"]

            # Only use DB setting if it's not defined in settings.py
            # module, in which case add it to conflicting list for
            # warning.
            if force_editable:
                self._editable_cache[setting_obj.name] = setting_value
            else:
                try:
                    getattr(django_settings, setting_obj.name)
                except AttributeError:
                    self._editable_cache[setting_obj.name] = setting_value
                else:
                    if setting_value != registry[setting_obj.name]["default"]:
                        conflicting_settings.append(setting_obj.name)

        if removed_settings:
            Setting.objects.filter(name__in=removed_settings).delete()
        if conflicting_settings:
            warn("These settings are defined in both settings.py and "
                 "the database: %s. The settings.py values will be used."
                 % ", ".join(conflicting_settings))
        self._loaded = True

    def __iter__(self):
        for entry in registry:
            yield (entry, getattr(self, entry))

    def __getattr__(self, name):
        name = "{}{}".format(self._prefix, name)
        # Lookup name as a registered setting or a Django setting.
        try:
            setting = registry[name]
        except KeyError:
            return getattr(django_settings, name)

        # First access for an editable setting - load from DB into cache.
        if setting["editable"] and not self._loaded:
            self._load()

        # Use cached editable setting if found, otherwise use the
        # value defined in the project's settings.py module if it
        # exists, finally falling back to the default defined when
        # registered.
        try:
            value = self._editable_cache[name]
            return value
        except KeyError:
            return getattr(django_settings, name, setting["default"])

settings = Settings()


class ProjectSettings(Settings):


    def __init__(self, prefix=""):
        self._registry = {}
        super(ProjectSettings, self).__init__(prefix)

    def register(self, *args, **kwargs):

        # kwargs['name'] = self._prefix + '_' + kwargs['name']
        kwargs['registry'] = self._registry
        return register_setting(*args, **kwargs)

    def __getattr__(self, item):
        fullname= "{}_{}".format(self.prefix, item)
        if item in self.defaults:
            return getattr(settings, fullname)




def register_setting(name=None, default=None, editable=False, descriptor=None,
                     label=None, description=None, prefix=None,
                     force_editable=False,
                     choices=None,
                     registry=registry):

    if name is None:
        raise TypeError("project_settings.conf.register_setting requires the "
                        "'name' keyword argument.")
    if force_editable:
        editable = True
    if editable and default is None:
        raise TypeError("Cannot register `%s`: project_settings.conf.register_setting requires the "
                        "'default' keyword argument when 'editable' is True.", name)

    if hasattr(django_settings, name):
        # editable = False
        default = getattr(django_settings, name)
        warn("`{}` cannot be edited as same setting is present in settings.py".format(name))

    if label is None:
        label = name.replace("_", " ").title()
    if descriptor is None:
        descriptor = get_descriptor(default)
    else:
        descriptor = descriptor(default)

    # if editable:
    #     Setting.objects.get_or_create(name=name,
    #                                   defaults={'value':default}, prefix=prefix or '')
    #
    registry[name] = {"name": name, "label": label, "editable": editable,
                      "force_editable": force_editable,
                      "description": description, "default": default,
                      "choices": choices, "descriptor": descriptor}

