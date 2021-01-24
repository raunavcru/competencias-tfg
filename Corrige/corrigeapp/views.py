from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import activate, get_language
from django.views import generic

from . import forms
from . import models
from . import services

class HomeView(generic.TemplateView):
    template_name = 'home.html'

@method_decorator(login_required, name='dispatch')
class StudentCreateView(generic.CreateView):
    form_class = forms.StudentCreateForm
    template_name = "students/create.html"
    success_url = reverse_lazy('students_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(StudentCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class StudentDeleteView(generic.DeleteView):
    template_name = 'students/delete.html'
    model = models.Student
    success_url = reverse_lazy('students_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(StudentDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class StudentsListView(generic.ListView):
    model = models.Student
    template_name = 'students/list.html'
    context_object_name = 'student_list'

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(StudentsListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Student.objects.all()
        return queryset

@method_decorator(login_required, name='dispatch')
class StudentUpdateView(generic.UpdateView):
    model = models.Student
    form_class = forms.StudentCreateForm
    template_name = "students/create.html"
    success_url = reverse_lazy('students_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(StudentUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class TeacherCreateView(generic.CreateView):
    form_class = forms.TeacherCreateForm
    template_name = "teachers/create.html"
    success_url = reverse_lazy('teachers_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(TeacherCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def form_valid(self, form):
        user = form.save()
        birthdate = form.cleaned_data.get('birthdate')
        initials = form.cleaned_data.get('initials')
        profile = models.Teacher.objects.create(user=user, birthdate=birthdate, initials=initials, role='TEACHER')
        profile.save()
        return super(TeacherCreateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class TeacherDeleteView(generic.DeleteView):
    model = models.Teacher
    template_name = 'teachers/confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(TeacherDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        teacher_pk = self.kwargs.get('pk')
        teacher = models.Teacher.objects.get(pk=teacher_pk)
        teacher.user.delete()
        teacher.delete()

        return redirect('teachers_list')

@method_decorator(login_required, name='dispatch')
class TeachersListView(generic.ListView):
    model = models.Teacher
    template_name = 'teachers/list.html'
    context_object_name = 'teacher_list'

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(TeachersListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Teacher.objects.all()
        return queryset

@method_decorator(login_required, name='dispatch')        
class TeacherUpdateView(generic.UpdateView):
    model = models.User
    form_class = forms.UserUpdateForm
    teacher_form_class = forms.TeacherUpdateForm
    template_name = "teachers/create.html"
    success_url = reverse_lazy('teachers_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(TeacherUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

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

@method_decorator(login_required, name='dispatch')
class SetsListView(generic.ListView):
    model = models.Set
    template_name = 'sets/list.html'
    context_object_name = 'set_list'

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SetsListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Set.objects.all()
        return queryset

@method_decorator(login_required, name='dispatch')
class SetDeleteView(generic.DeleteView):
    template_name = 'sets/delete.html'
    model = models.Set
    success_url = reverse_lazy('sets_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SetDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class SetCreateView(generic.CreateView):
    form_class = forms.SetCreateForm
    template_name = "sets/create.html"
    success_url = reverse_lazy('sets_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SetCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class SetUpdateView(generic.UpdateView):
    model = models.Set
    form_class = forms.SetCreateForm
    template_name = "sets/create.html"
    success_url = reverse_lazy('sets_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SetUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')


class not_impl(generic.TemplateView):
    template_name = "not_impl.html"