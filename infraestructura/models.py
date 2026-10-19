from django.db import models
from django.core.exceptions import ValidationError

class NodoServidor(models.Model):
    # Opciones predefinidas para el panel
    MOTORES_CONTENEDOR = [
        ('docker', 'Docker'),
        ('podman', 'Podman'),
        ('lxc', 'LXC Linux Containers'),
        ('ninguno', 'Sin contenedores'),
    ]

    
    def validar_ip_corporativa(value):
        if value.startswith("192.168.100."):
            raise ValidationError("Las direcciones IP en el segmento 192.168.100.x están reservadas para pruebas internas de aislamiento.")

    nombre_host = models.CharField(max_length=100, unique=True, verbose_name="Hostname")
    direccion_ip = models.GenericIPAddressField(verbose_name="Dirección IP", validators=[validar_ip_corporativa])
    motor_contenedores = models.CharField(
        max_length=20,
        choices=MOTORES_CONTENEDOR,
        default='podman',
        verbose_name="Motor de Contenedores"
    )
    

    proxy_inverso = models.BooleanField(default=True, verbose_name="¿Enrutado por Nginx?")
    en_produccion = models.BooleanField(default=True, verbose_name="Estado Producción")
    fecha_despliegue = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_host} [{self.direccion_ip}]"

    class Meta:
        verbose_name = "Nodo de Servidor"
        verbose_name_plural = "Flota de Servidores"

class RegistroAuditoria(models.Model):
    servidor = models.ForeignKey(
        NodoServidor,
        on_delete=models.CASCADE,
        related_name='auditorias'
    )
    detalles = models.TextField(verbose_name="Detalle del Evento")
    fecha_evento = models.DateTimeField(auto_now_add=True)

class IncidenciaServidor(models.Model):
    # Opciones predefinidas para la severidad de la incidencia
    NIVELES_SEVERIDAD = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    servidor = models.ForeignKey(
        NodoServidor,
        on_delete=models.CASCADE,
        related_name='incidencias',
        verbose_name="Servidor Afectado"
    )
    titulo = models.CharField(max_length=150, verbose_name="Título de la Incidencia")
    descripcion = models.TextField(verbose_name="Descripción del Fallo")
    severidad = models.CharField(
        max_length=20,
        choices=NIVELES_SEVERIDAD,
        default='media',
        verbose_name="Severidad"
    )
    resuelta = models.BooleanField(default=False, verbose_name="¿Incidencia Resuelta?")
    fecha_reporte = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_severidad_display()}] {self.titulo} - {self.servidor.nombre_host}"

    class Meta:
        verbose_name = "Incidencia de Servidor"
        verbose_name_plural = "Incidencias Operativas"
        ordering = ['-fecha_reporte']

class MantenimientoNodo(models.Model):
    TIPO_TAREA = [
        ('actualizacion', 'Actualización de Sistema'),
        ('backup', 'Respaldo de Base de Datos'),
        ('seguridad', 'Parche de Seguridad'),
        ('hardware', 'Revisión de Hardware'),
    ]
    servidor = models.ForeignKey(
        NodoServidor,
        on_delete=models.CASCADE,
        related_name='mantenimientos',
        verbose_name="Servidor Asignado"
    )
    
    titulo_tarea = models.CharField(max_length=150, verbose_name="Título del Mantenimiento")
    descripcion_tecnica = models.TextField(verbose_name="Descripción de la Tarea")
    tipo = models.CharField(max_length=30, choices=TIPO_TAREA, default='actualizacion', verbose_name="Tipo de Tarea")
    completado = models.BooleanField(default=False, verbose_name="¿Tarea Ejecutada?")
    fecha_programada = models.DateTimeField(verbose_name="Fecha y Hora Programada")
    
    def __str__(self):
        return f"{self.titulo_tarea} - {self.servidor.nombre_host}"
    
    class Meta:
        verbose_name = "Mantenimiento de Servidor"
        verbose_name_plural = "Programación de Mantenimientos"