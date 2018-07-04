from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from BaseUser.models import StudentCourse


class PasswordChgForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class StudentCourseForm(forms.ModelForm):
    # pass
    class Meta:
        model = StudentCourse
        fields = ('student', 'course', 'type_course',)
