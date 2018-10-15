# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180619_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(max_length=30, choices=[('register', '\u6ce8\u518c'), ('forget', '\u627e\u56de\u5bc6\u7801'), ('update_email', '\u66f4\u65b0\u90ae\u7bb1')]),
        ),
    ]
