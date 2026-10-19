from django.contrib import admin
from django.urls import path
from .views import lista_servidores, detalle_servidor, crear_servidor, editar_servidor, eliminar_servidor, registrar_incidencia, resolver_incidencia
from .views import (
MantenimientoListView, MantenimientoDetailView,
MantenimientoCreateView, MantenimientoUpdateView, MantenimientoDeleteView
)

urlpatterns = [
    path('', lista_servidores, name='home_servidores'),
    path('servidor/<int:pk>/', detalle_servidor, name='detalle_servidor'),
    path('servidor/nuevo/', crear_servidor, name='crear_servidor'),
    path('servidor/<int:pk>/editar/', editar_servidor, name='editar_servidor'),
    path('servidor/<int:pk>/eliminar/', eliminar_servidor, name='eliminar_servidor'),
    path('servidor/<int:pk>/incidencia/nueva/', registrar_incidencia, name='registrar_incidencia'),
    path('incidencia/<int:pk>/resolver/', resolver_incidencia, name='resolver_incidencia'),
]

urlpatterns += [
    path('mantenimientos/', MantenimientoListView.as_view(), name='lista_mantenimientos'),
    path('mantenimientos/<int:pk>/', MantenimientoDetailView.as_view(),
    name='detalle_mantenimiento'),
    path('mantenimientos/nuevo/', MantenimientoCreateView.as_view(),
    name='crear_mantenimiento'),
    path('mantenimientos/<int:pk>/editar/', MantenimientoUpdateView.as_view(),
    name='editar_mantenimiento'),
    path('mantenimientos/<int:pk>/eliminar/', MantenimientoDeleteView.as_view(),
    name='eliminar_mantenimiento'),
]