from django.shortcuts import render
from .models import NodoServidor, IncidenciaServidor, MantenimientoNodo

def estadisticas(request):
    total = NodoServidor.objects.count()
    en_produccion = NodoServidor.objects.filter(en_produccion=True).count()
    porcentaje_produccion = round(en_produccion * 100 / total) if total else 0
    contexto = {
        'total_servidores': total,
        'en_produccion': en_produccion,
        'porcentaje_produccion': porcentaje_produccion,
        'incidencias_abiertas': IncidenciaServidor.objects.filter(resuelta=False).count(),
        'mantenimientos_pendientes': MantenimientoNodo.objects.filter(completado=False).count(),
    }
    return render(request, 'infraestructura/estadisticas.html', contexto)
