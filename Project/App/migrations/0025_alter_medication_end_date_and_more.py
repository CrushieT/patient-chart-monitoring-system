# Generated by Django 5.2 on 2025-05-21 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0024_patientsnapshot_patient_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='end_date',
            field=models.DateTimeField(blank=True, help_text='Date and time when the medication ends or is discontinued', null=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
