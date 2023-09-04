from django.urls import path

from . import views
from lead.views import LeadListView, LeadDetailView

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.leads_delete, name='delete'),
    path('<int:pk>/edit/', views.edit_lead, name='edit'),
    path('<int:pk>/converted/', views.convert_to_client, name='convert'),
    path('add-lead/', views.add_lead, name='add'),
]
