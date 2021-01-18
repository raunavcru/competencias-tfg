from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from dal import autocomplete

from . import models

User = get_user_model()

teachers = models.Teacher.objects.all()
subjects = models.Subject.objects.all()
evaluations = models.Evaluation.objects.all()

class StudentCreateForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Raúl', 'id': 'first_name-create-student'}))
    surname = forms.CharField(required=True)
    birthdate = forms.DateField(required=True)
    initials = forms.CharField(required=True)

    class Meta:
        model = models.Student
        fields = (
            'name',
            'surname',
            'birthdate',
            'initials',

        )

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate >= now().date():
            raise ValidationError(
                'La fecha de cumpleaños debe ser en el pasado')
        return birthdate

class TeacherCreateForm(UserCreationForm):
    
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Alberto', 'id': 'first_name-create-teacher'}))
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(required=True)
    initials = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'birthdate',
            'initials',
            'password1',
            'password2'
        )
        
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate >= now().date():
            raise ValidationError(
                'La fecha de cumpleaños debe ser en el pasado')
        return birthdate

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exist = User.objects.filter(username=username)
        if exist:
            raise ValidationError('Usuario ya registrado')
        return username
        
class TeacherUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(required=True)
    initials = forms.CharField(required=True)

    class Meta:
        model = models.Teacher
        fields = (
            'birthdate',
            'initials',
        )   

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Alberto', 'id': 'first_name-create-teacher'}))
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )   

class SetCreateForm(forms.ModelForm):
    
    name = forms.CharField(required=True)
    level = forms.CharField(required=True)
    grade = forms.CharField(required=True)
    line = forms.CharField(required=True)
    teacher = forms.ModelChoiceField(queryset = models.Teacher.objects.all(),
        widget = autocomplete.ModelSelect2(url='autocomplete_teachers'))
    subject = forms.ModelChoiceField(subjects, empty_label=None)
    evaluation = forms.ModelChoiceField(evaluations, empty_label=None)

    class Meta:
        model = models.Set
        fields = (
            'name',
            'level',
            'grade',
            'line',
            'teacher',
            'subject',
            'evaluation',
        )
        widgets = {
            'teacher': autocomplete.ModelSelect2(url='autocomplete_teachers')
        } 