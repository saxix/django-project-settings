# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('prefix', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=150)),
                ('value', models.CharField(max_length=2000)),
                ('site', models.ForeignKey(to='sites.Site', default=1, editable=False)),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
            },
            bases=(models.Model,),
        ),
    ]
