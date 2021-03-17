from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import get_language, activate
from django.contrib.auth.hashers import check_password

from . import models
from . import services

User = get_user_model()

teachers = models.Teacher.objects.all()
subjects = models.Subject.objects.all()
evaluations_final = models.Evaluation.objects.filter(is_final=True)

CHOICES_YES_NO = ((False, "No"), (True, "Sí"))
CHOICES_YES_NO_EN = ((False, "No"), (True, "Yes"))
CHOICES_LEVEL = (("1º","1º"),("2º","2º"),("3º","3º"),("4º","4º"),("5º","5º"),("6º","6º"))
CHOICES_GRADE = (("PrimarySchool","Educación Primaria"),("SecondaryEducation","Educación Secundaria"),("SixthForm","Bachillerato"),("FurtherEducation","Grado Medio o Superior"),("University","Grado Universitario"))
CHOICES_GRADE_EN = ((" PrimarySchool","Primary School"),("SecondaryEducation","Secondary Education"),("SixthForm","Sixth Form"),("FurtherEducation","Further Education"),("University","University"))


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
MESSAGE_GRADE = 'La calificación no puede tener más de 50 caracteres'
MESSAGE_GRADE_EN = 'Grade can not be longer of 50 characters'
MESSAGE_LEVEL_EN = 'Level can not be longer of 50 characters'
MESSAGE_LEVEL = 'El tamaño del nivel no puede ser mayor que 50'
MESSAGE_LINE_EN = 'Line must be a letter'
MESSAGE_LINE = 'Línea solo pueden ser un letra'
MESSAGE_DESCRIPTION_EN = 'Description can not be longer of 100 characters'
MESSAGE_DESCRIPTION = 'El tamaño de la descripción no puede ser mayor que 100'
MESSAGE_CODE_EN = 'Code can not be longer of 50 characters'
MESSAGE_CODE = 'El tamaño del código no puede ser mayor que 50'
PLACEHOLDER_NAME_EVALUATION = 'Matemáticas 5º Primaria'
PLACEHOLDER_PERIOD_EVALUATION = '1er Trimestre'

# Activity
class ActivityUpdateForm(forms.ModelForm):
    date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    weight = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': '1', 'id': 'wieight-create-competence'}))
    evaluation = forms.ModelChoiceField(evaluations_final, empty_label=None)
    is_recovery = forms.ChoiceField(
        widget = forms.Select(),
        choices = CHOICES_YES_NO
    )

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices', None)
        super(ActivityUpdateForm, self).__init__(*args, **kwargs)
        self.fields['evaluation'].queryset = self.choices
        if get_language() == 'en':
            self.fields['date'].widget.attrs['placeholder'] = DATE_PLACEHOLDER_EN
            self.fields['date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['is_recovery'].choices = CHOICES_YES_NO_EN
    
    class Meta:
        model = models.Activity
        fields = (
            'date',
            'weight',
            'evaluation',
            'is_recovery',
        )   

# Administrator
class AdministratorUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    initials = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AdministratorUpdateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = DATE_PLACEHOLDER_EN
            self.fields['birthdate'].widget.format = settings.DATE_INPUT_FORMATS[0]

    class Meta:
        model = models.Administrator
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

# Competences
class CompetenceCreateForm(forms.ModelForm):

    code = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'CC1', 'id': 'code-create-competence'}))
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Comunicación lingüística', 'id': 'name-create-competence'}))
    description = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Comunicación lingüística.	', 'id': 'description-create-competence'}))
    weight = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': '1', 'id': 'wieight-create-competence'}))

    class Meta:
        model = models.Competence
        fields = (
            'code',
            'name',
            'description',
            'weight',
        )
        
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if len(code) > 50:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_CODE_EN)
            else:
                raise ValidationError(
                    MESSAGE_CODE)
        return code

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 300:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_DESCRIPTION_EN)
            else:
                raise ValidationError(
                    MESSAGE_DESCRIPTION)
        return description

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 300:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_NAME_EN)
            else:
                raise ValidationError(
                    MESSAGE_NAME)
        return name

# Exercices
class ExerciseUpdateForm(forms.ModelForm):
    weight = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': '1', 'id': 'weight-create-exercice'}))
    statement = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'id': 'statement-create-exercice'}))

    class Meta:
        model = models.Exercise
        fields = (
            'weight',
            'statement',
        )  

# Exercices_competence
class ExerciseCompetenceUpdateForm(forms.ModelForm):
    intensity = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': '1', 'id': 'intensity-create-exercice_competence'}))
    weight = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': '1', 'id': 'weight-create-exercice_competence'}))

    class Meta:
        model = models.Exercise_competence
        fields = (
            'intensity',
            'weight',
        )  

# Evaluations
class EvaluationCreateForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    subject = forms.ModelChoiceField(subjects, empty_label=None)

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'start_date',
            'end_date',
            'subject',
        )

class EvaluationCreateAllForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'start_date',
            'end_date',
        )

class EvaluationCreateChildForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    period = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'period',
            'start_date',
            'end_date',
        )

class EvaluationCreateOneFinalThreePartialForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    period_1 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    start_date_1 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date_1 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    period_2 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    start_date_2 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date_2 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    period_3 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    start_date_3 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date_3 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    
    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'start_date',
            'end_date',
            'period_1',
            'start_date_1',
            'end_date_1',
            'period_2',
            'start_date_2',
            'end_date_2',
            'period_3',
            'start_date_3',
            'end_date_3',
        )

class EvaluationCreateOneFinalTwoPartialForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    period_1 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    start_date_1 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date_1 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    period_2 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    start_date_2 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    end_date_2 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    
    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'start_date',
            'end_date',
            'period_1',
            'start_date_1',
            'end_date_1',
            'period_2',
            'start_date_2',
            'end_date_2',
        )

# Sets
class SetCreateForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Matemáticas', 'id': 'name-create-set'}))
    line = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'A', 'id': 'line-create-set'}))
    teacher = forms.ModelChoiceField(teachers, empty_label=None)
    subject = forms.ModelChoiceField(subjects, empty_label=None)
    evaluation = forms.ModelChoiceField(evaluations_final, empty_label=None)

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
            'level': forms.Select(choices=CHOICES_LEVEL),
            'grade': forms.Select(choices=CHOICES_GRADE)
        }

    def clean_level(self):
        level = self.cleaned_data.get('level')
        if len(level) > 50:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_LEVEL_EN)
            else:
                raise ValidationError(
                    MESSAGE_LEVEL)
        return level


    def clean_line(self):
        line = self.cleaned_data.get('line')
        if not line.isalpha() or len(line) > 1:
            if get_language() == 'en':
                raise ValidationError(
                    MESSAGE_LINE_EN)
            else:
                raise ValidationError(
                    MESSAGE_LINE)
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

# Student
class StudentCreateForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Raúl', 'id': 'first_name-create-student'}))
    surname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Navarro Cruz', 'id': 'surname-create-student'}))
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    initials = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'placeholder': 'RNC', 'id': 'initials-create-student'}))

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

# Subjects
class SubjectCreateForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Ciencias Sociales', 'id': 'name-create-subject'}))
    description = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Las ciencias sociales son las ramas de la ciencia relacionadas con ...', 'id': 'description-create-subject'}))

    class Meta:
        model = models.Subject
        fields = (
            'name',
            'level',
            'grade',
            'description',
        )
        widgets = {
            'level': forms.Select(choices=CHOICES_LEVEL),
            'grade': forms.Select(choices=CHOICES_GRADE)
        }

    def clean_level(self):
        level = self.cleaned_data.get('level')
        if len(level) > 50:
            services.FormService().raise_error(MESSAGE_LEVEL_EN, MESSAGE_LEVEL)
        return level

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 100:
            services.FormService().raise_error(MESSAGE_DESCRIPTION_EN, MESSAGE_DESCRIPTION)
        return description

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            services.FormService().raise_error(MESSAGE_NAME_EN, MESSAGE_NAME)
        return name

# Users 
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

class UserCreateForm(UserCreationForm):
    
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Alberto', 'id': 'first_name-create-teacher'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Cordón', 'id': 'last_name-create-teacher'}))
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'alberto26', 'id': 'username-create-teacher'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'alberto@gmail.com', 'id': 'email-create-teacher'}))
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    initials = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'ACA', 'id': 'initials-create-teacher'}))
    password1 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': '*************', 'id': 'password1-create-teacher'}))
    password2 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': '*************', 'id': 'password2-create-teacher'}))

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = DATE_PLACEHOLDER_EN
            self.fields['birthdate'].widget.format = settings.DATE_INPUT_FORMATS[0]

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

class UserForm(UserChangeForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Alberto', 'id': 'first_name-update-profile'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'placeholder': 'Cordón', 'id': 'last_name-update-profile'}))
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'alberto26', 'id': 'username-update-profile'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'alberto@gmail.com', 'id': 'email-update-profile'}))
    

    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name',
            'username', 
            'email', 
            
        )

class UserProfileForm(UserChangeForm):
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    initials = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = DATE_PLACEHOLDER_EN
            self.fields['birthdate'].widget.format = settings.DATE_INPUT_FORMATS[0]
    
    class Meta:
        model = models.Profile
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
        
# Teachers
class TeacherUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': DATE_PLACEHOLDER}
        )
    )
    initials = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(TeacherUpdateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = DATE_PLACEHOLDER_EN
            self.fields['birthdate'].widget.format = settings.DATE_INPUT_FORMATS[0]

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