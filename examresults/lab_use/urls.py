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
    path('extraction/start/', views.start_extraction),
    path('extraction/end/<int:id>/', views.end_extraction),
    path('extraction/view/<int:id>/', views.view_extraction),
    path('pcr/start/', views.start_pcr),
    path('pcr/view/<int:id>/', views.view_pcr),
    path('pcr/end/<int:id>/', views.end_pcr),
]
