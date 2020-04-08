from django.db import models

RESULT_CHOICES = [
        ('positive', 'POS'),
        ('negative', 'NEG'),
        ('indetermined', 'IND'),
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
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    sample_id = models.CharField(max_length=40, blank=False)
    patient_unique_id = models.CharField(max_length=30, blank=False)
    patient_full_name = models.CharField(max_length=200, blank=False)
    patient_birthday = models.DateField('Patient birthday', null=False)
    sample_date = models.DateField('Sample obtained date', blank=False)
    sample_receive_date = models.DateField('Sample received date', blank=True, null=True)
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

    def sample_types_as_string(self):
        if self.sample_types.count() < 1:
            return ''
        elif self.sample_types.count() == 1:
            return self.sample_types.first().name
        else:
            name_list = [ st.name for st in self.sample_types.all() ]
            return '/'.join(name_list)
            

    def __str__(self):
        return '{} from {} on {}'.format(self.sample_types_as_string(),
                                         self.patient_unique_id,
                                         self.sample_date)


