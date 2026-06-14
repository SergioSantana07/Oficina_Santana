from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('produtos/', views.produtos, name='produtos'),
    path('servicos/', views.servicos, name='servicos'),
    path('contato/', views.contato, name='contato'),
]