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

class SampleType(models.Model):
    name = models.CharField(max_length=50)


class ExamResult(models.Model):
    #patient_full_name = models.CharField(max_length=200)
    #patient_id = models.CharField(max_length=20)
    #institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    sample_id = models.CharField(max_length=40, blank=False)
    patient_unique_id = models.CharField(max_length=30, unique=True, blank=False)
    patient_full_name = models.CharField(max_length=200, blank=False)
    patient_birthday = models.DateField('Patient birthday', null=False)
    sample_date = models.DateField('Sample obtained date', blank=False)
    sample_types = models.ManyToManyField(SampleType, blank=True)
    reported_sample_type = models.ForeignKey(SampleType, related_name="use_on_report", on_delete=models.CASCADE, blank=True, null=True)
    symptoms_start_date = models.DateField('Symptoms start date', blank=True, null=True)
    extraction_team = models.CharField(max_length=80, blank=True)
    extraction_kit = models.CharField(max_length=80, blank=True)
    pcr_team = models.CharField(max_length=80, blank=True)
    pcr_equipment = models.CharField(max_length=80, blank=True)
    result = models.CharField(max_length=200, blank=True)
    conclusion = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    result_date = models.DateField('Date of result', blank=True, null=True)
    ready_for_PDF = models.BooleanField(default=False, blank=False)
    PDF_sent = models.BooleanField(default=False, blank=False)




