# Generated by Django 2.0.4 on 2018-06-07 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Administration', '0010_marks_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseAverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Averages Score')),
                ('divisor', models.IntegerField(verbose_name='Divisors')),
                ('total', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Total Scores')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Course_Avg', to='Administration.Courses', verbose_name='Course Average')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_Avgs', to='Administration.Semester', verbose_name='Semester.')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Student_Averages', to=settings.AUTH_USER_MODEL, verbose_name='Student`s Averages')),
            ],
        ),
        migrations.CreateModel(
            name='FinalScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True)),
            ],
        ),
    ]
