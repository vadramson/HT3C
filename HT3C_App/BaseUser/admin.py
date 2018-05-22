from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from BaseUser.models import Student, StudentLevel, StudentCourse, TeacherCourses


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline,)
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role', 'get_birth_date', 'get_departmet',
    'get_birth_place')
    list_select_related = ('student',)


    def get_departmet(self, instance):
        return instance.student.department

    get_departmet.short_description = 'Student`s Dpt.'

    def get_role(self, instance):
        return instance.student.role

    get_role.short_description = 'User Role'

    def get_birth_date(self, instance):
        return instance.student.birthDate

    get_birth_date.short_description = 'Birth Date'

    def get_birth_place(self, instance):
        return instance.student.birthPlace

    get_birth_place.short_description = 'Birth Place'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)



class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'dateReg')
    list_filter = [
        'course'
    ]


class StudentLevelCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name_level', 'code_level')
    list_filter = [
        'name_level'
    ]


class TeacherCoursesAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'levele')
    list_search = 'user'
    list_filter = [
        'course'
    ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(StudentLevel, StudentLevelCourseAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(TeacherCourses, TeacherCoursesAdmin)
