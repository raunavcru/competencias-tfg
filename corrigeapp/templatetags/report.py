from django import template

register = template.Library()

@register.filter(name = 'level1')
def level1(self, parent):
    return self.student_competence_evaluation.filter(competence__level = 1, competence__parent = parent).order_by('competence__code')

@register.filter(name = 'evaluations_list')
def evaluations_list(self, set_object):
    final = self.student_evaluation_mark.filter(evaluation__evaluation_set = set_object).order_by('evaluation__name')
    partials = self.student_evaluation_mark.filter(evaluation__parent__evaluation_set = set_object).order_by('evaluation__name')
    return final | partials

@register.filter(name = 'activities_list')
def activities_list(self, evaluation):
    return self.student_activity_mark.filter(activity__evaluation = evaluation).order_by('activity__title')
    