from django.contrib import admin

# Register your models here.
from Administration.models import Courses, Department, AcademicYear, Semester, ContinuousAssessment, Exam, Marks


class CoursesAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'credit', 'code')
    list_select_related = ('user',)


class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('user', 'accStart', 'accEnd')
    list_select_related = ('user',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'department_name', 'description', 'address', 'createdOn')
    list_filter = [
        'department_name'
    ]


class SemesterAdmin(admin.ModelAdmin):
    list_display = ('user', 'academic_year', 'semStart', 'semEnd', 'semester')
    list_filter = [
        'academic_year'
    ]


class ContinuousAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'semester', 'dateStart', 'dateEnd', 'ca')
    list_filter = [
        'ca'
    ]


class ExamAdmin(admin.ModelAdmin):
    list_display = ('user', 'semester', 'examStart', 'examEnd')
    list_filter = [
        'examStart'
    ]


class MarksAdmin(admin.ModelAdmin):
    list_display = ('user', 'student', 'score', 'course', 'exam')
    list_filter = [
        'exam'
    ]


admin.site.register(Courses, CoursesAdmin)
admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(ContinuousAssessment, ContinuousAssessmentAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Marks, MarksAdmin)
