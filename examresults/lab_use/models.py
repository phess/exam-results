# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    text = models.TextField()
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:10]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    new_field = models.CharField(max_length=50)

    def __str__(self):
        return self.text[:10]



class Estado(models.Model):
    nome = models.CharField(_('Estado'), max_length=50, db_index=True,
                            help_text=_('Defina o Estado'))
    sigla = models.CharField(_('Sigla'), max_length=5,
                                  db_index=True,
                                  help_text=_('Sigla do Estado'))
    dt_criacao = models.DateTimeField(_('Criado em'), auto_now_add=True)

    def __str__(self):
        return self.nome

#     class Meta:
#         verbose_name = _('State')
#         verbose_name_plural = _('States')
#         ordering = ['name']


class Cidade(models.Model):
    estado = models.ForeignKey(Estado, related_name='estado',
                              on_delete=models.CASCADE)
    nome = models.CharField(_('Cidade'), max_length=100, db_index=True,
                            help_text=_('Informe o nome da cidade'))
    dt_criacao = models.DateTimeField(_('Criado em'), auto_now_add=True)

    def __str__(self):
        return f'{self.nome}, {self.estado.sigla}'


#     class Meta:
#         verbose_name = _('City')
#         verbose_name_plural = _('Cities')
#         ordering = ['name']
#         unique_together = ('name', 'state')


class LabEmail(models.Model):
    email = models.CharField(_('Email'), max_length=100, db_index=True,
                            help_text=_('Informe o email'))

    def __str__(self):
        return f'{self.email}'
    

class Laboratorio(models.Model):
    RESULT_CHOICES = (
        ('positive', 'POS'),
        ('negative', 'NEG'),
        ('indetermined', 'IND'),
)
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=15)    
 
    email = models.CharField(max_length=100, blank=True)

    # email = MultiSelectField(choices = RESULT_CHOICES)

    # email = MultiSelectField(choices = models.ForeignKey(lab_email,
    #                                    on_delete=models.CASCADE,
    #                                    help_text=_('Email')))

    # email = models.ForeignKey(lab_email,
    #                          on_delete=models.CASCADE,
    #                          help_text=_('Email'))




    cidade = models.ForeignKey(Cidade, related_name='cidade',
                             on_delete=models.CASCADE,
                             help_text=_('Nome da Cidade'))
    dt_criacao = models.DateTimeField(_('Criado em'), auto_now_add=True)

    def __str__(self):
        return f'{self.nome},{self.sigla}'
    

    # modified = models.DateTimeField(_('Created at'), auto_now=True)

#     def state(self):
#         return self.city.state

#     def __str__(self):
#         return f'{self.name}'

#     # def save(self):
#     #    self.short_name = self.short_name + 'waldirio'
#     #    super(Laboratory, self).save()

#     @property
#     def status(self):
#         return True

#     @status.setter
#     def status(self, value):
#         self.short_name = value
#         self.save()

#     # def generate_report(self):
#     #     print("oi")

#     class Meta:
#         verbose_name = _('Laboratory')
#         verbose_name_plural = _('Laboratories')
#         ordering = ['name']



# Inicio Paciente

class Paciente(models.Model):
    nome = models.CharField(_('Nome'), max_length=50, db_index=True,
                            help_text=_('Nome do Paciente'), blank=True)
    email = models.CharField(_('Email'), max_length=50, db_index=True,
                            help_text=_('Email do Paciente'), blank=True)
    cpf = models.CharField(_('CPF'), max_length=50, db_index=True,
                            help_text=_('CPF do Paciente'), blank=True)
    dt_nascimento = models.DateField(_('Data de Nascimento'), max_length=50, db_index=True,
                            help_text=_('Data de Nascimento do Paciente'), blank=True, null=True)

    def __str__(self):
        return f'{self.nome}, {self.cpf}'
    

# Fim Paciente






# Inicio Amostra

class TipoAmostra(models.Model):
    nome = models.CharField(_('Tipo de Amostra'), max_length=50, db_index=True,
                            help_text=_('Tipo de Amostra'), blank=True, null=True)

    sigla = models.CharField(_('Sigla da Amostra'), max_length=50, db_index=True,
                            help_text=_('Sigla da Amostra'), blank=True, null=True)

    def __str__(self):
        return f'{self.nome}, {self.sigla}'

class Sintoma(models.Model):
    nome = models.CharField(_('Sintoma'), max_length=50, db_index=True,
                            help_text=_('Tipo de Sintoma'), blank=True, null=True)

    # status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome}' 


class Amostra(models.Model):
    # cod_amostra = models.CharField(_('Código da Amostra'), max_length=50, db_index=True,
    #                         help_text=_('Código da Amostra'), primary_key=True)

    cod_amostra = models.AutoField(primary_key=True)

    paciente = models.ForeignKey(Paciente,
                             on_delete=models.CASCADE,
                             help_text=_('Paciente'))

    tipo_amostra = models.ForeignKey(TipoAmostra,
                             on_delete=models.CASCADE,
                             help_text=_('Tipo de Amostra'))

    laboratorio = models.ForeignKey(Laboratorio,
                             on_delete=models.CASCADE,
                             help_text=_('Laboratorio'))


    dt_coleta = models.DateField(_('Data da Coleta'), blank=True, null=True)
    dt_inicial_sintoma = models.DateField(_('Data Inicial dos Sintomas'), blank=True, null=True)

    descricao = models.CharField(_('Descrição'), max_length=50, db_index=True,
                            help_text=_('Descrição'), blank=True, null=True)


    # febre = models.BooleanField(default=False)
    # tosse = models.BooleanField(default=False)
    # dor_de_garganta = models.BooleanField(default=False)
    # dispneia = models.BooleanField(default=False)
    # desconforto_respiratorio = models.BooleanField(default=False)
    # saturacao_95 = models.BooleanField(default=False)
    # diarreia = models.BooleanField(default=False)
    # vomito = models.BooleanField(default=False)

    sintoma = models.ManyToManyField(Sintoma,
                             related_name='amostra_sintoma',
                             verbose_name='Sintoma do paciente',
                             help_text=_('Sintoma'),
                             blank=True)

    resultado = models.CharField(_('Resultado'), max_length=50, db_index=True,
                            help_text=_('Resultado'), blank=True, null=True)

    dt_criacao = models.DateField(_('Criado em'), auto_now_add=True, null=True)
    
    extraido = models.BooleanField(_('Extraído com sucesso'), default=False)
    amplificado = models.BooleanField(_('PCR finalizado'), default=False)





    def __str__(self):
        return f'{self.cod_amostra}{self.tipo_amostra.sigla}'
    






# Fim Amostra



# # Inicio PCR

# class TipoAlvo(models.Model):
#     sigla = models.CharField(_('Tipo do Alvo'), max_length=50, db_index=True,
#                             help_text=_('Tipo do Alvo'), blank=True, null=True)

#     descricao = models.CharField(_('Descrição do Alvo'), max_length=50, db_index=True,
#                             help_text=_('Descrição do Alvo'), blank=True, null=True)


#     def __str__(self):
#         return f'{self.sigla},{self.descricao}'
    

# class MaqPcr(models.Model):
#     nome = models.CharField(_('Termociclador'), max_length=50, db_index=True,
#                             help_text=_('Termociclador'), blank=True, null=True)

#     def __str__(self):
#         return f'{self.nome}'

# # class resultado_pcr(models.Model):

# class ResultadoPcr(models.Model):
#     amostra = models.ForeignKey(Amostra,
#                              on_delete=models.CASCADE,
#                              help_text=_('Amostra'))


#     resultado = models.CharField(_('Resultado do PCR'), max_length=50, db_index=True,
#                             help_text=_('Resultado do PCR'), blank=True)
    
#     def __str__(self):
#         return "Amostras Aqui"


# class Pcr(models.Model):
#     nome_da_tabela = models.CharField(_('Tabela do PCR'), max_length=50, db_index=True,
#                             help_text=_('Tabela do PCR'))

#     dt_criacao = models.DateTimeField(_('Criado em'), auto_now_add=True)

#     primeiro_alvo = models.ForeignKey(TipoAlvo, related_name='primeiro_alvo',
#                              on_delete=models.CASCADE,
#                              help_text=_('Primeiro Alvo'))

#     segundo_alvo = models.ForeignKey(TipoAlvo, related_name='segundo_alvo',
#                              on_delete=models.CASCADE,
#                              help_text=_('Segungo Alvo'))

#     maq_pcr = models.ForeignKey(MaqPcr,
#                              on_delete=models.CASCADE,
#                              help_text=_('Máquina do PCR'))

#     resultado = models.ForeignKey(ResultadoPcr,
#                              on_delete=models.CASCADE,
#                              help_text=_('Resultado do PCR'))

#     def __str__(self):
#         return f'{self.nome_da_tabela}'
    

# # Fim PCR


# Inicio PCR

class TipoAlvo(models.Model):
    sigla = models.CharField(_('Tipo do Alvo'), max_length=50, db_index=True,
                            help_text=_('Tipo do Alvo'), blank=True, null=True)

    descricao = models.CharField(_('Descrição do Alvo'), max_length=50, db_index=True,
                            help_text=_('Descrição do Alvo'), blank=True, null=True)


    def __str__(self):
        return f'{self.sigla},{self.descricao}'


class MaqPcr(models.Model):
    nome = models.CharField(_('Termociclador'), max_length=50, db_index=True,
                            help_text=_('Termociclador'), blank=True, null=True)

    def __str__(self):
        return f'{self.nome}'

    

class Pcr(models.Model):
    nome_da_tabela = models.CharField(_('Nome da Tabela PCR'), max_length=50, db_index=True,
                            help_text=_('Nome da Tabela PCR'))

    dt_criacao = models.DateTimeField(_('Criado em'), auto_now_add=True)

    # amostra = model.ManyToManyField()
    amostra = models.ManyToManyField(Amostra,
                             related_name='pcr_resultadoextracao',
                             verbose_name='ResultadoExtracao',
                             help_text=_('ResultadoExtracao'))    

    tipo_alvo_1 = models.ForeignKey(TipoAlvo,
                             related_name='tipo_alvo_1',
                             on_delete=models.CASCADE,
                             help_text=_('Primeiro Alvo'))

    tipo_alvo_2 = models.ForeignKey(TipoAlvo,
                             related_name='tipo_alvo_2',
                             on_delete=models.CASCADE,
                             help_text=_('Segundo Alvo'))


    maq_pcr = models.ForeignKey(MaqPcr,
                             on_delete=models.CASCADE,
                             help_text=_('Termociclador'))

    # resultado_extracao = models.ForeignKey('resultado_extracao', related_name='resultado_aux',
    #                          on_delete=models.CASCADE,
    #                          help_text=_('Resultado da Extracao'))

    def __str__(self):
        return f'{self.nome_da_tabela}'



class ResultadoPcr(models.Model):
    amostra = models.ForeignKey(Amostra,
                             on_delete=models.CASCADE,
                             help_text=_('Amostra da Extracao'))

    # extracao = models.ForeignKey(Extracao,related_name='extracao',
    #                          on_delete=models.CASCADE,
    #                          help_text=_('Extracao'))

    resultado_n1 = models.CharField(_('Resultado do primeiro alvo'), max_length=50, db_index=True,
                            help_text=_('Resultado do primeiro alvo'), blank=True)

    resultado_n2 = models.CharField(_('Resultado do segundo alvo'), max_length=50, db_index=True,
                            help_text=_('Resultado do segundo alvo'), blank=True)

    resultado_rp = models.CharField(_('Resultado do RP'), max_length=50, db_index=True,
                            help_text=_('Resultado do RP'), blank=True)

    def __str__(self):
        return f'{self.id}'



# Fim PCR



# Inicio Extracao

class TipoExtracao(models.Model):
    tipo = models.CharField(_('Tipo de Extração'), max_length=50, db_index=True,
                            help_text=_('Tipo de Extração'), blank=True)

    def __str__(self):
        return f'{self.tipo}'
    

class KitExtracao(models.Model):
    nome = models.CharField(_('Kit de Extração'), max_length=50, db_index=True,
                            help_text=_('Kit de Extração'), blank=True, null=True)
    cod_kit = models.CharField(_('Código do Kit de Extração'), max_length=50, db_index=True,
                            help_text=_('Código do Kit de Extração'), blank=True, null=True)

    def __str__(self):
        return f'{self.nome}'


class MaqExtracao(models.Model):
    nome = models.CharField(_('Maquina de Extração'), max_length=50, db_index=True,
                            help_text=_('Maquina de Extração'), blank=True, null=True)

    def __str__(self):
        return f'{self.nome}'

    

class Extracao(models.Model):
    nome_da_lista = models.CharField(_('Lista de Extração'), max_length=50, db_index=True,
                            help_text=_('Lista de Extração'))

    dt_criacao = models.DateTimeField(_('Criado em'), auto_now_add=True)

    # amostra = model.ManyToManyField()
    amostra = models.ManyToManyField(Amostra,
                             related_name='extracao_amostra',
                             verbose_name='Amostra',
                             help_text=_('Amostra'))    

    tipo_extracao = models.ForeignKey(TipoExtracao,
                             on_delete=models.CASCADE,
                             help_text=_('Tipo de Extracao'))

    kit_extracao = models.ForeignKey(KitExtracao,
                             on_delete=models.CASCADE,
                             help_text=_('Kit de Extracao'))

    maq_extracao = models.ForeignKey(MaqExtracao,
                             on_delete=models.CASCADE,
                             help_text=_('Máquina de Extracao'))

    # resultado_extracao = models.ForeignKey('resultado_extracao', related_name='resultado_aux',
    #                          on_delete=models.CASCADE,
    #                          help_text=_('Resultado da Extracao'))

    def __str__(self):
        return f'{self.nome_da_lista}'
    


class ResultadoExtracao(models.Model):
    amostra = models.ForeignKey(Amostra,
                             on_delete=models.CASCADE,
                             help_text=_('Amostra'))

    extracao = models.ForeignKey(Extracao,related_name='extracao',
                             on_delete=models.CASCADE,
                             help_text=_('Extracao'))

    resultado = models.CharField(_('Resultado da Extração'), max_length=50, db_index=True,
                            help_text=_('Resultado da Extração'), blank=True)
    
    def __str__(self):
        return f'{self.id}'



# Fim Extracao



# Inicio <<>>
# Fim <<>>


# =======================================

# class tipo_amostra(models.Model):




# RESULT_CHOICES = (
#         ('positive', 'POS'),
#         ('negative', 'NEG'),
#         ('indetermined', 'IND'),
# )

# COLLECTED_MATERIAL = (
#         ('sangue', 'blood'),
#         ('swab', 'swab'),
#         ('lavado', 'lavado'),
# )


# class State(models.Model):
#     name = models.CharField(_('State'), max_length=50, db_index=True,
#                             help_text=_('Define the State'))
#     short_name = models.CharField(_('State Short Name'), max_length=5,
#                                   db_index=True,
#                                   help_text=_('State Short Name'))
#     created = models.DateTimeField(_('Created at'), auto_now_add=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = _('State')
#         verbose_name_plural = _('States')
#         ordering = ['name']


# class City(models.Model):
#     state = models.ForeignKey(State, related_name='state',
#                               on_delete=models.CASCADE)
#     name = models.CharField(_('City'), max_length=100, db_index=True,
#                             help_text=_('Define the City'))
#     created = models.DateTimeField(_('Created at'), auto_now_add=True)

#     def __str__(self):
#         return f'{self.name}, {self.state.short_name}'

#     class Meta:
#         verbose_name = _('City')
#         verbose_name_plural = _('Cities')
#         ordering = ['name']
#         unique_together = ('name', 'state')


# class Laboratory(models.Model):
#     short_name = models.SlugField(max_length=15)
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=100, blank=True)
#     city = models.ForeignKey(City, related_name='city',
#                              on_delete=models.CASCADE,
#                              help_text=_('Enter the city name'))
#     created = models.DateTimeField(_('Created at'), auto_now_add=True)
#     # modified = models.DateTimeField(_('Created at'), auto_now=True)

#     def state(self):
#         return self.city.state

#     def __str__(self):
#         return f'{self.name}'

#     # def save(self):
#     #    self.short_name = self.short_name + 'waldirio'
#     #    super(Laboratory, self).save()

#     @property
#     def status(self):
#         return True

#     @status.setter
#     def status(self, value):
#         self.short_name = value
#         self.save()

#     # def generate_report(self):
#     #     print("oi")

#     class Meta:
#         verbose_name = _('Laboratory')
#         verbose_name_plural = _('Laboratories')
#         ordering = ['name']


# class SampleType(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


# class ExtractionTeam(models.Model):
#     name = models.CharField(_('Team Name'), max_length=50, db_index=True,
#                             help_text=_('Define the Team Name'))
#     short_name = models.CharField(_('Team Short Name'), max_length=20,
#                                   db_index=True,
#                                   help_text=_('Team Short Name'))
#     created = models.DateTimeField(_('Created at'), auto_now_add=True)

#     def __str__(self):
#         return f'{self.name}'


# class PcrTeam(models.Model):
#     name = models.CharField(_('PCR Team Name'), max_length=50, db_index=True,
#                             help_text=_('Define the PCR Team Name'))
#     short_name = models.CharField(_('PCR Team Short Name'), max_length=20,
#                                   db_index=True,
#                                   help_text=_('PCR Team Short Name'))
#     created = models.DateTimeField(_('Created at'), auto_now_add=True)

#     def __str__(self):
#         return f'{self.name}'


# class ExamResult(models.Model):
#     send_report = models.BooleanField(default=False)
#     priority = models.BooleanField(default=False)
#     is_blood = models.BooleanField(default=False)
#     is_swab = models.BooleanField(default=False)
#     is_lavado = models.BooleanField(default=False)
#     lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
#     sample_received = models.DateField('date received')
#     sample_id = models.CharField(max_length=40)
#     patient_id = models.CharField(max_length=20)
#     patient_full_name = models.CharField(max_length=200)
#     dob_date = models.DateField('dob issued', auto_now_add=False, null=True)
#     exam_date = models.DateField('exam date', auto_now_add=False, null=True)
#     # collected_material = models.CharField(choices=COLLECTED_MATERIAL, max_length=30, null=True)
#     beginning_symptoms = models.DateField('beginning symptoms',
#                                           auto_now_add=False, null=True)

#     extraction_team = models.ForeignKey(ExtractionTeam,
#                                         on_delete=models.CASCADE,
#                                         blank=True, null=True)
#     extraction_kit = models.CharField(max_length=200, blank=True)

#     pcr_team = models.ForeignKey(PcrTeam, on_delete=models.CASCADE,
#                                  blank=True, null=True)
#     pcr_machine = models.CharField(max_length=200, blank=True)

#     result_target_E = models.CharField(max_length=20, blank=True)
#     result_target_P2 = models.CharField(max_length=20, blank=True)
#     result_target_N1 = models.CharField(max_length=20, blank=True)
#     result_target_N2 = models.CharField(max_length=20, blank=True)
#     result_target_RP = models.CharField(max_length=20, blank=True)

#     exam_result = models.CharField(choices=RESULT_CHOICES, max_length=30, blank=True)
#     conclusion = models.CharField(max_length=200, blank=True)
#     obs = models.CharField(max_length=800, blank=True)


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
