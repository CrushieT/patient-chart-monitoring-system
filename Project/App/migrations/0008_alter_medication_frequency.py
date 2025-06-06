# Generated by Django 5.2 on 2025-04-25 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_merge_20250425_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='frequency',
            field=models.CharField(choices=[('daily', 'Once Daily'), ('bid', 'Twice Daily (BID)'), ('tid', 'Three Times Daily (TID)'), ('qid', 'Four Times Daily (QID)'), ('prn', 'As Needed (PRN)'), ('q6h', 'Every 6 Hours'), ('q8h', 'Every 8 Hours')], max_length=20),
        ),
    ]
