from django.urls import path

from . import views
from lead.views import LeadListView, LeadDetailView, LeadDeleteView, LeadUpdateView, AddFileView

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit'),
    path('<int:pk>/converted/', views.ConvertToCLientView.as_view(), name='convert'),
    path('<int:pk>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/add-file/', views.AddFileView.as_view(), name='add_file'),
    path('add-lead/', views.LeadCreateView.as_view(), name='add'),
    path('export/', views.lead_export_csv, name='export'),
]
