from django.urls import path, re_path
from . import views

urlpatterns = [
    path('students/list', views.StudentsListView.as_view(), name = 'students_list'),
    path('students/create', views.StudentCreateView.as_view(), name = 'students_create'),
    path('students/<int:pk>/delete', views.StudentDeleteView.as_view(), name='students_delete'),
    path('students/<int:pk>/update', views.StudentUpdateView.as_view(), name = 'students_update'),
    path('teachers/list', views.TeachersListView.as_view(), name = 'teachers_list'),
    path('teachers/create', views.TeacherCreateView.as_view(), name = 'teachers_create'),
    path('teachers/<int:pk>/update', views.TeacherUpdateView.as_view(), name = 'teachers_update'),
]