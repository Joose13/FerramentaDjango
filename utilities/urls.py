from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('seleccionar_modulo/', views.seleccionar_modulo, name='seleccionar_modulo'),  # Página de configuración del módulo
    path('ejecutar_copia/', views.ejecutar_copia, name='ejecutar_copia'),  # Ejecutar el módulo con las opciones seleccionada
    path('ejecutar_copia_tiendas/', views.ejecutar_copia_tiendas, name='ejecutar_copia_tiendas'),  # Ejecutar el módulo con las opciones seleccionada
    path('contar_pedidos_total/', views.contar_pedidos_total_view, name='contar_pedidos_total'),
    path('maxprep/', views.insertar_maxprep, name='maxprep'),
    path("weekend_days/", views.weekend_days_view, name="weekend_days")
]
