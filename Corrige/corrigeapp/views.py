from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy

from . import forms
from . import models

class StudentCreateView(generic.CreateView):
    form_class = forms.StudentCreateForm
    template_name = "students/create.html"
    success_url = reverse_lazy('students_list')

class StudentDeleteView(generic.DeleteView):
    template_name = 'students/delete.html'
    model = models.Student
    success_url = reverse_lazy('students_list')

class StudentsListView(generic.ListView):
    model = models.Student
    template_name = 'students/list.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        queryset = models.Student.objects.all()
        return queryset

class StudentUpdateView(generic.UpdateView):
    model = models.Student
    form_class = forms.StudentCreateForm
    template_name = "students/create.html"
    success_url = reverse_lazy('students_list')

class TeacherCreateView(generic.CreateView):
    form_class = forms.TeacherCreateForm
    template_name = "teachers/create.html"
    success_url = reverse_lazy('teachers_list')

    def form_valid(self, form):
        user = form.save()
        birthdate = form.cleaned_data.get('birthdate')
        initials = form.cleaned_data.get('initials')
        profile = models.Teacher.objects.create(user=user, birthdate=birthdate, initials=initials, role='TEACHER')
        profile.save()
        return super(TeacherCreateView, self).form_valid(form)

class TeacherDeleteView(generic.DeleteView):
    model = models.Teacher
    template_name = 'teachers/confirm_delete.html'

    def post(self, request, *args, **kwargs):
        teacher_pk = self.kwargs.get('pk')
        teacher = models.Teacher.objects.get(pk=teacher_pk)
        teacher.user.delete()
        teacher.delete()

        return redirect('teachers_list')

class TeachersListView(generic.ListView):
    model = models.Teacher
    template_name = 'teachers/list.html'
    context_object_name = 'teacher_list'

    def get_queryset(self):
        queryset = models.Teacher.objects.all()
        return queryset
        
class TeacherUpdateView(generic.UpdateView):
    model = models.User
    form_class = forms.UserUpdateForm
    teacher_form_class = forms.TeacherUpdateForm
    template_name = "teachers/create.html"
    success_url = reverse_lazy('teachers_list')

    def get_context_data(self, **kwargs):
        context = super(TeacherUpdateView, self).get_context_data(**kwargs)
        context['teacher_form'] = self.teacher_form_class(instance=self.object.profile)

        return context

    def get_object(self):
        teacher_pk = self.kwargs.get('pk')
        teacher = models.Teacher.objects.get(pk=teacher_pk)
        teacher_user = teacher.user
        return teacher_user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        teacher_form = self.teacher_form_class(
            request.POST, instance=self.object.profile)
        if form.is_valid() and teacher_form.is_valid():
            user = form.save()
            teacher_form.save(user)
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, profile_form=teacher_form))

class SetsListView(generic.ListView):
    model = models.Set
    template_name = 'sets/list.html'
    context_object_name = 'set_list'

    def get_queryset(self):
        queryset = models.Set.objects.all()
        return queryset

class SetDeleteView(generic.DeleteView):
    template_name = 'sets/delete.html'
    model = models.Set
    success_url = reverse_lazy('sets_list')