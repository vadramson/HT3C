# Generated by Django 2.0.4 on 2018-05-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseUser', '0003_auto_20180518_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='contact_person_address',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='contact person address '),
        ),
    ]