from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_leads, name='all_leads'),
    path('<int:pk>/', views.leads_detail, name='leads_detail'),
    path('<int:pk>/delete/', views.leads_delete, name='leads_delete'),
    path('<int:pk>/edit/', views.edit_lead, name='edit_lead'),
    path('<int:pk>/converted/', views.convert_to_client, name='lead_convert'),
    path('add-lead/', views.add_lead, name='add_lead'),
]
