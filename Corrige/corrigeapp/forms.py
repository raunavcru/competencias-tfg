from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import get_language, activate
from django.contrib.auth.hashers import check_password

from . import models

User = get_user_model()

teachers = models.Teacher.objects.all()
subjects = models.Subject.objects.all()
evaluations = models.Evaluation.objects.all()

DATE_PLACEHOLDER = 'dd/mm/aaaa'
DATE_PLACEHOLDER_EN = 'mm/dd/yyyy'
MESSAGE_INITIALS = 'El tamaño de las iniciales no puede ser mayor que 9'
MESSAGE_INITIALS_EN = 'Initials can not be longer of 9 characters'
MESSAGE_NAME = 'El tamaño del nombre no puede ser mayor que 100'
MESSAGE_NAME_EN = 'Name can not be longer of 100 characters'
MESSAGE_SURNAME = 'El tamaño del apellido no puede ser mayor que 100'
MESSAGE_SURNAME_EN = 'Surname can not be longer of 100 characters'
MESSAGE_BIRTHDATE = 'La fecha de cumpleaños debe ser en el pasado'
MESSAGE_BIRTHDATE_EN = 'Birthdate can not be past'

class StudentCreateForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Raúl', 'id': 'first_name-create-student'}))
    surname = forms.CharField(required=True)
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    initials = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(StudentCreateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = DATE_PLACEHOLDER_EN
            self.fields['birthdate'].widget.format = settings.DATE_INPUT_FORMATS[0]


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
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_INITIALS_EN)
            else:
                raise ValidationError(
                    MESSAGE_INITIALS)
        return initials

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_NAME_EN)
            else:
                raise ValidationError(
                    MESSAGE_NAME)
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if len(surname) > 100:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_SURNAME_EN)
            else:
                raise ValidationError(
                    MESSAGE_SURNAME)
        return surname
    
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate >= now().date():
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_BIRTHDATE_EN)
            else:
                raise ValidationError(
                    MESSAGE_BIRTHDATE)
        return birthdate

class TeacherCreateForm(UserCreationForm):
    
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Alberto', 'id': 'first_name-create-teacher'}))
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
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
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_INITIALS_EN)
            else:
                raise ValidationError(
                    MESSAGE_INITIALS)
        return initials

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 100:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_NAME_EN)
            else:
                raise ValidationError(
                    MESSAGE_NAME)
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
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_SURNAME_EN)
            else:
                raise ValidationError(
                    MESSAGE_SURNAME)
        return last_name
        
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate >= now().date():
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_BIRTHDATE_EN)
            else:
                raise ValidationError(
                    MESSAGE_BIRTHDATE)
        return birthdate

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exist = User.objects.filter(username=username)
        if exist:
            raise ValidationError('Usuario ya registrado')
        return username
        
class TeacherUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
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
                MESSAGE_BIRTHDATE)
        return birthdate

    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        
        if len(initials) > 9:
            raise ValidationError(
                MESSAGE_INITIALS)
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
                MESSAGE_NAME)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 100:
            raise ValidationError(
                MESSAGE_SURNAME)
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
    teacher = forms.ModelChoiceField(teachers, empty_label=None)
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
            if get_language() == 'en':
                raise ValidationError(
                    'Grade can not be longer of 50 characters')
            else:
                raise ValidationError(
                    'El tamaño del grado no puede ser mayor que 50')
        return grade

    def clean_level(self):
        level = self.cleaned_data.get('level')
        if len(level) > 50:
            if get_language() == 'en':
                raise ValidationError(
                    'Level can not be longer of 50 characters')
            else:
                raise ValidationError(
                    'El tamaño del nivel no puede ser mayor que 50')
        return level


    def clean_line(self):
        line = self.cleaned_data.get('line')
        if len(line) > 50:
            if get_language() == 'en':
                raise ValidationError(
                    'Line can not be longer of 50 characters')
            else:
                raise ValidationError(
                    'El tamaño de la línea no puede ser mayor que 50')
        return line

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_NAME_EN)
            else:
                raise ValidationError(
                    MESSAGE_NAME)
        return name

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': "albsoucru"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': "***************"}))

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


