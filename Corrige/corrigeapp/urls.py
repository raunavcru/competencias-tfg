from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('teachers/list', views.TeachersListView.as_view(), name = 'teachers_list'),
]