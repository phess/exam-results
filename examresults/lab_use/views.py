from django.shortcuts import render
from django.http import HttpResponse
from .models import ExamResult, Institution
from django.views import generic
from django.template import loader

class IndexView(generic.ListView):
    template_name = 'lab_use/latest_results.html'
    context_object_name = 'result_list'

    def get_queryset(self):
        """Return the last 10 submitted results."""
        return ExamResult.objects.order_by('-exam_date')[:10]

def new_result(request):
    return render(request, 'lab_use/new_result.html')
    #return HttpResponse('running new_result')

def report(request):
    all_results = ExamResult.objects.order_by('-exam_date')
    latest_five_results = [ (r.patient_full_name, r.exam_result, r.exam_date) for r in all_results ][:5]
    context = {
            'latest_five_results': latest_five_results,
    }
    return render(request, 'lab_use/report.html', context)
