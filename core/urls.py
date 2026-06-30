from django.urls import path
from . import views

urlpatterns = [
    # PAGES
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('servicos/', views.servicos, name='servicos'),
    path('contato/', views.contato, name='contato'),
    # ADMIN E DASHBOARD
    path('admin-santana/login/', views.admin_login, name='admin_login'),
    path('admin-santana/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-santana/logout/', views.admin_logout, name='admin_logout'),
    # CLIENTES
    path('admin-santana/clientes/', views.clientes_lista, name='clientes_lista'),
    path('admin-santana/clientes/novo/', views.cliente_novo, name='cliente_novo'),
    path('admin-santana/clientes/editar/<int:id>/', views.cliente_editar, name='cliente_editar'),
    path('admin-santana/clientes/excluir/<int:id>/', views.cliente_excluir, name='cliente_excluir'),
    # VEÍCULOS
    path('admin-santana/veiculos/', views.veiculos_lista, name='veiculos_lista'),
    path('admin-santana/veiculos/novo/', views.veiculo_novo, name='veiculo_novo'),
    path('admin-santana/veiculos/editar/<int:id>/', views.veiculo_editar, name='veiculo_editar'),
    path('admin-santana/veiculos/excluir/<int:id>/', views.veiculo_excluir, name='veiculo_excluir'),
]