# Generated by Django 3.2.25 on 2024-07-03 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20240630_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='fhir_id',
        ),
    ]
