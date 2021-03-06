# Generated by Django 2.0.4 on 2018-05-21 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0003_auto_20180518_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='exam',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='marks',
            name='ca_score',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CA_Score', to='Administration.ContinuousAssessment', verbose_name='CA Score'),
        ),
        migrations.AlterField(
            model_name='marks',
            name='exam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Exam_Score', to='Administration.Exam', verbose_name='Exam Score'),
        ),
        migrations.AlterField(
            model_name='marks',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True),
        ),
        migrations.AlterField(
            model_name='marks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Lecturer/Teacher'),
        ),
    ]
