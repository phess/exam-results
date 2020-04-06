from django.db import models

RESULT_CHOICES = [
        ('positive', 'POS'),
        ('negative', 'NEG'),
        ('indetermined', 'IND'),
]


class Institution(models.Model):
    short_name = models.SlugField(max_length=15)
    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='I will set this later')
    state = models.CharField(max_length=2, default='XX')

class ExamResult(models.Model):
    #patient_full_name = models.CharField(max_length=200)
    #patient_id = models.CharField(max_length=20)
    #institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    
    exam_date = models.DateTimeField('date issued', auto_now_add=False)

    status = models.CharField(max_length=30)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    sample_received = models.DateField('Sample received date')
    sample_id = models.CharField(max_length=40)
    patient_unique_id = models.CharField(max_length=30)
    patient_full_name = models.CharField(max_length=200)
    patient_birthday = models.DateField('Patient birthday')
    sample_date = models.DateField('Sample obtained date')
    symptoms_start_date = models.DateField('Symptoms start date')
    extraction_team = models.CharField(max_length=80)
    extraction_kit = models.CharField(max_length=80)
    pcr_team = models.CharField(max_length=80)
    pcr_equipment = models.CharField(max_length=80)
    result = models.CharField(max_length=200)
    conclusion = models.CharField(max_length=30)
    notes = models.TextField()
