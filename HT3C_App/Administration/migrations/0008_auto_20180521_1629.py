# Generated by Django 2.0.4 on 2018-05-21 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0007_auto_20180521_1610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marks',
            old_name='ca_score',
            new_name='ca',
        ),
    ]
