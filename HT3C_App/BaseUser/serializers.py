from rest_framework import serializers

from Administration.models import ContinuousAssessment, Exam, Marks, CourseAverage, Semester, AcademicYear
from .models import Courses, StudentCourse


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"


class StudentCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField()
    course_credit = serializers.ReadOnlyField()
    course_code = serializers.ReadOnlyField()

    class Meta:
        model = StudentCourse
        fields = "__all__"


class ContinuousAssessmentSerializer(serializers.ModelSerializer):
    sem = serializers.ReadOnlyField()
    aca = serializers.ReadOnlyField()

    class Meta:
        model = ContinuousAssessment
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    sem = serializers.ReadOnlyField()
    aca = serializers.ReadOnlyField()

    class Meta:
        model = Exam
        fields = "__all__"


class AcademicYearSerializer(serializers.ModelSerializer):
    aca = serializers.ReadOnlyField()

    class Meta:
        model = AcademicYear
        fields = "__all__"


class SemesterSerializer(serializers.ModelSerializer):
    sem = serializers.ReadOnlyField()
    aca = serializers.ReadOnlyField()

    class Meta:
        model = Semester
        fields = "__all__"


class MarksSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField()
    course_credit = serializers.ReadOnlyField()
    course_code = serializers.ReadOnlyField()
    course_ca = serializers.ReadOnlyField()

    class Meta:
        model = Marks
        fields = "__all__"


class CourseAverageSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField()
    course_credit = serializers.ReadOnlyField()
    course_code = serializers.ReadOnlyField()

    class Meta:
        model = CourseAverage
        fields = "__all__"
