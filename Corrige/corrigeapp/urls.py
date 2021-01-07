from django.urls import path, re_path
from . import views

urlpatterns = [
    path('students/list', views.StudentsListView.as_view(), name = 'students_list'),
    path('teachers/list', views.TeachersListView.as_view(), name = 'teachers_list'),
    path('students/create', views.StudentCreateView.as_view(), name = 'students_create'),

]