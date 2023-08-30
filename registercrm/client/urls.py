from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_clients, name='all_clients'),
    path('<int:pk>', views.client_detail, name='client_detail'),
    path('<int:pk>/delete/', views.delete_client, name='delete_client'),
    path('<int:pk>/edit/', views.edit_client, name='edit_client'),
    path('add/', views.add_client, name='add_client'),
]
