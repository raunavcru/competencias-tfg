# Generated by Django 3.1.6 on 2021-04-17 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrigeapp', '0005_auto_20210406_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='competence',
            name='subject_weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='subject_weight'),
        ),
    ]
