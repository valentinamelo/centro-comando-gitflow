from django.db.models import Q
from django.shortcuts import render

from .models import NodoServidor


def buscar_servidores(request):
    termino = request.GET.get('q', '').strip()
    resultados = NodoServidor.objects.none()
    if termino:
        resultados = NodoServidor.objects.filter(
            Q(nombre_host__icontains=termino) | Q(direccion_ip__icontains=termino)
        )
    return render(request, 'infraestructura/buscar_servidores.html', {
        'termino': termino,
        'resultados': resultados,
    })
