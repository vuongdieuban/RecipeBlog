# Generated by Django 2.0.7 on 2018-10-12 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_auto_20181012_1736'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='user',
            new_name='author',
        ),
    ]
