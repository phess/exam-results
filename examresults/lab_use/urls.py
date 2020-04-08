from django.urls import path, include
from . import views

app_name = 'lab_use'
urlpatterns = [
        path('', views.home_view),
        path('home/', views.home_view),
        path('report/', views.report_view),
        path('new_result/', views.result_view, name='add_result'),
        path('upload/', views.upload_view),
        path('resend/', views.resend_view),
        path('pdf_generate/', views.pdf_generate_view),
        path('pdf_generate/<int:id>/', views.pdf_generate_view),

]
