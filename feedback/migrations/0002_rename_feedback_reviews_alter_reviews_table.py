# Generated by Django 4.2.11 on 2024-05-01 15:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Feedback',
            new_name='Reviews',
        ),
        migrations.AlterModelTable(
            name='reviews',
            table='Reviews',
        ),
    ]
