from django import template

register = template.Library()

@register.filter(name = 'level1')
def level1(self, parent):
    return self.student_competence_evaluation.filter(competence__level = 1, competence__parent = parent).order_by('competence__code')