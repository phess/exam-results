from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

RESULT_CHOICES = [
        ('positive', 'POS'),
        ('negative', 'NEG'),
        ('indetermined', 'IND'),
]

COLLECTED_MATERIAL = [
        ('sangue', 'blood'),
        ('saliva', 'spittle'),
]

EXTRACTION_TEAM = [
        ('Time A', 'teama'),
        ('Time B', 'teamb'),
]

class Institution(models.Model):
    short_name = models.SlugField(max_length=15, blank=False)
    full_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, default='I will set this later', blank=True)
    state = models.CharField(max_length=2, default='XX', blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.short_name

class SampleType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class ExamResult(models.Model):
    # patient_full_name = models.CharField(max_length=200)
    # patient_id = models.CharField(max_length=20)
    # institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    # sample_received = models.DateField('date received')
    # sample_id = models.CharField(max_length=40)
    # exam_result = models.CharField(choices=RESULT_CHOICES, max_length=30)
    # exam_date = models.DateTimeField('date issued', auto_now_add=False)
    # result_submitted = models.BooleanField()

    send_report = models.BooleanField()
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    sample_received = models.DateField('date received')
    sample_id = models.CharField(max_length=40)
    patient_id = models.CharField(max_length=20)
    patient_full_name = models.CharField(max_length=200)
    dob_date = models.DateTimeField('dob issued', auto_now_add=False, null=True)
    exam_date = models.DateTimeField('exam date', auto_now_add=False, null=True)
    collected_material = models.CharField(choices=COLLECTED_MATERIAL, max_length=30, null=True)
    beginning_symptoms = models.DateTimeField('beginning symptoms', auto_now_add=False, null=True)
    extraction_team = models.CharField(choices=EXTRACTION_TEAM, max_length=30, null=True)
    extraction_kit = models.CharField(max_length=200, null=True)
    pcr_team = models.CharField(max_length=200, null=True)
    pcr_machine = models.CharField(max_length=200, null=True)
    exam_result = models.CharField(choices=RESULT_CHOICES, max_length=30, null=True)
    conclusion = models.CharField(max_length=200, null=True)
    obs = models.CharField(max_length=800, null=True)
    
    # result_submitted = models.BooleanField()

# class Document(models.Model):
#     description = models.CharField(max_length=255, blank=True)
#     document = models.FileField(upload_to='documents/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

# modificado. testing.
