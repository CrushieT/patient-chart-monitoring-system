# Generated by Django 5.2 on 2025-04-24 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_vitalsigns1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_name', models.CharField(max_length=100)),
                ('dose', models.DecimalField(decimal_places=2, max_digits=10)),
                ('units', models.CharField(choices=[('mg', 'Milligrams (mg)'), ('g', 'Grams (g)'), ('ml', 'Milliliters (mL)'), ('tablet', 'Tablets'), ('capsule', 'Capsules'), ('drop', 'Drops')], max_length=20)),
                ('frequency', models.CharField(choices=[('daily', 'Once Daily'), ('bid', 'Twice Daily (BID)'), ('tid', 'Three Times Daily (TID)'), ('qid', 'Four Times Daily (QID)'), ('prn', 'As Needed (PRN)')], max_length=20)),
                ('route', models.CharField(choices=[('oral', 'Oral'), ('iv', 'Intravenous (IV)'), ('im', 'Intramuscular (IM)'), ('sc', 'Subcutaneous (SC)'), ('topical', 'Topical'), ('inhalation', 'Inhalation')], max_length=20)),
                ('duration', models.PositiveIntegerField(help_text="e.g., '7 days'")),
                ('quantity', models.PositiveIntegerField(help_text='Total quantity dispensed')),
                ('start_date', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('health_diagnostics', models.TextField(blank=True, help_text='Relevant health conditions for this medication', null=True)),
                ('patient_instructions', models.TextField(blank=True, help_text='Instructions for the patient', null=True)),
                ('pharmacist_instructions', models.TextField(blank=True, help_text='Special instructions for the pharmacist', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medications', to='App.patientinformation')),
            ],
            options={
                'verbose_name_plural': 'Medications',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='NurseNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(help_text='Detailed nursing notes (supports paragraphs and formatting)', verbose_name='Clinical Notes')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Note Date')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('nurse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nurse_notes', to='App.employee', to_field='employee_id', verbose_name='Nurse')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nurse_notes', to='App.patientinformation', verbose_name='Patient')),
            ],
            options={
                'verbose_name_plural': 'Nurse Notes',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='VitalSigns2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_and_time', models.DateTimeField(auto_now_add=True)),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, help_text='Temperature in °C (e.g., 36.6)', max_digits=5, null=True)),
                ('blood_pressure', models.CharField(blank=True, help_text="Format: '120/80'", max_length=10, null=True)),
                ('pulse_rate', models.PositiveIntegerField(blank=True, help_text='Beats per minute (e.g., 72)', null=True)),
                ('respiratory_rate', models.PositiveIntegerField(blank=True, help_text='Breaths per minute (e.g., 16)', null=True)),
                ('oxygen_saturation', models.DecimalField(blank=True, decimal_places=2, help_text='SpO2 percentage (e.g., 98.5)', max_digits=5, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vital_signs2', to='App.patientinformation')),
            ],
            options={
                'verbose_name_plural': 'Vital Signs 2',
                'ordering': ['-date_and_time'],
            },
        ),
    ]
