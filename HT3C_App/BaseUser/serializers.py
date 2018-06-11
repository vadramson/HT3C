from rest_framework import serializers
from .models import Courses, StudentCourse


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"


class StudentCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField()

    class Meta:
        model = StudentCourse
        fields = "__all__"
