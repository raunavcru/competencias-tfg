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

        self.calculate_evaluation_mark(evaluation = activity.evaluation, set_object = activity.set_activity, student = student)

    def calculate_competence_evaluation_level1(self, competence_mark: models.Competence_mark) -> None:

        if not models.Competence_evaluation.objects.filter(competence=competence_mark.competence, student=competence_mark.student).exists():
            c_e = models.Competence_evaluation.objects.create(competence=competence_mark.competence, student=competence_mark.student)
            c_e.save()
        
        competence_evaluation = models.Competence_evaluation.objects.get(competence=competence_mark.competence, student=competence_mark.student)
        competence_mark_list = models.Competence_mark.objects.filter(competence = competence_mark.competence, student=competence_mark.student)

        intensity_sum = 0.0
        marks_sum = 0.0
        for c_m in competence_mark_list:
            exercise_competence = models.Exercise_competence.objects.get(exercise = c_m.exercise, competence = c_m.competence)
            intensity_sum = intensity_sum + float(exercise_competence.intensity)
            marks_sum = marks_sum + float(c_m.mark * exercise_competence.intensity)
        
        mark = marks_sum/intensity_sum

        competence_evaluation.mark = mark
        competence_evaluation.save()

        self.calculate_competence_evaluation_level2(competence_evaluation = competence_evaluation)
    
    def calculate_competence_evaluation_level2(self, competence_evaluation: models.Competence_evaluation) -> None:

        parent = models.Competence.objects.filter(competence_parent=competence_evaluation.competence).first()

        if not models.Competence_evaluation.objects.filter(competence=parent, student=competence_evaluation.student).exists():
            c_e = models.Competence_evaluation.objects.create(competence=parent, student=competence_evaluation.student)
            c_e.save()
        
        competence_evaluation_level2 = models.Competence_evaluation.objects.get(competence=parent, student=competence_evaluation.student)

        competence_list = models.Competence.objects.filter(parent = parent)
        for c in competence_list:
            if not models.Competence_evaluation.objects.filter(competence=c, student=competence_evaluation.student).exists():
                c_e_level1 = models.Competence_evaluation.objects.create(competence=c, student=competence_evaluation.student)
                c_e_level1.save()
        
        competence_evaluation_list = models.Competence_evaluation.objects.filter(competence__parent = parent, student=competence_evaluation.student)
        
        weight_total = 0.0
        mark_total = 0.0
        for c_e in competence_evaluation_list:
            weight_total = weight_total + float(c_e.competence.weight)

            if c_e.mark:
                mark_total = mark_total + float(c_e.mark * c_e.competence.weight)
        
        mark = mark_total/weight_total

        competence_evaluation_level2.mark = mark
        competence_evaluation_level2.save()

        self.calculate_competence_evaluation_level2_parent(competence_evaluation = competence_evaluation_level2)
    
    def calculate_competence_evaluation_level2_parent(self, competence_evaluation: models.Competence_evaluation) -> None:

        parents = models.Competence.objects.filter(competence_parent=competence_evaluation.competence)

        for parent in parents:

            if not models.Competence_evaluation.objects.filter(competence=parent, student=competence_evaluation.student).exists():
                c_e = models.Competence_evaluation.objects.create(competence=parent, student=competence_evaluation.student)
                c_e.save()
            
            competence_evaluation_level3 = models.Competence_evaluation.objects.get(competence=parent, student=competence_evaluation.student)

            self.calculate_competence_evaluation_level3(competence_evaluation = competence_evaluation_level3)
    
    def calculate_competence_evaluation_level3(self, competence_evaluation: models.Competence_evaluation) -> None:

        competence_evaluation_list = models.Competence_evaluation.objects.filter(competence__parent = competence_evaluation.competence, student=competence_evaluation.student)

        weight_total = 0.0
        mark_total = 0.0
        for c_e in competence_evaluation_list:
            weight_total = weight_total + float(c_e.competence.weight)

            if c_e.mark:
                mark_total = mark_total + float(c_e.mark * c_e.competence.weight)
        
        mark = mark_total/weight_total

        competence_evaluation.mark = mark
        competence_evaluation.save()

    def calculate_evaluation_mark(self, evaluation: models.Evaluation, set_object: models.Set, student: models.Student) -> None:
        if evaluation.is_final:
            if set_object.evaluation_type_final == "BY_COMPETENCES":
                self.calculate_evaluation_mark_by_competences(evaluation = evaluation, set_object = set_object, student = student)
            elif set_object.evaluation_type_final == "BY_EVALUATION_NO_RECOVERY":
                self.calculate_evaluation_mark_by_partial_evaluations(evaluation = evaluation, set_object = set_object, student = student)
            elif set_object.evaluation_type_final == "BY_EVALUATION_RECOVERY":
                self.calculate_evaluation_mark_by_recovery_activities(evaluation = evaluation, set_object = set_object, student = student)
        else:
            if set_object.evaluation_type_partial == "BY_ALL_ACTIVITIES":
                self.calculate_evaluation_mark_by_all_activities(evaluation = evaluation, set_object = set_object, student = student)
            elif set_object.evaluation_type_partial == "BY_RECOVERY_ACTIVITIES": 
                self.calculate_evaluation_mark_by_recovery_activities(evaluation = evaluation, set_object = set_object, student = student)

    def calculate_evaluation_mark_by_competences(self, evaluation: models.Evaluation, set_object: models.Set, student: models.Student) -> None:
        if not models.Evaluation_mark.objects.filter(evaluation = evaluation, student = student).exists():
            e_m = models.Evaluation_mark.objects.create(evaluation = evaluation, student = student)
            e_m.save()
        
        evaluation_mark = models.Evaluation_mark.objects.get(evaluation = evaluation, student = student)
        competence_ls = models.Competence.objects.filter(competence_parent__competence_parent__competence_exercise_competence__exercise__activity__set_activity = set_object, level = 3)
        for competence in competence_ls:
            if not models.Competence_evaluation.objects.filter(competence = competence, student = student).exists():
                e_v = models.Competence_evaluation.objects.create(competence = competence, student = student)
                e_v.save()

        competence_evaluation_ls = models.Competence_evaluation.objects.filter(competence__competences__subject_set = set_object, competence__level = 3, student = student)

        weight_total = 0.0
        mark_total = 0.0
        for competence_evaluation in competence_evaluation_ls:
            weight_total = weight_total + float(competence_evaluation.competence.weight)

            if competence_evaluation.mark:
                mark_total = mark_total + float(competence_evaluation.mark * competence_evaluation.competence.weight)
        
        mark = mark_total/weight_total

        evaluation_mark.mark = mark
        evaluation_mark.save()

    def calculate_evaluation_mark_by_all_activities(self, evaluation: models.Evaluation, set_object: models.Set, student: models.Student) -> None:
        if not models.Evaluation_mark.objects.filter(evaluation = evaluation, student = student).exists():
            e_m = models.Evaluation_mark.objects.create(evaluation = evaluation, student = student)
            e_m.save()
        
        evaluation_mark = models.Evaluation_mark.objects.get(evaluation = evaluation, student = student)
        activity_mark_ls = models.Activity_mark.objects.filter(activity__evaluation = evaluation, activity__set_activity = set_object)

        weight_total = 0.0
        mark_total = 0.0
        for activity_mark in activity_mark_ls:
            weight_total = weight_total + float(activity_mark.activity.weight)

            if activity_mark.mark:
                if activity_mark.evaluation_type == "AUTOMATIC":
                    mark_total = mark_total + float(activity_mark.mark * activity_mark.activity.weight)
                else:
                    mark_total = mark_total + float(activity_mark.manual_mark * activity_mark.activity.weight)
        
        mark = mark_total/weight_total

        evaluation_mark.mark = mark
        evaluation_mark.save()

        self.calculate_evaluation_mark(evaluation = evaluation.parent, set_object = set_object, student = student)
    
    def calculate_evaluation_mark_by_no_recovery_activities(self, evaluation: models.Evaluation, set_object: models.Set, student: models.Student) -> None:
        if evaluation.is_final:
            self.calculate_evaluation_mark_by_partial_evaluations(evaluation = evaluation, set_object = set_object, student = student)
        else:
            self.calculate_evaluation_mark_by_all_activities(evaluation = evaluation, set_object = set_object, student = student)

    def calculate_evaluation_mark_by_partial_evaluations(self, evaluation: models.Evaluation, set_object: models.Set, student: models.Student) -> None:
        if not models.Evaluation_mark.objects.filter(evaluation = evaluation, student = student).exists():
            e_m = models.Evaluation_mark.objects.create(evaluation = evaluation, student = student)
            e_m.save()

        evaluation_mark_final = models.Evaluation_mark.objects.get(evaluation = evaluation, student = student)
        evaluation_mark_ls = models.Evaluation_mark.objects.filter(evaluation__parent = evaluation, student = student)

        weight_total = 0.0
        mark_total = 0.0
        if evaluation_mark_ls:
            for evaluation_mark in evaluation_mark_ls:
                weight_total = weight_total + float(evaluation_mark.evaluation.weight)

                if evaluation_mark.mark:
                    if evaluation_mark.evaluation_type == "AUTOMATIC":
                        mark_total = mark_total + float(evaluation_mark.mark * evaluation_mark.evaluation.weight)
                    else:
                        mark_total = mark_total + float(evaluation_mark.manual_mark * evaluation_mark.evaluation.weight)
            
            mark = mark_total/weight_total

            evaluation_mark_final.mark = mark
            evaluation_mark_final.save()

    def calculate_evaluation_mark_by_recovery_activities(self, evaluation: models.Evaluation, set_object: models.Set, student: models.Student) -> None:
        if not models.Evaluation_mark.objects.filter(evaluation = evaluation, student = student).exists():
            e_m = models.Evaluation_mark.objects.create(evaluation = evaluation, student = student)
            e_m.save()
        
        evaluation_mark = models.Evaluation_mark.objects.get(evaluation = evaluation, student = student)
        activity_mark_ls = models.Activity_mark.objects.filter(activity__evaluation=evaluation, activity__set_activity=set_object, activity__is_recovery=True)

        weight_total = 0.0
        mark_total = 0.0
        if activity_mark_ls:
            for activity_mark in activity_mark_ls:
                weight_total = weight_total + float(activity_mark.weight)

                if activity_mark.mark:
                    if activity_mark.evaluation_type == "AUTOMATIC":
                        mark_total = mark_total + float(activity_mark.mark * activity_mark.activity.weight)
                    else:
                        mark_total = mark_total + float(activity_mark.manual_mark * activity_mark.activity.weight)
            
            mark = mark_total/weight_total

            evaluation_mark.mark = mark
            evaluation_mark.save()
        else:
            self.calculate_evaluation_mark_by_no_recovery_activities(evaluation = evaluation, set_object = set_object, student = student)

        if not evaluation.is_final:
            self.calculate_evaluation_mark(evaluation = evaluation.parent, set_object = set_object, student = student)

    def calculate_exercise_mark(self, exercise: models.Exercise, student: models.Student) -> None:
        if not models.Exercise_mark.objects.filter(exercise = exercise, student = student).exists():
            e_m = models.Exercise_mark.objects.create(exercise = exercise, student = student)
            e_m.save()
        
        exercise_mark = models.Exercise_mark.objects.get(exercise = exercise, student = student)
        competence_mark_ls = models.Competence_mark.objects.filter(exercise=exercise).order_by('competence')

        weight_total = 0.0
        mark_total = 0.0
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

    def create_competence_evaluation(self, set_object: models.Set, student: models.Student) -> None:

        competence_list = models.Competence.objects.filter(competences__subject_set = set_object)
        competence_evaluation_list = models.Competence_evaluation.objects.filter(competence__competences__subject_set = set_object, student = student)
        print("=================================================================")
        print(competence_list.count())
        print("=================================================================")
        print(competence_evaluation_list.count())

        if not competence_list.count() == competence_evaluation_list.count():
            for competence in competence_list:
                if not models.Competence_evaluation.objects.filter(competence = competence, student = student).exists():
                    competence_evaluation = models.Competence_evaluation.objects.create(competence = competence, student = student)
                    competence_evaluation.save()
                    
    def mark_activity_mark(self, mark: float, activity_mark: models.Activity_mark) -> None:
        activity_mark.manual_mark = mark
        activity_mark.evaluation_type = "MANUAL"
        activity_mark.save()

        self.calculate_evaluation_mark(evaluation = activity_mark.activity.evaluation, set_object = activity_mark.activity.set_activity, student = activity_mark.student)

    def mark_competence_mark(self, mark: float, competence_mark: models.Competence_mark) -> None:
        competence_mark.mark = mark
        competence_mark.save()

        self.calculate_competence_evaluation_level1(competence_mark=competence_mark)
        self.calculate_exercise_mark(exercise = competence_mark.exercise, student=competence_mark.student)

    
    def mark_evaluation_mark(self, mark: float, evaluation_mark: models.Evaluation_mark) -> None:
        evaluation_mark.manual_mark = mark
        evaluation_mark.evaluation_type = "MANUAL"
        evaluation_mark.save()

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
