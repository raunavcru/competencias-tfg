# Generated by Django 3.1.4 on 2021-04-06 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrigeapp', '0002_competence_mark_exercise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competence_evaluation',
            name='mark',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='mark'),
        ),
    ]
