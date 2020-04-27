from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import *
#from .models import (
#    ExamResult, SampleType,
#    State, City, Laboratory,
#    ExtractionTeam, PcrTeam
#)

#admin.site.register(SampleType)

PER_PAGE = 20

class StateAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name')
    ordering = ['name']
    search_fields = ['name', 'short_name']
    list_per_page = PER_PAGE
    list_display = ('name', 'short_name', 'created')


admin.site.register(State, StateAdmin)


class CityAdmin(admin.ModelAdmin):
    fields = ('name', 'state')
    ordering = ['name']
    search_fields = ['name', 'state__name']
    list_per_page = PER_PAGE
    list_display = ('name', 'state', 'created')


admin.site.register(City, CityAdmin)


class LaboratoryAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name', 'email', 'city')
    ordering = ['name']
    search_fields = ['name', 'city__name', 'city__state__name']
    # raw_id_fields = ['state']
    list_per_page = PER_PAGE
    list_display = ('name', 'short_name', 'city', 'email', 'state', 'created')
    # list_filter = ['city__state']
    list_filter = ['city__state']


admin.site.register(Laboratory, LaboratoryAdmin)


#class ExamResultAdmin(admin.ModelAdmin):
#    fields = ('send_report', 'priority',
#              'is_blood', 'is_swab', 'is_lavado', 'lab',
#              'sample_received', 'sample_id', 'patient_id',
#              'patient_full_name', 'dob_date', 'exam_date',
#              'beginning_symptoms',
#              'extraction_team', 'extraction_kit', 'pcr_team',
#              'pcr_machine', 'exam_result', 'conclusion',
#              'result_target_P2', 'result_target_E', 'result_target_RP',
#              'result_target_N1', 'result_target_N2', 'obs'
#             )
#    list_per_page = PER_PAGE
#    list_display = ('lab', 'send_report', 'priority', 'sample_id',
#                    'patient_full_name', 'exam_result'
#                   )
#    search_fields = ['patient_full_name']
#    list_filter = ['lab', 'priority', 'send_report',
#                   'exam_result', 'extraction_team', 'pcr_team',
#                   'is_blood', 'is_swab', 'is_lavado'
#                  ]


#admin.site.register(ExamResult, ExamResultAdmin)


class ExtractionTeamAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name')
    list_display = ('name', 'short_name', 'created')
    list_per_page = PER_PAGE
    list_filter = ['name', 'short_name']


#admin.site.register(ExtractionTeam, ExtractionTeamAdmin)


class PcrTeamAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name')
    list_display = ('name', 'short_name', 'created')
    list_per_page = PER_PAGE
    list_filter = ['name', 'short_name']


#admin.site.register(PcrTeam, PcrTeamAdmin)

class PatientInline(admin.TabularInline):
    model = Patient
    

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    filter_horizontal = ('symptom_list',)
    fieldsets = (
        ('Amostra', {
            'fields': ('high_priority', ('sample_id', 'sample_type', 'registration_date'), 'origin', 'collect_date'),
        }),
        ('Análise', {
            'fields': ('analysis_state',),
        }),
        ('Dados clínicos', {
            'fields': ('patient', 'symptoms_start_date', 'symptom_list'),
        }),
        ('PCR', {
            'fields': ('pcr_target_pair', 'result'),
        }),

    )

#class SampleInline(admin.TabularInline):
#    model = Sample

#class ExtractionEventAdmin(admin.ModelAdmin):
#    inlines = [
#        SampleInline,
#    ]
#admin.site.register(ExtractionEvent, ExtractionEventAdmin)


class SymptomAdmin(admin.ModelAdmin):
    pass
admin.site.register(Symptom, SymptomAdmin)

class ResultAdmin(admin.ModelAdmin):
    pass
admin.site.register(Result, ResultAdmin)

class PcrTargetPairAdmin(admin.ModelAdmin):
    pass
admin.site.register(PcrTargetPair, PcrTargetPairAdmin)

class ExtractionKitAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExtractionKit, ExtractionKitAdmin)

class PcrKitAdmin(admin.ModelAdmin):
    pass
admin.site.register(PcrKit, PcrKitAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class SampleTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(SampleType, SampleTypeAdmin)

class ExtractionEventAdmin(admin.ModelAdmin):
    filter_horizontal = ('sample_list',)
    fields = (
        ('sample_list',),
        ('start_time', 'end_time',),
        ('extraction_kit', 'machine',),
        ('status',),
    )
admin.site.register(ExtractionEvent, ExtractionEventAdmin)

class ExtractionTeamMemberAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExtractionTeamMember, ExtractionTeamMemberAdmin)

class PcrTeamMemberAdmin(admin.ModelAdmin):
    pass
admin.site.register(PcrTeamMember, PcrTeamMemberAdmin)

class EventAdmin(admin.ModelAdmin):
    pass
admin.site.register(Event, EventAdmin)

#class PcrQueueAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(PcrQueue, PcrQueueAdmin)

class ExtractionQueueAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExtractionQueue, ExtractionQueueAdmin)

class ExtractionMachineAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExtractionMachine, ExtractionMachineAdmin)


class PcrEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(PcrEvent, PcrEventAdmin)


