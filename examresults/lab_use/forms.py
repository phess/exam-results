from django import forms
# from .models import Institution

# class NewResultForm(forms.ModelForm):
#     class Meta:
#         model = ExamResult
#         fields = ['patient_full_name', 'institution', 'sample_received', 'sample_id', 'exam_result', 'exam_date']

class UploadSheetForm(forms.Form):
    #institution = Institution
    #title = forms.CharField(max_length=50)
    planilha = forms.FileField()
