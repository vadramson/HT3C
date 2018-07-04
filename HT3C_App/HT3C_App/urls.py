"""HT3C_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from BaseUser import views as urs_views
# from BaseUser.views import MyMajorCourses

router = SimpleRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', urs_views.home, name='home'),
    url(r'^courses/home/$', urs_views.course_reg_home, name='course_reg_home'),
    url(r'^transcript/home/$', urs_views.transcript_home, name='transcript_home'),
    url(r'^transcript/check/code/$', urs_views.transcript_test_code, name='transcript_test_code'),
    url(r'^transcript/code/$', urs_views.transcript_code, name='transcript_code'),
    url(r'^major/course/$', urs_views.major_reg_course_list, name='major_reg_course_list'),
    url(r'^major/course/add/$', urs_views.major_create, name='major_create'),
    url(r'^major/course/(?P<pk>\d+)/drop/$', urs_views.major_delete, name='major_delete'),
    url(r'^minor/course/$', urs_views.minor_reg_course_list, name='minor_reg_course_list'),
    url(r'^minor/course/add/$', urs_views.minor_create, name='minor_create'),
    url(r'^minor/course/(?P<pk>\d+)/drop/$', urs_views.minor_delete, name='minor_delete'),
    url(r'^elective/course/$', urs_views.elective_reg_course_list, name='elective_reg_course_list'),
    url(r'^elective/course/add/$', urs_views.elective_create, name='elective_create'),
    url(r'^elective/course/(?P<pk>\d+)/drop/$', urs_views.elective_delete, name='elective_delete'),
    url(r'^required/course/$', urs_views.required_reg_course_list, name='required_reg_course_list'),
    url(r'^required/course/add/$', urs_views.required_create, name='required_create'),
    url(r'^required/course/(?P<pk>\d+)/drop/$', urs_views.required_delete, name='required_delete'),
    url(r'^final/course/registered/$', urs_views.final_reg_course_list, name='final_reg_course_list'),
    url(r'^my/results/CA/$', urs_views.ca_results_home, name='ca_results_home'),
    url(r'^my/results/EXAMS/$', urs_views.exam_results_home, name='exam_results_home'),
    url(r'^my/final/results/$', urs_views.final_results_home, name='final_results_home'),
    url(r'^my/yearly/transcript/$', urs_views.transcript_calculation, name='transcript_calculation'),
    url(r'^my/course/$', urs_views.my_courses_list, name='my_courses_list'),
    url(r'^register/marks/(?P<pk>\d+)/$', urs_views.fill_marks, name='fill_marks'),
    url(r'^register/exam/marks/(?P<pk>\d+)/$', urs_views.fill_marks_exam, name='fill_marks_exam'),
    url(r'^register/ca/marks/(?P<pk>\d+)/$', urs_views.fill_marks_ca, name='fill_marks_ca'),
    url(r'^print/results/(?P<pk>\d+)/$', urs_views.print_results, name='print_results'),
    url(r'^print/transcript/(?P<pk>\d+)/$', urs_views.print_transcript, name='print_transcript'),
    url(r'^results/marks/(?P<pk>\d+)/$', urs_views.results_marks, name='results_marks'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^user/change/my-Password$', urs_views.change_password, name='change_password'),

    # API URLs
    url(r'^', include(router.urls)),
    url(r'^api/h3tc/get/all/courses/$', urs_views.get_all_courses),
    # url(r'^api/h3tc/get/all/major/courses/$', MyMajorCourses.as_view()),
    url(r'^api/h3tc/get/all/major/courses/$', urs_views.my_major_courses),
    url(r'^api/h3tc/get/all/minor/courses/$', urs_views.my_minor_courses),
    url(r'^api/h3tc/get/all/elective/courses/$', urs_views.my_elective_courses),
    url(r'^api/h3tc/get/all/required/courses/$', urs_views.my_required_courses),
    url(r'^api/h3tc/add/major/courses/$', urs_views.save_major_courses),
    url(r'^api/h3tc/add/minor/courses/$', urs_views.save_minor_courses),
    url(r'^api/h3tc/add/elective/courses/$', urs_views.save_elective_courses),
    url(r'^api/h3tc/add/required/courses/$', urs_views.save_required_courses),
    url(r'^api/h3tc/my/courses/$', urs_views.my_courses),
    url(r'^api/h3tc/drop/major/courses/$', urs_views.drop_major_courses),
    url(r'^api/h3tc/drop/minor/courses/$', urs_views.drop_minor_courses),
    url(r'^api/h3tc/drop/elective/courses/$', urs_views.drop_elective_courses),
    url(r'^api/h3tc/drop/required/courses/$', urs_views.drop_required_courses),
    url(r'^api/h3tc/ca/results/$', urs_views.ca_results_home_drf),
    url(r'^api/h3tc/exam/list/$', urs_views.exam_s),
    url(r'^api/h3tc/semester/list/$', urs_views.semester_s),
    url(r'^api/h3tc/academic/year/list/$', urs_views.academic_year_s),
    url(r'^api/h3tc/semester/results/$', urs_views.semester_results),
    url(r'^api/h3tc/transcript/results/$', urs_views.my_transcript),
    url(r'^api/h3tc/exam/results/$', urs_views.exam_results_home_drf),
    url(r'^api/h3tc/ca/list/$', urs_views.ca_s),
    url(r'^api/h3tc/jwt-auth/$', obtain_jwt_token),
    url(r'^api/h3tc/login/$', urs_views.my_drf_login),
    url(r'^api/h3tc/logout/$', urs_views.my_drf_logout),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

