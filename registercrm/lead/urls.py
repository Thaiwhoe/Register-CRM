from django.urls import path

from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.all_leads, name='list'),
    path('<int:pk>/', views.leads_detail, name='detail'),
    path('<int:pk>/delete/', views.leads_delete, name='delete'),
    path('<int:pk>/edit/', views.edit_lead, name='edit'),
    path('<int:pk>/converted/', views.convert_to_client, name='convert'),
    path('add-lead/', views.add_lead, name='add'),
]
