from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import (
    ExamResult, SampleType,
    State, City, Laboratory,
    ExtractionTeam, PcrTeam
)

admin.site.register(SampleType)

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


class ExamResultAdmin(admin.ModelAdmin):
    fields = ('send_report', 'priority',
              'is_blood', 'is_swab', 'is_lavado', 'lab',
              'sample_received', 'sample_id', 'patient_id',
              'patient_full_name', 'dob_date', 'exam_date',
              'beginning_symptoms',
              'extraction_team', 'extraction_kit', 'pcr_team',
              'pcr_machine', 'exam_result', 'conclusion',
              'result_target_P2', 'result_target_E', 'result_target_RP',
              'result_target_N1', 'result_target_N2', 'obs'
             )
    list_per_page = PER_PAGE
    list_display = ('lab', 'send_report', 'priority', 'sample_id',
                    'patient_full_name', 'exam_result'
                   )
    search_fields = ['patient_full_name']
    list_filter = ['lab', 'priority', 'send_report',
                   'exam_result', 'extraction_team', 'pcr_team',
                   'is_blood', 'is_swab', 'is_lavado'
                  ]


admin.site.register(ExamResult, ExamResultAdmin)


class ExtractionTeamAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name')
    list_display = ('name', 'short_name', 'created')
    list_per_page = PER_PAGE
    list_filter = ['name', 'short_name']


admin.site.register(ExtractionTeam, ExtractionTeamAdmin)


class PcrTeamAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name')
    list_display = ('name', 'short_name', 'created')
    list_per_page = PER_PAGE
    list_filter = ['name', 'short_name']


admin.site.register(PcrTeam, PcrTeamAdmin)
