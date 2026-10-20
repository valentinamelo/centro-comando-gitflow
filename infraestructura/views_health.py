from django.http import JsonResponse
from .models import NodoServidor


def health_check(request):
    """Endpoint de monitoreo: indica que la app y la base de datos responden."""
    return JsonResponse({
        'status': 'ok',
        'servicio': 'centro-comando',
        'servidores_registrados': NodoServidor.objects.count(),
    })
