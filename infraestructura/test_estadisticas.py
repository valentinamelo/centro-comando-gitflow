from django.test import TestCase
from django.urls import reverse

from .models import NodoServidor


class EstadisticasTests(TestCase):
    def test_calcula_porcentaje_en_produccion(self):
        NodoServidor.objects.create(nombre_host='web-01', direccion_ip='10.0.0.1', en_produccion=True)
        NodoServidor.objects.create(nombre_host='web-02', direccion_ip='10.0.0.2', en_produccion=False)

        respuesta = self.client.get(reverse('estadisticas'))

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context['total_servidores'], 2)
        self.assertEqual(respuesta.context['porcentaje_produccion'], 50)
