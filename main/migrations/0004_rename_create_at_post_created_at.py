# Generated by Django 4.1.5 on 2023-01-26 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='create_at',
            new_name='created_at',
        ),
    ]