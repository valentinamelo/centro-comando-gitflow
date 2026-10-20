from django.shortcuts import render
from .models import NodoServidor


def health_check(request):
    """Endpoint de monitoreo: indica que la app y la base de datos responden."""
    return render(request, 'infraestructura/health.html', {
        'status': 'ok',
        'servicio': 'centro-comando',
        'servidores_registrados': NodoServidor.objects.count(),
    })
