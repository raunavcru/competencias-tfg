from django.urls import path, re_path
from . import views
from . import models

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('404', views.not_impl.as_view(), name = '404'),

    path('administrators/create', views.AdministratorCreateView.as_view(), name = 'administrators_create'),
    path('administrators/<int:pk>/delete', views.AdministratorDeleteView.as_view(), name='administrators_delete'),
    path('administrators/list', views.AdministratorsListView.as_view(), name = 'administrators_list'),
    path('administrators/<int:pk>/update', views.AdministratorUpdateView.as_view(), name = 'administrators_update'),

    path('competences/create', views.CompetenceCreateLevel3View.as_view(), name = 'competences_create'),
    path('competences/list/level1', views.CompetenceListLevel1View.as_view(), name = 'competences_list1'),
    path('competences/list/level2', views.CompetenceListLevel2View.as_view(), name = 'competences_list2'),
    path('competences/list/level3', views.CompetenceListLevel3View.as_view(), name = 'competences_list3'),
    path('competences/<int:pk>/delete', views.CompetencesDeleteView.as_view(), name='competences_delete'),
    path('competences/<int:pk>/update', views.CompetenceUpdateView.as_view(), name = 'competences_update'),
    path('competences/<int:pk>/list', views.CompetencesListChildView.as_view(), name='competences_relation'),
    path('competences/<int:pk>/create', views.CompetenceCreateChildView.as_view(), name='competences_relation2'),

    path('evaluations/create', views.EvaluationCreateView.as_view(), name = 'evaluations_create'),
    path('evaluations/list', views.EvaluationsListView.as_view(), name = 'evaluations_list'),
    path('evaluations/<int:pk>/delete', views.EvaluationDeleteView.as_view(), name='evaluations_delete'),
    path('evaluations/<int:pk>/update', views.EvaluationUpdateView.as_view(), name = 'evaluations_update'),

    path('my_sets/list', views.MySetsListView.as_view(), name = 'my_sets_list'),
    path('my_subjects/list', views.SubjectsOwnerListView.as_view(), name = 'my_subjects_list'),

    path('sets/<int:pk>/assign/list', views.SetAssignStudentListView.as_view(), name = 'sets_assign_student_list'),
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