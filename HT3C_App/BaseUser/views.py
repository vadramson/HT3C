from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Min, Sum, Avg
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
from BaseUser.forms import PasswordChgForm


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
