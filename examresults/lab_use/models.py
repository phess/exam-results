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
    patient_full_name = models.CharField(max_length=200)
    patient_id = models.CharField(max_length=20)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    sample_received = models.DateField('date received')
    sample_id = models.CharField(max_length=40)
    exam_result = models.CharField(choices=RESULT_CHOICES, max_length=30)
    exam_date = models.DateTimeField('date issued', auto_now_add=False)
    result_submitted = models.BooleanField()

