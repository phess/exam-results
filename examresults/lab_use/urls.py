from django.urls import path, include
from . import views

app_name = 'lab_use'
urlpatterns = [
        #path('', views.new_result, name='add_result'),
        path('', views.IndexView.as_view(), name='index'),
        path('report/', views.report),
        path('new_result/', views.new_result, name='add_result'),
]
