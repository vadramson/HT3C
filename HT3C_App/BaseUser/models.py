from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.
from Administration.models import Courses, Department


class StudentLevel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='Level')
    code_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='Code')

    def __str__(self):  # __unicode__ for Python 2
        return self.name_level


class Student(models.Model):
    ADMIN = 1
    TEACHER = 2
    STUDENT = 3

    ROLES = ((ADMIN, 'Admin'), (TEACHER, 'Teacher'), (STUDENT, 'Student'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.ForeignKey(StudentLevel, on_delete=models.CASCADE, related_name='Student_level')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='Student_Department',
                                   verbose_name='Student Department')
    phone = models.CharField(max_length=254, unique=True, blank=True)
    address = models.CharField(max_length=254, blank=True)
    matriculation = models.CharField(max_length=254, unique=True, blank=True)
    picture = models.ImageField(null=True, upload_to="%Y/%m/%d")
    birthDate = models.DateField(blank=True, null=True)
    birthPlace = models.CharField(max_length=254, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLES, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)
    instance.student.save()


class StudentCourse(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Student_Course', verbose_name="student")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='Student_Course',
                               verbose_name='Student Course')
    dateReg = models.DateTimeField(default=timezone.now)

    def __str__(self):  # __unicode__ for Python 2
        return self.course
