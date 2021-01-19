from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from dal import autocomplete
from django.contrib.auth.hashers import check_password

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

    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        if len(initials) > 9:
            raise ValidationError(
                'El tamaño de las iniciales no puede ser mayor que 9')
        return initials

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            raise ValidationError(
                'El tamaño del nombre no puede ser mayor que 100')
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if len(surname) > 100:
            raise ValidationError(
                'El tamaño del apellido no puede ser mayor que 100')
        return surname
    
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


    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        if len(initials) > 9:
            raise ValidationError(
                'El tamaño de las iniciales no puede ser mayor que 9')
        return initials

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 100:
            raise ValidationError(
                'El tamaño del nombre no puede ser mayor que 100')
        return first_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('El email es necesario')
        elif User.objects.filter(email=email).exists():
            raise ValidationError('El email ya existe')
        return email

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 100:
            raise ValidationError(
                'El tamaño del apellido no puede ser mayor que 100')
        return last_name
        
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

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate >= now().date():
            raise ValidationError(
                'La fecha de cumpleaños debe ser en el pasado')
        return birthdate

    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        if len(initials) > 9:
            raise ValidationError(
                'El tamaño de las iniciales no puede ser mayor que 9')
        return initials

    
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

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 100:
            raise ValidationError(
                'El tamaño del nombre no puede ser mayor que 100')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 100:
            raise ValidationError(
                'El tamaño del apellido no puede ser mayor que 100')
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('El email es necesario')
        elif User.objects.filter(email=email).exists():
            raise ValidationError('El email ya existe')
        return email

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

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if len(grade) > 50:
            raise ValidationError(
                'El tamaño del grado no puede ser mayor que 50')
        return line

    def clean_level(self):
        level = self.cleaned_data.get('level')
        if len(level) > 50:
            raise ValidationError(
                'El tamaño del nivel no puede ser mayor que 50')
        return line

    def clean_line(self):
        line = self.cleaned_data.get('line')
        if len(line) > 50:
            raise ValidationError(
                'El tamaño de la línea no puede ser mayor que 50')
        return line

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            raise ValidationError(
                'El tamaño del nombre no puede ser mayor que 100')
        return name