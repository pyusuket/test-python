from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    MARITAL_STATUS_CHOICES = [
        ('', '選択してください'),
        ('S', '未婚'),
        ('M', '既婚'),
        ('D', '離婚'),
        ('W', '死別')
    ]

    family_name = forms.CharField(label='姓', max_length=100)
    given_name = forms.CharField(label='名', max_length=100)
    address_text = forms.CharField(label='住所', widget=forms.Textarea(attrs={'rows': 3}), required=False)
    telecom_value = forms.CharField(label='連絡先', max_length=100, required=False)
    marital_status = forms.ChoiceField(label='婚姻状況', choices=MARITAL_STATUS_CHOICES, required=False)

    class Meta:
        model = Patient
        fields = ['family_name', 'given_name', 'birth_date', 'gender', 'address_text', 'telecom_value',
                  'marital_status', 'active', 'deceased', 'contact', 'communication',
                  'managing_organization', 'general_practitioner']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('', '選択してください'), ('male', '男性'), ('female', '女性'), ('other', 'その他')]),
            'deceased': forms.DateInput(attrs={'type': 'date'}),
            'contact': forms.Textarea(attrs={'rows': 3}),
            'communication': forms.Textarea(attrs={'rows': 3}),
            'general_practitioner': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'birth_date': '生年月日',
            'gender': '性別',
            'active': 'アクティブ状態',
            'deceased': '死亡日',
            'contact': '緊急連絡先',
            'communication': '使用言語',
            'managing_organization': '管理組織',
            'general_practitioner': 'かかりつけ医',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.required:
                field.label += ' *'
            else:
                field.required = False

        # 以下のフィールドにデフォルト値を設定
        self.fields['deceased'].initial = None
        self.fields['contact'].initial = ''
        self.fields['communication'].initial = ''
        self.fields['managing_organization'].initial = ''
        self.fields['general_practitioner'].initial = ''

        # Noneの代わりに空文字列を使用
        for field_name in ['contact', 'communication', 'managing_organization', 'general_practitioner']:
            if self.initial.get(field_name) is None:
                self.initial[field_name] = ''
