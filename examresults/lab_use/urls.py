from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.new_result, name='tralala'),
        path('report/', views.report),
]
