
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . views import *

urlpatterns = [
    path('', CombinedListView.as_view(), name = "home"),
    path('auth/signup/', signup_view, name='signup'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('get-tasks-for-date/<date_str>/', get_tasks_for_date, name='get-tasks-for-date'),
]