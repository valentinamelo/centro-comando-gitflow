from django.contrib import admin
from .models import NodoServidor, RegistroAuditoria, IncidenciaServidor

@admin.action(description='Activar Producción Masiva')
def marcar_como_produccion(_modeladmin, _request, queryset):
    queryset.update(en_produccion=True)

@admin.action(description='Poner en Mantenimiento')
def marcar_como_mantenimiento(_modeladmin, _request, queryset):
    queryset.update(en_produccion=False)

@admin.register(NodoServidor)
class NodoServidorAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la tabla principal
    list_display = ('nombre_host', 'direccion_ip', 'motor_contenedores', 'proxy_inverso', 'en_produccion')

    # Filtros laterales para hacer búsquedas rápidas
    list_filter = ('motor_contenedores', 'proxy_inverso', 'en_produccion')

    # Barra de búsqueda superior
    search_fields = ('nombre_host', 'direccion_ip')

    # Orden por defecto
    ordering = ('-fecha_despliegue',)

    actions = (marcar_como_produccion, marcar_como_mantenimiento)

@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('servidor', 'detalles', 'fecha_evento')
    list_filter = ('fecha_evento',)
    search_fields = ('servidor__nombre_host', 'detalles')
    ordering = ('-fecha_evento',)

@admin.action(description='Marcar como Resuelta')
def marcar_como_resuelta(_modeladmin, _request, queryset):
    queryset.update(resuelta=True)

@admin.action(description='Reabrir Incidencia')
def marcar_como_activa(_modeladmin, _request, queryset):
    queryset.update(resuelta=False)

@admin.register(IncidenciaServidor)
class IncidenciaServidorAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'servidor', 'severidad', 'resuelta', 'fecha_reporte')
    list_filter = ('severidad', 'resuelta')
    search_fields = ('titulo', 'servidor__nombre_host')
    ordering = ('-fecha_reporte',)
    actions = (marcar_como_resuelta, marcar_como_activa)