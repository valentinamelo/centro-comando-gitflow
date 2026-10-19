from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import NodoServidor


class ApiServidorTests(APITestCase):
	def test_crud_servidor_y_creacion_de_incidencia(self):
		lista_url = reverse('servidor-list')
		datos_servidor = {
			'nombre_host': 'api-web-01',
			'direccion_ip': '10.0.0.10',
			'motor_contenedores': 'docker',
			'proxy_inverso': True,
			'en_produccion': True,
		}

		respuesta = self.client.post(lista_url, datos_servidor, format='json')
		self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
		servidor_id = respuesta.data['id']

		detalle_url = reverse('servidor-detail', args=[servidor_id])
		datos_actualizados = {
			'nombre_host': 'api-web-01',
			'direccion_ip': '10.0.0.11',
			'motor_contenedores': 'podman',
			'proxy_inverso': False,
			'en_produccion': False,
		}
		respuesta = self.client.put(
			detalle_url,
			datos_actualizados,
			format='json',
		)
		self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
		self.assertEqual(respuesta.data['direccion_ip'], '10.0.0.11')
		self.assertEqual(respuesta.data['motor_contenedores'], 'podman')
		self.assertFalse(respuesta.data['en_produccion'])

		respuesta = self.client.post(
			reverse('incidencia-list'),
			{
				'servidor': servidor_id,
				'titulo': 'Prueba de API',
				'descripcion': 'Incidencia creada desde el endpoint REST.',
				'severidad': 'baja',
				'resuelta': False,
			},
			format='json',
		)
		self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)

		respuesta = self.client.delete(detalle_url)
		self.assertEqual(respuesta.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(NodoServidor.objects.filter(pk=servidor_id).exists())

	def test_rechaza_ip_reservada_para_pruebas(self):
		respuesta = self.client.post(
			reverse('servidor-list'),
			{
				'nombre_host': 'api-reservado',
				'direccion_ip': '192.168.100.20',
				'motor_contenedores': 'podman',
				'proxy_inverso': True,
				'en_produccion': True,
			},
			format='json',
		)

		self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
