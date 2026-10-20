from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_muestra_estado_del_servicio_en_html(self):
        respuesta = self.client.get(reverse('health_check'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'infraestructura/health.html')
        self.assertEqual(respuesta.context['status'], 'ok')
        self.assertEqual(respuesta.context['servicio'], 'centro-comando')
        self.assertEqual(respuesta.context['servidores_registrados'], 0)
        self.assertContains(respuesta, 'Disponible')
