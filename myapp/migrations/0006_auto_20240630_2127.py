# Generated by Django 3.2.25 on 2024-06-30 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='communication',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='contact',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='deceased',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='general_practitioner',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='managing_organization',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='marital_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='telecom',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
