# Generated by Django 3.0.8 on 2020-08-14 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20200813_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmechanic',
            name='html',
            field=models.TextField(default=''),
        ),
    ]
