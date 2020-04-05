from django.shortcuts import render
from django.http import HttpResponse
from .models import ExamResult, Institution
from django.template import loader

def new_result(request):
    return HttpResponse('running new_result')

def report(request):
    all_results = ExamResult.objects.order_by('-exam_date')
    latest_five_results = [ (r.patient_full_name, r.exam_result, r.exam_date) for r in all_results ][:5]
    context = {
            'latest_five_results': latest_five_results,
    }
    return render(request, 'lab_use/report.html', context)
