# Generated by Django 3.0.8 on 2020-08-24 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20200824_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamer',
            name='social_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.SocialProfile'),
        ),
    ]
