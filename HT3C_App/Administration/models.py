import random
import string
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _


# Create your models here.


class AcademicYear(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accStart = models.DateField(unique=True, blank=False, null=False)
    accEnd = models.DateField(unique=True, blank=False, null=False)

    def __str__(self):
        st = str(self.accStart)
        ed = str(self.accEnd)
        sl = ' / '
        return st + sl + ed


class Semester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='School_Year',
                                      verbose_name='Academic Year')
    semStart = models.DateField(unique=True, blank=False, null=False)
    semEnd = models.DateField(unique=True, blank=False, null=False)
    semester = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        academic_year = str(self.academic_year)
        of = ' OF '
        return self.semester + of + academic_year


class Department(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Author')
    department_name = models.CharField(unique=True, blank=False, null=False, max_length=255)
    description = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(unique=True, blank=False, null=False, max_length=255)
    createdOn = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.department_name


OPEN = 1
CLOSED = 0

CA_STATUS = ((OPEN, 'Open'), (CLOSED, 'Closed'))


class ContinuousAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='Semester', verbose_name='Semester')
    dateStart = models.DateField(unique=True, blank=False, null=False)
    dateEnd = models.DateField(unique=True, blank=False, null=False)
    ca = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(choices=CA_STATUS, verbose_name='CA Status')

    def __str__(self):
        sem = str(self.semester)
        spa = ' - '
        return self.ca + spa + sem


class Courses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(blank=True, null=True, max_length=255)
    credit = models.CharField(blank=True, null=True, max_length=255)
    code = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.course


OPEN = 1
CLOSED = 0

EXAM_STATUS = ((OPEN, 'Open'), (CLOSED, 'Closed'))


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='Semester_Exam',
                                 verbose_name='Semester Exam')
    examStart = models.DateField(unique=True, blank=False, null=False)
    examEnd = models.DateField(unique=True, blank=False, null=False)
    exam = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(choices=EXAM_STATUS, verbose_name='Exam Status')

    def __str__(self):
        sem = str(self.semester)
        spa = ' - '
        return self.exam + spa + sem


OPEN = 1
CLOSED = 0

RESIT_STATUS = ((OPEN, 'Open'), (CLOSED, 'Closed'))


class Resit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='Semester_Resit',
                                 verbose_name='Semester Resit')
    resit_start = models.DateField(unique=True, blank=False, null=False)
    resit_end = models.DateField(unique=True, blank=False, null=False)
    resit = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(choices=RESIT_STATUS, verbose_name='Resit Status')

    def __str__(self):
        sem = str(self.semester)
        spa = ' - '
        return self.resit + spa + sem


class Marks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Lecturer/Teacher')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Student', verbose_name='Student')
    score = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='Course', verbose_name='Course')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='Exam_Score', verbose_name='Exam Score',
                             blank=True, null=True)
    ca = models.ForeignKey(ContinuousAssessment, on_delete=models.CASCADE, related_name='CA_Score',
                           verbose_name='CA Score', blank=True, null=True)

    def __str__(self):
        stu = str(self.student)
        crs = str(self.course)
        scr = str(self.score)
        exa = str(self.exam)
        ca = str(self.ca)
        spa = ' - '
        return stu + spa + crs + spa + scr + spa + exa + spa + ca
