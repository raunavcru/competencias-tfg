from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import password_validators_help_texts
from django.utils.timezone import now
from django.utils.translation import get_language, activate

from . import models
from . import services

User = get_user_model()

teachers = models.Teacher.objects.all()
subjects = models.Subject.objects.all()
evaluations_final = models.Evaluation.objects.filter(is_final=True)

# Choices
CHOICES_YES_NO = ((False, "No"), (True, "Sí"))
CHOICES_YES_NO_EN = ((False, "No"), (True, "Yes"))
CHOICES_LEVEL = (("1º","1º"),("2º","2º"),("3º","3º"),("4º","4º"),("5º","5º"),("6º","6º"))
CHOICES_GRADE = (
    ("PrimarySchool","Educación Primaria"),
    ("SecondaryEducation","Educación Secundaria"),
    ("SixthForm","Bachillerato"),
    ("FurtherEducation","Grado Medio o Superior"),
    ("University","Grado Universitario"))
CHOICES_GRADE_EN = (
    ("PrimarySchool","Primary School"),
    ("SecondaryEducation","Secondary Education"),
    ("SixthForm","Sixth Form"),
    ("FurtherEducation","Further Education"),
    ("University","University"))
CHOICES_EVALUATION_TYPE_FINAL_EN =(
    ("BY_COMPETENCES", "By Competences"), 
    ("BY_EVALUATION_NO_RECOVERY", "By Evaluations (No recovery)"), 
    ("BY_EVALUATION_RECOVERY", "By Evaluations (Recovery)"))
CHOICES_EVALUATION_TYPE_FINAL =(
    ("BY_COMPETENCES", "Por Competencias"), 
    ("BY_EVALUATION_NO_RECOVERY", "Por evaluaciones (Sin recuperación)"), 
    ("BY_EVALUATION_RECOVERY", "Por evaluaciones (Con recuperación)"))
CHOICES_EVALUATION_TYPE_PARTIAL_EN =(("BY_ALL_ACTIVITIES", "By all Activities"), ("BY_RECOVERY_ACTIVITIES", "By Recovery Activities"))
CHOICES_EVALUATION_TYPE_PARTIAL =(("BY_ALL_ACTIVITIES", "Por todas las Actividades"), ("BY_RECOVERY_ACTIVITIES", "Por Recuperaciones"))

# Messages: Length
MESSAGE_CODE = 'El tamaño del código no puede ser mayor que 50.'
MESSAGE_CODE_EN = 'Code can not be longer of 50 characters.'
MESSAGE_DESCRIPTION_100 = 'El tamaño de la descripción no puede ser mayor que 100.'
MESSAGE_DESCRIPTION_100_EN = 'Description can not be longer of 100 characters.'
MESSAGE_DESCRIPTION_300 = 'El tamaño de la descripción no puede ser mayor que 300.'
MESSAGE_DESCRIPTION_300_EN = 'Description can not be longer of 300 characters.'
MESSAGE_EMAIL_50 = 'El tamaño del nombre de usuario no puede ser mayor que 50.'
MESSAGE_EMAIL_50_EN = 'Username can not be longer of 50 characters.'
MESSAGE_FIRST_NAME = 'El tamaño del nombre no puede ser mayor que 100.'
MESSAGE_FIRST_NAME_EN = 'First name can not be longer of 100 characters.'
MESSAGE_INITIALS = 'El tamaño de las iniciales no puede ser mayor que 9.'
MESSAGE_INITIALS_EN = 'Initials can not be longer of 9 characters.'
MESSAGE_LAST_NAME = 'El tamaño del apellido no puede ser mayor que 100.'
MESSAGE_LAST_NAME_EN = 'Last name can not be longer of 100 characters.'
MESSAGE_NAME_50 = 'El tamaño del nombre no puede ser mayor que 50.'
MESSAGE_NAME_50_EN = 'Name can not be longer of 50 characters.'
MESSAGE_NAME_100 = 'El tamaño del nombre no puede ser mayor que 100.'
MESSAGE_NAME_100_EN = 'Name can not be longer of 100 characters.'
MESSAGE_NAME_300 = 'El tamaño del nombre no puede ser mayor que 300.'
MESSAGE_NAME_300_EN = 'Name can not be longer of 300 characters.'
MESSAGE_PERIOD = 'El tamaño del período no puede ser mayor que 50.'
MESSAGE_PERIOD_EN = 'Period can not be longer of 50 characters.'
MESSAGE_STATEMENT = 'El tamaño del enunciado no puede ser mayor que 300.'
MESSAGE_STATEMENT_EN = 'Statement can not be longer of 300 characters.'
MESSAGE_SURNAME = 'El tamaño del apellido no puede ser mayor que 100.'
MESSAGE_SURNAME_EN = 'Surname can not be longer of 100 characters.'
MESSAGE_TITLE = 'El tamaño del título no puede ser mayor que 50.'
MESSAGE_TITLE_EN = 'Title can not be longer of 50 characters.'
MESSAGE_USERNAME_50 = 'El tamaño del nombre de usuario no puede ser mayor que 50.'
MESSAGE_USERNAME_50_EN = 'Username can not be longer of 50 characters.'

# Messages: Range
MESSAGE_INTENSITY = 'Intensidad debe estar por encima de 0.00.'
MESSAGE_INTENSITY_EN = 'Intensity must be above 0.00.'
MESSAGE_MARK = 'Nota debe estar entre 0.00 y 10.00.'
MESSAGE_MARK_EN = 'Mark must be between 0.00 and 10.00.'
MESSAGE_SUBJETC_WEIGHT = 'Peso debe estar por encima de 0.00.'
MESSAGE_SUBJETC_WEIGHT_EN = 'Subject weight must be above 0.00.'
MESSAGE_WEIGHT = 'Peso debe estar por encima de 0.00.'
MESSAGE_WEIGHT_EN = 'Weight must be above 0.00.'

# Messages: Unique
MESSAGE_EMAIL = 'Email ya ha sido registrado.'
MESSAGE_EMAIL_EN = 'Email has already been registered.'
MESSAGE_USERNAME = 'Nombre de usuario ya ha sido registrado.'
MESSAGE_USERNAME_EN = 'Username has already been registered.'

# Messages: Other
MESSAGE_BIRTHDATE = 'La fecha de cumpleaños debe ser en el pasado.'
MESSAGE_BIRTHDATE_EN = 'Birthdate can not be past.'
MESSAGE_LINE = 'Línea solo pueden ser un letra.'
MESSAGE_LINE_EN = 'Line must be a letter.'

# Placeholder
PLACEHOLDER_DATE = 'dd/mm/aaaa'
PLACEHOLDER_DATE_EN = 'mm/dd/yyyy'
PLACEHOLDER_NAME_EVALUATION = 'Matemáticas 5º Primaria'
PLACEHOLDER_PERIOD_EVALUATION = '1er Trimestre'

# Activity
class ActivityUpdateForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Ex 1', 'id': 'title-create-activity'}))
    date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    weight = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight-create-activity'}))
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
            self.fields['date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['is_recovery'].choices = CHOICES_YES_NO_EN
    
    class Meta:
        model = models.Activity
        fields = (
            'title',
            'date',
            'weight',
            'evaluation',
            'is_recovery',
        )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 50:
            services.FormService().raise_error(MESSAGE_TITLE_EN, MESSAGE_TITLE)
        return title 

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if float(weight) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight   

# Administrator
class AdministratorUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    initials = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AdministratorUpdateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
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
            services.FormService().raise_error(MESSAGE_BIRTHDATE_EN, MESSAGE_BIRTHDATE)
        return birthdate

    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        if len(initials) > 9:
            services.FormService().raise_error(MESSAGE_INITIALS_EN, MESSAGE_INITIALS)
        return initials

# Block
class BlockCreateChildForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-block'}))
    period = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    weight = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required': True, 'placeholder': '1.0', 'id': 'weight-create-block'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )

    def __init__(self, *args, **kwargs):
        super(BlockCreateChildForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['start_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date'].widget.format = settings.DATE_INPUT_FORMATS[0]

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'period',
            'weight',
            'start_date',
            'end_date',
        )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            services.FormService().raise_error(MESSAGE_NAME_50_EN, MESSAGE_NAME_50)
        return name 
    
    def clean_period(self):
        period = self.cleaned_data.get('period')
        if len(period) > 50:
            services.FormService().raise_error(MESSAGE_PERIOD_EN, MESSAGE_PERIOD)
        return period 

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if float(weight) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight  

# Competences
class CompetenceLevel1CreateForm(forms.ModelForm):

    code = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'CC1', 'id': 'code-create-competence'}))
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Comunicación lingüística', 'id': 'name-create-competence'}))
    description = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Comunicación lingüística', 'id': 'description-create-competence'}))
    weight = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight-create-competence'}))

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
            services.FormService().raise_error(MESSAGE_CODE_EN, MESSAGE_CODE)
        return code

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 300:
            services.FormService().raise_error(MESSAGE_NAME_300_EN, MESSAGE_NAME_300)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 300:
            services.FormService().raise_error(MESSAGE_DESCRIPTION_300_EN, MESSAGE_DESCRIPTION_300)
        return description
    
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if float(weight) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight 

class CompetenceLevel2CreateForm(forms.ModelForm):

    code = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'CC1', 'id': 'code-create-competence'}))
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Comunicación lingüística', 'id': 'name-create-competence'}))
    description = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Comunicación lingüística.', 'id': 'description-create-competence'}))
    weight = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight-create-competence'}))
    subject_weight = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'subject_weight-create-competence'}))

    class Meta:
        model = models.Competence
        fields = (
            'code',
            'name',
            'description',
            'weight',
            'subject_weight',
        )
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if len(code) > 50:
            services.FormService().raise_error(MESSAGE_CODE_EN, MESSAGE_CODE)
        return code
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 300:
            services.FormService().raise_error(MESSAGE_NAME_300_EN, MESSAGE_NAME_300)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 300:
            services.FormService().raise_error(MESSAGE_DESCRIPTION_300_EN, MESSAGE_DESCRIPTION_300)
        return description

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if float(weight) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight

    def clean_subject_weight(self):
        subject_weight = self.cleaned_data.get('subject_weight')
        if float(subject_weight) < 0.00:
            services.FormService().raise_error(MESSAGE_SUBJETC_WEIGHT_EN, MESSAGE_SUBJETC_WEIGHT)
        return subject_weight 

class CompetenceLevel3CreateForm(forms.ModelForm):

    code = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'CC1', 'id': 'code-create-competence'}))
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Comunicación lingüística', 'id': 'name-create-competence'}))
    description = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Comunicación lingüística.', 'id': 'description-create-competence'}))

    class Meta:
        model = models.Competence
        fields = (
            'code',
            'name',
            'description',
        )
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if len(code) > 50:
            services.FormService().raise_error(MESSAGE_CODE_EN, MESSAGE_CODE)
        return code

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 300:
            services.FormService().raise_error(MESSAGE_NAME_300_EN, MESSAGE_NAME_300)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 300:
            services.FormService().raise_error(MESSAGE_DESCRIPTION_300_EN, MESSAGE_DESCRIPTION_300)
        return description

# Exercices
class ExerciseUpdateForm(forms.ModelForm):
    weight = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight-create-exercise'}))
    statement = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'id': 'statement-create-exercice'}))

    class Meta:
        model = models.Exercise
        fields = (
            'weight',
            'statement',
        )

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if float(weight) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight    
        
    def clean_statement(self):
        statement = self.cleaned_data.get('statement')
        if len(statement) > 300:
            services.FormService().raise_error(MESSAGE_STATEMENT_EN, MESSAGE_STATEMENT)
        return statement

# Exercices_competence
class ExerciseCompetenceUpdateForm(forms.ModelForm):

    intensity = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'intensity-create-exercise-competence'}))
    weight = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight-create-exercise-competence'}))

    class Meta:
        model = models.Exercise_competence
        fields = (
            'intensity',
            'weight',
        )

    def clean_intensity(self):
        intensity = self.cleaned_data.get('intensity')
        if float(intensity) < 0.00:
            services.FormService().raise_error(MESSAGE_INTENSITY_EN, MESSAGE_INTENSITY)
        return intensity   

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if float(weight) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight

# Evaluations
class EvaluationCreateForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    subject = forms.ModelChoiceField(subjects, empty_label=None)

    def __init__(self, *args, **kwargs):
        super(EvaluationCreateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['start_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date'].widget.format = settings.DATE_INPUT_FORMATS[0]

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'start_date',
            'end_date',
            'subject',
        )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            services.FormService().raise_error(MESSAGE_NAME_50_EN, MESSAGE_NAME_50)
        return name

class EvaluationCreateAllForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )

    def __init__(self, *args, **kwargs):
        super(EvaluationCreateAllForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['start_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date'].widget.format = settings.DATE_INPUT_FORMATS[0]

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'start_date',
            'end_date',
        )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            services.FormService().raise_error(MESSAGE_NAME_50_EN, MESSAGE_NAME_50)
        return name

class EvaluationCreateChildForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    period = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )

    def __init__(self, *args, **kwargs):
        super(EvaluationCreateChildForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['start_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date'].widget.format = settings.DATE_INPUT_FORMATS[0]

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'weight',
            'period',
            'start_date',
            'end_date',
        )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            services.FormService().raise_error(MESSAGE_NAME_50_EN, MESSAGE_NAME_50)
        return name 
    
    def clean_period(self):
        period = self.cleaned_data.get('period')
        if len(period) > 50:
            services.FormService().raise_error(MESSAGE_PERIOD_EN, MESSAGE_PERIOD)
        return period 

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if float(weight) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight

class EvaluationCreateOneFinalThreePartialForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    period_1 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    weight_1 = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight_1'}))
    start_date_1 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date_1 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    period_2 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    weight_2 = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight_2'}))
    start_date_2 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date_2 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    period_3 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    weight_3 = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight_3'}))
    start_date_3 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date_3 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    
    def __init__(self, *args, **kwargs):
        super(EvaluationCreateOneFinalThreePartialForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['start_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['start_date_1'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date_1'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date_1'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date_1'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['start_date_2'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date_2'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date_2'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date_2'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['start_date_3'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date_3'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date_3'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date_3'].widget.format = settings.DATE_INPUT_FORMATS[0]

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'start_date',
            'end_date',
            'period_1',
            'weight_1',
            'start_date_1',
            'end_date_1',
            'period_2',
            'weight_2',
            'start_date_2',
            'end_date_2',
            'period_3',
            'weight_3',
            'start_date_3',
            'end_date_3',
        )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            services.FormService().raise_error(MESSAGE_NAME_50_EN, MESSAGE_NAME_50)
        return name 
    
    def clean_period_1(self):
        period_1 = self.cleaned_data.get('period_1')
        if len(period_1) > 50:
            services.FormService().raise_error(MESSAGE_PERIOD_EN, MESSAGE_PERIOD)
        return period_1
    
    def clean_period_2(self):
        period_2 = self.cleaned_data.get('period_2')
        if len(period_2) > 50:
            services.FormService().raise_error(MESSAGE_PERIOD_EN, MESSAGE_PERIOD)
        return period_2 
    
    def clean_period_3(self):
        period_3 = self.cleaned_data.get('period_3')
        if len(period_3) > 50:
            services.FormService().raise_error(MESSAGE_PERIOD_EN, MESSAGE_PERIOD)
        return period_3 

    def clean_weight_1(self):
        weight_1 = self.cleaned_data.get('weight_1')
        if float(weight_1) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight_1

    def clean_weight_2(self):
        weight_2 = self.cleaned_data.get('weight_2')
        if float(weight_2) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight_2

    def clean_weight_3(self):
        weight_3 = self.cleaned_data.get('weight_3')
        if float(weight_3) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight_3

class EvaluationCreateOneFinalTwoPartialForm(forms.ModelForm):
    
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_NAME_EVALUATION, 'id': 'name-create-evaluation'}))
    start_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    period_1 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    weight_1 = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight_1'}))
    start_date_1 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date_1 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    period_2 = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': PLACEHOLDER_PERIOD_EVALUATION}))
    weight_2 = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '1.0', 'id': 'weight_2'}))
    start_date_2 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    end_date_2 = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    
    def __init__(self, *args, **kwargs):
        super(EvaluationCreateOneFinalTwoPartialForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['start_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['start_date_1'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date_1'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date_1'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date_1'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['start_date_2'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['start_date_2'].widget.format = settings.DATE_INPUT_FORMATS[0]
            self.fields['end_date_2'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['end_date_2'].widget.format = settings.DATE_INPUT_FORMATS[0]

    class Meta:
        model = models.Evaluation
        fields = (
            'name',
            'start_date',
            'end_date',
            'period_1',
            'weight_1',
            'start_date_1',
            'end_date_1',
            'period_2',
            'weight_2',
            'start_date_2',
            'end_date_2',
        )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            services.FormService().raise_error(MESSAGE_NAME_50_EN, MESSAGE_NAME_50)
        return name 
    
    def clean_period_1(self):
        period_1 = self.cleaned_data.get('period_1')
        if len(period_1) > 50:
            services.FormService().raise_error(MESSAGE_PERIOD_EN, MESSAGE_PERIOD)
        return period_1
    
    def clean_period_2(self):
        period_2 = self.cleaned_data.get('period_2')
        if len(period_2) > 50:
            services.FormService().raise_error(MESSAGE_PERIOD_EN, MESSAGE_PERIOD)
        return period_2 
    
    def clean_weight_1(self):
        weight_1 = self.cleaned_data.get('weight_1')
        if float(weight_1) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight_1

    def clean_weight_2(self):
        weight_2 = self.cleaned_data.get('weight_2')
        if float(weight_2) < 0.00:
            services.FormService().raise_error(MESSAGE_WEIGHT_EN, MESSAGE_WEIGHT)
        return weight_2


# Marks
class ActivityMarkCreateForm(forms.ModelForm):
    manual_mark = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '7.0', 'id': 'mark-create-input'}))

    class Meta:
        model = models.Activity_mark
        fields = (
            'manual_mark',
        )
    
    def clean_manual_mark(self):
        manual_mark = self.cleaned_data.get('manual_mark')
        if float(manual_mark) < 0.00 or float(manual_mark) > 10.00:
            services.FormService().raise_error(MESSAGE_MARK_EN, MESSAGE_MARK)
        return manual_mark  

class CompetenceMarkCreateForm(forms.ModelForm):
    mark = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '7.0', 'id': 'mark-create-input'}))

    class Meta:
        model = models.Competence_mark
        fields = (
            'mark',
        )
    
    def clean_mark(self):
        mark = self.cleaned_data.get('mark')
        if float(mark) < 0.00 or float(mark) > 10.00:
            services.FormService().raise_error(MESSAGE_MARK_EN, MESSAGE_MARK)
        return mark  

class EvaluationMarkCreateForm(forms.ModelForm):
    manual_mark = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '7.0', 'id': 'mark-create-input'}))

    class Meta:
        model = models.Evaluation_mark
        fields = (
            'manual_mark',
        )
    
    def clean_manual_mark(self):
        manual_mark = self.cleaned_data.get('manual_mark')
        if float(manual_mark) < 0.00 or float(manual_mark) > 10.00:
            services.FormService().raise_error(MESSAGE_MARK_EN, MESSAGE_MARK)
        return manual_mark  
        
class ExerciseMarkCreateForm(forms.ModelForm):
    manual_mark = forms.DecimalField(
        widget=forms.NumberInput(attrs={'required':True, 'placeholder': '7.0', 'id': 'mark-create-input'}))

    class Meta:
        model = models.Exercise_mark
        fields = (
            'manual_mark',
        )
    
    def clean_manual_mark(self):
        manual_mark = self.cleaned_data.get('manual_mark')
        if float(manual_mark) < 0.00 or float(manual_mark) > 10.00:
            services.FormService().raise_error(MESSAGE_MARK_EN, MESSAGE_MARK)
        return manual_mark  

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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            services.FormService().raise_error(MESSAGE_NAME_50_EN, MESSAGE_NAME_50)
        return name

    def clean_line(self):
        line = self.cleaned_data.get('line')
        if not line.isalpha() or len(line) > 1:
            services.FormService().raise_error(MESSAGE_LINE_EN, MESSAGE_LINE)
        return line

class SetUpdateEvaluationTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SetUpdateEvaluationTypeForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['evaluation_type_final'].choices = CHOICES_EVALUATION_TYPE_FINAL_EN
            self.fields['evaluation_type_partial'].choices = CHOICES_EVALUATION_TYPE_PARTIAL_EN

    class Meta:
        model = models.Set
        fields = (
            'evaluation_type_final',
            'evaluation_type_partial',
        )
        widgets = {
            'evaluation_type_final': forms.Select(choices=CHOICES_EVALUATION_TYPE_FINAL),
            'evaluation_type_partial': forms.Select(choices=CHOICES_EVALUATION_TYPE_PARTIAL),
        }

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
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    initials = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'placeholder': 'RNC', 'id': 'initials-create-student'}))

    def __init__(self, *args, **kwargs):
        super(StudentCreateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['birthdate'].widget.format = settings.DATE_INPUT_FORMATS[0]


    class Meta:
        model = models.Student
        fields = (
            'name',
            'surname',
            'birthdate',
            'initials',
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            services.FormService().raise_error(MESSAGE_NAME_100_EN, MESSAGE_NAME_100)
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if len(surname) > 100:
            services.FormService().raise_error(MESSAGE_SURNAME_EN, MESSAGE_SURNAME)
        return surname
    
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate >= now().date():
            services.FormService().raise_error(MESSAGE_BIRTHDATE_EN, MESSAGE_BIRTHDATE)
        return birthdate

    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        if len(initials) > 9:
            services.FormService().raise_error(MESSAGE_INITIALS_EN, MESSAGE_INITIALS)
        return initials

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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            services.FormService().raise_error(MESSAGE_NAME_100, MESSAGE_NAME_100)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 100:
            services.FormService().raise_error(MESSAGE_DESCRIPTION_100_EN, MESSAGE_DESCRIPTION_100)
        return description

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
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    initials = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'ACA', 'id': 'initials-create-teacher'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': '*************', 'id': 'password1-create-teacher'}), help_text=password_validators_help_texts())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': '*************', 'id': 'password2-create-teacher'}))

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
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

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 100:
            services.FormService().raise_error(MESSAGE_FIRST_NAME_EN, MESSAGE_FIRST_NAME)
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 100:
            services.FormService().raise_error(MESSAGE_LAST_NAME_EN, MESSAGE_LAST_NAME)
        return last_name
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            services.FormService().raise_error(MESSAGE_USERNAME_EN, MESSAGE_USERNAME)
        elif len(username) > 50:
            services.FormService().raise_error(MESSAGE_USERNAME_50_EN, MESSAGE_USERNAME_50)
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            services.FormService().raise_error(MESSAGE_EMAIL_EN, MESSAGE_EMAIL)
        elif len(email) > 50:
            services.FormService().raise_error(MESSAGE_EMAIL_50_EN, MESSAGE_EMAIL_50)
        return email

    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        if len(initials) > 9:
            services.FormService().raise_error(MESSAGE_INITIALS_EN, MESSAGE_INITIALS)
        return initials

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate >= now().date():
            services.FormService().raise_error(MESSAGE_BIRTHDATE_EN, MESSAGE_BIRTHDATE)
        return birthdate

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
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 100:
            services.FormService().raise_error(MESSAGE_FIRST_NAME_EN, MESSAGE_FIRST_NAME)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 100:
            services.FormService().raise_error(MESSAGE_LAST_NAME_EN, MESSAGE_LAST_NAME)
        return last_name
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() and username != self.initial.get('username'):
            services.FormService().raise_error(MESSAGE_USERNAME_EN, MESSAGE_USERNAME)
        elif len(username) > 50:
            services.FormService().raise_error(MESSAGE_USERNAME_50_EN, MESSAGE_USERNAME_50)
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and email != self.initial.get('email'):
            services.FormService().raise_error(MESSAGE_EMAIL_EN, MESSAGE_EMAIL)
        elif len(email) > 50:
            services.FormService().raise_error(MESSAGE_EMAIL_50_EN, MESSAGE_EMAIL_50)
        return email

class UserPasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': '*************', 'id': 'old_password'}))
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': '*************', 'id': 'new_password1'}), help_text=password_validators_help_texts())
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': '*************', 'id': 'new_password2'}))

    class Meta:
        model = User
        fields = (
            'old_password', 
            'new_password1',
            'new_password2',
        )

class UserProfileForm(UserChangeForm):
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    initials = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
            self.fields['birthdate'].widget.format = settings.DATE_INPUT_FORMATS[0]
    
    class Meta:
        model = models.Profile
        fields = (
            'birthdate', 
            'initials',
        )
    
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate >= now().date():
            services.FormService().raise_error(MESSAGE_BIRTHDATE_EN, MESSAGE_BIRTHDATE)
        return birthdate

    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        if len(initials) > 9:
            services.FormService().raise_error(MESSAGE_INITIALS_EN, MESSAGE_INITIALS)
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
            services.FormService().raise_error(MESSAGE_FIRST_NAME_EN, MESSAGE_FIRST_NAME)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 100:
            services.FormService().raise_error(MESSAGE_LAST_NAME_EN, MESSAGE_LAST_NAME)
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and email != self.initial.get('email'):
            services.FormService().raise_error(MESSAGE_EMAIL_EN, MESSAGE_EMAIL)
        elif len(email) > 50:
            services.FormService().raise_error(MESSAGE_EMAIL_50_EN, MESSAGE_EMAIL_50)
        return email
        
# Teachers
class TeacherUpdateForm(forms.ModelForm):
    birthdate = forms.DateField(required=True, 
        input_formats=settings.DATE_INPUT_FORMATS, 
        widget=forms.DateInput(
            format=settings.DATE_INPUT_FORMATS[0],
            attrs={'placeholder': PLACEHOLDER_DATE}
        )
    )
    initials = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(TeacherUpdateForm, self).__init__(*args, **kwargs)
        if get_language() == 'en':
            self.fields['birthdate'].widget.attrs['placeholder'] = PLACEHOLDER_DATE_EN
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
            services.FormService().raise_error(MESSAGE_BIRTHDATE_EN, MESSAGE_BIRTHDATE)
        return birthdate

    def clean_initials(self):
        initials = self.cleaned_data.get('initials')
        if len(initials) > 9:
            services.FormService().raise_error(MESSAGE_INITIALS_EN, MESSAGE_INITIALS)
        return initials