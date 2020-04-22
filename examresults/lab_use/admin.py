from django.utils.translation import gettext_lazy as _
from django.contrib import admin
# from .models import (
#     ExamResult, SampleType,
#     State, City, Laboratory,
#     ExtractionTeam, PcrTeam
# )

# admin.site.register(SampleType)

from .models import (
    Paciente, Estado, Cidade, Laboratorio,
    TipoExtracao, KitExtracao, MaqExtracao, Extracao, ResultadoExtracao,
    TipoAlvo, MaqPcr, Pcr, ResultadoPcr,
    TipoAmostra, Amostra, Sintoma,
    LabEmail,
    Question, Answer
)

class Answer1TabularInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [Answer1TabularInline]
    class Meta:
        model = Question

admin.site.register(Question, QuestionAdmin)

admin.site.register(Sintoma)

admin.site.register(Answer)

PER_PAGE = 20


class pcrInline(admin.TabularInline):
    model = Pcr
    # extra

class resultado_pcrAdmin(admin.ModelAdmin):
    inlines = [
        pcrInline,
    ]


admin.site.register(LabEmail)


admin.site.register(TipoAmostra)
admin.site.register(Amostra)

admin.site.register(TipoAlvo)
admin.site.register(MaqPcr)
admin.site.register(Pcr)
admin.site.register(ResultadoPcr)



admin.site.register(TipoExtracao)
admin.site.register(KitExtracao)
admin.site.register(MaqExtracao)

# class resultado_extracaoTabularInline(admin.TabularInline):
#     model = resultado_extracao


# class ExtracaoTabularInline(admin.TabularInline):
#     model = extracao

class ResultadoExtracaoAdmin(admin.ModelAdmin):
    # inlines = [ExtracaoTabularInline]
    # class Meta:
    #     model = resultado_extracao

    fields = ('amostra', 'extracao', 'resultado')
    list_display = ('amostra', 'extracao', 'resultado')
    list_filter = ['amostra', 'extracao', 'resultado']
    # inlines = [resultado_extracaoTabularInline]

    # class Meta:
    #     model = amostra

admin.site.register(ResultadoExtracao, ResultadoExtracaoAdmin)



class extracaoAdmin(admin.ModelAdmin):
    fields = ('nome_da_lista', 'tipo_extracao', 'kit_extracao',
              'maq_extracao',)
    ordering = ['nome_da_lista', 'tipo_extracao', 'kit_extracao',
                'maq_extracao']
    search_fields = ['nome', 'email', 'cpf', 'dt_nascimento']
    list_per_page = PER_PAGE
    # list_display = ('nome', 'email', 'cpf', 'dt_nascimento')
    list_display = ('nome_da_lista', 'tipo_extracao', 'kit_extracao',
              'maq_extracao', 'dt_criacao')

    # class Meta:
    #     model = amostra

admin.site.register(Extracao, extracaoAdmin)





class pacienteAdmin(admin.ModelAdmin):
    fields = ('nome', 'email', 'cpf', 'dt_nascimento')
    ordering = ['nome']
    search_fields = ['nome', 'email', 'cpf', 'dt_nascimento']
    list_per_page = PER_PAGE
    list_display = ('nome', 'email', 'cpf', 'dt_nascimento')
    # list_filter = ['nome', 'email', 'cpf', 'dt_nascimento']


admin.site.register(Paciente, pacienteAdmin)




# -----------------

class estadoAdmin(admin.ModelAdmin):
    fields = ('nome', 'sigla')
    ordering = ['nome']
    search_fields = ['nome', 'sigla']
    list_per_page = PER_PAGE
    list_display = ('nome', 'sigla', 'dt_criacao')

admin.site.register(Estado, estadoAdmin)


class cidadeAdmin(admin.ModelAdmin):
    fields = ('nome', 'estado')
    ordering = ['nome']
    search_fields = ['nome', 'estado__nome']
    list_per_page = PER_PAGE
    list_display = ('nome', 'estado', 'dt_criacao')

admin.site.register(Cidade, cidadeAdmin)


class laboratorioAdmin(admin.ModelAdmin):
    fields = ('nome', 'sigla', 'email', 'cidade')
    ordering = ['nome']
    # search_fields = ['nome', 'city__name', 'city__state__name']
    search_fields = ['nome']
    # raw_id_fields = ['state']
    list_per_page = PER_PAGE
    # list_display = ('nome', 'sigla', 'cidade', 'estado', 'dt_criacao')
    list_display = ('nome', 'sigla', 'email', 'cidade', 'dt_criacao')
    # list_filter = ['city__state']
    # list_filter = ['city__state']

admin.site.register(Laboratorio, laboratorioAdmin)


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


# admin.site.register(ExamResult, ExamResultAdmin)


class ExtractionTeamAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name')
    list_display = ('name', 'short_name', 'created')
    list_per_page = PER_PAGE
    list_filter = ['name', 'short_name']


# admin.site.register(ExtractionTeam, ExtractionTeamAdmin)


class PcrTeamAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name')
    list_display = ('name', 'short_name', 'created')
    list_per_page = PER_PAGE
    list_filter = ['name', 'short_name']


# admin.site.register(PcrTeam, PcrTeamAdmin)
