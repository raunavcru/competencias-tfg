# Generated by Django 3.1.4 on 2021-04-06 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrigeapp', '0003_auto_20210406_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='evaluation_type_final',
            field=models.CharField(default='s', max_length=100, verbose_name='evaluation_type_final'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='set',
            name='evaluation_type_partial',
            field=models.CharField(default='1', max_length=100, verbose_name='evaluation_type_partial'),
            preserve_default=False,
        ),
    ]
