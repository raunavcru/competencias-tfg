from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import get_language

from . import models

User = get_user_model()

class UserService():

    def is_admin(self, user: User) -> bool:
        res = False

        if user.profile.role == 'ADMINISTRATOR':
            res = True

        return res
    
    def is_teacher(self, user: User) -> bool:
        res = False

        if user.profile.role == 'TEACHER':
            res = True

        return res

class FormService():

    def raise_error(self, en_message: str, es_message: str):
        
        if get_language() == 'en':
            raise ValidationError(
                en_message)
        else:
            raise ValidationError(
                es_message)
