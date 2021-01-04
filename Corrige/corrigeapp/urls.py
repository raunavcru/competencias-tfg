from django.urls import path

from . import views

urlpatterns = [
    path('teachers/list', views.TeachersListView.as_view(), name = 'teachers_list'),
]