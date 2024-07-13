from django.urls import path
from . import views
from .views import export_csv

urlpatterns = [
    path('export_csv/', export_csv, name='export_csv'),
    path('create_patient/', views.create_patient, name='create_patient'),
    path('list_patients/', views.list_patients, name='list_patients'),
]
