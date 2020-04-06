from django.shortcuts import render, get_object_or_404, redirect
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

def bulk_upload(request):
    pass


def new_result_with_url(request, institution_id):
    """Renders the new_result template, passes institution from URL"""
    institution = get_object_or_404(Institution, pk=institution_id)
    context = {
                'institution': institution,
    }
    return render(request, 'lab_use/new_result.html', context)

def new_result_with_post(request):
    """Renders the new_result template, passes institution from POST"""
    institution_id = request.POST['institution_id']
    institution = get_object_or_404(Institution, pk=institution_id)
    context = {
                'institution': institution,
    }
    return render(request, 'lab_use/new_result.html', context)

def new_result(request):
    """Renders the new_result template, shows institution picker"""
    sorted_results = ExamResult.objects.order_by('-exam_date')
    results_institutions = [ r.institution for r in sorted_results ]
    latest_institutions = []
    for inst in results_institutions:
        if inst not in latest_institutions:
            latest_institutions.append(inst)
            if len(latest_institutions) > 9:
                break

    all_institutions = Institution.objects.all()

    context = {
            'latest_institutions': latest_institutions,
            'all_institutions': all_institutions,
    }
    return render(request, 'lab_use/choose_institution.html', context)
    #return HttpResponse('running new_result')

def new_institution(request):
    """Creates new institution with POST data, renders new_result template"""
    full_name = request.POST['full_name']
    short_name = request.POST['short_name']
    city = request.POST['city']
    state = request.POST['state']
    i = Institution(full_name=full_name,
                    short_name=short_name,
                    city=city,
                    state=state)
    i.save()
    context = {
                'institution': i.id,
    }
    #return render(request, 'lab_use/new_result.html', context)
    return redirect('/new_result/{}'.format(i.id))

def report(request):
    all_results = ExamResult.objects.order_by('-exam_date')
    latest_five_results = [ (r.patient_full_name, r.exam_result, r.exam_date) for r in all_results ][:5]
    context = {
            'latest_five_results': latest_five_results,
    }
    return render(request, 'lab_use/report.html', context)

def commit_result(request):
    institution = get_object_or_404(Institution,
                                    pk=request.POST['institution_id'])
    if '' in request.POST.values():
        pass
    r = ExamResult( #patient_id = request.POST['patient_id'],
                    institution = institution,
                    sample_received = request.POST['sample_received'],
                    sample_id = request.POST['sample_id'],
                    exam_result = request.POST['exam_result'],
                    exam_date = request.POST['exam_date'],
                    result_submitted = False)
    r.save()
    #return render(request, 'lab_use/new_result.html')
    return redirect('/new_result/')
