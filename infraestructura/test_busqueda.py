from django.test import TestCase
from django.urls import reverse

from .models import NodoServidor


class BusquedaTests(TestCase):
    def setUp(self):
        NodoServidor.objects.create(nombre_host='web-01', direccion_ip='10.0.0.1')
        NodoServidor.objects.create(nombre_host='db-01', direccion_ip='10.0.0.2')

    def test_busca_por_hostname(self):
        respuesta = self.client.get(reverse('buscar_servidores'), {'q': 'web'})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context['resultados'].count(), 1)

    def test_sin_termino_no_devuelve_resultados(self):
        respuesta = self.client.get(reverse('buscar_servidores'))
        self.assertEqual(respuesta.context['resultados'].count(), 0)
