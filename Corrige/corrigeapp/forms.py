from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from . import models
from django.utils.timezone import now

User = get_user_model()

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