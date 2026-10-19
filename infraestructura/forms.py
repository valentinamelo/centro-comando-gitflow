from django import forms
from .models import NodoServidor, IncidenciaServidor
from .models import MantenimientoNodo

class NodoServidorForm(forms.ModelForm):
    class Meta:
        model = NodoServidor
        fields = ['nombre_host', 'direccion_ip', 'motor_contenedores', 'proxy_inverso', 'en_produccion']
        # fields = --all

class IncidenciaServidorForm(forms.ModelForm):
    class Meta:
        model = IncidenciaServidor
        fields = ['titulo', 'descripcion', 'severidad', 'resuelta']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Caída del servicio Nginx'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detalle técnico del fallo o alerta detectada'
            }),
            'severidad': forms.Select(attrs={'class': 'form-select'}),
            'resuelta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoNodo
        fields = ['servidor', 'titulo_tarea', 'descripcion_tecnica', 'tipo',
        'fecha_programada', 'completado']
        widgets = {
        'servidor': forms.Select(attrs={'class': 'form-select'}),
        'titulo_tarea': forms.TextInput(attrs={'class': 'form-control'}),
        'descripcion_tecnica': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        'tipo': forms.Select(attrs={'class': 'form-select'}),
        'fecha_programada': forms.DateTimeInput(attrs={'class': 'form-control', 'type':
        'datetime-local'}),
        'completado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }