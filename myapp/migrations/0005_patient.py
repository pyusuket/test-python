# Generated by Django 3.2.25 on 2024-06-30 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_delete_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fhir_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('birth_date', models.DateField()),
            ],
        ),
    ]
