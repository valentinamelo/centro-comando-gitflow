from rest_framework import serializers

from .models import IncidenciaServidor, NodoServidor, RegistroAuditoria


class NodoServidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodoServidor
        fields = '__all__'
        read_only_fields = ['id', 'fecha_despliegue']


class RegistroAuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAuditoria
        fields = '__all__'
        read_only_fields = ['id', 'fecha_evento']


class IncidenciaServidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidenciaServidor
        fields = '__all__'
        read_only_fields = ['id', 'fecha_reporte']