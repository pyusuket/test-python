# Generated by Django 3.2.25 on 2024-07-03 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_patient_fhir_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='fhir_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
