# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(max_length=30, choices=[('register', '\u6ce8\u518c'), ('forget', '\u627e\u56de\u5bc6\u7801'), ('update', '\u66f4\u65b0')]),
        ),
    ]
