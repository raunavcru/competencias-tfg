from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import get_language

from . import models

User = get_user_model()

class ActivityService():

    def is_owner(self, user: User, activity_object: models.Activity) -> bool:
        res = False

        if activity_object.created_by == user:
            res = True
        
        return res

class BlockService():

    def is_owner(self, user: User, block: models.Evaluation) -> bool:
        res = False

        if block.teacher.user == user:
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

class MarkService():

    def calculate_activity_mark(self, activity: models.Activity, student: models.Student) -> None:
        if not models.Activity_mark.objects.filter(activity = activity, student = student).exists():
            a_m = models.Exercise_mark.objects.create(activity = activity, student = student)
            a_m.save()
        
        activity_mark = models.Activity_mark.objects.get(activity = activity, student = student)
        exercise_mark_ls = models.Exercise_mark.objects.filter(exercise__activity=activity).order_by('exercise')

        weight_total = 0.0
        mark_total = 0.0
        if exercise_mark_ls:
            for exercise_mark in exercise_mark_ls:
                weight_total = weight_total + float(exercise_mark.exercise.weight)

                if exercise_mark.evaluation_type == "AUTOMATIC" and exercise_mark.mark:
                    mark_total = mark_total + float(exercise_mark.mark * exercise_mark.exercise.weight)
                elif exercise_mark.manual_mark:
                    mark_total = mark_total + float(exercise_mark.manual_mark * exercise_mark.exercise.weight)
            
            mark = mark_total/weight_total

            activity_mark.mark = mark
            activity_mark.save()

    def calculate_competence_evaluation(self, exercise_object: models.Exercise, student_object: models.Student) -> None:

        competence_mark_distinct_list = models.Competence_mark.objects.filter(competence__competence_exercise_competence__exercise = exercise_object, student=student_object).distinct('competence')

        for c_m in competence_mark_distinct_list:
            competence_mark_list = models.Competence_mark.objects.filter(competence=c_m.competence ,student=student_object)

            if not models.Competence_evaluation.filter(competence=c_m.competence ,student=student_object).exists():
                c_e = models.Competence_evaluation.create(competence=c_m.competence ,student=student_object)
                c_e.save()
            
            intensity_sum = 0.0
            marks_sum = 0.0
            c_e_saved = models.Competence_evaluation.filter(competence=c_m.competence, student=student_object)

            for c_m_c in competence_mark_list:
                e_c = models.Exercise_competence(exercise_activity__set_activity__students = student_object,  competece = c_m.competence)
                intensity_sum = intensity_sum + e_c.intensity
                marks_sum = marks_sum + c_m_c.mark
            
            mark = marks_sum/intensity_sum
            c_e_saved.mark = mark

    def calculate_exercise_mark(self, exercise: models.Exercise, student: models.Student) -> None:
        if not models.Exercise_mark.objects.filter(exercise = exercise, student = student).exists():
            e_m = models.Exercise_mark.objects.create(exercise = exercise, student = student)
            e_m.save()
        
        exercise_mark = models.Exercise_mark.objects.get(exercise = exercise, student = student)
        competence_mark_ls = models.Competence_mark.objects.filter(exercise=exercise).order_by('competence')

        weight_total = 0.0
        mark_total = 0.0
        if competence_mark_ls:
            for competence_mark in competence_mark_ls:
                exercise_competence = models.Exercise_competence.objects.get(exercise=exercise, competence=competence_mark.competence)
                weight_total = weight_total + float(exercise_competence.weight)
                if competence_mark.mark:
                    if competence_mark.evaluation_type == "AUTOMATIC":
                        mark_total = mark_total + float(competence_mark.mark * exercise_competence.weight)
                    else:
                        mark_total = mark_total + float(competence_mark.manual_mark * exercise_competence.weight)
                
            
            mark = mark_total/weight_total

            exercise_mark.mark = mark
            exercise_mark.save()

        self.calculate_activity_mark(activity = exercise_mark.exercise.activity, student=exercise_mark.student)

    def mark_activity_mark(self, mark: float, activity_mark: models.Activity_mark) -> None:
        activity_mark.manual_mark = mark
        activity_mark.evaluation_type = "MANUAL"
        activity_mark.save()

    def mark_competence_mark(self, mark: float, competence_mark: models.Competence_mark) -> None:
        competence_mark.mark = mark
        competence_mark.save()

        self.calculate_exercise_mark(exercise = competence_mark.exercise, student=competence_mark.student)
    
    def mark_exercise_mark(self, mark: float, exercise_mark: models.Exercise_mark) -> None:
        exercise_mark.manual_mark = mark
        exercise_mark.evaluation_type = "MANUAL"
        exercise_mark.save()

        self.calculate_activity_mark(activity = exercise_mark.exercise.activity, student=exercise_mark.student)
    
    

class SetService():

    def is_owner(self, user: User, set_object: models.Set) -> bool:
        res = False

        if set_object.teacher.user == user:
            res = True
        
        return res

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
