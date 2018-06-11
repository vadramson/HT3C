import random

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
from Administration.models import Semester, ContinuousAssessment, Exam, Marks, Courses, CourseAverage, AcademicYear
from BaseUser.forms import PasswordChgForm, StudentCourseForm
from BaseUser.models import StudentCourse, TeacherCourses, Student
from BaseUser.serializers import CoursesSerializer, StudentCourseSerializer


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
    global test_marks_list, cour_avg
    if request.method == 'POST':
        ex = request.POST.get('exam')
        print('ex is')
        print(ex)
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
                # cour_avg = CourseAverage()
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
                    mark.credit = crse.credit
                    mark.semester = exam.semester
                    mark.academic_year = exam.semester.academic_year
                    mark.score = (int(scores) * 3)
                    type_score = 'exam'
                if c != '':
                    ca = get_object_or_404(ContinuousAssessment, pk=request.POST.get('ca'))
                    mark.ca = ca
                    mark.semester = ca.semester
                    mark.academic_year = ca.semester.academic_year
                    mark.score = (int(scores) * 2)
                    type_score = 'ca'
                    test_average = CourseAverage.objects.all().filter(
                        Q(student=student) & Q(course=crse) & Q(semester=ca.semester))
                    if test_average.exists():
                        type_average = 'Exists'
                        cour_avg = get_object_or_404(CourseAverage,
                                                     Q(student=student) & Q(course=crse) & Q(semester=ca.semester))
                        cour_avg.total += (int(scores) * 2)
                        cour_avg.divisor += 1
                        cour_avg.average = (cour_avg.total / cour_avg.divisor)
                    else:
                        type_average = 'Not Exists'
                        # cour_avg = CourseAverage()
                        cour_avg.total = (int(scores) * 2)
                        cour_avg.divisor = 1
                        cour_avg.average = (int(scores) * 2)
                        cour_avg.student = student
                        cour_avg.semester = ca.semester
                        cour_avg.course = crse
                        cour_avg.academic_year = ca.semester.academic_year
                        cour_avg.credit = crse.credit
                mark.student = student
                mark.course = crse
                mark.credit = crse.credit
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
                    cour_avg.save()
                    # average = Averages()

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


# MY RESULTS

@login_required
def ca_results_home(request):
    if request.method == 'POST':
        ca = request.POST.get('ca')
        result = Marks.objects.all().filter(Q(student=request.user) & Q(ca=ca)).order_by('id')
        cas = ContinuousAssessment.objects.all().order_by('-id')
        result_list = list(result)
        if result.exists():
            query_outcome = 'Results Found'
        else:
            query_outcome = 'No Results'
        return render(request, 'my_results/ca_results.html',
                      {"query_outcome": query_outcome, "result_list": result_list, "cas": cas})
    else:
        cas = ContinuousAssessment.objects.all().order_by('-id')
        return render(request, 'my_results/ca_results.html', {"cas": cas})


@login_required
def exam_results_home(request):
    if request.method == 'POST':
        exam = request.POST.get('exam')
        result = Marks.objects.all().filter(Q(student=request.user) & Q(exam=exam)).order_by('id')
        exams = Exam.objects.all().order_by('-id')
        result_list = list(result)
        if result.exists():
            query_outcome = 'Results Found'
        else:
            query_outcome = 'No Results'
        return render(request, 'my_results/exam_results.html',
                      {"query_outcome": query_outcome, "result_list": result_list, "exams": exams})
    else:
        exams = Exam.objects.all().order_by('-id')
        return render(request, 'my_results/exam_results.html', {"exams": exams})


@login_required
def final_results_home(request):
    query_outcome = ''
    exams = Exam.objects.all().order_by('-id')
    semesters = Semester.objects.all().order_by('-id')
    if request.method == 'POST':
        semester = request.POST.get('semester')
        semester = get_object_or_404(Semester, pk=semester)
        result = CourseAverage.objects.all().filter(Q(student=request.user) & Q(semester=semester)).order_by('-course')
        result_exam = Marks.objects.all().filter(Q(student=request.user) & Q(semester=semester) & Q(ca=None)).order_by(
            '-course')
        credit = \
            CourseAverage.objects.all().filter(Q(student=request.user) & Q(semester=semester)).aggregate(
                sum=Sum('credit'))[
                'sum']
        credit_earn = Marks.objects.all().filter(
            Q(student=request.user) & Q(semester=semester) & Q(ca=None) & Q(score__lt=10)).aggregate(sum=Sum('credit'))[
            'sum']
        print(result_exam)
        result_list = list(result)
        result_list_exam = list(result_exam)
        final_exam = zip(result_list, result_list_exam)
        if result.exists():
            query_outcome = 'Found Results'
        else:
            query_outcome = 'No Results'
        return render(request, 'my_results/final_results.html',
                      {"query_outcome": query_outcome, "result_list": result_list, "result_list_exam": result_list_exam,
                       "exams": exams, "semesters": semesters, "final_exam": final_exam, "semester": semester,
                       "credit": credit, "credit_earn": credit_earn})
    else:
        return render(request, 'my_results/final_results.html', {"exams": exams, "semesters": semesters})


@login_required
def print_results(request, pk):
    print(pk)
    semester = get_object_or_404(Semester, pk=pk)
    result = CourseAverage.objects.all().filter(Q(student=request.user) & Q(semester=semester)).order_by('-course')
    result_exam = Marks.objects.all().filter(Q(student=request.user) & Q(semester=semester) & Q(ca=None)).order_by(
        '-course')
    result_list = list(result)
    print(semester)
    credit = \
        CourseAverage.objects.all().filter(Q(student=request.user) & Q(semester=semester)).aggregate(sum=Sum('credit'))[
            'sum']
    credit_earn = \
        Marks.objects.all().filter(
            Q(student=request.user) & Q(semester=semester) & Q(ca=None) & Q(score__lt=10)).aggregate(
            sum=Sum('credit'))['sum']
    print(credit)
    print(credit_earn)
    result_list_exam = list(result_exam)
    final_exam = zip(result_list, result_list_exam)
    return render(request, 'my_results/final_results_print.html',
                  {"final_exam": final_exam, "semester": semester, "credit": credit, "credit_earn": credit_earn})


@login_required
def transcript_home(request):
    return render(request, 'my_results/transcript_pay.html')


@login_required
def transcript_test_code(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        check_number = Student.objects.all().filter(phone=phone)
        if check_number.exists():
            phone_number = get_object_or_404(Student, phone=phone)
            code = random.randrange(1, 10000)
            print("code is ...")
            print(code)
            request.session['code'] = code
            # Generate uniquic code and call twillo function and pass the number to send code as message
            return render(request, 'my_results/transcript_code_check.html', {"code": code})
        else:
            msg = 'Invalid Phone Number'
            print(msg)
            return render(request, 'my_results/transcript_pay.html', {"msg": msg})
    else:
        return render(request, 'my_results/transcript_pay.html')


@login_required
def transcript_code(request):
    if request.method == "POST":
        post_code = request.POST.get('code')
        sent_code = request.session.get('code')
        code = int(post_code)
        print("Entered Code is")
        print(code)
        print("Session Code is")
        print(sent_code)
        if code == sent_code:
            acc_yr = AcademicYear.objects.all()
            return render(request, 'my_results/transcript.html', {"code": code, "acc_yr": acc_yr})
        else:
            msg = 'Invalid Code'
            print(msg)
            return render(request, 'my_results/transcript_code_check.html', {"msg": msg})
    else:
        return render(request, 'my_results/transcript_code_check.html')


@login_required
def transcript_calculation(request):
    query_outcome = ''
    exams = Exam.objects.all().order_by('-id')
    semesters = Semester.objects.all().order_by('-id')
    academic_year = get_object_or_404(AcademicYear, pk=request.POST.get('academic_year'))
    if request.method == 'POST':
        result = CourseAverage.objects.all().filter(Q(student=request.user) & Q(academic_year=academic_year)).order_by('-course')
        result_exam = Marks.objects.all().filter(Q(student=request.user) & Q(academic_year=academic_year) & Q(ca=None)).order_by(
            '-course')
        credit = \
            CourseAverage.objects.all().filter(Q(student=request.user) & Q(academic_year=academic_year)).aggregate(
                sum=Sum('credit'))[
                'sum']
        credit_earn = Marks.objects.all().filter(
            Q(student=request.user) & Q(academic_year=academic_year) & Q(ca=None) & Q(score__lt=10)).aggregate(sum=Sum('credit'))[
            'sum']
        print(result_exam)
        result_list = list(result)
        result_list_exam = list(result_exam)
        final_exam = zip(result_list, result_list_exam)
        if result.exists():
            query_outcome = 'Found Results'
        else:
            query_outcome = 'No Results'
        return render(request, 'my_results/transcript.html',
                      {"query_outcome": query_outcome, "result_list": result_list, "result_list_exam": result_list_exam,
                       "exams": exams, "semesters": semesters, "final_exam": final_exam, "academic_year": academic_year,
                       "credit": credit, "credit_earn": credit_earn})
    else:
        return render(request, 'my_results/transcript.html', {"exams": exams, "semesters": semesters})


@login_required
def print_transcript(request, pk):
    print(pk)
    academic_year = get_object_or_404(AcademicYear, pk=pk)
    result = CourseAverage.objects.all().filter(Q(student=request.user) & Q(academic_year=academic_year)).order_by('-course')
    result_exam = Marks.objects.all().filter(Q(student=request.user) & Q(academic_year=academic_year) & Q(ca=None)).order_by(
        '-course')
    result_list = list(result)
    print(academic_year)
    credit = \
        CourseAverage.objects.all().filter(Q(student=request.user) & Q(academic_year=academic_year)).aggregate(sum=Sum('credit'))[
            'sum']
    credit_earn = \
        Marks.objects.all().filter(
            Q(student=request.user) & Q(academic_year=academic_year) & Q(ca=None) & Q(score__lt=10)).aggregate(
            sum=Sum('credit'))['sum']
    print(credit)
    print(credit_earn)
    result_list_exam = list(result_exam)
    final_exam = zip(result_list, result_list_exam)
    return render(request, 'my_results/final_transcript_print.html',
                  {"final_exam": final_exam, "academic_year": academic_year, "credit": credit, "credit_earn": credit_earn})




# API VIEWS


# Authentication API Views Start


@api_view(["POST"])
def my_drf_login(request):
    # data = dict()
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    urs = get_object_or_404(User, pk=token.user_id)
    return Response(
        {"token": token.key, "user_id": token.user_id, "Username": urs.username, "Name": urs.get_full_name(),
         "role": urs.student.role, "department": urs.student.department.department_name,
         "program": urs.student.degree_programm, "picture": urs.student.picture.url})


# {"token": token.key, "user_id": token.user_id, "Username": urs.username, "Name": urs.get_full_name(),
#  "picture": urs.profile.picture.url, "Role": urs.profile.role}


@api_view(["POST"])
def my_drf_logout(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Unknown User"}, status=HTTP_401_UNAUTHORIZED)
    logout(request)
    return Response({"Respond": "Logout"})


# Authentication API Views Ends


@api_view(["GET"])
def get_all_courses(self):
    subject = Courses.objects.all().order_by('-id')
    serializer = CoursesSerializer(subject, many=True)
    return Response({"courses": serializer.data})


@api_view(["POST"])
def my_major_courses(request):
    tken = request.data.get("user")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Major').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"major": serializer.data})
    # return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
def my_minor_courses(request):
    tken = request.data.get("user")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Minor').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"minor": serializer.data})


@api_view(["POST"])
def my_elective_courses(request):
    tken = request.data.get("user")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Elective').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"elective": serializer.data})


@api_view(["POST"])
def my_required_courses(request):
    tken = request.data.get("user")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Required').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"required": serializer.data})


@api_view(["POST"])
def save_major_courses(request):
    tken = request.data.get("user")
    course = request.data.get("id")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    crse = get_object_or_404(Courses, pk=course)
    register_courses = StudentCourse.objects.all().filter(student=urs, course=course).order_by('-id')
    if register_courses.exists():
        register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Major').order_by('-id')
        serializer = StudentCourseSerializer(register_courses, many=True)
        return Response({"major": serializer.data, "message": "Cant`t Register the same course twice"})
    else:
        stu_crse = StudentCourse()
        stu_crse.student = urs
        stu_crse.course = crse
        stu_crse.type_course = 'Major'
        stu_crse.save()
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Major').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"major": serializer.data, "message": "New Major Course Registered"})


@api_view(["POST"])
def save_minor_courses(request):
    tken = request.data.get("user")
    course = request.data.get("id")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    crse = get_object_or_404(Courses, pk=course)
    register_courses = StudentCourse.objects.all().filter(student=urs, course=course).order_by('-id')
    if register_courses.exists():
        register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Minor').order_by('-id')
        serializer = StudentCourseSerializer(register_courses, many=True)
        return Response({"major": serializer.data, "message": "Cant`t Register the same course twice"})
    else:
        stu_crse = StudentCourse()
        stu_crse.student = urs
        stu_crse.course = crse
        stu_crse.type_course = 'Minor'
        stu_crse.save()
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Minor').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"major": serializer.data, "message": "New Minor Course Registered"})


@api_view(["POST"])
def save_elective_courses(request):
    tken = request.data.get("user")
    course = request.data.get("id")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    crse = get_object_or_404(Courses, pk=course)
    register_courses = StudentCourse.objects.all().filter(student=urs, course=course).order_by('-id')
    if register_courses.exists():
        register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Elective').order_by('-id')
        serializer = StudentCourseSerializer(register_courses, many=True)
        return Response({"major": serializer.data, "message": "Cant`t Register the same course twice"})
    else:
        stu_crse = StudentCourse()
        stu_crse.student = urs
        stu_crse.course = crse
        stu_crse.type_course = 'Elective'
        stu_crse.save()
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Elective').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"major": serializer.data, "message": "New Elective Course Registered"})


@api_view(["POST"])
def save_required_courses(request):
    tken = request.data.get("user")
    course = request.data.get("id")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    crse = get_object_or_404(Courses, pk=course)
    register_courses = StudentCourse.objects.all().filter(student=urs, course=course).order_by('-id')
    if register_courses.exists():
        register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Required').order_by('-id')
        serializer = StudentCourseSerializer(register_courses, many=True)
        return Response({"major": serializer.data, "message": "Cant`t Register the same course twice"})
    else:
        stu_crse = StudentCourse()
        stu_crse.student = urs
        stu_crse.course = crse
        stu_crse.type_course = 'Required'
        stu_crse.save()
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Required').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"major": serializer.data, "message": "New Required Course Registered"})


@api_view(["POST"])
def my_courses(request):
    tken = request.data.get("user")
    print(tken)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs).order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"my_courses": serializer.data})


@api_view(["POST"])
def drop_major_courses(request):
    tken = request.data.get("user")
    course = request.data.get("id")
    print(course)
    major = get_object_or_404(StudentCourse, pk=course)
    print(major)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    major.delete()
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Major').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"message": "Major Course dropped", "major": serializer.data})


@api_view(["POST"])
def drop_minor_courses(request):
    tken = request.data.get("user")
    course = request.data.get("id")
    print(course)
    major = get_object_or_404(StudentCourse, pk=course)
    print(major)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    major.delete()
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Minor').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"message": "Minor Course dropped", "major": serializer.data})


@api_view(["POST"])
def drop_elective_courses(request):
    tken = request.data.get("user")
    course = request.data.get("id")
    print(course)
    major = get_object_or_404(StudentCourse, pk=course)
    print(major)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    major.delete()
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Elective').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"message": "Minor Elective dropped", "major": serializer.data})


@api_view(["POST"])
def drop_required_courses(request):
    tken = request.data.get("user")
    course = request.data.get("id")
    print(course)
    major = get_object_or_404(StudentCourse, pk=course)
    print(major)
    token = get_object_or_404(Token, user_id=tken)
    print(token.key)
    major.delete()
    urs = get_object_or_404(User, pk=tken)
    register_courses = StudentCourse.objects.all().filter(student=urs, type_course='Required').order_by('-id')
    serializer = StudentCourseSerializer(register_courses, many=True)
    return Response({"message": "Minor Required dropped", "major": serializer.data})
