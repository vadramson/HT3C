# Generated by Django 2.0.4 on 2018-05-21 16:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0006_exam_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='continuousassessment',
            name='ca',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
