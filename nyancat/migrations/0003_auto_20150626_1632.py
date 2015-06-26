# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nyancat', '0002_person_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='url',
            field=models.CharField(default=b'd2b7d884f7a442bba1198e86e3ebb9b7', unique=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(default=b'8a9d27308c4d4072b185165d7688ceb3', unique=True, max_length=32),
        ),
    ]
