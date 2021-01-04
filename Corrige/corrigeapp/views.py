from django.shortcuts import render
from django.views import generic

from . import models

class TeachersListView(generic.ListView):
    model = models.Teacher
    template_name = 'teachers/list.html'
    context_object_name = 'teacher_list'


    def get_queryset(self):
        queryset = models.Teacher.objects.all()
        return queryset