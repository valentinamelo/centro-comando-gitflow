from rest_framework.viewsets import ModelViewSet

from .models import IncidenciaServidor, NodoServidor, RegistroAuditoria
from .serializer import (
    IncidenciaServidorSerializer,
    NodoServidorSerializer,
    RegistroAuditoriaSerializer,
)


class NodoServidorViewSet(ModelViewSet):
    queryset = NodoServidor.objects.all()
    serializer_class = NodoServidorSerializer


class RegistroAuditoriaViewSet(ModelViewSet):
    queryset = RegistroAuditoria.objects.all()
    serializer_class = RegistroAuditoriaSerializer


class IncidenciaServidorViewSet(ModelViewSet):
    queryset = IncidenciaServidor.objects.all()
    serializer_class = IncidenciaServidorSerializer