from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import activate, get_language
from django.views import generic


from . import forms
from . import models
from . import services

COMPETENCE_LIST = 'competences/list.html'
COMPETENCE_CREATE = "competences/create.html"
EVALUATION_UPDATE = "evaluations/update.html"
EXERCISE_CREATE = 'exercises/create.html'


# Generic
class HomeView(generic.TemplateView):
    template_name = 'home.html'

class not_impl(generic.TemplateView):
    template_name = "not_impl.html"

# Activities
@method_decorator(login_required, name='dispatch')
class ActivityCreateView(generic.CreateView):
    form_class = forms.ActivityUpdateForm
    template_name = 'activities/create.html'

    def get(self, request, *args, **kwargs):
        set_pk = self.kwargs.get('pk')
        set_object = models.Set.objects.get(pk=set_pk)
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ActivityCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        set_pk = self.kwargs.get('pk')
        context = super(ActivityCreateView, self).get_context_data(**kwargs)
        context['set_pk'] = set_pk
        return context
    
    def get_form_kwargs(self):
        kwargs = super(ActivityCreateView, self).get_form_kwargs()
        set_pk = self.kwargs.get('pk')
        set_object = models.Set.objects.get(pk=set_pk)
        evaluations = models.Evaluation.objects.filter(evaluation_set=set_pk) | models.Evaluation.objects.filter(parent=set_object.evaluation)
        kwargs['choices'] = evaluations
        return kwargs

    def form_valid(self, form):
        set_pk = self.kwargs.get('pk')
        set_object = models.Set.objects.get(pk=set_pk)
        if services.UserService().is_teacher(self.request.user) and services.SetService().is_owner(user=self.request.user, set_object=set_object):
            activity = form.save(commit=False)
            activity.set_activity = set_object
            activity.subject = set_object.subject
            activity.save()

            return redirect('activities_list', pk=set_pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class ActivityCopyView(generic.TemplateView):   

    def get(self, request, *args, **kwargs):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_pk = self.kwargs.get('id')
        set_object = models.Set.objects.get(pk=set_pk)
        if services.UserService().is_teacher(self.request.user) and services.SetService().is_owner(user=self.request.user, set_object=set_object) and services.SetService().is_owner(user=self.request.user, set_object=activity_object.set_activity):
            copy = models.Activity.objects.create(date=activity_object.date, weight=activity_object.weight, is_recovery=activity_object.is_recovery, set_activity=set_object, evaluation=set_object.evaluation, subject=set_object.subject)
            copy.save()
            return redirect('activities_list', pk=set_pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class ActivityDeleteView(generic.DeleteView):
    model = models.Activity
    template_name = 'activities/delete.html'

    def get(self, request, *args, **kwargs):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ActivityDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    
    def get_context_data(self, **kwargs):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        set_pk = set_object.pk
        context = super(ActivityDeleteView, self).get_context_data(**kwargs)
        context['set_pk'] = set_pk
        return context

    def post(self, request, *args, **kwargs):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        set_pk = set_object.pk
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            activity_pk = self.kwargs.get('pk')
            activity_object = models.Activity.objects.get(pk=activity_pk)
            activity_object.delete()

            return redirect('activities_list', pk=set_pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class ActivitiesListView(generic.ListView):
    model = models.Activity
    template_name = 'activities/list.html'
    context_object_name = 'activities_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        set_pk = self.kwargs.get('pk')
        set_object = models.Set.objects.get(pk=set_pk)
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ActivitiesListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    
    def get_context_data(self, **kwargs):
        set_pk = self.kwargs.get('pk')
        context = super(ActivitiesListView, self).get_context_data(**kwargs)
        context['set_pk'] = set_pk
        context['no_copy_list'] = True
        return context

    def get_queryset(self):
        set_pk = self.kwargs.get('pk')
        set_object = models.Set.objects.get(pk=set_pk)
        queryset = models.Activity.objects.filter(set_activity=set_object).order_by('date')
        return queryset

@method_decorator(login_required, name='dispatch')
class ActivitiesListCopyView(generic.ListView):
    model = models.Activity
    template_name = 'activities/list.html'
    context_object_name = 'activities_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        set_pk = self.kwargs.get('pk')
        set_object = models.Set.objects.get(pk=set_pk)
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ActivitiesListCopyView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    
    def get_context_data(self, **kwargs):
        set_pk = self.kwargs.get('pk')
        context = super(ActivitiesListCopyView, self).get_context_data(**kwargs)
        context['set_pk'] = set_pk
        return context

    def get_queryset(self):
        queryset = models.Activity.objects.filter(set_activity__teacher__user=self.request.user).order_by('date')
        return queryset

@method_decorator(login_required, name='dispatch')
class ActivityUpdateView(generic.UpdateView):
    model = models.Activity
    form_class = forms.ActivityUpdateForm
    template_name = 'activities/create.html'

    def get(self, request, *args, **kwargs):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ActivityUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        set_pk = self.kwargs.get('pk')
        context = super(ActivityUpdateView, self).get_context_data(**kwargs)
        context['set_pk'] = set_pk
        context['update'] = True
        return context
    
    def get_form_kwargs(self):
        kwargs = super(ActivityUpdateView, self).get_form_kwargs()
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        set_pk = set_object.pk
        evaluations = models.Evaluation.objects.filter(evaluation_set=set_pk) | models.Evaluation.objects.filter(parent=set_object.evaluation)
        kwargs['choices'] = evaluations
        return kwargs

    def form_valid(self, form):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        set_pk = set_object.pk
        if services.UserService().is_teacher(self.request.user) and services.SetService().is_owner(user=self.request.user, set_object=set_object):
            form.save()

            return redirect('activities_list', pk=set_pk)
        else:
            return redirect('/')

# Administrators
@method_decorator(login_required, name='dispatch')
class AdministratorCreateView(generic.CreateView):
    form_class = forms.UserCreateForm
    template_name = "administrators/create.html"
    success_url = reverse_lazy('administrators_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(AdministratorCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def form_valid(self, form):
        user = form.save()
        birthdate = form.cleaned_data.get('birthdate')
        initials = form.cleaned_data.get('initials')
        profile = models.Administrator.objects.create(user=user, birthdate=birthdate, initials=initials, role='ADMINISTRATOR')
        profile.save()
        return super(AdministratorCreateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class AdministratorDeleteView(generic.DeleteView):
    model = models.Administrator
    template_name = 'administrators/confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(AdministratorDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        admin_pk = self.kwargs.get('pk')
        admin = models.Administrator.objects.get(pk=admin_pk)
        admin.user.delete()
        admin.delete()

        return redirect('administrators_list')

@method_decorator(login_required, name='dispatch')
class AdministratorsListView(generic.ListView):
    model = models.Administrator
    template_name = 'administrators/list.html'
    context_object_name = 'administrator_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(AdministratorsListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        user = self.request.user
        admin_log = models.Administrator.objects.filter(user=user).first()
        queryset = models.Administrator.objects.all().order_by('user__last_name').exclude(pk = admin_log.pk)
        return queryset

@method_decorator(login_required, name='dispatch')        
class AdministratorUpdateView(generic.UpdateView):
    model = models.User
    form_class = forms.UserUpdateForm
    administrator_form_class = forms.TeacherUpdateForm
    template_name = "administrators/create.html"
    success_url = reverse_lazy('administrators_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(AdministratorUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(AdministratorUpdateView, self).get_context_data(**kwargs)
        context['administrator_form'] = self.administrator_form_class(instance=self.object.profile)
        return context
    
    def get_object(self):
        admin_pk = self.kwargs.get('pk')
        admin = models.Administrator.objects.get(pk=admin_pk)
        admin_user = admin.user
        return admin_user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        administrator_form = self.administrator_form_class(
            request.POST, instance=self.object.profile)
        if form.is_valid() and administrator_form.is_valid():
            user = form.save()
            administrator_form.save(user)
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, profile_form=administrator_form))

# Competences
@method_decorator(login_required, name='dispatch')
class CompetenceCreateChildView(generic.CreateView):
    form_class = forms.CompetenceCreateForm
    template_name = COMPETENCE_CREATE
    
    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(CompetenceCreateChildView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    
    def get_context_data(self, **kwargs):
        context = super(CompetenceCreateChildView, self).get_context_data(**kwargs)
        competence_pk = self.kwargs.get('pk')
        context['competence_pk'] = competence_pk
        context['competence_parent'] = True
        return context

    def form_valid(self, form):
        competence_pk = self.kwargs.get('pk')
        competence = models.Competence.objects.get(pk=competence_pk)
        competence_new = form.save(commit=False)

        if competence.level == 3:
            competence_new.level = 2
        elif competence.level == 2:
            competence_new.level = 1
        else:
            return redirect('/')
            
        competence_new.save()
        competence_new.parent.add(competence) 

        return redirect('competences_relation', pk=competence_pk)

@method_decorator(login_required, name='dispatch')
class CompetenceCreateLevel3View(generic.CreateView):
    form_class = forms.CompetenceCreateForm
    template_name = COMPETENCE_CREATE
    success_url = reverse_lazy('competences_list3')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(CompetenceCreateLevel3View, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    
    def get_context_data(self, **kwargs):
        context = super(CompetenceCreateLevel3View, self).get_context_data(**kwargs)
        context['create_level3'] = True
        return context
    
    def form_valid(self, form):
        competence_new = form.save(commit=False)
        competence_new.level = 3
        competence_new.save()

        return redirect('competences_list3')

@method_decorator(login_required, name='dispatch')
class CompetencesDeleteView(generic.DeleteView):
    template_name = 'competences/delete.html'
    model = models.Competence

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(CompetencesDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        competence_pk = self.kwargs.get('pk')
        competence = models.Competence.objects.get(pk=competence_pk)
        context = super(CompetencesDeleteView, self).get_context_data(**kwargs)
        context['list_level3'] = False
        context['list_level2'] = False
        context['list_level1'] = False
        if competence.level == 3:
            context['list_level3'] = True
            
        elif competence.level == 2:
            context['list_level2'] = True
        else:
            context['list_level1'] = True

        return context

    def post(self, request, *args, **kwargs):
        competence_pk = self.kwargs.get('pk')
        competence = models.Competence.objects.get(pk=competence_pk)
        competence.delete()
        
        if competence.level == 3:
            return redirect('competences_list3')
            
        elif competence.level == 2:
            return redirect('competences_list2')
        else:
            return redirect('competences_list1')

@method_decorator(login_required, name='dispatch')
class CompetencesListChildView(generic.ListView):
    model = models.Competence
    template_name = COMPETENCE_LIST
    context_object_name = 'competence_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(CompetencesListChildView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    
    def get_context_data(self, **kwargs):
        context = super(CompetencesListChildView, self).get_context_data(**kwargs)
        competence_pk = self.kwargs.get('pk')
        competence = models.Competence.objects.get(pk=competence_pk)
        context['competence_pk'] = competence_pk
        context['listall_level3'] = False
        context['listall_level2'] = False
        context['list_level2'] = False
        context['list_level1'] = False

        if competence.level == 3:
            context['list_level2'] = True
        elif competence.level == 2:
            context['list_level1'] = True

        return context

    def get_queryset(self):
        level3_pk = self.kwargs.get('pk')
        level3 = models.Competence.objects.get(pk=level3_pk)
        queryset = models.Competence.objects.filter(parent=level3).order_by('code')
        return queryset

@method_decorator(login_required, name='dispatch')
class CompetenceListLevel1View(generic.ListView):
    model = models.Competence
    template_name = COMPETENCE_LIST
    context_object_name = 'competence_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(CompetenceListLevel1View, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(CompetenceListLevel1View, self).get_context_data(**kwargs)
        context['listall_level3'] = False
        context['listall_level2'] = False
        context['list_level2'] = False

        return context

    def get_queryset(self):
        queryset = models.Competence.objects.filter(level="1").order_by('code')
        return queryset

@method_decorator(login_required, name='dispatch')
class CompetenceListLevel2View(generic.ListView):
    model = models.Competence
    template_name = COMPETENCE_LIST
    context_object_name = 'competence_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(CompetenceListLevel2View, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(CompetenceListLevel2View, self).get_context_data(**kwargs)
        context['listall_level3'] = False
        context['listall_level2'] = True
        context['list_level2'] = False

        return context

    def get_queryset(self):
        queryset = models.Competence.objects.filter(level="2").order_by('code')
        return queryset

@method_decorator(login_required, name='dispatch')
class CompetenceListLevel3View(generic.ListView):
    model = models.Competence
    template_name = COMPETENCE_LIST
    context_object_name = 'competence_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(CompetenceListLevel3View, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(CompetenceListLevel3View, self).get_context_data(**kwargs)
        context['listall_level3'] = True
        context['listall_level2'] = False
        context['list_level3'] = False
        context['list_level2'] = False

        return context

    def get_queryset(self):
        queryset = models.Competence.objects.filter(level="3").order_by('code')
        return queryset

@method_decorator(login_required, name='dispatch')
class CompetenceUpdateView(generic.UpdateView):
    model = models.Competence
    form_class = forms.CompetenceCreateForm
    template_name = COMPETENCE_CREATE

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(CompetenceUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(CompetenceUpdateView, self).get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def form_valid(self, form):
        competence = form.save()

        if competence.level == 3:
            return redirect('competences_list3')
        elif competence.level == 2:
            return redirect('competences_list2')
        else:
            return redirect('competences_list1')

# Exercices
@method_decorator(login_required, name='dispatch')
class ExerciseCreateView(generic.CreateView):
    form_class = forms.ExerciseUpdateForm
    template_name = EXERCISE_CREATE

    def get(self, request, *args, **kwargs):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ExerciseCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        activity_pk = self.kwargs.get('pk')
        context = super(ExerciseCreateView, self).get_context_data(**kwargs)
        context['activity_pk'] = activity_pk
        return context

    def form_valid(self, form):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(self.request.user) and services.SetService().is_owner(user=self.request.user, set_object=set_object):
            exercice = form.save(commit=False)
            exercice.activity = activity_object
            exercice.save()

            return redirect('exercises_list', type=1, pk=activity_pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class ExerciseDeleteView(generic.DeleteView):
    model = models.Exercise
    template_name = 'exercises/delete.html'

    def get(self, request, *args, **kwargs):
        exercise_pk = self.kwargs.get('pk')
        exercise_object = models.Exercise.objects.get(pk=exercise_pk)
        activity_object = models.Activity.objects.get(pk=exercise_object.activity.pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ExerciseDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        exercise_pk = self.kwargs.get('pk')
        exercise_object = models.Exercise.objects.get(pk=exercise_pk)
        activity_object = models.Activity.objects.get(pk=exercise_object.activity.pk)
        context = super(ExerciseDeleteView, self).get_context_data(**kwargs)
        context['activity_pk'] = activity_object.pk
        return context

    def post(self, request, *args, **kwargs):
        exercise_pk = self.kwargs.get('pk')
        exercise_object = models.Exercise.objects.get(pk=exercise_pk)
        activity_object = models.Activity.objects.get(pk=exercise_object.activity.pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(self.request.user) and services.SetService().is_owner(user=self.request.user, set_object=set_object):
            exercise_object.delete()

            return redirect('exercises_list', type=1, pk=activity_object.pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class ExercisesListView(generic.ListView):
    model = models.Exercise
    template_name = 'exercises/list.html'
    context_object_name = 'exercises_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ExercisesListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        type_url = self.kwargs.get('type')
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        set_pk = activity_object.set_activity.pk
        context = super(ExercisesListView, self).get_context_data(**kwargs)
        context['activity_pk'] = activity_pk
        context['set_pk'] = set_pk
        context['type_url'] = type_url
        return context

    def get_queryset(self):
        activity_pk = self.kwargs.get('pk')
        activity_object = models.Activity.objects.get(pk=activity_pk)
        queryset = models.Exercise.objects.filter(activity=activity_object).order_by('statement')
        return queryset

@method_decorator(login_required, name='dispatch')
class ExerciseUpdateView(generic.UpdateView):
    model = models.Exercise
    form_class = forms.ExerciseUpdateForm
    template_name = EXERCISE_CREATE

    def get(self, request, *args, **kwargs):
        exercise_pk = self.kwargs.get('pk')
        exercise_object = models.Exercise.objects.get(pk=exercise_pk)
        activity_object = models.Activity.objects.get(pk=exercise_object.activity.pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(ExerciseUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        exercise_pk = self.kwargs.get('pk')
        exercise_object = models.Exercise.objects.get(pk=exercise_pk)
        activity_object = models.Activity.objects.get(pk=exercise_object.activity.pk)
        list_exercise_competence = models.Exercise_competence.objects.filter(exercise=exercise_object)
        list_competences_unassigned = models.Competence.objects.filter(level=1, competences=activity_object.set_activity.subject).exclude(competence_exercise_competence__exercise=exercise_object).order_by('code')
        context = super(ExerciseUpdateView, self).get_context_data(**kwargs)
        context['exercise_pk'] = exercise_pk
        context['activity_pk'] = activity_object.pk
        context['update'] = True
        context['list_competences_assigned'] = list_exercise_competence
        context['list_competences_unassigned'] = list_competences_unassigned
        context['exercise_competence_form'] = forms.ExerciseCompetenceUpdateForm
        return context

    def form_valid(self, form):
        exercise_pk = self.kwargs.get('pk')
        exercise_object = models.Exercise.objects.get(pk=exercise_pk)
        activity_object = models.Activity.objects.get(pk=exercise_object.activity.pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(self.request.user) and services.SetService().is_owner(user=self.request.user, set_object=set_object):
            form.save()

            return redirect('exercises_list', type=1, pk=activity_object.pk)
        else:
            return redirect('/')

# Exercices_competence
@method_decorator(login_required, name='dispatch')
class ExerciseCompetenceDeleteView(generic.DeleteView):
    model = models.Exercise_competence

    def get(self, request, *args, **kwargs):
        return redirect('/')

    def delete(self, request, *args, **kwargs):
        exercise_competence_pk = self.kwargs.get('pk')
        exercise_competence_object = models.Exercise_competence.objects.get(pk=exercise_competence_pk)
        exercise_pk = self.kwargs.get('id')
        exercise_object = models.Exercise.objects.get(pk=exercise_pk)
        activity_object = models.Activity.objects.get(pk=exercise_object.activity.pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(self.request.user) and services.SetService().is_owner(user=self.request.user, set_object=set_object):
            exercise_competence_object.delete()
            return redirect('exercises_update', pk=exercise_pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class ExerciseCompetenceCreateView(generic.CreateView):
    form_class = forms.ExerciseCompetenceUpdateForm
    template_name = EXERCISE_CREATE

    def get(self, request, *args, **kwargs):
        return redirect('/')

    def form_valid(self, form):
        exercise_pk = self.kwargs.get('pk')
        exercise_object = models.Exercise.objects.get(pk=exercise_pk)
        competence_pk = self.kwargs.get('id')
        competence_object = models.Competence.objects.get(pk=competence_pk)
        activity_object = models.Activity.objects.get(pk=exercise_object.activity.pk)
        set_object = activity_object.set_activity
        if services.UserService().is_teacher(self.request.user) and competence_object.level == 1 and services.SetService().is_owner(user=self.request.user, set_object=set_object):
            exercice_competence = form.save(commit=False)
            exercice_competence.exercise = exercise_object
            exercice_competence.competence = competence_object
            exercice_competence.save()

            return redirect('exercises_update', pk=exercise_pk)
        else:
            return redirect('/')
    
    def form_invalid(self, form):
        exercise_pk = self.kwargs.get('pk')
        return redirect('exercises_update', pk=exercise_pk)

# Evaluations 
@method_decorator(login_required, name='dispatch')
class EvaluationCreateView(generic.CreateView):
    form_class = forms.EvaluationCreateForm
    template_name = EVALUATION_UPDATE
    success_url = reverse_lazy('evaluations_list_final')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(EvaluationCreateView, self).get_context_data(**kwargs)
        context['partial'] = True
        context['create_final'] = True
        return context

    def form_valid(self, form):

        evaluation = form.save(commit=False) 
        evaluation.is_final=True
        evaluation.period = "Final"
        evaluation.save()

        return redirect('evaluations_list_final')

@method_decorator(login_required, name='dispatch')
class EvaluationCreateAllView(generic.CreateView):
    form_class = forms.EvaluationCreateAllForm
    template_name = EVALUATION_UPDATE
    success_url = reverse_lazy('evaluations_list_final')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationCreateAllView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(EvaluationCreateAllView, self).get_context_data(**kwargs)
        context['create_final'] = True
        return context

    def form_valid(self, form):
        subjects = models.Subject.objects.all().order_by('name')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        for subject in subjects:
            evaluation = models.Evaluation.objects.create(name=subject.name + " " + subject.level + "Final", start_date=start_date, end_date=end_date,
            is_final=True, period="Final", subject=subject)
            evaluation.save()
        

        return redirect('evaluations_list_final')

@method_decorator(login_required, name='dispatch')
class EvaluationCreateAllOneFinalThreePartialView(generic.CreateView):
    form_class = forms.EvaluationCreateOneFinalThreePartialForm
    template_name = EVALUATION_UPDATE
    success_url = reverse_lazy('evaluations_list_final')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationCreateAllOneFinalThreePartialView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(EvaluationCreateAllOneFinalThreePartialView, self).get_context_data(**kwargs)
        context['part1'] = True
        context['part2'] = True
        context['part3'] = True
        context['create_final'] = True
        return context

    def form_valid(self, form):
        subjects = models.Subject.objects.all().order_by('name')
        name = form.cleaned_data.get('name')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        period_1 = form.cleaned_data.get('period_1')
        start_date_1 = form.cleaned_data.get('start_date_1')
        end_date_1 = form.cleaned_data.get('end_date_1')
        period_2 = form.cleaned_data.get('period_2')
        start_date_2 = form.cleaned_data.get('start_date_2')
        end_date_2 = form.cleaned_data.get('end_date_2')
        period_3 = form.cleaned_data.get('period_3')
        start_date_3 = form.cleaned_data.get('start_date_3')
        end_date_3 = form.cleaned_data.get('end_date_3')
        

        for subject in subjects:
            evaluation = models.Evaluation.objects.create(name=name + " Final", start_date=start_date, end_date=end_date,
            is_final=True, period="Final", subject=subject)
            evaluation.save()
            evaluation1 = models.Evaluation.objects.create(name=name + " " + period_1, start_date=start_date_1, end_date=end_date_1,
            is_final=False, period=period_1, subject=subject, parent=evaluation)
            evaluation1.save()
            evaluation2 = models.Evaluation.objects.create(name=name + " " + period_2, start_date=start_date_2, end_date=end_date_2,
                is_final=False, period=period_2, subject=subject, parent=evaluation)
            evaluation2.save()
            evaluation3 = models.Evaluation.objects.create(name=name + " " + period_3, start_date=start_date_3, end_date=end_date_3,
                is_final=False, period=period_3, subject=subject, parent=evaluation)
            evaluation3.save()
        

        return redirect('evaluations_list_final')

@method_decorator(login_required, name='dispatch')
class EvaluationCreateAllOneFinalTwoPartialView(generic.CreateView):
    form_class = forms.EvaluationCreateOneFinalTwoPartialForm
    template_name = EVALUATION_UPDATE
    success_url = reverse_lazy('evaluations_list_final')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationCreateAllOneFinalTwoPartialView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(EvaluationCreateAllOneFinalTwoPartialView, self).get_context_data(**kwargs)
        context['part1'] = True
        context['part2'] = True
        context['create_final'] = True
        return context

    def form_valid(self, form):
        subjects = models.Subject.objects.all().order_by('name')
        name = form.cleaned_data.get('name')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        period_1 = form.cleaned_data.get('period_1')
        start_date_1 = form.cleaned_data.get('start_date_1')
        end_date_1 = form.cleaned_data.get('end_date_1')
        period_2 = form.cleaned_data.get('period_2')
        start_date_2 = form.cleaned_data.get('start_date_2')
        end_date_2 = form.cleaned_data.get('end_date_2')
        
        for subject in subjects:
            evaluation = models.Evaluation.objects.create(name=name + " Final", start_date=start_date, end_date=end_date,
            is_final=True, period="Final", subject=subject)
            evaluation.save()
            evaluation1 = models.Evaluation.objects.create(name=name + " " + period_1, start_date=start_date_1, end_date=end_date_1,
            is_final=False, period=period_1, subject=subject, parent=evaluation)
            evaluation1.save()
            evaluation2 = models.Evaluation.objects.create(name=name + " " + period_2, start_date=start_date_2, end_date=end_date_2,
                is_final=False, period=period_2, subject=subject, parent=evaluation)
            evaluation2.save()
        

        return redirect('evaluations_list_final')

@method_decorator(login_required, name='dispatch')
class EvaluationCreateChildView(generic.CreateView):
    form_class = forms.EvaluationCreateChildForm
    template_name = EVALUATION_UPDATE
    success_url = reverse_lazy('evaluations_list_final')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationCreateChildView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        evaluation_pk = self.kwargs.get('pk')
        context = super(EvaluationCreateChildView, self).get_context_data(**kwargs)
        context['create_partial'] = True
        context['parent_pk'] = evaluation_pk
        return context

    def form_valid(self, form):
        evaluation_pk = self.kwargs.get('pk')
        parent = models.Evaluation.objects.get(pk=evaluation_pk)

        evaluation = form.save(commit=False) 
        evaluation.is_final=False
        evaluation.parent = parent
        evaluation.subject = parent.subject
        evaluation.save()

        return redirect('evaluations_list_partial', pk=evaluation_pk)

@method_decorator(login_required, name='dispatch')
class EvaluationDeleteView(generic.DeleteView):
    template_name = 'evaluations/delete.html'
    model = models.Evaluation
    success_url = reverse_lazy('evaluations_list_final')

    def get(self, request, *args, **kwargs):
        evaluation_pk = self.kwargs.get('pk')
        parent = models.Evaluation.objects.get(pk=evaluation_pk)
        if services.UserService().is_admin(request.user):
            return super(EvaluationDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def delete(self, request, *args, **kwargs):
        evaluation_pk = self.kwargs.get('pk')
        evaluation = models.Evaluation.objects.get(pk=evaluation_pk)
        evaluation.delete()
        if evaluation.is_final:
            return redirect('evaluations_list_final')
        else:
            return redirect('evaluations_list_partial', pk=evaluation.parent.pk )

@method_decorator(login_required, name='dispatch')
class EvaluationsListFinalView(generic.ListView):
    model = models.Evaluation
    template_name = 'evaluations/list.html'
    context_object_name = 'evaluations_list'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationsListFinalView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    
    def get_context_data(self, **kwargs):
        context = super(EvaluationsListFinalView, self).get_context_data(**kwargs)
        context['list_final'] = True
        return context

    def get_queryset(self):
        queryset = models.Evaluation.objects.filter(is_final = True).order_by('name','subject', 'start_date')
        return queryset

@method_decorator(login_required, name='dispatch')
class EvaluationsListPartialView(generic.ListView):
    model = models.Evaluation
    template_name = 'evaluations/list.html'
    context_object_name = 'evaluations_list'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        parent_pk = self.kwargs.get('pk')
        parent = models.Evaluation.objects.get(pk=parent_pk)
        if services.UserService().is_admin(request.user) and parent.is_final:
            return super(EvaluationsListPartialView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')
    
    def get_context_data(self, **kwargs):
        parent_pk = self.kwargs.get('pk')
        context = super(EvaluationsListPartialView, self).get_context_data(**kwargs)
        context['list_partial'] = True
        context['parent_pk'] = parent_pk
        return context

    def get_queryset(self):
        parent_pk = self.kwargs.get('pk')
        parent = models.Evaluation.objects.get(pk=parent_pk)
        queryset = models.Evaluation.objects.filter(parent = parent).order_by('name','subject', 'start_date')
        return queryset
    
@method_decorator(login_required, name='dispatch')
class EvaluationUpdateView(generic.UpdateView):
    model = models.Evaluation
    form_class = forms.EvaluationCreateAllForm
    template_name = EVALUATION_UPDATE
    success_url = reverse_lazy('evaluations_list_final')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(EvaluationUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(EvaluationUpdateView, self).get_context_data(**kwargs)
        context['update'] = True
        return context
    
    def form_valid(self, form):
        evaluation = form.save()
        if evaluation.is_final:
            return redirect('evaluations_list_final')
        else:
            return redirect('evaluations_list_partial', pk=evaluation.parent.pk ) 

# Marks
@method_decorator(login_required, name='dispatch')        
class MarkActivityListView(generic.ListView):
    model = models.Activity_mark
    template_name = 'marks/activities.html'

    def get(self, request, *args, **kwargs):
        evalution_pk = self.kwargs.get('id')
        evaluation_object = models.Evaluation.objects.get(pk=evalution_pk)
        if evaluation_object.is_final:
            set_object = models.Set.objects.get(evaluation=evaluation_object)
        else:
            set_object = models.Set.objects.get(evaluation=evaluation_object.parent)
        
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(MarkActivityListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        evalution_pk = self.kwargs.get('id')
        evaluation_object = models.Evaluation.objects.get(pk=evalution_pk)
        student_pk = self.kwargs.get('pk')
        student_object = models.Student.objects.get(pk=student_pk)
        activities = models.Activity.objects.filter(evaluation=evaluation_object).order_by('date')
        if evaluation_object.is_final:
            set_object = models.Set.objects.get(evaluation=evaluation_object)
        else:
            set_object = models.Set.objects.get(evaluation=evaluation_object.parent)

        for ac in activities:
            if not models.Activity_mark.objects.filter(activity = ac, student=student_object).exists():
                ac_mark = models.Activity_mark.objects.create(activity = ac, student=student_object, evaluation_type="AUTOMATIC")
                ac_mark.save()
        
        ac_mark_saved = models.Activity_mark.objects.filter(activity__evaluation = evaluation_object, student=student_object).order_by('activity__date')

        context = super(MarkActivityListView, self).get_context_data(**kwargs)
        context['set_object'] = set_object
        context['student_object'] = student_object
        context['evaluation_object'] = evaluation_object
        context['ac_mark_saved'] = ac_mark_saved
        
        return context

@method_decorator(login_required, name='dispatch')        
class MarkEvaluationListView(generic.ListView):
    model = models.Evaluation_mark
    template_name = 'marks/evaluations.html'

    def get(self, request, *args, **kwargs):
        set_pk = self.kwargs.get('id')
        set_object = models.Set.objects.get(pk=set_pk)
        if services.UserService().is_teacher(request.user) and services.SetService().is_owner(user=request.user, set_object=set_object):
            return super(MarkEvaluationListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        set_pk = self.kwargs.get('id')
        set_object = models.Set.objects.get(pk=set_pk)
        student_pk = self.kwargs.get('pk')
        student_object = models.Student.objects.get(pk=student_pk)
        parent = set_object.evaluation
        evaluations = models.Evaluation.objects.filter(parent=parent).order_by('period')

        if not models.Evaluation_mark.objects.filter(evaluation = parent, student=student_object).exists():
            parent_mark = models.Evaluation_mark.objects.create(evaluation = parent, student=student_object, evaluation_type="AUTOMATIC")
            parent_mark.save()

        for ev in evaluations:
            if not models.Evaluation_mark.objects.filter(evaluation = ev, student=student_object).exists():
                ev_mark = models.Evaluation_mark.objects.create(evaluation = ev, student=student_object, evaluation_type="AUTOMATIC")
                ev_mark.save()
        
        parent_mark_saved = models.Evaluation_mark.objects.filter(evaluation = parent, student=student_object).first()
        ev_mark_saved = models.Evaluation_mark.objects.filter(evaluation__parent = parent, student=student_object).order_by('evaluation__period')

        context = super(MarkEvaluationListView, self).get_context_data(**kwargs)
        context['set_object'] = set_object
        context['student_object'] = student_object
        context['parent_mark_saved'] = parent_mark_saved
        context['ev_mark_saved'] = ev_mark_saved
        
        return context

# My
@method_decorator(login_required, name='dispatch')        
class MySetStudentListView(generic.ListView):
    model = models.Set
    template_name = 'students/list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_teacher(request.user):
            return super(MySetStudentListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        set_object_pk = self.kwargs.get('pk')
        set_object = models.Set.objects.get(pk=set_object_pk)
        object_list = set_object.students.all().order_by('surname')
        context = super(MySetStudentListView, self).get_context_data(object_list=object_list, **kwargs)
        context['set_object_pk'] = set_object_pk

        return context

@method_decorator(login_required, name='dispatch')
class MySetsListView(generic.ListView):
    model = models.Set
    template_name = 'sets/list.html'
    context_object_name = 'set_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_teacher(request.user):
            return super(MySetsListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Set.objects.filter(teacher__user=self.request.user).order_by('name')
        return queryset

# Sets
@method_decorator(login_required, name='dispatch') 
class SetAssignStudentView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            student_pk = self.kwargs.get('pk')
            student = models.Student.objects.get(pk=student_pk)
            set_pk = self.kwargs.get('id')
            set_object = models.Set.objects.get(pk=set_pk)

            set_object.students.add(student)
            set_object.save()
            return redirect('sets_assign_student_list', pk=set_pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')        
class SetAssignStudentListView(generic.ListView, generic.list.MultipleObjectMixin):
    model = models.Set
    template_name = 'students/list_assign_student.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SetAssignStudentListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        set_object_pk = self.kwargs.get('pk')
        set_object = models.Set.objects.get(pk=set_object_pk)
        object_list = set_object.students.all().order_by('surname')
        context = super(SetAssignStudentListView, self).get_context_data(
            object_list=object_list, **kwargs)
        context['other_students'] = models.Student.objects.all().exclude(id__in=object_list).order_by('surname')
        context['set_object_pk'] = set_object_pk

        return context

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
class SetsListView(generic.ListView):
    model = models.Set
    template_name = 'sets/list.html'
    context_object_name = 'set_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SetsListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Set.objects.all().order_by('name')
        return queryset

@method_decorator(login_required, name='dispatch') 
class SetUnassignStudentView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            student_pk = self.kwargs.get('pk')
            student = models.Student.objects.get(pk=student_pk)
            set_pk = self.kwargs.get('id')
            set_object = models.Set.objects.get(pk=set_pk)

            set_object.students.remove(student)
            set_object.save()
            return redirect('sets_assign_student_list', pk=set_pk)
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

# Students
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
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user) :
            return super(StudentsListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Student.objects.all().order_by('surname')
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

# Subjects
@method_decorator(login_required, name='dispatch')   
class SubjectAssignCompetenceView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            competence_pk = self.kwargs.get('pk')
            competence = models.Competence.objects.get(pk=competence_pk)
            subject_pk = self.kwargs.get('id')
            subject_object = models.Subject.objects.get(pk=subject_pk)

            subject_object.competences.add(competence)
            subject_object.save()
            subject_object.competences.add(competence.parent)
            subject_object.save()
            subject_object.competences.add(competence.parent.parent)
            subject_object.save()
            return redirect('subjects_assign_competence_list', pk=subject_pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')        
class SubjectAssignCompetenceListView(generic.ListView, generic.list.MultipleObjectMixin):
    model = models.Subject
    template_name = 'competences/list_assign_competence.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SubjectAssignCompetenceListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        subject_object_pk = self.kwargs.get('pk')
        subject_object = models.Subject.objects.get(pk=subject_object_pk)
        object_list = subject_object.competences.all().order_by('code')
        context = super(SubjectAssignCompetenceListView, self).get_context_data(
            object_list=object_list, **kwargs)
        context['other_competences'] = models.Competence.objects.filter(level = 1).exclude(id__in=object_list).order_by('code')
        context['subject_object_pk'] = subject_object_pk

        return context

@method_decorator(login_required, name='dispatch')
class SubjectCreateView(generic.CreateView):
    form_class = forms.SubjectCreateForm
    template_name = "subjects/create.html"
    success_url = reverse_lazy('subjects_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SubjectCreateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class SubjectsDeleteView(generic.DeleteView):
    template_name = 'subjects/delete.html'
    model = models.Subject
    success_url = reverse_lazy('subjects_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SubjectsDeleteView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')
class SubjectsListView(generic.ListView):
    model = models.Subject
    template_name = 'subjects/list.html'
    context_object_name = 'subject_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SubjectsListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Subject.objects.all().order_by('name')
        return queryset

@method_decorator(login_required, name='dispatch')   
class SubjectListCompetenceView(generic.ListView):
    model = models.Subject
    template_name = 'subjects/competence_list.html'
    context_object_name = 'subject_competence_list'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_teacher(request.user):
            return super(SubjectListCompetenceView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        subject_object_pk = self.kwargs.get('pk')
        subject_object = models.Subject.objects.get(pk=subject_object_pk)
        queryset = subject_object.competences.all().order_by('code')
        return queryset

@method_decorator(login_required, name='dispatch')
class SubjectsOwnerListView(generic.ListView):
    model = models.Student
    template_name = 'subjects/list.html'
    context_object_name = 'subject_list'
    paginate_by = 5


    def get(self, request, *args, **kwargs):
        if services.UserService().is_teacher(request.user):
            return super(SubjectsOwnerListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        user = self.request.user
        teacher = models.Teacher.objects.get(user=user)
        subjects = teacher.subjects.all().order_by('name')
        return subjects     
        
@method_decorator(login_required, name='dispatch')        
class SubjectsUpdateView(generic.UpdateView):
    model = models.Subject
    form_class = forms.SubjectCreateForm
    template_name = "subjects/create.html"
    success_url = reverse_lazy('subjects_list')

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(SubjectsUpdateView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')   
class SubjectUnassignCompetenceView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            competence_pk = self.kwargs.get('pk')
            competence = models.Competence.objects.get(pk=competence_pk)
            subject_pk = self.kwargs.get('id')
            subject_object = models.Subject.objects.get(pk=subject_pk)
            parent = competence.parent
            grandparent = competence.parent.parent

            level2_list = models.Competence.objects.filter(parent = grandparent, competences = subject_object)
            count_level2 = level2_list.count()

            level1_list = models.Competence.objects.filter(parent = parent, competences = subject_object)
            count_level1 = level1_list.count()

            if count_level1 == 1:
                subject_object.competences.remove(parent)

            if count_level1 == 1 and count_level2 == 1:
                subject_object.competences.remove(grandparent)
            
            subject_object.competences.remove(competence)
            subject_object.save()

            return redirect('subjects_assign_competence_list', pk=subject_pk)
        else:
            return redirect('/')
            
# Teachers
@method_decorator(login_required, name='dispatch') 
class TeacherAssignSubjectView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            subject_pk = self.kwargs.get('pk')
            subject = models.Subject.objects.get(pk=subject_pk)
            teacher_pk = self.kwargs.get('id')
            teacher_object = models.Teacher.objects.get(pk=teacher_pk)

            teacher_object.subjects.add(subject)
            teacher_object.save()
            return redirect('teachers_assign_subject_list', pk=teacher_pk)
        else:
            return redirect('/')

@method_decorator(login_required, name='dispatch')        
class TeacherAssignSubjectListView(generic.ListView, generic.list.MultipleObjectMixin):
    model = models.Teacher
    template_name = 'subjects/list_assign_subject.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(TeacherAssignSubjectListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_context_data(self, **kwargs):
        teacher_object_pk = self.kwargs.get('pk')
        teacher_object = models.Teacher.objects.get(pk=teacher_object_pk)
        object_list = teacher_object.subjects.all().order_by('name')
        context = super(TeacherAssignSubjectListView, self).get_context_data(
            object_list=object_list, **kwargs)
        context['other_subjects'] = models.Subject.objects.all().exclude(id__in=object_list).order_by('name')
        context['teacher_object_pk'] = teacher_object_pk

        return context

@method_decorator(login_required, name='dispatch')
class TeacherCreateView(generic.CreateView):
    form_class = forms.UserCreateForm
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
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            return super(TeachersListView, self).get(self, request, *args, **kwargs)
        else:
            return redirect('/')

    def get_queryset(self):
        queryset = models.Teacher.objects.all().order_by('user__last_name')
        return queryset

@method_decorator(login_required, name='dispatch') 
class TeacherUnassignSubjectView(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        if services.UserService().is_admin(request.user):
            subject_pk = self.kwargs.get('pk')
            subject = models.Subject.objects.get(pk=subject_pk)
            teacher_pk = self.kwargs.get('id')
            teacher_object = models.Teacher.objects.get(pk=teacher_pk)

            teacher_object.subjects.remove(subject)
            teacher_object.save()
            return redirect('teachers_assign_subject_list', pk=teacher_pk)
        else:
            return redirect('/')

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

