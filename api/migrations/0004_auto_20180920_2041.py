# Generated by Django 2.1.1 on 2018-09-20 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180920_2040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attributes',
            old_name='message',
            new_name='validation_fail_message',
        ),
        migrations.RenameField(
            model_name='attributes',
            old_name='regex',
            new_name='validation_regex',
        ),
    ]
