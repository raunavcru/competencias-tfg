from django.urls import path, re_path
from . import views
from . import models

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('404', views.not_impl.as_view(), name = '404'),

    path('activities/<int:pk>/create', views.ActivityCreateView.as_view(), name = 'activities_create'),
    path('activities/<int:pk>/delete', views.ActivityDeleteView.as_view(), name = 'activities_delete'),
    path('activities/<int:pk>/list', views.ActivitiesListView.as_view(), name = 'activities_list'),
    path('activities/<int:pk>/list/copy', views.ActivitiesListCopyView.as_view(), name = 'activities_list_copy'),
    path('activities/<int:pk>/update', views.ActivityUpdateView.as_view(), name = 'activities_update'),
    path('activities/<int:pk>/<int:id>/copy', views.ActivityCopyView.as_view(), name = 'activities_copy'),

    path('administrators/create', views.AdministratorCreateView.as_view(), name = 'administrators_create'),
    path('administrators/<int:pk>/delete', views.AdministratorDeleteView.as_view(), name='administrators_delete'),
    path('administrators/list', views.AdministratorsListView.as_view(), name = 'administrators_list'),
    path('administrators/<int:pk>/update', views.AdministratorUpdateView.as_view(), name = 'administrators_update'),

    path('blocks/<int:pk>/create', views.BlockCreateView.as_view(), name = 'blocks_create'),
    path('blocks/<int:pk>/delete', views.BlockDeleteView.as_view(), name = 'blocks_delete'),
    path('blocks/<int:pk>/list', views.BlocksListView.as_view(), name = 'blocks_list'),
    path('blocks/<int:pk>/update', views.BlockUpdateView.as_view(), name = 'blocks_update'),

    path('competences/create', views.CompetenceCreateLevel3View.as_view(), name = 'competences_create'),
    path('competences/list/level1', views.CompetenceListLevel1View.as_view(), name = 'competences_list1'),
    path('competences/list/level2', views.CompetenceListLevel2View.as_view(), name = 'competences_list2'),
    path('competences/list/level3', views.CompetenceListLevel3View.as_view(), name = 'competences_list3'),
    path('competences/<int:pk>/delete', views.CompetencesDeleteView.as_view(), name='competences_delete'),
    path('competences/<int:pk>/update', views.CompetenceUpdateView.as_view(), name = 'competences_update'),
    path('competences/<int:pk>/list', views.CompetencesListChildView.as_view(), name='competences_list_child'),
    path('competences/<int:pk>/create', views.CompetenceCreateChildView.as_view(), name='competences_relation2'),
    path('competences/<int:id>/<int:pk>/delete', views.CompetencesDeleteView.as_view(), name='competences_delete_child'),
    path('competences/<int:id>/<int:pk>/update', views.CompetenceUpdateView.as_view(), name = 'competences_update_child'),

    path('exercises/<int:pk>/create', views.ExerciseCreateView.as_view(), name = 'exercises_create'),
    path('exercises/<int:pk>/delete', views.ExerciseDeleteView.as_view(), name = 'exercises_delete'),
    path('exercises/<int:pk>/update', views.ExerciseUpdateView.as_view(), name = 'exercises_update'),
    path('exercises/<int:type>/<int:pk>/list', views.ExercisesListView.as_view(), name = 'exercises_list'),

    path('exercises/competence/<int:id>/<int:pk>/delete', views.ExerciseCompetenceDeleteView.as_view(), name = 'exercise_competences_delete'),
    path('exercises/competence/<int:id>/<int:pk>/create', views.ExerciseCompetenceCreateView.as_view(), name = 'exercise_competences_create'),

    path('evaluations/create', views.EvaluationCreateView.as_view(), name = 'evaluations_create'),
    path('evaluations/create/all', views.EvaluationCreateAllView.as_view(), name = 'evaluations_create_all'),
    path('evaluations/create/all/oneFinalThreePartial', views.EvaluationCreateAllOneFinalThreePartialView.as_view(), name = 'evaluations_create_all_oneFinalThreePartial'),
    path('evaluations/create/all/oneFinalTwoPartial', views.EvaluationCreateAllOneFinalTwoPartialView.as_view(), name = 'evaluations_create_all_oneFinalTwoPartial'),
    path('evaluations/list', views.EvaluationsListFinalView.as_view(), name = 'evaluations_list_final'),
    path('evaluations/<int:pk>/create/child', views.EvaluationCreateChildView.as_view(), name = 'evaluations_create_child'),
    path('evaluations/<int:pk>/delete', views.EvaluationDeleteView.as_view(), name='evaluations_delete'),
    path('evaluations/<int:pk>/list', views.EvaluationsListPartialView.as_view(), name = 'evaluations_list_partial'),
    path('evaluations/<int:pk>/update', views.EvaluationUpdateView.as_view(), name = 'evaluations_update'),

    path('marks/activities/<int:pk>/create', views.MarkActivityCreateView.as_view(), name = 'marks_activities_create'),
    path('marks/activities/<int:sk>/<int:id>/<int:pk>/list', views.MarkActivityListView.as_view(), name = 'marks_activities_list'),
    path('marks/competences/<int:id>/<int:pk>/create', views.MarkCompetenceCreateView.as_view(), name = 'marks_competences_create'),
    path('marks/competences/<int:id>/<int:pk>/list', views.MarkCompetenceListView.as_view(), name = 'marks_competences_list'),
    path('marks/evaluations/<int:id>/<int:pk>/create', views.MarkEvaluationCreateView.as_view(), name = 'marks_evaluations_create'),
    path('marks/evaluations/<int:id>/<int:pk>/list', views.MarkEvaluationListView.as_view(), name = 'marks_evaluations_list'),
    path('marks/exercises/<int:pk>/create', views.MarkExerciseCreateView.as_view(), name = 'marks_exercises_create'),
    path('marks/exercises/<int:id>/<int:pk>/list', views.MarkExerciseListView.as_view(), name = 'marks_exercises_list'),

    path('my_sets/list', views.MySetsListView.as_view(), name = 'my_sets_list'),
    path('my_subjects/list', views.SubjectsOwnerListView.as_view(), name = 'my_subjects_list'),

    path('profile/update', views.UserUpdateView.as_view(), name = 'profile_update'),

    path('sets/<int:pk>/assign/list', views.SetAssignStudentListView.as_view(), name = 'sets_assign_student_list'),
    path('sets/<int:pk>/list', views.MySetStudentListView.as_view(), name = 'sets_student_list'),
    path('sets/<int:pk>/<int:id>/assign/', views.SetAssignStudentView.as_view(), name = 'sets_assign_student'),
    path('sets/<int:pk>/<int:id>/unassign/', views.SetUnassignStudentView.as_view(), name = 'sets_unassign_student'),
    path('sets/create', views.SetCreateView.as_view(), name = 'sets_create'),
    path('sets/<int:pk>/update', views.SetUpdateView.as_view(), name = 'sets_update'),
    path('sets/list', views.SetsListView.as_view(), name = 'sets_list'),
    path('sets/<int:pk>/delete', views.SetDeleteView.as_view(), name='sets_delete'),
    
    path('students/list', views.StudentsListView.as_view(), name = 'students_list'),
    path('students/create', views.StudentCreateView.as_view(), name = 'students_create'),
    path('students/<int:pk>/delete', views.StudentDeleteView.as_view(), name='students_delete'),
    path('students/<int:pk>/update', views.StudentUpdateView.as_view(), name = 'students_update'),

    path('subjects/list', views.SubjectsListView.as_view(), name = 'subjects_list'),
    path('subjects/create', views.SubjectCreateView.as_view(), name = 'subjects_create'),
    path('subjects/<int:pk>/delete', views.SubjectsDeleteView.as_view(), name='subjects_delete'),
    path('subjects/<int:pk>/update', views.SubjectsUpdateView.as_view(), name = 'subjects_update'),
    path('subjects/<int:pk>/assign/list', views.SubjectAssignCompetenceListView.as_view(), name = 'subjects_assign_competence_list'),
    path('subjects/<int:pk>/competence/list', views.SubjectListCompetenceView.as_view(), name = 'subject_competence_list'),
    path('subjects/<int:pk>/<int:id>/assign/', views.SubjectAssignCompetenceView.as_view(), name = 'subjects_assign_competence'),
    path('subjects/<int:pk>/<int:id>/unassign/', views.SubjectUnassignCompetenceView.as_view(), name = 'subjects_unassign_competence'),

    path('teachers/create', views.TeacherCreateView.as_view(), name = 'teachers_create'),
    path('teachers/<int:pk>/delete', views.TeacherDeleteView.as_view(), name='teachers_delete'),
    path('teachers/list', views.TeachersListView.as_view(), name = 'teachers_list'),
    path('teachers/<int:pk>/update', views.TeacherUpdateView.as_view(), name = 'teachers_update'),
    path('teachers/<int:pk>/assign/list', views.TeacherAssignSubjectListView.as_view(), name = 'teachers_assign_subject_list'),
    path('teachers/<int:pk>/<int:id>/assign/', views.TeacherAssignSubjectView.as_view(), name = 'teachers_assign_subject'),
    path('teachers/<int:pk>/<int:id>/unassign/', views.TeacherUnassignSubjectView.as_view(), name = 'teachers_unassign_subject'),


]