from django.urls import path, include
from . import views

app_name = 'lab_use'
urlpatterns = [
        #path('', views.new_result, name='add_result'),
        path('', views.IndexView.as_view(), name='index'),
        path('report/', views.report),
        path('new_result/<int:institution_id>/', views.new_result_with_url),
        path('new_result/with_institution/', views.new_result_with_post),
        path('new_result/', views.new_result),
        path('new_institution/', views.new_institution),
        path('commit_result/', views.commit_result, name='add_result'),
        path('bulk_upload/', views.bulk_upload, name='bulk_add'),
]
