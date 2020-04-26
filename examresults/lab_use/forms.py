from django import forms
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
        model = Amostra
        filter_horizontal = ('sintoma',)
        fieldsets = (
            ('Amostra', {
                'fields': ('prioridade', ('cod_amostra', 'tipo_amostra'), 
                           'paciente', 'laboratorio', 'dt_coleta', ('descrição',)),
            }),
            ('Análise', {
                'fields': (('extraido', 'amplificado'), 'resultado'),
            }),
            ('Dados clínicos', {
                'fields': ('dt_inicial_sintoma', 'sintoma'),
            }),
            ('Fluxo', {
                'fields': ('dt_criacao'),
            }),
        )
    
        #fields = ['sample_id', 'sample_type', 'origin', 'collect_date',
        #              'high_priority',
        #              'symptoms_start_date', 'symptom_list', 'is_extracted',
        #              'is_amplified', 'result', 'pcr_target_pair']
    
