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
from django.views.generic import TemplateView
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from BaseUser import views as urs_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', urs_views.home, name='home'),
    url(r'^courses/home/$', urs_views.course_reg_home, name='course_reg_home'),
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
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^user/change/my-Password$', urs_views.change_password, name='change_password'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

