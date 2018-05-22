from builtins import print

from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Min, Sum, Avg, Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import now
from httplib2 import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
# from .serializers import ProductSerializer, UserSerializer, TabsSerializer, OrdersSerializer, ProfileSerializer, \
#      SalesSerializer, LossSerializer, ExpenseSerializer, AvarisSerializer, PurchasesSerializer, AttendanceSerializer\

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token

# Create your views here.
from Administration.models import Semester, ContinuousAssessment, Exam, Marks, Courses
from BaseUser.forms import PasswordChgForm, StudentCourseForm
from BaseUser.models import StudentCourse, TeacherCourses


@login_required
def home(request):
    # return render(request, 'index.html')
    return render(request, 'home/home.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChgForm(data=request.POST, user=request.user)
        if form.is_valid():
            print('valid')
            form.save()
            print('valid')
            pwd_updated = 'Password Updated'
            args = {'pwd_updated': pwd_updated}
            update_session_auth_hash(request, form.user)
            return render(request, 'home/home.html', args)
        else:
            pwd_updated = 'Password Not Updated'
            print('Not Valid')
            form = PasswordChgForm(user=request.user)
            args = {
                'pwd_updated': pwd_updated,
                'form': form
            }
            return render(request, 'home/change_password.html', args)
    else:
        form = PasswordChgForm(user=request.user)
        return render(request, 'home/change_password.html', {'form': form})


@login_required
def course_reg_home(request):
    ac_yr = request.user.student.academic_year
    # sem_response = Semester.objects.all().filter(Q(academic_year=ac_yr) & Q(semStart__lte=datetime.datetime.today()) & Q(semEnd__gte=datetime.datetime.today()))
    sem_response = Semester.objects.all().filter(Q(academic_year=ac_yr) & Q(semStart__lte=datetime.datetime.today()))
    sem = list(sem_response)
    print(datetime.datetime.today())
    print(sem)
    return render(request, 'course_registration/information.html', {'sem': sem})


# MAJOR COURSES VIEWS

@login_required
def major_reg_course_list(request):
    register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Major').order_by('-id')
    return render(request, 'course_registration/major/major_list.html', {"register_courses": register_courses})


@login_required
def save_major_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            print('save_major_form is valid')
            course = form.cleaned_data['course']
            print(course)
            test_register_courses = StudentCourse.objects.all().filter(student=request.user, course=course).order_by(
                '-id')
            if test_register_courses.exists():
                data['registered'] = True
            else:
                form.save()
                data['form_is_valid'] = True
            register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Major').order_by(
                '-id')
            data['html_major_list'] = render_to_string('course_registration/major/includes/partial_major_list.html',
                                                       {"register_courses": register_courses})
        else:
            data['form_is_not_valid'] = True
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def major_create(request):
    if request.method == 'POST':
        form = StudentCourseForm(request.POST)
    else:
        form = StudentCourseForm()
    return save_major_form(request, form, 'course_registration/major/includes/partial_major_create.html')


@login_required
def major_delete(request, pk):
    print('Attempting to drop Major')
    major = get_object_or_404(StudentCourse, pk=pk)
    data = dict()
    if request.method == 'POST':
        major.delete()
        data['major_deleted'] = True
        register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Major').order_by('-id')
        data['html_major_list'] = render_to_string('course_registration/major/includes/partial_major_list.html',
                                                   {"register_courses": register_courses})
    else:
        context = {'major': major}
        data['html_form'] = render_to_string('course_registration/major/includes/partial_major_delete.html', context,
                                             request=request)
    return JsonResponse(data)


# MINOR COURSES VIEWS

@login_required
def minor_reg_course_list(request):
    register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Minor').order_by('-id')
    return render(request, 'course_registration/minor/minor_list.html', {"register_courses": register_courses})


@login_required
def save_minor_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            print('save_minor_form is valid')
            course = form.cleaned_data['course']
            print(course)
            test_register_courses = StudentCourse.objects.all().filter(student=request.user, course=course).order_by(
                '-id')
            if test_register_courses.exists():
                data['registered'] = True
            else:
                form.save()
                data['form_is_valid'] = True
            register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Minor').order_by(
                '-id')
            data['html_minor_list'] = render_to_string('course_registration/minor/includes/partial_minor_list.html',
                                                       {"register_courses": register_courses})
        else:
            data['form_is_not_valid'] = True
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def minor_create(request):
    if request.method == 'POST':
        form = StudentCourseForm(request.POST)
    else:
        form = StudentCourseForm()
    return save_minor_form(request, form, 'course_registration/minor/includes/partial_minor_create.html')


@login_required
def minor_delete(request, pk):
    print('Attempting to drop minor')
    minor = get_object_or_404(StudentCourse, pk=pk)
    data = dict()
    if request.method == 'POST':
        minor.delete()
        data['minor_deleted'] = True
        register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Minor').order_by('-id')
        data['html_minor_list'] = render_to_string('course_registration/minor/includes/partial_minor_list.html',
                                                   {"register_courses": register_courses})
    else:
        context = {'minor': minor}
        data['html_form'] = render_to_string('course_registration/minor/includes/partial_minor_delete.html', context,
                                             request=request)
    return JsonResponse(data)


# ELECTIVE COURSES VIEWS

@login_required
def elective_reg_course_list(request):
    register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Elective').order_by('-id')
    return render(request, 'course_registration/elective/elective_list.html', {"register_courses": register_courses})


@login_required
def save_elective_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            print('save_elective_form is valid')
            course = form.cleaned_data['course']
            print(course)
            test_register_courses = StudentCourse.objects.all().filter(student=request.user, course=course).order_by(
                '-id')
            if test_register_courses.exists():
                data['registered'] = True
            else:
                form.save()
                data['form_is_valid'] = True
            register_courses = StudentCourse.objects.all().filter(student=request.user,
                                                                  type_course='Elective').order_by(
                '-id')
            data['html_elective_list'] = render_to_string(
                'course_registration/elective/includes/partial_elective_list.html',
                {"register_courses": register_courses})
        else:
            data['form_is_not_valid'] = True
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def elective_create(request):
    if request.method == 'POST':
        form = StudentCourseForm(request.POST)
    else:
        form = StudentCourseForm()
    return save_elective_form(request, form, 'course_registration/elective/includes/partial_elective_create.html')


@login_required
def elective_delete(request, pk):
    print('Attempting to drop elective')
    elective = get_object_or_404(StudentCourse, pk=pk)
    data = dict()
    if request.method == 'POST':
        elective.delete()
        data['elective_deleted'] = True
        register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Elective').order_by(
            '-id')
        data['html_elective_list'] = render_to_string(
            'course_registration/elective/includes/partial_elective_list.html',
            {"register_courses": register_courses})
    else:
        context = {'elective': elective}
        data['html_form'] = render_to_string('course_registration/elective/includes/partial_elective_delete.html',
                                             context,
                                             request=request)
    return JsonResponse(data)


# REQUIRED COURSES VIEWS

@login_required
def required_reg_course_list(request):
    register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Required').order_by('-id')
    return render(request, 'course_registration/required/required_list.html', {"register_courses": register_courses})


@login_required
def save_required_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            print('save_required_form is valid')
            course = form.cleaned_data['course']
            print(course)
            test_register_courses = StudentCourse.objects.all().filter(student=request.user, course=course).order_by(
                '-id')
            if test_register_courses.exists():
                data['registered'] = True
            else:
                form.save()
                data['form_is_valid'] = True
            register_courses = StudentCourse.objects.all().filter(student=request.user,
                                                                  type_course='Required').order_by(
                '-id')
            data['html_required_list'] = render_to_string(
                'course_registration/required/includes/partial_required_list.html',
                {"register_courses": register_courses})
        else:
            data['form_is_not_valid'] = True
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def required_create(request):
    if request.method == 'POST':
        form = StudentCourseForm(request.POST)
    else:
        form = StudentCourseForm()
    return save_required_form(request, form, 'course_registration/required/includes/partial_required_create.html')


@login_required
def required_delete(request, pk):
    print('Attempting to drop required')
    required = get_object_or_404(StudentCourse, pk=pk)
    data = dict()
    if request.method == 'POST':
        required.delete()
        data['required_deleted'] = True
        register_courses = StudentCourse.objects.all().filter(student=request.user, type_course='Required').order_by(
            '-id')
        data['html_required_list'] = render_to_string(
            'course_registration/required/includes/partial_required_list.html',
            {"register_courses": register_courses})
    else:
        context = {'required': required}
        data['html_form'] = render_to_string('course_registration/required/includes/partial_required_delete.html',
                                             context,
                                             request=request)
    return JsonResponse(data)


# FINAL REGISTERED COURSES

@login_required
def final_reg_course_list(request):
    register_courses = StudentCourse.objects.all().filter(student=request.user).order_by('-id')
    return render(request, 'course_registration/final/final_list.html', {"register_courses": register_courses})


# MY COURSES

@login_required
def my_courses_list(request):
    courses = TeacherCourses.objects.all().filter(user=request.user).order_by('-id')
    return render(request, 'my_courses/myCourses_list.html', {"courses": courses})


@login_required
def fill_marks(request, pk):
    global test_marks_list
    if request.method == 'POST':
        ex = request.POST.get('exam')
        c = request.POST.get('ca')
        fat_1 = ''
        if c == '' and ex != '':
            fat_1 = ''
        if c != '' and ex == '':
            fat_1 = ''
        if c != '' and ex != '':
            fat_1 = 'Both Filled'
        if c == '' and ex == '':
            fat_1 = 'Both Empty'

        if fat_1 == '':
            courses = get_object_or_404(TeacherCourses, pk=pk)
            course = courses.course
            stus = StudentCourse.objects.all().filter(course=course).order_by('id')
            print('Post Received')
            ct = stus.count()
            print(ct)
            course_id = request.POST.get('course_id')
            score_list = request.POST.getlist('score')
            student_list = request.POST.getlist('student')
            print('First score List')
            print(score_list)
            print('First student List')
            print(student_list)
            stu_scr = zip(score_list, student_list)
            st = []
            mrk_list = []
            for scores, stdts in stu_scr:
                type_score = ''
                mark = Marks()
                if scores == '':
                    scores = 0
                score = scores
                # print(score)
                sts = stdts
                # print(sts)
                student = get_object_or_404(User, pk=sts)
                crse = get_object_or_404(Courses, pk=course_id)
                if ex != '':
                    exam = get_object_or_404(Exam, pk=request.POST.get('exam'))
                    mark.exam = exam
                    type_score = 'exam'
                if c != '':
                    ca = get_object_or_404(ContinuousAssessment, pk=request.POST.get('ca'))
                    mark.ca = ca
                    type_score = 'ca'
                mark.student = student
                mark.score = scores
                mark.course = crse
                mark.user = request.user
                if type_score == 'exam':
                    test_marks_list = Marks.objects.all().filter(
                        ((Q(student=mark.student) & Q(course=mark.course)) & Q(exam=mark.exam)))
                if type_score == 'ca':
                        test_marks_list = Marks.objects.all().filter(
                        ((Q(student=mark.student) & Q(course=mark.course)) & Q(ca=mark.ca)))
                if test_marks_list.exists():
                    print('Exists')
                    test_marks = list(test_marks_list)
                else:
                    mark.save()
                print('mrks cores are ')
                # print(st)
                continue
            fatal = 'None'
            result_list = []
            if c != '':
                result = Marks.objects.all().filter(Q(course=course) & Q(ca=c)).order_by('id')
                result_list = list(result)
            if ex != '':
                result = Marks.objects.all().filter(Q(course=course) & Q(exam=ex)).order_by('id')
                result_list = list(result)
            crse = get_object_or_404(TeacherCourses, pk=pk)
            return render(request, 'my_courses/success_registration.html',
                          {"fatal": fatal, "result_list": result_list, "crse": crse})
        else:
            fatal = 'Occurred'
            print('Fatal Occurred')
            courses = get_object_or_404(TeacherCourses, pk=pk)
            course = courses.course
            possible_ca = ContinuousAssessment.objects.all().filter(status=1).order_by('-id')
            possible_exam = Exam.objects.all().filter(status=1).order_by('-id')
            stus = StudentCourse.objects.all().filter(course=course).order_by('id')
            return render(request, 'my_courses/register_marks.html',
                          {"courses": courses, "stus": stus, "possible_ca": possible_ca,
                           "possible_exam": possible_exam, "fatal": fatal})

    else:
        courses = get_object_or_404(TeacherCourses, pk=pk)
        course = courses.course
        print(course)
        possible_ca = ContinuousAssessment.objects.all().filter(status=1).order_by('-id')
        possible_exam = Exam.objects.all().filter(status=1).order_by('-id')
        stus = StudentCourse.objects.all().filter(course=course).order_by('id')
        return render(request, 'my_courses/register_marks.html',
                      {"courses": courses, "stus": stus, "possible_ca": possible_ca, "possible_exam": possible_exam})


@login_required
def results_marks(request, pk):
    courses = get_object_or_404(TeacherCourses, pk=pk)
    course = courses.course
    result = Marks.objects.all().filter(Q(course=course) & Q(user=request.user)).order_by('-id')
    result_list = list(result)
    crse = get_object_or_404(TeacherCourses, pk=pk)
    return render(request, 'my_courses/results_marks.html', {"result_list": result_list, "crse": crse})
