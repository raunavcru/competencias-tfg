from django.urls import path, re_path
from . import views
from . import models

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('404', views.not_impl.as_view(), name = '404'),
    path('students/list', views.StudentsListView.as_view(), name = 'students_list'),
    path('students/create', views.StudentCreateView.as_view(), name = 'students_create'),
    path('students/<int:pk>/delete', views.StudentDeleteView.as_view(), name='students_delete'),
    path('students/<int:pk>/update', views.StudentUpdateView.as_view(), name = 'students_update'),
    path('teachers/create', views.TeacherCreateView.as_view(), name = 'teachers_create'),
    path('teachers/<int:pk>/delete', views.TeacherDeleteView.as_view(), name='teachers_delete'),
    path('teachers/list', views.TeachersListView.as_view(), name = 'teachers_list'),
    path('teachers/<int:pk>/update', views.TeacherUpdateView.as_view(), name = 'teachers_update'),
    path('teachers/create', views.TeacherCreateView.as_view(), name = 'teachers_create'),
    path('sets/create', views.SetCreateView.as_view(), name = 'sets_create'),
    path('sets/<int:pk>/update', views.SetUpdateView.as_view(), name = 'sets_update'),
    path('sets/list', views.SetsListView.as_view(), name = 'sets_list'),
    path('sets/<int:pk>/delete', views.SetDeleteView.as_view(), name='sets_delete'),
    path('subjects/list', views.SubjectsListView.as_view(), name = 'subjects_list'),
    path('subjects/create', views.SubjectCreateView.as_view(), name = 'subjects_create'),
    path('subjects/<int:pk>/delete', views.SubjectsDeleteView.as_view(), name='subjects_delete'),
    path('subjects/<int:pk>/update', views.SubjectsUpdateView.as_view(), name = 'subjects_update'),


]