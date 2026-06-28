from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('servicos/', views.servicos, name='servicos'),
    path('contato/', views.contato, name='contato'),
    path('admin-santana/login/', views.admin_login, name='admin_login'),
    path('admin-santana/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-santana/logout/', views.admin_logout, name='admin_logout'),
]