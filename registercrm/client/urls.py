from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.all_clients, name='list'),
    path('<int:pk>', views.client_detail, name='detail'),
    path('<int:pk>/delete/', views.delete_client, name='delete'),
    path('<int:pk>/edit/', views.edit_client, name='edit'),
    path('add/', views.add_client, name='add'),
]
