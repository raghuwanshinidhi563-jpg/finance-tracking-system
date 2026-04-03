from django.urls import path
from . import views

urlpatterns = [
    path('api/records/', views.manage_record, name='record-list-create'),
    path('api/records/<int:pk>/', views.manage_record, name='record-detail'),
    path('api/summary/', views.financial_summary, name='financial-summary'),
]
