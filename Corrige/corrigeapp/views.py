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
        print(self.request.user)

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

@method_decorator(login_required, name='dispatch')
class EvaluationsListView(generic.ListView):
    model = models.Evaluation
    template_name = 'evaluations/list.html'
    context_object_name = 'evaluations_list'

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationsListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Evaluation.objects.all().order_by('name','subject', 'parent', 'start_date')
        return queryset

@method_decorator(login_required, name='dispatch')
class EvaluationDeleteView(generic.DeleteView):
    template_name = 'evaluations/delete.html'
    model = models.Evaluation
    success_url = reverse_lazy('evaluations_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class EvaluationCreateView(generic.CreateView):
    form_class = forms.EvaluationCreateForm
    template_name = "evaluations/update.html"
    success_url = reverse_lazy('evaluations_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        start_date = form.cleaned_data.get('start_date')
        end_date_1 = form.cleaned_data.get('end_date_1')
        start_date_2 = form.cleaned_data.get('start_date_2')
        end_date_2 = form.cleaned_data.get('end_date_2')
        start_date_3 = form.cleaned_data.get('start_date_3')
        end_date = form.cleaned_data.get('end_date')
        subject = form.cleaned_data.get('subject')

        evaluation = form.save(commit=False)
        evaluation.is_final=True
        evaluation.save()
        evaluation1 = models.Evaluation.objects.create(name=name, start_date=start_date, end_date=end_date_1,
            is_final=False, period="1st", subject=subject, parent=evaluation)
        evaluation1.save()
        evaluation2 = models.Evaluation.objects.create(name=name, start_date=start_date_2, end_date=end_date_2,
            is_final=False, period="2nd", subject=subject, parent=evaluation)
        evaluation2.save()
        evaluation3 = models.Evaluation.objects.create(name=name, start_date=start_date_3, end_date=end_date,
            is_final=False, period="3rd", subject=subject, parent=evaluation)
        evaluation3.save()

        return redirect('evaluations_list')
    

@method_decorator(login_required, name='dispatch')
class EvaluationUpdateView(generic.UpdateView):
    model = models.Evaluation
    form_class = forms.EvaluationUpdateForm
    template_name = "evaluations/update.html"
    success_url = reverse_lazy('evaluations_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    