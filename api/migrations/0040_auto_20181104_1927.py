# Generated by Django 2.1.1 on 2018-11-05 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20181104_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='score',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
    ]
