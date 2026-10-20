from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_responde_ok(self):
        respuesta = self.client.get(reverse('health_check'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()['status'], 'ok')
