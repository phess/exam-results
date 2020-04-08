from django.contrib import admin
from .models import ExamResult, Institution, SampleType

admin.site.register(ExamResult)
admin.site.register(Institution)
admin.site.register(SampleType)
