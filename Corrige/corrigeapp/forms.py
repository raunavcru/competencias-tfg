from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm

User = get_user_model()

class TeacherCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
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
    