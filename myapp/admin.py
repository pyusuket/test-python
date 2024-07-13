from django.contrib import admin
from .models import Patient, Person

# Register your models here.
admin.site.register(Patient)
admin.site.register(Person)
