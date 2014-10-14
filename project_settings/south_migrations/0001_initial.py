# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Setting'
        db.create_table(u'project_settings_setting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name=u'project_setting', to=orm['sites.Site'])),
        ))
        db.send_create_signal(u'project_settings', ['Setting'])

    def backwards(self, orm):
        # Deleting model 'Setting'
        db.delete_table(u'project_settings_setting')

    models = {
        u'project_settings.setting': {
            'Meta': {'object_name': 'Setting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "u'project_setting'", 'to': u"orm['sites.Site']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        u'sites.site': {
            'Meta': {'object_name': 'Site', 'ordering': "(u'domain',)", 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['project_settings']
