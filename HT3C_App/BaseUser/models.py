from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
from Administration.models import Courses, Department, AcademicYear


class StudentLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='Level')
    code_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='Code')

    def __str__(self):  # __unicode__ for Python 2
        return self.name_level


class Student(models.Model):
    ADMIN = 1
    TEACHER = 2
    STUDENT = 3

    MALE = 4
    FEMALE = 5

    MARRIED = 6
    SINGLE = 7

    ROLES = ((ADMIN, 'Admin'), (TEACHER, 'Teacher'), (STUDENT, 'Student'))
    GENDER = ((MALE, 'Male'), (FEMALE, 'Femaile'))
    MARITAL_STATUS = ((MARRIED, 'Married'), (SINGLE, 'Single'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.ForeignKey(StudentLevel, on_delete=models.CASCADE, related_name='Student_level', null=True,
                              blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='Student_Department',
                                   verbose_name='Student Department', blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='Academic_year',
                                      verbose_name='Academic Year', blank=True, null=True)
    phone = models.CharField(max_length=254, unique=True, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True)
    matriculation = models.CharField(max_length=254, unique=True, blank=True, null=True)
    picture = models.ImageField(null=True, upload_to="%Y/%m/%d", blank=True)
    birthDate = models.DateField(blank=True, null=True)
    birthPlace = models.CharField(max_length=254, blank=True, null=True)
    nationality = models.CharField(max_length=254, blank=True, null=True)
    contact_person_address = models.CharField(max_length=254, blank=True, null=True, verbose_name='contact person '
                                                                                                  'address ')
    degree_programm = models.CharField(max_length=254, blank=True, null=True)
    id_number = models.IntegerField(unique=True, verbose_name='ID Card Number', null=True, blank=True)
    region = models.CharField(max_length=254, blank=True, verbose_name='Region of Origin', null=True)
    role = models.PositiveSmallIntegerField(choices=ROLES, blank=True, null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER, blank=True, null=True)
    marital_status = models.PositiveSmallIntegerField(choices=MARITAL_STATUS, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python 2
        # return self.user.get_full_name
        return self.user.last_name


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)
    instance.student.save()


class StudentCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Student_Course',
                                verbose_name="student", null=True, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='Student_Course',
                               verbose_name='Student Course', null=True, blank=True)
    dateReg = models.DateTimeField(default=timezone.now)
    type_course = models.CharField(max_length=35, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.course


class TeacherCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    levele = models.ForeignKey(StudentLevel, on_delete=models.CASCADE, verbose_name='Level')
