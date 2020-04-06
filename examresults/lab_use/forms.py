from django.forms import ModelForm
from lab_use.models import *

class NewResultForm(ModelForm):
    class Meta:
        model = ExamResult
        fields = ['patient_full_name', 'institution', 'sample_received', 'sample_id', 'exam_result', 'exam_date']
