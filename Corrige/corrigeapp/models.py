from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

User = get_user_model()

# Common class.
class Common(models.Model):
    created_at = models.DateTimeField(
        'Created at', default=now, blank=True, editable=False)
    updated_at = models.DateTimeField(
        'Updated at', default=now, blank=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_created',  blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_updated', blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now()
        self.updated_at = now()

        super(Common, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)

    birthdate = models.DateField('birthdate')

    initials = models.CharField(("initials"), max_length=9)

    role = models.CharField(("role"))

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username + ' profile'

class Teacher(Profile):

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return self.user.username + ' teacher profile'

class Administrator(Profile):

    class Meta:
        verbose_name = 'Admistrator'
        verbose_name_plural = 'Admistrators'

    def __str__(self):
        return self.user.username + ' admin profile'

class Subject(Common):
    name = models.CharField(("name"), max_length=100)

    level = models.CharField(("level"), max_length=50)

    grade = models.CharField(("grade"), max_length=50)

    description = models.CharField(("description"), max_length=100)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name + ' ' + self.level + ' ' + self.grade

class Evaluation(Common):
    name = models.CharField(("name"), max_length=50)

    start_date = models.DateField('start_date')

    end_date = models.DateField('end_date')

    is_final = models.BooleanField(("is_final"))

    period = models.CharField(("period"), max_length=50)

    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'
    
    def __str__(self):
        return self.name + ' ' + self.period

class Set(Common):
    name = models.CharField(("name"), max_length=50)

    level = models.CharField(("level"), max_length=50)

    grade = models.CharField(("grade"), max_length=50)

    line = models.CharField(("line"), max_length=50)

    class Meta:
        verbose_name = 'Set'
        verbose_name_plural = 'Sets'
    
    def __str__(self):
        return self.name + ' ' + self.level + ' ' + self.grade + ' ' + self.line

class Activity(Common):
    date = models.DateField('date')

    weight = models.DecimalField('weight', max_digits=1, decimal_places=2)

    is_recovery = models.BooleanField(("is_recovery"))

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        if self.is_recovery:
            return self.date + ' recovery activity'
        else:
            return self.date + ' activity'

class Evaluation_mark(Common):
    mark = models.DecimalField('mark', max_digits=2, decimal_places=2)

    manual_mark = models.DecimalField('manual_mark', max_digits=2, decimal_places=2)

    evaluation_type = models.CharField(("evaluation_type"), max_length=50)

    class Meta:
        verbose_name = 'Evaluation_mark'
        verbose_name_plural = 'Evaluation_marks'
    
    def __str__(self):
        return self.mark
