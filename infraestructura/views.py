from django.shortcuts import render, get_object_or_404, redirect
from .models import NodoServidor, IncidenciaServidor
from .forms import NodoServidorForm, IncidenciaServidorForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import MantenimientoNodo
from .forms import MantenimientoForm

def registrar_incidencia(request, pk):
    nodo = get_object_or_404(NodoServidor, pk=pk)
    if request.method == 'POST':
        form = IncidenciaServidorForm(request.POST)
        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.servidor = nodo
            incidencia.save()
            return redirect('detalle_servidor', pk=nodo.pk)
    else:
        form = IncidenciaServidorForm()
    return render(request, 'infraestructura/registrar_incidencia.html', {'form': form, 'nodo': nodo})

def resolver_incidencia(request, pk):
    incidencia = get_object_or_404(IncidenciaServidor, pk=pk)
    incidencia.resuelta = True
    incidencia.save()
    return redirect('detalle_servidor', pk=incidencia.servidor.pk)

def eliminar_servidor(request, pk):
    nodo = get_object_or_404(NodoServidor, pk=pk)
    if request.method == 'POST':
        nodo.delete()
        return redirect('home_servidores')
    return render(request, 'infraestructura/eliminar_servidor.html', {'nodo': nodo})

def editar_servidor(request, pk):
    nodo = get_object_or_404(NodoServidor, pk=pk)
    if request.method == 'POST':
        form = NodoServidorForm(request.POST, instance=nodo)
        if form.is_valid():
            form.save()
            return redirect('detalle_servidor', pk=nodo.pk)
    else:
        form = NodoServidorForm(instance=nodo)
    return render(request, 'infraestructura/editar_servidor.html', {'form': form, 'nodo': nodo})

def crear_servidor(request):
    if request.method == 'POST':
        form = NodoServidorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_servidores')
    else:
        form = NodoServidorForm()
    return render(request, 'infraestructura/crear_servidor.html', {'form': form})

def detalle_servidor(request, pk):
    nodo = get_object_or_404(NodoServidor, pk=pk)
    incidencias = nodo.incidencias.all()
    return render(request, 'infraestructura/detalle.html', {'nodo': nodo, 'incidencias': incidencias})

def lista_servidores(request):
    servidores = NodoServidor.objects.all()
    contexto = {'servidores': servidores}
    return render(request, 'infraestructura/index.html', contexto)

class MantenimientoListView(ListView):
    model = MantenimientoNodo
    template_name = 'infraestructura/mantenimiento_list.html'
    context_object_name = 'mantenimientos'
    
class MantenimientoDetailView(DetailView):
    model = MantenimientoNodo
    template_name = 'infraestructura/mantenimiento_detail.html'
    context_object_name = 'mantenimiento'
    
class MantenimientoCreateView(CreateView):
    model = MantenimientoNodo
    form_class = MantenimientoForm
    template_name = 'infraestructura/mantenimiento_form.html'
    success_url = reverse_lazy('lista_mantenimientos')
    
class MantenimientoUpdateView(UpdateView):
    model = MantenimientoNodo
    form_class = MantenimientoForm
    template_name = 'infraestructura/mantenimiento_form.html'
    success_url = reverse_lazy('lista_mantenimientos')
    
class MantenimientoDeleteView(DeleteView):
    model = MantenimientoNodo
    template_name = 'infraestructura/mantenimiento_confirm_delete.html'
    success_url = reverse_lazy('lista_mantenimientos')