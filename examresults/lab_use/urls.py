"""
URL file to redirect all the requests
"""
# from django.urls import path, include
from django.urls import path
from . import views

app_name = 'lab_use'
urlpatterns = [
    path('', views.home_view),
    #path('home/', views.home_view),
    path('report/', views.report_view),
    #path('new_result/', views.result_view, name='add_result'),
    #path('upload/', views.upload_view),
    #path('resend/', views.resend_view),
    path('pdf_generate/', views.pdf_generate_view),
    path('pdf_generate/<int:id>/', views.pdf_generate_view),
    
    path('start/', views.start),
    path('sample/add/', views.add_sample),
    path('sample/<int:id>/view/', views.view_sample),
    path('sample/view_all/', views.view_all_samples),
    #path('extraction/list_samples/', views.ready_for_extraction),
    path('extraction/start/', views.start_extraction),
    path('extraction/end/', views.choose_extraction_to_end),
    path('extraction/<int:id>/end/', views.end_extraction),
    path('extraction/<int:id>/view/', views.view_extraction),
    path('pcr/start/', views.start_pcr),
    path('pcr/<int:id>/view/', views.view_pcr),
    path('pcr/<int:id>/end/', views.end_pcr),
]
