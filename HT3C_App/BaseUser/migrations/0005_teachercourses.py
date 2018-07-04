# Generated by Django 2.0.4 on 2018-05-18 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0002_auto_20180518_1430'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BaseUser', '0004_student_contact_person_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administration.Courses')),
                ('levele', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BaseUser.StudentLevel', verbose_name='Level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
