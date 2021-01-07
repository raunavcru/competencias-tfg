from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy

from . import forms
from . import models


class StudentsListView(generic.ListView):
    model = models.Student
    template_name = 'students/list.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        queryset = models.Student.objects.all()
        return queryset


class TeachersListView(generic.ListView):
    model = models.Teacher
    template_name = 'teachers/list.html'
    context_object_name = 'teacher_list'


    def get_queryset(self):
        queryset = models.Teacher.objects.all()
        return queryset

class StudentCreateView(generic.CreateView):
    form_class = forms.StudentCreateForm
    template_name = "students/create.html"
    success_url = reverse_lazy('students_list')