from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .models import Patient
from django.utils import timezone
import csv
import json
from .forms import PatientForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pytz

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patients.csv"'
    response.write('\ufeff'.encode('utf8'))  # BOM (Byte Order Mark) to indicate UTF-8 encoding

    writer = csv.writer(response)
    field_names = [field.name for field in Patient._meta.fields]

    # Write header row with field names
    writer.writerow(field_names)

    # Query all patients
    patients = Patient.objects.all()

    # Iterate through patients and write each row
    for patient in patients:
        row = []
        for field in field_names:
            value = getattr(patient, field)

            # Convert datetime fields to the specified timezone and format
            if isinstance(value, timezone.datetime):
                jp_timezone = pytz.timezone('Asia/Tokyo')
                value = value.astimezone(jp_timezone)
                value = value.strftime('%Y-%m-%d %H:%M:%S')

            # Convert JSONField to string if necessary
            elif isinstance(value, dict) or isinstance(value, list):
                value = str(value)

            row.append(value)

        writer.writerow(row)

    return response


def get_credentials():
    try:
        return service_account.Credentials.from_service_account_file(
            settings.SERVICE_ACCOUNT_KEY_PATH,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None

def get_fhir_service():
  credentials = get_credentials()
  if credentials:
    return build('healthcare', 'v1', credentials=credentials)
  else:
    raise Exception("Failed to get credentials")

# FHIRストアの情報
PROJECT_ID = settings.PROJECT_ID
LOCATION = settings.LOCATION
DATASET_ID = settings.DATASET_ID
FHIR_STORE_ID = settings.FHIR_STORE_ID

# 患者リソースの一覧を取得するビュー関数
def list_patients(request):
    if request.method == 'GET':
        try:
            # FHIR サービスを取得
            fhir_service = get_fhir_service()

            # FHIR ストアの名前を設定
            fhir_store_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/datasets/{DATASET_ID}/fhirStores/{FHIR_STORE_ID}"

            # FHIR サービスを使用して患者リソースを検索
            fhir_request = fhir_service.projects().locations().datasets().fhirStores().fhir().search(
                parent=fhir_store_name,
                body={
                    "resourceType": "Patient"
                }
            )

            # 検索結果を取得
            response = fhir_request.execute()
            patients = response.get('entry', [])

            for entry in patients:
                patient_data = entry['resource']
                name = patient_data.get('name', [{}])[0]
                family_name = name.get('family', '')
                given_name = ' '.join(name.get('given', []))
                full_name = f"{family_name} {given_name}".strip()

                gender_mapping = {'male': '男性', 'female': '女性'}
                gender = gender_mapping.get(patient_data.get('gender', ''), patient_data.get('gender', ''))

                patient, created = Patient.objects.update_or_create(
                    fhir_id=patient_data['id'],
                    defaults={
                        'name': full_name,
                        'birth_date': patient_data.get('birthDate'),
                        'gender': gender,
                        'address': patient_data.get('address'),
                        'telecom': patient_data.get('telecom'),
                        'marital_status': patient_data.get('maritalStatus', {}).get('coding', [{}])[0].get('code'),
                        'active': patient_data.get('active', True),
                        'deceased': patient_data.get('deceasedBoolean') or patient_data.get('deceasedDateTime'),
                        'contact': patient_data.get('contact'),
                        'communication': patient_data.get('communication'),
                        'managing_organization': patient_data.get('managingOrganization', {}).get('reference'),
                        'general_practitioner': patient_data.get('generalPractitioner'),
                    }
                )

            # データベースから患者一覧を取得
            patient_list = Patient.objects.all()

            # 患者リソースのデータを整形
            formatted_patients = []
            for patient in patient_list:
                formatted_patient = {
                    'id': patient.id,
                    'name': patient.name,
                    'birth_date': patient.birth_date.strftime('%Y年%m月%d日') if patient.birth_date else '',
                    'gender': patient.gender,
                    # 他のフィールドも必要に応じて追加
                }
                formatted_patients.append(formatted_patient)

            # PatientFormをコンテキストに追加
            form = PatientForm()

            # 患者一覧をテンプレートに渡してレンダリング
            return render(request, 'patient_list.html', {'patients': patient_list, 'form': form})

        except Exception as e:
            error_message = f"Error retrieving patients: {str(e)}"
            print(error_message)
            return render(request, 'error.html', {'error_message': error_message})

    else:
        return render(request, 'error.html', {'error_message': 'This endpoint only accepts GET requests.'})

@csrf_exempt
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            try:
                # FHIR サービスを取得
                fhir_service = get_fhir_service()

                # FHIR ストアの名前を設定
                fhir_store_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/datasets/{DATASET_ID}/fhirStores/{FHIR_STORE_ID}"

                # FHIR Patient リソースを作成
                patient_resource = {
                    "resourceType": "Patient",
                    "name": [
                        {
                            "family": form.cleaned_data['family_name'],
                            "given": [form.cleaned_data['given_name']]
                        }
                    ],
                    "birthDate": form.cleaned_data['birth_date'].strftime('%Y-%m-%d'),
                    "gender": form.cleaned_data['gender'],
                    "address": [
                        {
                            "text": form.cleaned_data['address_text']
                        }
                    ],
                    "telecom": [
                        {
                            "system": "phone",
                            "value": form.cleaned_data['telecom_value']
                        }
                    ]
                }

                # FHIR サービスを使用して患者リソースを作成
                fhir_request = fhir_service.projects().locations().datasets().fhirStores().fhir().create(
                    parent=fhir_store_name,
                    type='Patient',
                    body=patient_resource
                )

                # リクエストを実行
                response = fhir_request.execute()

                # レスポンスから FHIR ID を取得
                fhir_id = response['id']

                # データベースに患者を保存
                patient = form.save(commit=False)
                patient.fhir_id = fhir_id
                patient.name = f"{form.cleaned_data['family_name']} {form.cleaned_data['given_name']}"
                patient.address = {'text': form.cleaned_data['address_text']}
                patient.telecom = [{'value': form.cleaned_data['telecom_value']}]
                patient.save()

                return JsonResponse({
                    'success': True,
                    'patient': {
                        'id': patient.id,
                        'fhir_id': patient.fhir_id,
                        'name': patient.name,
                        'birth_date': patient.birth_date.strftime('%Y年%m月%d日') if patient.birth_date else '-',
                        'gender': patient.gender or '-',
                        'address': patient.address.get('text', '-') if patient.address else '-',
                        'telecom': patient.telecom[0]['value'] if patient.telecom else '-'
                    }
                })
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})
