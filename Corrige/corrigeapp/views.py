from django.shortcuts import render

class TeachersListView(generic.ListView):
    model = models.Teacher
    template_name = 'teachers/list.html'
    context_object_name = 'teacher_list'


    def get_queryset(self):
        queryset = models.Teacher.objects.all()
        return queryset