"""
Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views import generic
from django.template import loader
from .forms import *
import csv
import io
import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage


def bulk_upload(request):
    """
    TODO
    """
    pass


def start(request):
    """Start page"""
    # Show all extractions and PCRs currently running"
    # Show also the extraction queue and PCR queue
    # Show also the latest N samples added to db
    active_extractions = ExtractionEvent.objects.filter(status='started')
    active_pcrs = PcrEvent.objects.filter(status='started')
    latest_samples = Sample.objects.order_by('-registration_date')
    high_prio_samples = Sample.objects.filter(high_priority=True)
    pcr_ready_samples = Sample.objects.filter(analysis_state='ready for pcr')
    return render(request, 'lab_use/status_panel.html', {
                                        'extractions': active_extractions,
                                        'pcrs': active_pcrs,
                                        'latest_samples': latest_samples,
                                        'prio_list': high_prio_samples,
                                        'pcr_queue': pcr_ready_samples,
                                        })

def add_sample(request):
    if request.method == 'POST':
        form = NewSampleForm(request.POST)
        if form.is_valid():
            form.save()
            this_sample = Sample.objects.last()
            this_id = this_sample.id
            return HttpResponseRedirect('/sample/{}/view/'.format(this_id))
    else:
        form = NewSampleForm()
    return render(request, 'lab_use/add_sample.html', {'form': form})

def view_all_samples(request):
    return HttpResponseRedirect('/admin/lab_use/sample/')

def view_sample(request, id):
    return HttpResponseRedirect('/admin/lab_use/sample/{}/'.format(id))

def get_extraction_queue():
    ready_for_extraction = Sample.objects.filter(
                                    analysis_state='ready for extraction')
    prioritized_list = ready_for_extraction.order_by('-high_priority', 
                                                     '-collect_date')
    return prioritized_list

def start_extraction(request):
    if request.method == 'POST':
        sample_id_list = [ int(key) for key, val in request.POST.items() 
                                                            if val == 'True' ]
        if len(sample_id_list) > 12:
            ## TODO: fail graciously if >12 samples given
            pass
        extraction = ExtractionEvent(start_time = datetime.datetime.now(),
                                     status = 'started')
        extraction.save()
        sample_list = [ Sample.objects.get(pk=i) for i in sample_id_list ]
        extraction.sample_list.add(*sample_list)
        extraction.save()
        for sample in sample_list:
            sample.extraction_state = 'started'
            sample.save()

        return HttpResponseRedirect(
                '/admin/lab_use/extractionevent/{}/change/'.format(extraction.pk))
    else:
        sample_list = get_extraction_queue()
        return render(request, 'lab_use/view_samples.html', {'sample_list': sample_list})

def choose_extraction_to_end(request):
    started_list = ExtractionEvent.objects.filter(status='started')
    return render(request, 'lab_use/choose_extraction_to_end.html', {'extraction_list': started_list})

def end_extraction(request, id):
    extraction = ExtractionEvent.objects.get(pk=id)
    samples_in_this_extraction = extraction.sample_list.all()
    
    if request.method == 'POST':
        
        successfully_extracted = [ key for key,value in request.POST.items() if
                                                              value == 'True' ]
        failed_extraction = [ samp for samp in samples_in_this_extraction if
                                        samp.pk not in successfully_extracted ]

        # Mark successfully extracted samples as such
        for sample_id in successfully_extracted:
            sample = Sample.objects.get(pk=sample_id)
            sample.extraction_state = 'finished'
            sample.pcr_state = 'ready for pcr'
            sample.save()
        
        extraction.status = 'finished'
        extraction.end_time = datetime.datetime.now()
        extraction.save()

    else:
        return render(request, 'lab_use/end_extraction.html', 
                                                    {'extraction': extraction})

def view_extraction(request, id):
    return HttpResponseRedirect('/admin/lab_use/extractionevent/{}/'.format(id))
   

def get_pcr_queue():
    ready_for_pcr = Sample.objects.filter(pcr_state='ready for pcr')
    prioritized_list = ready_for_pcr.order_by('-high_priority', 
                                                '-collect_date')
    return prioritized_list


def start_pcr(request):
    if request.method == 'POST':
        sample_id_list = [ int(key) for key, val in request.POST.items() 
                                                            if val == 'True' ]
        pcr = PcrEvent(start_time = datetime.datetime.now(), status = 'started')
        pcr.save()
        sample_list = [ Sample.objects.get(pk=i) for i in sample_id_list ]
        pcr.sample_list.add(*sample_list)
        pcr.save()
    
        return HttpResponseRedirect(
                '/admin/lab_use/pcrevent/{}/change/'.format(pcr.pk))
    else:
        sample_list = get_pcr_queue()
        return render(request, 'lab_use/view_samples.html', {'sample_list': sample_list})


def end_pcr(request, pcr_id = id):
    pass

def view_pcr(request, pcr_id = id):
    pass

















def process_sheet(f):
    """
    TODO
    """
    fcontents = f.read().decode('utf-8')
    infile = io.StringIO(fcontents)
    reader = csv.DictReader(infile, dialect='excel')

    header_field_map = {
        # csv : model
        'Instituição': 'institution',
        'Data de recebimento': 'sample_receive_date',
        'Número de registro': 'sample_id',
        'CPF': 'patient_unique_id',
        'Nome': 'patient_full_name',
        'Data de Nascimento': 'patient_birthday',
        'Data da coleta': 'sample_date',
        'Material coletado': 'sample_types',
        'Data do início dos sintomas': 'symptoms_start_date',
        'Equipe extração': 'extraction_team',
        'Kit extração': 'extraction_kit',
        'Equipe PCR': 'pcr_team',
        'Máquina PCR': 'pcr_equipment',
        'Resultado': 'result',
        'Conclusão': 'conclusion',
        'Observação': 'notes',
    }

    for row in reader:
        # ret_list.append(row)
        new_result = ExamResult()
        for k, v in row.items():
            new_key = header_field_map[k]
            if new_key == 'sample_types':
                new_value = []
                for sub_value in v.split('/'):
                    new_sub_value = SampleType.objects.get_or_create(name=sub_value)[0]
                    # Adding sample_types can only be done once new_result has
                    # been committed to the DB and has an ID.
                    # new_result.sample_types.add(new_value)
                    new_value.append(new_sub_value)
                    add_after_save = True
            elif new_key == 'institution':
                inst = Institution.objects.get_or_create(short_name=v)
                new_result.institution = inst[0]
            elif 'day' in new_key or 'date' in new_key:
                # If the last 4 characters are digits, then the format is
                # DD-MM-YYYY and we need to reverse it.
                if v[-4:].isdigit():
                    # D-M-Y  -->  Y-M-D
                    # we need to split by '-', then reverse, then join by '-':
                    d_m_y = v.split('-')
                    y_m_d = d_m_y.copy()
                    y_m_d.reverse()
                    y_m_d = '-'.join(y_m_d)
                    new_result.__dict__[new_key] = y_m_d
                else:
                    new_result.__dict__[new_key] = v
            else:
                new_result.__dict__[new_key] = v

        new_result.save()
        if add_after_save:
            add_after_save = False
            for val in new_value:
                new_result.sample_types.add(val)

    return new_result.__dict__


def sheet_upload(request):
    """Offer a csv file upload dialog."""

    if request.method == 'POST':
        form = UploadSheetForm(request.POST, request.FILES)
        if form.is_valid():
            csv_contents = process_sheet(request.FILES['planilha'])
            return render(request, 'lab_use/show_data.html', {'data': csv_contents})
            return HttpResponseRedirect('/successful_upload/')
    else:
        form = UploadSheetForm()
    return render(request, 'lab_use/sheet_upload.html', {'form': form})



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
    sorted_results = ExamResult.objects.order_by('-result_date')
    results_institutions = [r.institution for r in sorted_results]
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
    # return HttpResponse('running new_result')

# def new_institution(request):
#     """Creates new institution with POST data, renders new_result template"""
#     full_name = request.POST['full_name']
#     short_name = request.POST['short_name']
#     city = request.POST['city']
#     state = request.POST['state']
#     i = Institution(full_name=full_name,
#                     short_name=short_name,
#                     city=city,
#                     state=state)
#     i.save()
#     context = {
#                 'institution': i.id,
#     }
#     #return render(request, 'lab_use/new_result.html', context)
#     return redirect('/new_result/{}'.format(i.id))


def report(request):
    """
    TODO
    """
    pass
    # all_results = ExamResult.objects.order_by('-exam_date')
    # latest_five_results = [ (r.patient_full_name, r.result, r.exam_date) for r in all_results ][:5]
    # context = {
    #         'latest_five_results': latest_five_results,
    # }
    # return render(request, 'lab_use/report.html', context)


def commit_result(request):
    """
    TODO
    """
    pass
    # institution = get_object_or_404(Institution,
    #                                 pk=request.POST['institution_id'])
    # if '' in request.POST.values():
    #     pass
    # r = ExamResult( #patient_id = request.POST['patient_id'],
    #                 institution = institution,
    #                 sample_received = request.POST['sample_received'],
    #                 sample_id = request.POST['sample_id'],
    #                 resykt = request.POST['result'],
    #                 exam_date = request.POST['exam_date'],
    #                 result_submitted = False)
    # r.save()
    # #return render(request, 'lab_use/new_result.html')
    # return redirect('/new_result/')

# class IndexView(generic.ListView):
#     template_name = 'lab_use/latest_results.html'
#     context_object_name = 'result_list'

#     def get_queryset(self):
#         """Return the last 10 submitted results."""
#         return ExamResult.objects.order_by('-exam_date')[:10]


def result_view(request):
    """
    TODO
    """
    return render(request, 'lab_use/new_result.html')
    # return HttpResponse('running new_result')

# def report_view(request):
#     all_results = ExamResult.objects.order_by('-exam_date')
#     latest_five_results = [ (r.patient_full_name, r.exam_result, r.exam_date) for r in all_results ][:5]
#     context = {
#             'latest_five_results': latest_five_results,
#             'all_results': all_results,
#     }
#     return render(request, 'lab_use/report.html', context)


def report_view(request):
    """
    TODO
    """
    query_set = ExamResult.objects.all()
    context = {
        'object_list': query_set
    }
    return render(request, 'lab_use/report.html', context)


def home_view(request):
    """
    TODO
    """
    context = {}
    return render(request, 'lab_use/home.html', context)


def upload_view(request):
    """
    TODO
    """
    context = {}
    return render(request, 'lab_use/upload.html', context)


def resend_view(request):
    """
    TODO
    """
    query_set = ExamResult.objects.all()
    context = {
        'object_list': query_set
    }
    return render(request, 'lab_use/resend.html', context)


def pdf_generate_view(request, id):
    """
    TODO
    """
    query_set = ExamResult.objects.get(id=id)
    context = {
        'object_list': query_set
    }
    return render(request, 'lab_use/pdf_generate.html', context)


def upload_view(request):
    """
    TODO
    """
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'lab_use/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'lab_use/upload.html')
