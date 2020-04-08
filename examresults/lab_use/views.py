from django.shortcuts import render
from django.http import HttpResponse
from .models import ExamResult, Institution
from django.views import generic
from django.template import loader

from django.conf import settings
from django.core.files.storage import FileSystemStorage

# class IndexView(generic.ListView):
#     template_name = 'lab_use/latest_results.html'
#     context_object_name = 'result_list'

#     def get_queryset(self):
#         """Return the last 10 submitted results."""
#         return ExamResult.objects.order_by('-exam_date')[:10]

def result_view(request):
    return render(request, 'lab_use/new_result.html')
    #return HttpResponse('running new_result')

# def report_view(request):
#     all_results = ExamResult.objects.order_by('-exam_date')
#     latest_five_results = [ (r.patient_full_name, r.exam_result, r.exam_date) for r in all_results ][:5]
#     context = {
#             'latest_five_results': latest_five_results,
#             'all_results': all_results,
#     }
#     return render(request, 'lab_use/report.html', context)

def report_view(request):
    query_set = ExamResult.objects.all()
    context = {
            'object_list': query_set
    }
    return render(request, 'lab_use/report.html', context)

def home_view(request):
    context = {}
    return render(request,'lab_use/home.html', context)

def upload_view(request):
    context={}
    return render(request,'lab_use/upload.html', context)

def resend_view(request):
    query_set = ExamResult.objects.all()
    context = {
            'object_list': query_set
    }
    return render(request,'lab_use/resend.html', context)

def pdf_generate_view(request, id):
    query_set = ExamResult.objects.get(id=id)
    context = {
            'object_list': query_set
    }
    return render(request,'lab_use/pdf_generate.html', context)


def upload_view(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'lab_use/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'lab_use/upload.html')