# Generated by Django 2.1.1 on 2018-09-24 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20180924_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='assignment',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='api.Assignment'),
        ),
    ]
