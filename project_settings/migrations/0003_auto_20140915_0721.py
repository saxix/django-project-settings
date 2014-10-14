# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20140912_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='site',
            field=models.ForeignKey(to='sites.Site', related_name='project_setting', editable=False, default=1),
        ),
    ]
