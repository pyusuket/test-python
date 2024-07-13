from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Django FHIR Platform
class Patient(models.Model):
    fhir_id = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    address = models.JSONField(null=True, blank=True)
    telecom = models.JSONField(null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=True)
    deceased = models.JSONField(null=True, blank=True)
    contact = models.JSONField(null=True, blank=True)
    communication = models.JSONField(null=True, blank=True)
    managing_organization = models.CharField(max_length=200, null=True, blank=True)
    general_practitioner = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
