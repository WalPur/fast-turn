# Generated by Django 2.2.10 on 2020-03-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SoftWay', '0004_queue_lastm'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='time',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
