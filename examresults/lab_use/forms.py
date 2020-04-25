from django import forms
from .models import *
# from .models import Institution

# class NewResultForm(forms.ModelForm):
#     class Meta:
#         model = ExamResult
#         fields = ['patient_full_name', 'institution', 'sample_received', 'sample_id', 'exam_result', 'exam_date']


class UploadSheetForm(forms.Form):
    # institution = Institution
    # title = forms.CharField(max_length=50)
    planilha = forms.FileField()

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        filter_horizontal = ('symptom_list',)
        fieldsets = (
            ('Amostra', {
                'fields': ('high_priority', ('sample_id', 'sample_type'), 'origin', 'collect_date'),
            }),
            ('Análise', {
                'fields': (('is_extracted', 'is_amplified'), 'pcr_target_pair', 'result'),
            }),
            ('Dados clínicos', {
                'fields': ('symptoms_start_date', 'symptom_list'),
            }),
        )
    
        fields = ['sample_id', 'sample_type', 'origin', 'collect_date',
                      'high_priority',
                      'symptoms_start_date', 'symptom_list', 'is_extracted',
                      'is_amplified', 'result', 'pcr_target_pair']
    
