# Generated by Django 5.0.6 on 2024-05-14 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customUser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]