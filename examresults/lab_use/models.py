# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

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

EXT_EVENT_CHOICES = ( 
        ( 'not started', 'não iniciado'),
        ( 'started', 'iniciado' ),
        ('finished', 'terminado' ),
)

class State(models.Model):
    name = models.CharField(_('State'), max_length=50, db_index=True,
                            help_text=_('Define the State'))
    short_name = models.CharField(_('State Short Name'), max_length=5,
                                  db_index=True,
                                  help_text=_('State Short Name'))
    created = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ['name']


class City(models.Model):
    state = models.ForeignKey(State, related_name='state',
                              on_delete=models.CASCADE)
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


class Symptom(models.Model):
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return self.name


class Result(models.Model):
    name = models.CharField(max_length=40)
    long_description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class PcrTargetPair(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class ExtractionKit(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
        
class PcrKit(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


class Patient(models.Model):
    full_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, blank=True)
    id_card = models.CharField(max_length=20, blank=True, unique=True)
    date_of_birth = models.DateField(null=True)
    

class Laboratory(models.Model):
    short_name = models.SlugField(max_length=15)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True)
    city = models.ForeignKey(City, related_name='city',
                             on_delete=models.CASCADE,
                             help_text=_('Enter the city name'))
    created = models.DateTimeField(_('Created at'), auto_now_add=True)
    # modified = models.DateTimeField(_('Created at'), auto_now=True)

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


class Sample(models.Model):
    high_priority = models.BooleanField(default=False)
    origin = models.ForeignKey(Laboratory, null=True, on_delete=models.CASCADE)
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE)
    sample_id = models.CharField(max_length=40)
    collect_date = models.DateField(null=True)
    symptoms_start_date = models.DateField(null=True)
    symptom_list = models.ManyToManyField(Symptom)
    is_extracted = models.BooleanField(default=False)
    is_amplified = models.BooleanField(default=False)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=True, blank=True)
    pcr_target_pair = models.ForeignKey(PcrTargetPair, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.sample_id

class ExtractionTeamMember(models.Model):
    name = models.CharField(max_length=100, blank=False)
    
    def __str__(self):
        return self.name

#class ExtractionTeam(models.Model):
#    name = models.CharField(_('Team Name'), max_length=50, db_index=True,
#                            help_text=_('Define the Team Name'))
#    short_name = models.CharField(_('Team Short Name'), max_length=20,
#                                  db_index=True,
#                                  help_text=_('Team Short Name'))
#    created = models.DateTimeField(_('Created at'), auto_now_add=True)
#
#    def __str__(self):
#        return f'{self.name}'

class PcrTeamMember(models.Model):
    name = models.CharField(max_length=100, blank=False)
    
    def __str__(self):
        return self.name


#class PcrTeam(models.Model):
#    name = models.CharField(_('PCR Team Name'), max_length=50, db_index=True,
#                            help_text=_('Define the PCR Team Name'))
#    short_name = models.CharField(_('PCR Team Short Name'), max_length=20,
#                                  db_index=True,
#                                  help_text=_('PCR Team Short Name'))
#    created = models.DateTimeField(_('Created at'), auto_now_add=True)
#
#    def __str__(self):
#        return f'{self.name}'


class Event(models.Model):
    """ExtractionEvent and PcrEvent will be based on this class"""
    sample_list = models.ManyToManyField(Sample)
    start_time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    status = models.CharField(max_length=20, choices=EXT_EVENT_CHOICES, blank=True)
    

    def is_started(self):
        return self.status == "started"
    
    def is_finished(self):
        return self.status == "finished"

    def modified_time(self):
        try:
            return max(self.start_time, self.end_time)
        # If either of these times is Null, TypeError will be raised
        except TypeError:
            if self.end_time != None:
                return self.end_time
            elif self.start_time != None:
                return self.start_time
            else:
                return 0

class Queue(models.Model):
    sample_list = models.ManyToManyField(Sample)
    date = models.DateField(auto_now_add=True)

class PcrQueue(Queue):
    
    def __str__(self):
        return "Samples ready for PCR"





class ExtractionQueue(Queue):
    #sample_list = models.ManyToManyField(Sample)
    #date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return "Samples ready for extraction"
    

class ExtractionMachine(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name




#class ExtractionEvent(models.Model):
class ExtractionEvent(Event):
    #sample_list = models.ManyToManyField(Sample)
    #start_time = models.DateTimeField(auto_now_add=True, null=True)
    #end_time = models.DateTimeField(auto_now_add=False, null=True)
    extraction_kit = models.ForeignKey(ExtractionKit, null=True, on_delete=models.CASCADE)
    #status = models.CharField(max_length=10, choices=EXT_EVENT_CHOICES, blank=True)
    machine = models.ForeignKey(ExtractionMachine, null=True, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.last_status_change()

    def last_status_change(self):
        return "{} {} at {}".format(self.machine, self.status, self.modified_time())   
    #def __str__(self):
    #    return "{} {} at {}".format(self.machine, self.status, self.modified_time())

    #def is_started(self):
    #    return self.status == "started"
    
    #def is_finished(self):
    #    return self.status == "finished"

    #def modified_time(self):
    #    try:
    #        return max(self.start_time, self.end_time)
    #    # If either of these times is Null, TypeError will be raised
    #    except TypeError:
    #        if self.end_time != None:
    #            return self.end_time
    #        elif self.start_time != None:
    #            return self.start_time
    #        else:
    #            return 0


class PcrMachine(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name



#class PcrEvent(models.Model):
class PcrEvent(Event):
    #sample_list = models.ManyToManyField(Sample)
    #start_time = models.DateTimeField(auto_now_add=True, null=True)
    #end_time = models.DateTimeField(auto_now_add=False, null=True)
    pcr_kit = models.ForeignKey(ExtractionKit, null=True, on_delete=models.CASCADE)
    amplified_target_pair = models.ForeignKey(PcrTargetPair, null=True, on_delete=models.CASCADE)
    machine = models.ForeignKey(PcrMachine, null=True, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.last_status_change()

    def last_status_change(self):
        return "{} {} at {}".format(self.machine, self.status, self.modified_time())

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
    media = models.FileField("Arquivo", upload_to="lab_use/media/",
                             storage=OverwriteStorage())
