from django.contrib.auth import get_user_model

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
