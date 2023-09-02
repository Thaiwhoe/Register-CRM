from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from core.views import index, about, userInfo
from userprofile.views import signup, myaccount
from dashboard.views import dashboard

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/teams/', include('team.urls')),
    path('myaccount/', myaccount, name='myaccount'),
    path('dashboard/', include('dashboard.urls')),
    path('about/', about, name='about'),
    path('sign-up/', signup, name='sign-up'),
    path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('log-out/', views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
