# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import gettext_lazy as _

RESULT_CHOICES = (
        ('positive', 'POS'),
        ('negative', 'NEG'),
        ('indetermined', 'IND'),
)

COLLECTED_MATERIAL = (
        ('sangue', 'blood'),
        ('swab', 'swab'),
        ('lavado', 'lavado'),
)

# EXTRACTION_TEAM = (
#         ('Time A', 'teama'),
#         ('Time B', 'teamb'),
# )

class State(models.Model):
    name = models.CharField(_('State'), max_length=50, db_index=True,
        help_text=_('Define the State'))
    short_name = models.CharField(_('State Short Name'), max_length=5, db_index=True,
        help_text=_('State Short Name'))
    created = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ['name']

class City(models.Model):
    state = models.ForeignKey(State, related_name='state', on_delete=models.CASCADE)
    name = models.CharField(_('City'), max_length=100, db_index=True,
        help_text=_('Define the City'))
    created = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return f'{self.name}, {self.state.short_name}'

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['name']
        unique_together = ('name', 'state')


class Laboratory(models.Model):
    short_name = models.SlugField(max_length=15)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='city', on_delete=models.CASCADE,
        help_text=_('Enter the city name'))
    created = models.DateTimeField(_('Created at'), auto_now_add=True)
    #modified = models.DateTimeField(_('Created at'), auto_now=True)

    def state(self):
        return self.city.state

    def __str__(self):
        return f'{self.name}'

    # def save(self):
    #    self.short_name = self.short_name + 'waldirio'
    #    super(Laboratory, self).save()


    @property
    def status(self):
        return True

    @status.setter
    def status(self, value):
        self.short_name = value
        self.save()

    # def generate_report(self):
    #     print("oi")

    class Meta:
        verbose_name = _('Laboratory')
        verbose_name_plural = _('Laboratories')
        ordering = ['name']


class SampleType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class ExtractionTeam(models.Model):
    name = models.CharField(_('Team Name'), max_length=50, db_index=True,
        help_text=_('Define the Team Name'))
    short_name = models.CharField(_('Team Short Name'), max_length=20, db_index=True,
        help_text=_('Team Short Name'))
    created = models.DateTimeField(_('Created at'), auto_now_add=True)


    def __str__(self):
        return f'{self.name}'


class PcrTeam(models.Model):
    name = models.CharField(_('PCR Team Name'), max_length=50, db_index=True,
        help_text=_('Define the PCR Team Name'))
    short_name = models.CharField(_('PCR Team Short Name'), max_length=20, db_index=True,
        help_text=_('PCR Team Short Name'))
    created = models.DateTimeField(_('Created at'), auto_now_add=True)


    def __str__(self):
        return f'{self.name}'



class ExamResult(models.Model):
    send_report = models.BooleanField(default=False)
    priority = models.BooleanField(default=False)
    
    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    sample_received = models.DateField('date received')
    sample_id = models.CharField(max_length=40)
    patient_id = models.CharField(max_length=20)
    patient_full_name = models.CharField(max_length=200)
    dob_date = models.DateField('dob issued', auto_now_add=False, null=True)
    exam_date = models.DateField('exam date', auto_now_add=False, null=True)
    collected_material = models.CharField(choices=COLLECTED_MATERIAL, max_length=30, null=True)
    beginning_symptoms = models.DateField('beginning symptoms', auto_now_add=False, null=True)
    
    extraction_team = models.ForeignKey(ExtractionTeam, on_delete=models.CASCADE)
    extraction_kit = models.CharField(max_length=200, blank=True)
    
    pcr_team = models.ForeignKey(PcrTeam, on_delete=models.CASCADE)
    pcr_machine = models.CharField(max_length=200, blank=True)
    exam_result = models.CharField(choices=RESULT_CHOICES, max_length=30, blank=True)
    conclusion = models.CharField(max_length=200, blank=True)
    obs = models.CharField(max_length=800, blank=True)
    

class OverwriteStorage(FileSystemStorage):
    '''
    Muda o comportamento padrão do Django e o faz sobrescrever arquivos de
    mesmo nome que foram carregados pelo usuário ao invés de renomeá-los.
    '''
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class Media(models.Model):
    name = models.CharField("Nome", max_length=128)
    media = models.FileField("Arquivo", upload_to="lab_use/media/", storage=OverwriteStorage())