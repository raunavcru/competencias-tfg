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

    role = models.CharField(("role"), max_length=50)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username + ' profile'

class Competence(Common):
    code = models.CharField(("code"), max_length=50)

    name = models.CharField(("name"), max_length=300)

    description = models.CharField(("description"), max_length=300)

    weight = models.DecimalField('weight', max_digits=3, decimal_places=2, blank=True, null=True)

    subject_weight = models.DecimalField('subject_weight', max_digits=3, decimal_places=2, blank=True, null=True)

    level = models.PositiveIntegerField('level')

    parent = models.ManyToManyField('self', "competence_parent", symmetrical=False, verbose_name=("competences_parent"), blank=True)

    class Meta:
        verbose_name = 'Competence'
        verbose_name_plural = 'Competences'
    
    def __str__(self):
        return self.name

class Subject(Common):
    name = models.CharField(("name"), max_length=100)

    level = models.CharField(("level"), max_length=50)

    grade = models.CharField(("grade"), max_length=50)

    description = models.CharField(("description"), max_length=100)

    competences = models.ManyToManyField(Competence, "competences", verbose_name=("competences_subject"))

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name + ' ' + self.level + ' ' + self.grade

class Teacher(Profile):
    subjects = models.ManyToManyField(Subject, "subjects", verbose_name=("subjects_teacher"))

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return self.user.last_name + ', ' + self.user.first_name

class Administrator(Profile):

    class Meta:
        verbose_name = 'Admistrator'
        verbose_name_plural = 'Admistrators'

    def __str__(self):
        return self.user.username + ' admin profile'

class Evaluation(Common):
    name = models.CharField(("name"), max_length=50)

    start_date = models.DateField('start_date')

    end_date = models.DateField('end_date')

    is_final = models.BooleanField(("is_final"))

    period = models.CharField(("period"), max_length=50)

    weight = models.DecimalField('weight', max_digits=3, decimal_places=2)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='evaluation_parent', blank=True, null=True)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_evaluation')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_evaluation', blank=True, null=True)

    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'
    
    def __str__(self):
        return self.name

class Student(Common):
    name = models.CharField(("name"), max_length=100)

    surname = models.CharField(("surname"), max_length=100)

    birthdate = models.DateField('birthdate')

    initials = models.CharField(("initials"), max_length=10)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return self.surname + ' ' + self.name

class Set(Common):
    name = models.CharField(("name"), max_length=50)

    level = models.CharField(("level"), max_length=50)

    grade = models.CharField(("grade"), max_length=50)

    line = models.CharField(("line"), max_length=50)

    evaluation_type_final = models.CharField(("evaluation_type_final"), max_length=100, blank=True, null=True)

    evaluation_type_partial = models.CharField(("evaluation_type_partial"), max_length=100, blank=True, null=True)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_set')

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_set')

    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='evaluation_set')

    students = models.ManyToManyField(Student, "student", verbose_name=("students_set"), blank=True)

    class Meta:
        verbose_name = 'Set'
        verbose_name_plural = 'Sets'
    
    def __str__(self):
        return self.name + ' ' + self.level + ' ' + self.grade + ' ' + self.line

class Activity(Common):
    title = models.CharField(("title"), max_length=50)

    date = models.DateField('date')

    weight = models.DecimalField('weight', max_digits=3, decimal_places=2)

    is_recovery = models.BooleanField(("is_recovery"))

    set_activity = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='set_activity')

    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='evaluation_activity')

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_activity')

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        if self.is_recovery:
            return self.date + ' recovery activity'
        else:
            return self.date + ' activity'

class Evaluation_mark(Common):
    mark = models.DecimalField('mark', max_digits=4, decimal_places=2, blank=True, null=True)

    manual_mark = models.DecimalField('manual_mark', max_digits=4, decimal_places=2, blank=True, null=True)

    evaluation_type = models.CharField(("evaluation_type"), max_length=50)

    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='evaluation_evaluation_mark')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_evaluation_mark')

    class Meta:
        verbose_name = 'Evaluation_mark'
        verbose_name_plural = 'Evaluation_marks'
    
    def __str__(self):
        return self.mark


class Activity_mark(Common):
    mark = models.DecimalField('mark', max_digits=4, decimal_places=2, blank=True, null=True)

    manual_mark = models.DecimalField('manual_mark', max_digits=4, decimal_places=2, blank=True, null=True)

    evaluation_type = models.CharField(("evaluation_type"), max_length=50)

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activity_activity_mark')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_activity_mark')

    class Meta:
        verbose_name = 'Activity_mark'
        verbose_name_plural = 'Activity_marks'
    
    def __str__(self):
        return self.mark

class Exercise(Common):
    weight = models.DecimalField('weight', max_digits=3, decimal_places=2)

    statement = models.CharField(("statement"), max_length=50)

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activity_exercise')

    class Meta:
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'
    
    def __str__(self):
        return self.statement

class Exercise_mark(Common):
    mark = models.DecimalField('mark', max_digits=4, decimal_places=2, blank=True, null=True)

    manual_mark = models.DecimalField('manual_mark', max_digits=4, decimal_places=2, blank=True, null=True)

    evaluation_type = models.CharField(("evaluation_type"), max_length=50)

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_exercise_mark')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_exercise_mark')

    class Meta:
        verbose_name = 'Exercise_mark'
        verbose_name_plural = 'Exercise_marks'
    
    def __str__(self):
        return self.mark

class Exercise_competence(Common):
    intensity = models.DecimalField('intensity', max_digits=3, decimal_places=2)

    weight = models.DecimalField('weight', max_digits=3, decimal_places=2)

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_exercise_competence')

    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, related_name='competence_exercise_competence')

    class Meta:
        verbose_name = 'Exercise_competence'
        verbose_name_plural = 'Exercise_competences'
    
    def __str__(self):
        return self.intensity + ' ' + self.weight


class Competence_mark(Common):
    mark = models.DecimalField('mark', max_digits=4, decimal_places=2, blank=True, null=True)

    evaluation_type = models.CharField(("evaluation_type"), max_length=50)

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_competence_mark')

    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, related_name='competence_competence_mark')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_competence_mark')

    class Meta:
        verbose_name = 'Competence_mark'
        verbose_name_plural = 'Competence_marks'
    
    def __str__(self):
        return self.mark

class Competence_evaluation(Common):
    mark = models.DecimalField('mark', max_digits=4, decimal_places=2, blank=True, null=True)

    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, related_name='competence_competence_evaluation')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_competence_evaluation')

    class Meta:
        verbose_name = 'Competence_evaluation'
        verbose_name_plural = 'Competence_evaluations'
    
    def __str__(self):
        return self.competence.code + ' ' +  self.student.name + ' ' + self.student.surname