from django.urls import path, include
from . import views

app_name = 'lab_use'
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('report/', views.report),
        path('sheet_upload/', views.sheet_upload, name='sheet_upload'),
        path('new_upload/', views.sheet_upload, name='new_upload'),
]
