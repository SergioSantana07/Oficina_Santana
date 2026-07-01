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
    # SERVIÇOS (ADMIN)
    path('admin-santana/servicos/', views.servicos_admin_lista, name='servicos_admin_lista'),
    path('admin-santana/servicos/novo/', views.servico_novo, name='servico_novo'),
    path('admin-santana/servicos/editar/<int:id>/', views.servico_editar, name='servico_editar'),
    path('admin-santana/servicos/excluir/<int:id>/', views.servico_excluir, name='servico_excluir'),
    
    # ORDEM DE SERVIÇO
    path('admin-santana/ordens/', views.ordens_lista, name='ordens_lista'),
    path('admin-santana/ordens/novo/', views.ordem_nova, name='ordem_nova'),
    path('admin-santana/ordens/editar/<int:id>/', views.ordem_editar, name='ordem_editar'),
    path('admin-santana/ordens/excluir/<int:id>/', views.ordem_excluir, name='ordem_excluir'),
    path('admin-santana/ordens/visualizar/<int:id>/', views.ordem_visualizar, name='ordem_visualizar'),
    path('admin-santana/ordens/pdf/<int:id>/', views.ordem_pdf, name='ordem_pdf'),
    path('admin-santana/ordens/status/<int:id>/', views.ordem_atualizar_status, name='ordem_atualizar_status'),
    path('admin-santana/api/veiculos-cliente/<int:cliente_id>/', views.api_veiculos_cliente, name='api_veiculos_cliente'),
]