# Generated by Django 4.1.5 on 2023-02-01 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_post_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='group',
            field=models.BooleanField(default=False),
        ),
    ]
