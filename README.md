# Centro de Comando – UdenarNova

## 1. Descripción del proyecto

Este proyecto consiste en una demostración práctica de **GitFlow** utilizando una aplicación web desarrollada con Django, denominada **Centro de Comando – UdenarNova**.

La aplicación permite administrar una flota de servidores, consultar información de los nodos registrados, visualizar incidencias, revisar mantenimientos y utilizar funcionalidades como la búsqueda de servidores y el panel de estadísticas.

El propósito de la práctica es demostrar cómo GitFlow permite organizar el desarrollo de software mediante ramas, integrar funcionalidades, resolver conflictos, preparar versiones y corregir errores críticos sin perder el control del código estable.

### Funcionalidades desarrolladas

- **Endpoint de monitoreo `/health/`:** permite consultar el estado del servicio, identificar el nombre del servicio y conocer cuántos servidores están registrados.
- **Panel de estadísticas `/estadisticas/`:** presenta información general de la flota, los servidores en producción, las incidencias abiertas y los mantenimientos pendientes.
- **Búsqueda de servidores `/buscar/`:** permite buscar servidores por hostname o dirección IP.
- **Corrección de errores:** se utiliza un `hotfix` para solucionar un error de división por cero cuando no hay servidores registrados.
- **Gestión de versiones:** se utilizan los archivos `VERSION` y `CHANGELOG.md`, junto con las etiquetas `v1.0.0` y `v1.0.1`.

## 2. Escenario de la demostración

La práctica está organizada en ramas que representan las diferentes etapas del ciclo de desarrollo.

| Rama | Qué se hace | Resultado esperado |
|---|---|---|
| `main` | Commit inicial y versiones `v1.0.0` y `v1.0.1`. | Contiene el código correspondiente a las versiones estables. |
| `develop` | Integración de las funcionalidades. | Sirve como base para crear las ramas de desarrollo. |
| `feature/health-check` | Desarrollo del endpoint `/health/`. | Integración sin conflicto. |
| `feature/estadisticas` | Desarrollo del panel `/estadisticas/`. | Integración de la funcionalidad de estadísticas. |
| `feature/buscador-servidores` | Desarrollo de la búsqueda `/buscar/`. | Conflicto controlado con la funcionalidad de estadísticas. |
| `release/1.0.0` | Preparación de `VERSION` y `CHANGELOG.md`. | Publicación de la versión `v1.0.0`. |
| `hotfix/1.0.1` | Corrección del error 500 en producción. | Publicación de la versión corregida `v1.0.1`. |

El conflicto se produce intencionalmente porque las funcionalidades de estadísticas y búsqueda modifican zonas compartidas de `base.html` y `urls.py`. Las vistas de cada funcionalidad están en archivos independientes para evitar que el conflicto se extienda a toda la lógica del proyecto.

El error que se corrige durante el `hotfix` también está preparado intencionalmente: la vista de estadísticas divide por cero cuando no existen servidores registrados. Las pruebas iniciales no contemplan ese caso, por lo que la corrección incorpora una prueba de regresión.

## 3. ¿Qué es GitFlow?

GitFlow es una estrategia de organización del desarrollo basada en ramas. Cada tipo de rama tiene una responsabilidad específica y permite trabajar en funcionalidades o correcciones sin modificar directamente el código estable.

### 3.1. Ramas principales

- **`main`:** representa el código estable y las versiones publicadas. En esta demostración recibe las versiones `v1.0.0` y `v1.0.1`.
- **`develop`:** reúne las funcionalidades desarrolladas y sirve como punto de partida para las ramas `feature`.

### 3.2. Ramas de apoyo

- **`feature/*`:** se utilizan para desarrollar funcionalidades de manera aislada.
- **`release/X.Y.Z`:** se utilizan para preparar una versión, actualizar la información de versión y verificar que el lanzamiento esté listo.
- **`hotfix/X.Y.Z`:** se utilizan para corregir errores críticos que afectan al código estable.

### 3.3. Flujo utilizado

1. Se inicializa el repositorio y se crea `main`.
2. Se crea `develop` como rama de integración.
3. Se desarrolla el endpoint de monitoreo en `feature/health-check`.
4. Se crean las ramas de estadísticas y búsqueda para simular dos desarrolladores.
5. Se resuelve el conflicto entre las funcionalidades antes de integrar la rama del buscador.
6. Se prepara y publica la versión `v1.0.0`.
7. Se corrige el error de división por cero mediante `hotfix/1.0.1`.
8. Se comprueba el historial final, las ramas, las etiquetas y las pruebas.

## 4. Convención de mensajes de commit

En el proyecto se utiliza la convención **Conventional Commits**, que permite identificar el propósito de cada cambio mediante un prefijo.

| Tipo | Uso |
|---|---|
| `feat` | Agregar una nueva funcionalidad. |
| `fix` | Corregir un error. |
| `docs` | Modificar la documentación. |
| `test` | Agregar o modificar pruebas. |
| `refactor` | Modificar la estructura interna sin cambiar el comportamiento esperado. |
| `chore` | Realizar tareas de mantenimiento, configuración o preparación de versiones. |

La estructura general es:

`tipo(alcance): descripción en minúscula y en presente`

Por ejemplo, `feat(health): agrega endpoint /health/ de monitoreo` indica que se incorpora una nueva funcionalidad relacionada con el monitoreo.

El mensaje de un commit no ejecuta la funcionalidad ni cambia el comportamiento del código por sí mismo: describe el conjunto de cambios que se registra en el historial.

---

# FASE 0. Preparación del proyecto

## 5. Preparar el entorno de trabajo

Primero se ingresa a la carpeta del proyecto. Si la carpeta descargada se llama `centro_comando-main`, se puede renombrar para trabajar con un nombre más claro.

También se elimina el archivo `.DS_Store`, que macOS genera para almacenar información de presentación de carpetas y que no forma parte del código de Django.

### Crear y activar el entorno virtual

```bash
python3 -m venv venv
# Windows: venv\Scripts\activate    |    Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

### Explicación de cada línea

**`python3 -m venv venv`**

- `python3`: ejecuta Python 3.
- `-m venv`: indica que se debe ejecutar el módulo estándar encargado de crear entornos virtuales.
- `venv`: es el nombre de la carpeta donde se crea el entorno virtual.

El entorno virtual permite instalar las dependencias del proyecto sin mezclarlas con las de otros proyectos de Python.

**`# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate`**

Es un comentario que indica cómo activar el entorno virtual según el sistema operativo. No se ejecuta como una instrucción por sí mismo cuando se encuentra dentro de un script de Bash.

En Windows se utiliza la ruta `venv\Scripts\activate`. En macOS y Linux se utiliza `source venv/bin/activate`.

**`pip install -r requirements.txt`**

- `pip`: herramienta para instalar paquetes de Python.
- `install`: indica que se van a instalar paquetes.
- `-r`: indica que la lista de paquetes se encuentra en un archivo.
- `requirements.txt`: contiene las dependencias necesarias para ejecutar el proyecto.

**`python manage.py migrate`**

- `python`: ejecuta Python.
- `manage.py`: es el archivo de administración del proyecto Django.
- `migrate`: aplica las migraciones pendientes a la base de datos.

Las migraciones permiten crear o actualizar las tablas y estructuras de base de datos definidas por el proyecto.

**`python manage.py test`**

Ejecuta las pruebas automatizadas de Django. Sirve para comprobar que las funcionalidades verificadas por las pruebas se comportan como se espera.

### Configurar Git

```bash
git --version
git config --global user.name "Valentina Melo Solarte"
git config --global user.email "valentinamelo2001 @gmail.com"
git config --global init.defaultBranch main
```

**`git --version`**

Muestra la versión de Git instalada en el sistema. Permite verificar que Git esté disponible antes de iniciar el trabajo.

**`git config --global user.name "Valentina Melo Solarte"`**

Configura el nombre que Git utilizará como autor en los nuevos commits. La opción `--global` aplica la configuración al usuario del sistema, no solamente a este repositorio.

**`git config --global user.email "valentinamelo2001 @gmail.com"`**

Configura el correo asociado a los nuevos commits. Este valor se guarda en los metadatos del autor de cada commit.

Se conserva aquí el comando de la guía original. Conviene comprobar que el correo esté escrito exactamente como se desea y que no contenga espacios accidentales, porque el correo del autor y el correo reconocido por GitHub pueden afectar la atribución de los commits.

**`git config --global init.defaultBranch main`**

Configura `main` como nombre predeterminado de la rama inicial de los nuevos repositorios creados con `git init`.

### Actualizar `.gitignore`

Se agrega la siguiente línea al final de `.gitignore`:

```gitignore
.DS_Store
```

El archivo `.gitignore` indica a Git qué archivos o carpetas debe ignorar cuando detecta archivos sin seguimiento. La regla `.DS_Store` evita que los archivos auxiliares de macOS se incorporen accidentalmente al repositorio.

---

# FASE 1. Crear el repositorio y la rama `main`

## 6. Archivo `README.md`

En la raíz del proyecto se crea el archivo `README.md`, que documenta el propósito de la aplicación, la estrategia de ramas, la convención de commits y los comandos para ejecutar el proyecto.

Su contenido inicial es:

```markdown
# Centro de Comando – UdenarNova

Panel Django para administrar una flota de servidores (servidores, incidencias, mantenimientos y API REST).

## Estrategia de ramas (GitFlow)

| Rama | Origen | Se fusiona en | Propósito |
|---|---|---|---|
| `main` | – | – | Código en producción. Cada versión lleva un tag `vX.Y.Z` |
| `develop` | `main` | – | Integración de funcionalidades |
| `feature/*` | `develop` | `develop` | Una funcionalidad por rama |
| `release/X.Y.Z` | `develop` | `main` y `develop` | Preparar la versión |
| `hotfix/X.Y.Z` | `main` | `main` y `develop` | Corregir errores en producción |

## Convención de commits (Conventional Commits)

`tipo(alcance): descripción en minúscula y en presente`

| Tipo | Uso |
|---|---|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de un error |
| `docs` | Documentación |
| `test` | Pruebas |
| `refactor` | Cambio interno sin alterar el comportamiento |
| `chore` | Tareas de mantenimiento, versiones, configuración |

## Ejecutar

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py test
```
```

### ¿Qué documenta este archivo?

- El título identifica el proyecto.
- La descripción resume el propósito de la aplicación.
- La tabla de ramas explica de dónde nace cada rama, dónde se integra y qué responsabilidad tiene.
- La sección de Conventional Commits explica cómo se clasifican los cambios.
- La sección de ejecución reúne los comandos básicos para preparar, ejecutar y verificar la aplicación.

El README es importante porque permite que otra persona entienda el proyecto sin tener que revisar todo el código fuente.

## 7. Inicializar el repositorio Git

```bash
git init
git branch -M main
git add .
git status
git commit -m "chore: commit inicial del proyecto Centro de Comando"
```

### Explicación de cada línea

**`git init`**

Inicializa un repositorio Git en la carpeta actual. Git crea la estructura interna necesaria para controlar las versiones de los archivos.

**`git branch -M main`**

Renombra la rama actual a `main`. La opción `-M` permite forzar el cambio de nombre si es necesario.

**`git add .`**

Prepara los archivos nuevos y modificados del directorio actual para que puedan formar parte del siguiente commit. No crea todavía un commit: prepara los cambios en el área de preparación (*staging area*).

**`git status`**

Muestra el estado del repositorio: la rama actual, los archivos modificados, los archivos nuevos sin seguimiento y los cambios que ya están preparados.

**`git commit -m "chore: commit inicial del proyecto Centro de Comando"`**

Crea el primer registro del historial con los cambios que se habían preparado. La opción `-m` permite escribir el mensaje del commit directamente en el comando.

El prefijo `chore` indica que se trata de una tarea inicial de configuración del proyecto.

## 8. Crear y conectar el repositorio remoto

Se crea en GitHub un repositorio vacío llamado `centro-comando-gitflow`, sin generar otro README desde GitHub, porque el archivo ya se crea localmente.

```bash
git remote add origin https://github.com/valentinamelo/centro-comando-gitflow.git
git push -u origin main
```

### Explicación de cada línea

**`git remote add origin https://github.com/valentinamelo/centro-comando-gitflow.git`**

- `git remote`: administra los repositorios remotos.
- `add`: agrega una nueva referencia remota.
- `origin`: es el nombre que se asigna al repositorio remoto.
- La URL identifica el repositorio de GitHub con el que se conectará el proyecto local.

El comando no crea el repositorio en GitHub; registra la dirección de un repositorio que ya existe.

**`git push -u origin main`**

- `git push`: envía commits desde el repositorio local al remoto.
- `origin`: indica a qué repositorio remoto se enviarán.
- `main`: indica qué rama se publicará.
- `-u`: configura la relación de seguimiento entre la rama local y la remota para facilitar futuras operaciones.

Al finalizar, el repositorio de GitHub tendrá la rama `main` y el historial inicial del proyecto.

---

# FASE 2. Crear la rama `develop`

## 9. Crear y publicar `develop`

```bash
git switch -c develop
git push -u origin develop
```

**`git switch -c develop`**

Crea la rama `develop` a partir de la rama actual y cambia automáticamente a ella.

La opción `-c` significa crear una rama nueva. `develop` será la rama de integración de las funcionalidades.

**`git push -u origin develop`**

Publica la rama `develop` en GitHub y establece su seguimiento remoto.

### Configuración de GitHub

En GitHub se realiza la siguiente configuración:

1. Entrar en **Settings → General** y establecer `develop` como rama predeterminada.
2. Agregar una regla de protección para `main`.
3. Entrar en **Settings → Branches → Add classic branch protection rule**.
4. En `Branch name pattern`, escribir `main`.
5. Marcar `Require a pull request before merging`, dejando las demás opciones desmarcadas según el escenario.
6. Desplazarse hasta el final y hacer clic en **Create**.

Esta configuración busca evitar que los cambios se integren directamente en la rama estable sin revisión.

**¿Por qué se utiliza `develop`?**

Porque permite integrar las funcionalidades antes de convertirlas en una versión estable. Así, los cambios en desarrollo no necesitan entrar directamente en `main`.

---

# FASE 3. Primera funcionalidad: `feature/health-check`

## 10. Crear la rama de monitoreo

```bash
git switch -c feature/health-check develop
```

Este comando crea la rama `feature/health-check` a partir de `develop` y cambia a ella.

La rama se utiliza para desarrollar el endpoint de monitoreo de forma aislada.

## 11. Archivo `infraestructura/views_health.py`

Este archivo contiene la vista Django que procesa las solicitudes al endpoint de monitoreo.

Código de la guía:

```python
from django.shortcuts import render
from .models import NodoServidor


def health_check(request):
    """Endpoint de monitoreo: indica que la app y la base de datos responden."""
    return render(request, 'infraestructura/health.html', {
        'status': 'ok',
        'servicio': 'centro-comando',
        'servidores_registrados': NodoServidor.objects.count(),
    })
```

### Explicación del código

**`from django.shortcuts import render`**

Importa la función `render`, que permite generar una respuesta HTTP utilizando una plantilla y un contexto de datos.

**`from .models import NodoServidor`**

Importa el modelo `NodoServidor` desde el archivo `models.py` del mismo paquete. Este modelo representa los servidores registrados en la aplicación.

**`def health_check(request):`**

Define una vista llamada `health_check`. Django la ejecuta cuando una URL configurada apunta a esta función.

El parámetro `request` contiene información sobre la solicitud HTTP recibida.

**La cadena de documentación de la función**

```python
"""Endpoint de monitoreo: indica que la app y la base de datos responden."""
```

Describe la finalidad de la vista para quien lea el código.

**`return render(request, 'infraestructura/health.html', {...})`**

Genera una respuesta HTML utilizando la plantilla `infraestructura/health.html` y los datos incluidos en el diccionario de contexto.

El contexto contiene tres valores:

- `'status': 'ok'`: indica que el endpoint responde con el estado esperado.
- `'servicio': 'centro-comando'`: identifica el nombre del servicio.
- `'servidores_registrados': NodoServidor.objects.count()`: consulta el ORM de Django para contar los registros de `NodoServidor`.

## 12. Plantilla HTML del estado del servicio

La plantilla de la guía contiene el siguiente código:

```html
{% extends 'infraestructura/base.html' %}
{% block title %}Estado del servicio{% endblock %}
{% block content %}
<h1 class="text-primary mb-4">Estado del servicio</h1>
<div class="row g-3">
    <div class="col-md-4">
        <div class="card shadow-sm h-100">
            <div class="card-body">
                <h6 class="text-muted">Estado</h6>
                <p class="mb-0">
                    <span class="badge bg-success fs-6">Disponible</span>
                </p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card shadow-sm h-100">
            <div class="card-body">
                <h6 class="text-muted">Servicio</h6>
                <p class="mb-0 fs-5 fw-bold">{{ servicio }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card shadow-sm h-100">
            <div class="card-body">
                <h6 class="text-muted">Servidores registrados</h6>
                <p class="mb-0 fs-5 fw-bold">{{ servidores_registrados }}</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Explicación del HTML y las etiquetas de Django

- `{% extends 'infraestructura/base.html' %}` indica que la plantilla hereda la estructura de `base.html`. De esta manera reutiliza elementos comunes de la interfaz.
- `{% block title %}...{% endblock %}` define el contenido del bloque de título.
- `{% block content %}` abre el bloque donde se encuentra el contenido de esta página.
- `<h1>` presenta el encabezado principal.
- Las clases `text-primary`, `mb-4`, `row`, `g-3`, `col-md-4`, `card` y `card-body` corresponden a clases de presentación de Bootstrap.
- `<span class="badge bg-success fs-6">Disponible</span>` muestra visualmente el estado como una etiqueta verde.
- `{{ servicio }}` imprime el valor `servicio` enviado desde la vista.
- `{{ servidores_registrados }}` imprime la cantidad de servidores recibida desde el contexto.
- `{% endblock %}` cierra el bloque de plantilla correspondiente.

La plantilla separa la presentación de los datos de la lógica de Python. La vista obtiene los valores y la plantilla los muestra.

## 13. Archivo `infraestructura/test_health.py`

Este archivo contiene las pruebas automatizadas del endpoint de monitoreo.

```python
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
```

### Explicación del código

- `from django.test import TestCase`: importa la clase base que proporciona Django para crear pruebas automatizadas.
- `from django.urls import reverse`: importa la función que obtiene una URL a partir de su nombre.
- `class HealthCheckTests(TestCase):`: define una clase que agrupa las pruebas del endpoint.
- `def test_health_muestra_estado_del_servicio_en_html(self):`: define una prueba cuyo nombre describe lo que se comprueba.
- `self.client.get(reverse('health_check'))`: simula una solicitud HTTP GET a la ruta identificada como `health_check`.
- `self.assertEqual(respuesta.status_code, 200)`: verifica que la respuesta tenga el código HTTP 200, que indica que la solicitud fue atendida correctamente.
- `self.assertTemplateUsed(...)`: comprueba que se utilizó la plantilla indicada.
- `self.assertEqual(respuesta.context['status'], 'ok')`: comprueba el valor del estado en el contexto.
- `self.assertEqual(respuesta.context['servicio'], 'centro-comando')`: verifica el nombre del servicio.
- `self.assertEqual(respuesta.context['servidores_registrados'], 0)`: verifica que el contexto contenga cero servidores en el escenario de prueba.
- `self.assertContains(respuesta, 'Disponible')`: comprueba que la respuesta contenga el texto `Disponible`.

## 14. Registrar la ruta `/health/`

Al final de `infraestructura/urls.py` se agrega:

```python
from .views_health import health_check
urlpatterns.append(path('health/', health_check, name='health_check'))
```

### Explicación

- `from .views_health import health_check`: importa la vista que atenderá la solicitud.
- `urlpatterns.append(...)`: añade una nueva ruta a la lista de rutas de Django.
- `path('health/', ...)`: define el segmento de URL `health/`.
- `health_check`: indica qué vista se ejecuta al acceder a esa URL.
- `name='health_check'`: asigna un nombre a la ruta para poder referenciarla desde el código y las pruebas mediante `reverse('health_check')`.

La guía indica que el archivo original no termina en un salto de línea; por eso, antes de pegar las líneas, se debe presionar Enter.

La ruta final depende de cómo estén configuradas las URL principales del proyecto. En este escenario se espera acceder a `/health/`.

## 15. Ejecutar pruebas y registrar la funcionalidad

```bash
python manage.py test
git add .
git commit -m "feat(health): agrega endpoint /health/ de monitoreo"
git push -u origin feature/health-check
```

**`python manage.py test`**

Ejecuta las pruebas automatizadas para verificar que la funcionalidad responda correctamente.

**`git add .`**

Prepara los cambios nuevos y modificados para el commit.

**`git commit -m "feat(health): agrega endpoint /health/ de monitoreo"`**

Registra la implementación del endpoint. `feat` identifica el cambio como una funcionalidad nueva y `health` indica su alcance.

**`git push -u origin feature/health-check`**

Publica la rama de monitoreo en GitHub y establece su seguimiento remoto.

## 16. Integrar `feature/health-check` en `develop`

```bash
git switch develop
git merge --no-ff feature/health-check -m "merge: feature/health-check en develop"
git push origin develop
git branch -d feature/health-check
git push origin --delete feature/health-check
git log --graph --oneline --all
```

### Explicación de cada línea

**`git switch develop`**

Cambia a la rama de integración para que el siguiente merge se realice en `develop`.

**`git merge --no-ff feature/health-check -m "merge: feature/health-check en develop"`**

Integra los cambios de la rama `feature/health-check` en la rama actual.

- `git merge`: integra el historial de otra rama.
- `--no-ff`: evita el avance directo (*fast-forward*) y crea un commit de merge.
- `feature/health-check`: identifica la rama que se integrará.
- `-m`: especifica el mensaje del commit de integración.

El objetivo de `--no-ff` es conservar un punto de integración visible en el historial.

**`git push origin develop`**

Publica en GitHub los cambios integrados en `develop`.

**`git branch -d feature/health-check`**

Elimina la rama local después de su integración. La opción `-d` comprueba que la rama se haya integrado antes de permitir su eliminación.

**`git push origin --delete feature/health-check`**

Elimina la rama remota de GitHub. No elimina los commits que ya forman parte de `develop`.

**`git log --graph --oneline --all`**

Muestra el historial de commits de todas las ramas locales conocidas:

- `--graph`: representa gráficamente las relaciones entre los commits.
- `--oneline`: resume cada commit en una sola línea.
- `--all`: incluye las referencias de todas las ramas locales.

---

# FASE 4. Dos desarrolladores y un conflicto

## 17. Crear las ramas desde el mismo punto de `develop`

```bash
git switch -c feature/estadisticas develop
git switch develop
git switch -c feature/buscador-servidores develop
```

**`git switch -c feature/estadisticas develop`**

Crea la rama de estadísticas a partir de `develop` y cambia a ella.

**`git switch develop`**

Regresa a la rama de integración.

**`git switch -c feature/buscador-servidores develop`**

Crea la rama del buscador a partir de `develop`.

Las dos ramas parten del mismo estado inicial. Esto es importante para la demostración, porque permite desarrollar las dos funcionalidades en paralelo y generar un conflicto controlado al modificar los mismos archivos compartidos.

## 18. Desarrollador A: `feature/estadisticas`

### Cambiar a la rama de estadísticas

```bash
git switch feature/estadisticas
```

Cambia a la rama donde se desarrollará el panel de estadísticas.

## 19. Archivo `infraestructura/views_estadisticas.py`

```python
from django.shortcuts import render

from .models import NodoServidor, IncidenciaServidor, MantenimientoNodo


def estadisticas(request):
    total = NodoServidor.objects.count()
    en_produccion = NodoServidor.objects.filter(en_produccion=True).count()
    porcentaje_produccion = round(en_produccion * 100 / total)

    contexto = {
        'total_servidores': total,
        'en_produccion': en_produccion,
        'porcentaje_produccion': porcentaje_produccion,
        'incidencias_abiertas': IncidenciaServidor.objects.filter(resuelta=False).count(),
        'mantenimientos_pendientes': MantenimientoNodo.objects.filter(completado=False).count(),
    }
    return render(request, 'infraestructura/estadisticas.html', contexto)
```

### Explicación del código

**`from django.shortcuts import render`**

Importa la función que permite devolver una respuesta HTML utilizando una plantilla.

**`from .models import NodoServidor, IncidenciaServidor, MantenimientoNodo`**

Importa los tres modelos utilizados por el panel:

- `NodoServidor`: representa los servidores registrados.
- `IncidenciaServidor`: representa las incidencias relacionadas con los servidores.
- `MantenimientoNodo`: representa los mantenimientos de los nodos.

**`def estadisticas(request):`**

Define la vista que prepara los datos del panel.

**`total = NodoServidor.objects.count()`**

Consulta la cantidad total de registros del modelo `NodoServidor`.

**`en_produccion = NodoServidor.objects.filter(en_produccion=True).count()`**

Filtra los servidores cuyo campo `en_produccion` tiene valor verdadero y cuenta cuántos cumplen esa condición.

**`porcentaje_produccion = round(en_produccion * 100 / total)`**

Calcula el porcentaje de servidores en producción y redondea el resultado al entero más cercano.

Esta es la línea que contiene el error intencional del escenario: cuando `total` es cero, la operación intenta dividir por cero y genera una excepción.

**`contexto = {...}`**

Crea un diccionario que contiene los datos que se mostrarán en la plantilla:

- `total_servidores`: cantidad total de servidores.
- `en_produccion`: cantidad de servidores que están en producción.
- `porcentaje_produccion`: porcentaje calculado.
- `incidencias_abiertas`: cantidad de incidencias cuyo campo `resuelta` es falso.
- `mantenimientos_pendientes`: cantidad de mantenimientos cuyo campo `completado` es falso.

**`return render(request, 'infraestructura/estadisticas.html', contexto)`**

Envía el diccionario a la plantilla `infraestructura/estadisticas.html` y devuelve la respuesta HTML al navegador.

## 20. Plantilla `infraestructura/templates/infraestructura/estadisticas.html`

```html
{% extends 'infraestructura/base.html' %}
{% block title %}Estadísticas{% endblock %}
{% block content %}
<h1 class="text-primary mb-4">Estadísticas de la Flota</h1>
<div class="row g-3">
    <div class="col-md-3">
        <div class="card shadow-sm text-center">
            <div class="card-body">
                <h6 class="text-muted">Servidores</h6>
                <p class="display-6 fw-bold">{{ total_servidores }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow-sm text-center">
            <div class="card-body">
                <h6 class="text-muted">En producción</h6>
                <p class="display-6 fw-bold text-success">{{ porcentaje_produccion }}%</p>
                <small class="text-muted">{{ en_produccion }} de {{ total_servidores }}</small>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow-sm text-center">
            <div class="card-body">
                <h6 class="text-muted">Incidencias abiertas</h6>
                <p class="display-6 fw-bold text-danger">{{ incidencias_abiertas }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card shadow-sm text-center">
            <div class="card-body">
                <h6 class="text-muted">Mantenimientos pendientes</h6>
                <p class="display-6 fw-bold text-warning">{{ mantenimientos_pendientes }}</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Explicación

- `{% extends 'infraestructura/base.html' %}` reutiliza la plantilla base del sistema.
- `{% block title %}` establece el título de la página.
- `{% block content %}` define el bloque que contiene el panel.
- `<h1>` muestra el encabezado del panel de estadísticas.
- Las clases `row`, `g-3` y `col-md-3` distribuyen las tarjetas en una cuadrícula de cuatro columnas en pantallas adecuadas.
- Las clases `card`, `card-body` y `text-center` estructuran y alinean visualmente el contenido.
- `{{ total_servidores }}` muestra la cantidad total.
- `{{ porcentaje_produccion }}%` muestra el porcentaje calculado.
- `{{ en_produccion }} de {{ total_servidores }}` muestra la cantidad de servidores en producción respecto del total.
- `{{ incidencias_abiertas }}` muestra el número de incidencias abiertas.
- `{{ mantenimientos_pendientes }}` muestra los mantenimientos pendientes.
- Las clases `text-success`, `text-danger` y `text-warning` distinguen visualmente los indicadores.
- `{% endblock %}` cierra el bloque de contenido.

## 21. Archivo `infraestructura/test_estadisticas.py`

```python
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
```

### Explicación del código

- `TestCase`: permite crear pruebas automatizadas con un entorno de base de datos de prueba.
- `reverse`: obtiene la URL asociada al nombre `estadisticas`.
- `NodoServidor`: es el modelo utilizado para crear los datos de prueba.
- `class EstadisticasTests(TestCase)`: agrupa las pruebas del panel.
- `test_calcula_porcentaje_en_produccion`: comprueba el cálculo del porcentaje de servidores en producción.
- `NodoServidor.objects.create(...)`: crea dos servidores para la prueba. Uno está en producción y el otro no.
- `self.client.get(reverse('estadisticas'))`: solicita la página de estadísticas.
- `self.assertEqual(respuesta.status_code, 200)`: comprueba que la vista responda correctamente.
- `self.assertEqual(respuesta.context['total_servidores'], 2)`: verifica que la vista cuente dos servidores.
- `self.assertEqual(respuesta.context['porcentaje_produccion'], 50)`: verifica que el porcentaje sea 50 %.

Esta prueba utiliza un total de dos servidores, por lo que no activa el error de división por cero. Ese caso se cubre posteriormente en la fase de `hotfix`.

## 22. Primer commit de estadísticas

```bash
git add .
git commit -m "feat(estadisticas): agrega vista con resumen de la flota"
```

- `git add .`: prepara los archivos nuevos o modificados de la funcionalidad.
- `git commit -m "feat(estadisticas): agrega vista con resumen de la flota"`: registra la vista, la plantilla y los archivos de prueba correspondientes al primer conjunto de cambios.

Este primer commit contiene la funcionalidad inicial del panel.

## 23. Registrar la ruta y el enlace de estadísticas

Al final de `urls.py` se agrega:

```python
from .views_estadisticas import estadisticas
urlpatterns.append(path('estadisticas/', estadisticas, name='estadisticas'))
```

- `from .views_estadisticas import estadisticas`: importa la vista.
- `urlpatterns.append(...)`: agrega una ruta a la configuración de URL.
- `path('estadisticas/', ...)`: establece el segmento de URL `estadisticas/`.
- `estadisticas`: es la vista que se ejecutará al solicitar la ruta.
- `name='estadisticas'`: asigna un nombre para referenciar la URL desde pruebas y plantillas.

En `templates/infraestructura/base.html`, justo debajo del enlace de Mantenimientos, se agrega:

```html
<a class="nav-link" href="{% url 'estadisticas' %}">Estadísticas</a>
```

Esta línea crea un enlace de navegación:

- `<a>` define un hipervínculo.
- `class="nav-link"` aplica la clase de navegación de Bootstrap.
- `href="{% url 'estadisticas' %}"` obtiene la URL a partir del nombre de ruta `estadisticas`.
- `Estadísticas` es el texto visible para el usuario.
- `</a>` cierra el enlace.

El archivo `base.html` contiene elementos compartidos por las páginas. Al modificarlo, el enlace aparece en la navegación de las plantillas que lo heredan.

### Probar, registrar y publicar los cambios

```bash
python manage.py test
git add .
git commit -m "feat(estadisticas): registra la ruta y el enlace en el menú"
git push -u origin feature/estadisticas

git switch develop
git merge --no-ff feature/estadisticas -m "merge: feature/estadisticas en develop"
git push origin develop
git branch -d feature/estadisticas
git push origin --delete feature/estadisticas
```

**`python manage.py test`** ejecuta las pruebas de Django antes de integrar la funcionalidad.

**`git add .`** prepara los cambios de la ruta y el menú.

**`git commit -m "feat(estadisticas): registra la ruta y el enlace en el menú"`** registra la incorporación de la ruta y el enlace.

**`git push -u origin feature/estadisticas`** publica la rama de estadísticas en GitHub y establece su seguimiento remoto.

**`git switch develop`** cambia a la rama de integración.

**`git merge --no-ff feature/estadisticas -m "merge: feature/estadisticas en develop"`** integra la funcionalidad y crea un commit de merge para conservar su punto de integración en el historial.

**`git push origin develop`** publica la integración en GitHub.

**`git branch -d feature/estadisticas`** elimina la rama local ya integrada.

**`git push origin --delete feature/estadisticas`** elimina la rama remota después de la integración.

---

## 24. Desarrollador B: `feature/buscador-servidores`

La segunda funcionalidad se desarrolla para simular el trabajo de otro integrante del equipo.

### Cambiar a la rama

```bash
git switch feature/buscador-servidores
```

Este comando cambia a la rama del buscador, que se creó previamente a partir del mismo punto de `develop` que la rama de estadísticas.

### ¿Para qué se utiliza `--author`?

En esta fase se emplea la opción `--author` en los commits para simular que los cambios fueron realizados por otro desarrollador.

Esta opción cambia la información del autor que queda registrada en el commit. No cambia el usuario del sistema, no crea una cuenta de GitHub y no otorga permisos a otra persona.

## 25. Archivo `infraestructura/views_busqueda.py`

```python
from django.db.models import Q
from django.shortcuts import render

from .models import NodoServidor


def buscar_servidores(request):
    termino = request.GET.get('q', '').strip()
    resultados = NodoServidor.objects.none()
    if termino:
        resultados = NodoServidor.objects.filter(
            Q(nombre_host__icontains=termino) | Q(direccion_ip__icontains=termino)
        )
    return render(request, 'infraestructura/buscar_servidores.html', {
        'termino': termino,
        'resultados': resultados,
    })
```

### Explicación del código

- `from django.db.models import Q`: importa `Q`, que permite construir condiciones de consulta y combinarlas con operadores lógicos.
- `from django.shortcuts import render`: importa la función que genera una respuesta utilizando una plantilla.
- `from .models import NodoServidor`: importa el modelo de servidores.
- `def buscar_servidores(request)`: define la vista encargada de procesar la búsqueda.
- `request.GET.get('q', '')`: obtiene el parámetro `q` de la URL. Si no existe, utiliza una cadena vacía.
- `.strip()`: elimina espacios al principio y al final del texto ingresado.
- `NodoServidor.objects.none()`: crea un conjunto de consulta vacío, de modo que inicialmente no se muestran resultados.
- `if termino:` comprueba que el usuario haya ingresado un criterio de búsqueda.
- `NodoServidor.objects.filter(...)`: filtra los servidores que coinciden con el criterio.
- `Q(nombre_host__icontains=termino)`: busca el texto en el hostname sin distinguir entre mayúsculas y minúsculas.
- `Q(direccion_ip__icontains=termino)`: busca el texto en la dirección IP.
- `|`: combina las condiciones con un operador lógico OR; un servidor coincide si satisface al menos una.
- `render(...)`: devuelve la plantilla `infraestructura/buscar_servidores.html`.
- `'termino': termino`: envía el criterio de búsqueda a la plantilla.
- `'resultados': resultados`: envía el conjunto de resultados a la plantilla.

## 26. Plantilla `infraestructura/templates/infraestructura/buscar_servidores.html`

```html
{% extends 'infraestructura/base.html' %}
{% block title %}Buscar servidores{% endblock %}
{% block content %}
<h1 class="text-primary mb-4">Buscar Servidores</h1>
<form method="get" class="row g-2 mb-4">
    <div class="col-md-9">
        <input type="text" name="q" value="{{ termino }}" class="form-control"
               placeholder="Hostname o dirección IP">
    </div>
    <div class="col-md-3">
        <button type="submit" class="btn btn-primary w-100">Buscar</button>
    </div>
</form>

{% if termino %}
<p class="text-muted">{{ resultados.count }} resultado(s) para "<strong>{{ termino }}</strong>"</p>
<table class="table table-striped table-hover bg-white shadow-sm rounded">
    <thead class="table-dark">
        <tr>
            <th>Hostname</th>
            <th>Dirección IP</th>
            <th>Estado</th>
        </tr>
    </thead>
    <tbody>
        {% for nodo in resultados %}
        <tr>
            <td><a href="{% url 'detalle_servidor' nodo.pk %}" class="fw-bold text-decoration-none">{{ nodo.nombre_host }}</a></td>
            <td>{{ nodo.direccion_ip }}</td>
            <td>
                {% if nodo.en_produccion %}
                <span class="badge bg-success">Producción</span>
                {% else %}
                <span class="badge bg-warning text-dark">Mantenimiento</span>
                {% endif %}
            </td>
        </tr>
        {% empty %}
        <tr><td colspan="3" class="text-center text-muted py-4">Sin coincidencias.</td></tr>
        {% endfor %}
    </tbody>
</table>
{% endif %}
{% endblock %}
```

### Explicación del código

- `{% extends 'infraestructura/base.html' %}` reutiliza la plantilla base.
- `{% block title %}` establece el título de la página.
- `{% block content %}` abre el contenido principal.
- `<form method="get">` crea un formulario que envía los datos mediante el método GET.
- `<input type="text" name="q">` crea el campo donde se escribe el hostname o la dirección IP. El atributo `name="q"` permite que Django reciba el texto como el parámetro `q`.
- `value="{{ termino }}"` conserva el término enviado en el contexto.
- `placeholder="Hostname o dirección IP"` muestra una indicación dentro del campo.
- `<button type="submit">Buscar</button>` permite enviar el formulario.
- `{% if termino %}` muestra la sección de resultados únicamente cuando hay un criterio de búsqueda.
- `{{ resultados.count }}` presenta la cantidad de resultados.
- `<table>` estructura los resultados en una tabla.
- `<thead>` contiene los encabezados de la tabla.
- `<tbody>` contiene las filas de servidores.
- `{% for nodo in resultados %}` recorre los registros encontrados.
- `{% url 'detalle_servidor' nodo.pk %}` genera el enlace al detalle del servidor usando el nombre de ruta y la clave primaria del registro.
- `{{ nodo.nombre_host }}` muestra el hostname.
- `{{ nodo.direccion_ip }}` muestra la dirección IP.
- `{% if nodo.en_produccion %}` comprueba si el servidor está en producción.
- `{% else %}` presenta el estado alternativo cuando no está en producción.
- `{% empty %}` muestra un mensaje cuando el conjunto de resultados no contiene registros.
- `{% endif %}`, `{% endfor %}` y `{% endblock %}` cierran las estructuras de control y el bloque de plantilla.

## 27. Archivo `infraestructura/test_busqueda.py`

```python
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
```

### Explicación

- `TestCase`: proporciona el entorno de pruebas de Django.
- `reverse`: obtiene la URL asociada a `buscar_servidores`.
- `NodoServidor`: modelo utilizado para crear los registros de prueba.
- `class BusquedaTests(TestCase)`: agrupa las pruebas del buscador.
- `setUp(self)`: método que Django ejecuta antes de cada prueba de esta clase.
- Los dos `objects.create(...)` crean los servidores `web-01` y `db-01` con direcciones IP diferentes.
- `test_busca_por_hostname`: verifica la búsqueda por hostname.
- `self.client.get(reverse('buscar_servidores'), {'q': 'web'})`: realiza una solicitud GET enviando el parámetro `q` con el valor `web`.
- `self.assertEqual(respuesta.status_code, 200)`: comprueba que la vista responda correctamente.
- `self.assertEqual(respuesta.context['resultados'].count(), 1)`: comprueba que la búsqueda devuelva un resultado.
- `test_sin_termino_no_devuelve_resultados`: verifica el comportamiento cuando no se proporciona un criterio.
- `self.client.get(reverse('buscar_servidores'))`: accede a la vista sin parámetros de búsqueda.
- `self.assertEqual(respuesta.context['resultados'].count(), 0)`: comprueba que el conjunto de resultados esté vacío.

## 28. Primer commit del buscador

```bash
git add .
git commit --author="Compañero Dev <dev@example.com>" -m "feat(busqueda): agrega vista de búsqueda por hostname o IP"
```

**`git add .`**

Prepara los cambios del buscador para registrarlos.

**`git commit --author="Compañero Dev <dev@example.com>" -m "feat(busqueda): agrega vista de búsqueda por hostname o IP"`**

Crea un commit que registra la vista y los cambios preparados.

- `--author="Compañero Dev <dev@example.com>"`: establece los datos de autor indicados en el comando.
- `-m`: proporciona el mensaje descriptivo.
- `feat(busqueda)`: indica una funcionalidad nueva relacionada con la búsqueda.

El autor es un dato de metadatos del commit; el comando no demuestra por sí solo que otra persona haya ejecutado el trabajo.

## 29. Agregar la ruta del buscador

Al final de `urls.py` se agrega:

```python
from .views_busqueda import buscar_servidores
urlpatterns.append(path('buscar/', buscar_servidores, name='buscar_servidores'))
```

- `from .views_busqueda import buscar_servidores`: importa la vista del buscador.
- `urlpatterns.append(...)`: añade la ruta a la configuración.
- `path('buscar/', ...)`: define el segmento `buscar/`.
- `buscar_servidores`: indica qué vista atenderá las solicitudes.
- `name='buscar_servidores'`: permite referenciar la ruta por su nombre desde pruebas y plantillas.

En `base.html`, debajo del enlace de Mantenimientos, se agrega:

```html
<a class="nav-link" href="{% url 'buscar_servidores' %}">Buscar</a>
```

- `<a>` crea el enlace.
- `class="nav-link"` aplica la clase de navegación.
- `{% url 'buscar_servidores' %}` obtiene la URL a partir de su nombre.
- `Buscar` es el texto que verá el usuario.

## 30. Segundo commit del buscador

```bash
git add .
git commit --author="Brayan Fuertes < fuerran789@udenar.edu.co>" -m "feat(busqueda): registra la ruta y el enlace en el menú"
git push -u origin feature/buscador-servidores
```

**`git add .`** prepara los cambios de rutas y navegación.

**`git commit --author="Brayan Fuertes < fuerran789@udenar.edu.co>" -m "feat(busqueda): registra la ruta y el enlace en el menú"`** registra los cambios y utiliza los datos de autor especificados en el comando.

Se conserva el comando de la guía original. El campo de autor contiene un espacio después de `<`; si se pretende que el autor se reconozca correctamente, debe verificarse el formato de los metadatos, sin modificar el comando documentado de la demostración.

**`git push -u origin feature/buscador-servidores`** publica la rama del buscador en GitHub y establece su seguimiento remoto.

---

## 31. Sincronizar y resolver el conflicto

La guía indica que el conflicto se resuelve en la rama de la funcionalidad y no directamente en `develop`. De esta manera, la resolución se verifica antes de integrar el buscador en la rama de integración.

### Incorporar los cambios de `develop`

```bash
git merge develop
```

Este comando intenta integrar los cambios de `develop` en la rama actual, que es `feature/buscador-servidores`.

Como las dos funcionalidades modificaron zonas compartidas de `urls.py` y `base.html`, Git puede mostrar conflictos de contenido.

### Identificar los archivos en conflicto

```bash
git status
git diff --name-only --diff-filter=U
```

**`git status`**

Muestra el estado del repositorio y los archivos que requieren resolución.

**`git diff --name-only --diff-filter=U`**

- `git diff`: consulta diferencias.
- `--name-only`: muestra únicamente los nombres de los archivos.
- `--diff-filter=U`: filtra los archivos que se encuentran sin resolver (*unmerged*).

Estos comandos permiten identificar los archivos que requieren intervención.

### Entender los marcadores del conflicto

Dentro de un archivo en conflicto pueden aparecer marcadores como:

```text
<<<<<<< HEAD
Cambios de la rama actual
=======
Cambios procedentes de develop
>>>>>>> develop
```

- `<<<<<<< HEAD` marca el comienzo de la versión correspondiente a la rama actual.
- `=======` separa las dos versiones.
- `>>>>>>> develop` marca el final del bloque que procede de `develop`.

En este escenario, la parte de `HEAD` contiene los cambios del buscador y la parte de `develop` contiene los cambios de estadísticas.

No se deben conservar los marcadores en el archivo final. Se deben eliminar y mantener ambos bloques de funcionalidad.

### Resolución de `urls.py`

El contenido que debe quedar, según la guía, incluye las dos rutas:

```python
from .views_busqueda import buscar_servidores
urlpatterns.append(path('buscar/', buscar_servidores, name='buscar_servidores'))
from .views_estadisticas import estadisticas
urlpatterns.append(path('estadisticas/', estadisticas, name='estadisticas'))
```

La finalidad es conservar tanto la ruta del buscador como la de estadísticas.

### Resolución de `base.html`

El contenido de navegación queda así:

```html
<a class="nav-link" href="{% url 'lista_mantenimientos' %}">Mantenimientos</a>
<a class="nav-link" href="{% url 'buscar_servidores' %}">Buscar</a>
<a class="nav-link" href="{% url 'estadisticas' %}">Estadísticas</a>
```

Se mantienen los tres enlaces:

- `lista_mantenimientos`: conduce a la sección de mantenimientos.
- `buscar_servidores`: conduce al buscador.
- `estadisticas`: conduce al panel de estadísticas.

La resolución conserva las funcionalidades de ambas ramas en el menú.

### Verificar que no queden marcadores

```bash
git grep -n -E "^(<<<<<<<|=======|>>>>>>>)" -- infraestructura/ ; echo "(sin salida = limpio)"
python manage.py test
git add .
git commit -m "merge: resuelve conflicto con develop (ruta y menú de estadísticas y búsqueda)"
```

**`git grep -n -E "^(<<<<<<<|=======|>>>>>>>)" -- infraestructura/ ; echo "(sin salida = limpio)"`**

- `git grep`: busca texto en los archivos que Git conoce.
- `-n`: muestra los números de línea donde se encuentran las coincidencias.
- `-E`: habilita expresiones regulares extendidas.
- `"^(<<<<<<<|=======|>>>>>>>)"`: busca líneas que comiencen con los marcadores del conflicto.
- `-- infraestructura/`: limita la búsqueda al directorio `infraestructura/`.
- `;`: separa dos comandos para ejecutarlos consecutivamente en la misma línea.
- `echo "(sin salida = limpio)"`: imprime un mensaje orientativo después de la búsqueda.

Si la búsqueda no encuentra marcadores, no se mostrarán coincidencias. El texto de `echo` se imprime independientemente de si la búsqueda encuentra coincidencias, por lo que debe revisarse la salida de la búsqueda para confirmar que realmente no queden marcadores.

**`python manage.py test`**

Ejecuta las pruebas automatizadas para comprobar que la resolución del conflicto no haya roto las funcionalidades.

**`git add .`**

Prepara los archivos que se han resuelto.

**`git commit -m "merge: resuelve conflicto con develop (ruta y menú de estadísticas y búsqueda)"`**

Registra la resolución del conflicto en un commit. El mensaje identifica los archivos compartidos y las funcionalidades que se conservaron.

La guía espera que se ejecuten seis pruebas en este punto. El número real depende de las pruebas detectadas por Django y de que los archivos estén configurados correctamente.

### ¿Qué hacer si la resolución sale mal?

```bash
git merge --abort
```

Este comando cancela el merge en curso y devuelve el repositorio al estado anterior al intento de integración, siempre que Git pueda reconstruir ese estado. Se utiliza como alternativa si la resolución se complica.

### Integrar el buscador en `develop`

Una vez resuelto el conflicto y verificado el resultado, se integra la rama del buscador:

```bash
git switch develop
git merge --no-ff feature/buscador-servidores -m "merge: feature/buscador-servidores en develop"
git push origin develop
git branch -D feature/buscador-servidores
git push origin --delete feature/buscador-servidores
```

**`git switch develop`**

Cambia a la rama de integración.

**`git merge --no-ff feature/buscador-servidores -m "merge: feature/buscador-servidores en develop"`**

Integra el buscador en `develop` y crea un commit de merge para mantener visible la integración.

**`git push origin develop`**

Publica la rama de integración actualizada.

**`git branch -D feature/buscador-servidores`**

Elimina la rama local. A diferencia de `-d`, la opción `-D` fuerza la eliminación aunque Git no considere que todos sus cambios estén integrados. En este escenario debe ejecutarse únicamente después de comprobar que la integración fue correcta.

**`git push origin --delete feature/buscador-servidores`**

Elimina la rama remota de GitHub.

---

# FASE 5. Release `1.0.0`

## 32. Crear la rama de lanzamiento

```bash
git switch -c release/1.0.0 develop
```

Crea la rama `release/1.0.0` a partir de `develop` y cambia a ella.

Esta rama se utiliza para preparar la versión inicial estable. En esta fase se registran la versión y el historial de cambios del lanzamiento.

## 33. Archivo `VERSION`

Se crea el archivo `VERSION` en la raíz del proyecto con una sola línea:

```text
1.0.0
```

Este archivo contiene el número de versión que se está preparando. En este caso, `1.0.0` identifica el primer lanzamiento de la aplicación.

La guía indica editar el archivo directamente y no utilizar `echo` para crearlo, con el fin de evitar posibles diferencias en el contenido generado según el entorno.

## 34. Archivo `CHANGELOG.md`

Se crea el archivo con el siguiente contenido:

```markdown
# Changelog

## [1.0.0] - 2026-10-16
### Added
- Endpoint de monitoreo `/health/`.
- Panel de estadísticas de la flota (`/estadisticas/`).
- Búsqueda de servidores por hostname o IP (`/buscar/`).
```

### Explicación

- `# Changelog`: título del registro de cambios.
- `## [1.0.0] - 2026-10-16`: identifica la versión y la fecha documentada para el lanzamiento.
- `### Added`: agrupa las funcionalidades añadidas.
- La lista documenta el endpoint de monitoreo, el panel de estadísticas y la búsqueda.

`CHANGELOG.md` permite conocer qué se incorporó en una versión sin tener que inspeccionar cada commit.

La fecha se conserva tal como aparece en la guía original.

## 35. Registrar la preparación de la versión

```bash
git add .
git commit -m "chore(release): prepara la versión 1.0.0"

git switch main
git merge --no-ff release/1.0.0 -m "merge: release 1.0.0 en main"
git tag -a v1.0.0 -m "Versión 1.0.0"

git switch develop
git merge --no-ff release/1.0.0 -m "merge: release 1.0.0 de vuelta en develop"
git branch -d release/1.0.0

git push origin main develop --tags
```

### Explicación línea por línea

**`git add .`**

Prepara los archivos nuevos o modificados, incluyendo `VERSION` y `CHANGELOG.md`.

**`git commit -m "chore(release): prepara la versión 1.0.0"`**

Registra los cambios de preparación del lanzamiento. El prefijo `chore(release)` indica que se trata de una tarea de mantenimiento asociada a una versión.

**`git switch main`**

Cambia a la rama estable.

**`git merge --no-ff release/1.0.0 -m "merge: release 1.0.0 en main"`**

Integra la rama de lanzamiento en `main`. La opción `--no-ff` conserva un commit de merge visible y `-m` define su mensaje.

**`git tag -a v1.0.0 -m "Versión 1.0.0"`**

Crea una etiqueta anotada llamada `v1.0.0`.

- `tag`: administra etiquetas del historial.
- `-a`: crea una etiqueta anotada.
- `v1.0.0`: es el nombre de la etiqueta.
- `-m`: añade el mensaje de la etiqueta.

La etiqueta identifica el punto del historial correspondiente a la versión.

**`git switch develop`**

Regresa a la rama de integración.

**`git merge --no-ff release/1.0.0 -m "merge: release 1.0.0 de vuelta en develop"`**

Integra también en `develop` los cambios realizados durante la preparación de la versión.

**`git branch -d release/1.0.0`**

Elimina la rama local de lanzamiento después de integrarla.

**`git push origin main develop --tags`**

Publica las ramas `main` y `develop`, junto con las etiquetas locales, en el remoto `origin`.

### Publicación opcional mediante GitHub CLI

```bash
gh release create v1.0.0 --title "v1.0.0" --notes-file CHANGELOG.md
```

Este comando es opcional y requiere tener instalada y autenticada la herramienta GitHub CLI (`gh`).

- `release create`: crea una publicación de GitHub Releases.
- `v1.0.0`: identifica la etiqueta de la versión.
- `--title "v1.0.0"`: establece el título de la publicación.
- `--notes-file CHANGELOG.md`: utiliza el contenido de `CHANGELOG.md` como notas de la publicación.

La etiqueta Git y la publicación GitHub Release están relacionadas, pero no son lo mismo: la etiqueta identifica un punto del historial; la publicación presenta la versión en la interfaz de GitHub.

---

# FASE 6. Hotfix `1.0.1`

## 36. Reproducir el error de producción

La demostración reproduce un error 500 en `/estadisticas/` cuando no existen servidores registrados. Para no perder la base de datos original, la guía propone renombrarla temporalmente.

```bash
git switch main
mv db.sqlite3 db.sqlite3.bak      # Windows: ren db.sqlite3 db.sqlite3.bak
python manage.py migrate
python manage.py runserver
```

### Explicación línea por línea

**`git switch main`**

Cambia a la rama estable, donde se encuentra la versión publicada antes de la corrección.

**`mv db.sqlite3 db.sqlite3.bak`**

Renombra el archivo de la base de datos SQLite para conservarlo temporalmente como respaldo.

El comentario indica la alternativa para Windows: `ren db.sqlite3 db.sqlite3.bak`.

Este paso debe ejecutarse con cuidado y desde el directorio donde se encuentre realmente la base de datos. No se debe continuar si el archivo no existe o si no se ha comprobado que se está trabajando sobre la base correcta.

**`python manage.py migrate`**

Aplica las migraciones de Django. Si no existe una base de datos en la ubicación configurada, Django puede crear una nueva y aplicar las migraciones.

**`python manage.py runserver`**

Inicia el servidor de desarrollo de Django para probar la aplicación en el navegador.

A continuación, se abre:

`http://127.0.0.1:8000/estadisticas/`

La guía espera que aparezca `ZeroDivisionError: division by zero`, porque la vista intenta dividir por el total de servidores, que es cero en la base de datos vacía.

## 37. Crear la rama `hotfix/1.0.1`

```bash
git switch -c hotfix/1.0.1 main
```

Crea la rama `hotfix/1.0.1` a partir de `main` y cambia a ella.

El `hotfix` nace de la rama estable, no de `develop`, porque su objetivo es corregir un error de la versión publicada sin incorporar funcionalidades que todavía estén en desarrollo.

## 38. Corregir `infraestructura/views_estadisticas.py`

La línea original es:

```python
porcentaje_produccion = round(en_produccion * 100 / total)
```

Se sustituye por:

```python
porcentaje_produccion = round(en_produccion * 100 / total) if total else 0
```

### Explicación

En la línea original, Python calcula el porcentaje dividiendo la cantidad de servidores en producción entre el total de servidores. Si `total` es cero, se produce `ZeroDivisionError`.

En la línea corregida se utiliza una expresión condicional:

- Si `total` tiene un valor distinto de cero, se calcula el porcentaje como antes.
- Si `total` es cero, el resultado se establece en `0`.

Esto evita la división por cero y permite que el panel responda cuando la flota todavía no tiene servidores registrados.

## 39. Agregar una prueba de regresión en `test_estadisticas.py`

Al final de la clase `EstadisticasTests` se agrega:

```python
    def test_sin_servidores_no_falla(self):
        respuesta = self.client.get(reverse('estadisticas'))

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context['porcentaje_produccion'], 0)
```

### Explicación

- `def test_sin_servidores_no_falla(self):` define una prueba que verifica que la vista funcione cuando no hay servidores.
- `self.client.get(reverse('estadisticas'))` simula una solicitud HTTP GET a la página de estadísticas.
- `self.assertEqual(respuesta.status_code, 200)` comprueba que la vista responda correctamente.
- `self.assertEqual(respuesta.context['porcentaje_produccion'], 0)` comprueba que el porcentaje sea cero cuando no hay servidores.

Esta es una **prueba de regresión** porque verifica que el error corregido no vuelva a aparecer en futuras modificaciones.

## 40. Ejecutar las pruebas y registrar la corrección

```bash
python manage.py test
git add .
git commit -m "fix(estadisticas): evita división por cero cuando no hay servidores"
```

**`python manage.py test`**

Ejecuta las pruebas automatizadas para comprobar la corrección y verificar que no se hayan introducido otros errores.

**`git add .`**

Prepara los cambios del código y de las pruebas.

**`git commit -m "fix(estadisticas): evita división por cero cuando no hay servidores"`**

Registra la corrección con un mensaje descriptivo. El prefijo `fix` indica que el cambio soluciona un error.

## 41. Actualizar `VERSION` y `CHANGELOG.md`

El archivo `VERSION` cambia a:

```text
1.0.1
```

Debajo de `# Changelog` en `CHANGELOG.md` se agrega:

```markdown
## [1.0.1] - 2026-10-16
### Fixed
- Error 500 en `/estadisticas/` cuando no hay servidores registrados.
```

### Explicación

- `1.0.1` identifica la versión que contiene la corrección.
- `## [1.0.1] - 2026-10-16` registra el número y la fecha de la versión.
- `### Fixed` agrupa los errores corregidos.
- La lista describe el error 500 que ocurría en `/estadisticas/` cuando no había servidores.

## 42. Cerrar el `hotfix` e integrar la corrección

```bash
git add .
git commit -m "chore(release): sube la versión a 1.0.1"

git switch main
git merge --no-ff hotfix/1.0.1 -m "merge: hotfix 1.0.1 en main"
git tag -a v1.0.1 -m "Hotfix 1.0.1"

git switch develop
git merge --no-ff hotfix/1.0.1 -m "merge: hotfix 1.0.1 de vuelta en develop"
git branch -d hotfix/1.0.1

git push origin main develop --tags

# restaura tu BD
mv db.sqlite3.bak db.sqlite3
```

### Explicación línea por línea

**`git add .`**

Prepara los cambios pendientes, incluidos los archivos de versión y documentación.

**`git commit -m "chore(release): sube la versión a 1.0.1"`**

Registra la actualización de versión. El prefijo `chore(release)` indica que el cambio corresponde a la preparación del lanzamiento.

**`git switch main`**

Cambia a la rama estable.

**`git merge --no-ff hotfix/1.0.1 -m "merge: hotfix 1.0.1 en main"`**

Integra la corrección en `main`, conservando un commit de merge visible.

**`git tag -a v1.0.1 -m "Hotfix 1.0.1"`**

Crea la etiqueta anotada `v1.0.1`, que identifica la versión que contiene el arreglo.

**`git switch develop`**

Cambia a la rama de integración.

**`git merge --no-ff hotfix/1.0.1 -m "merge: hotfix 1.0.1 de vuelta en develop"`**

Integra la corrección en `develop`. Es importante porque la rama de desarrollo debe conservar el arreglo para evitar que el mismo error reaparezca en una versión futura.

**`git branch -d hotfix/1.0.1`**

Elimina la rama local de corrección después de integrarla en ambas ramas.

**`git push origin main develop --tags`**

Publica las ramas `main` y `develop`, así como las etiquetas locales, en GitHub.

**`# restaura tu BD`**

Es un comentario que explica la finalidad de la siguiente instrucción.

**`mv db.sqlite3.bak db.sqlite3`**

Restaura el archivo de base de datos que se había renombrado al inicio de la demostración.

La restauración debe realizarse cuando ya no se necesite la base de datos vacía de prueba. Debe verificarse la existencia de ambos archivos antes de ejecutar el comando, para evitar sobrescribir o perder datos.

---

# FASE 7. Verificación final

## 43. Comprobar el historial, las ramas, las etiquetas y las pruebas

```bash
git log --graph --oneline --all --decorate
git branch -a
git tag
python manage.py test        # 7 tests, OK
```

### Explicación línea por línea

**`git log --graph --oneline --all --decorate`**

Muestra el historial del repositorio de forma resumida y gráfica.

- `git log`: consulta el historial de commits.
- `--graph`: dibuja las conexiones entre los commits y los merges.
- `--oneline`: muestra cada commit en una sola línea.
- `--all`: incluye todas las referencias de ramas conocidas.
- `--decorate`: muestra nombres de ramas y etiquetas junto a los commits correspondientes.

Este comando es especialmente útil para la exposición porque permite visualizar las ramas de GitFlow, las integraciones y las versiones.

**`git branch -a`**

Muestra las ramas locales y las referencias de ramas remotas conocidas.

Permite comprobar si aparecen `main`, `develop` y las referencias remotas correspondientes.

**`git tag`**

Muestra las etiquetas existentes en el repositorio. En esta demostración se espera encontrar `v1.0.0` y `v1.0.1`.

**`python manage.py test        # 7 tests, OK`**

Ejecuta las pruebas automatizadas de Django. El comentario indica el resultado esperado de la guía: siete pruebas correctas.

El número y el resultado deben comprobarse con la salida real del comando. Si las pruebas fallan, se deben revisar los errores antes de dar por finalizada la demostración.

### Resultado esperado

Al finalizar, se espera tener:

- Las ramas `main` y `develop` publicadas en el repositorio remoto.
- Las etiquetas `v1.0.0` y `v1.0.1`.
- El historial con los commits de las funcionalidades y los merges.
- El conflicto resuelto entre las estadísticas y el buscador.
- La corrección del error de división por cero.
- Las pruebas automatizadas ejecutadas correctamente.

---

# 44. Resumen de los comandos de Git utilizados

| Comando | Explicación |
|---|---|
| `git --version` | Muestra la versión de Git instalada. |
| `git config --global user.name` | Configura el nombre del autor para los commits. |
| `git config --global user.email` | Configura el correo asociado al autor de los commits. |
| `git config --global init.defaultBranch main` | Define `main` como rama inicial predeterminada para nuevos repositorios. |
| `git init` | Inicializa el repositorio Git. |
| `git branch -M main` | Renombra la rama actual a `main`, forzando el cambio si hace falta. |
| `git add .` | Prepara los cambios para el siguiente commit. |
| `git status` | Muestra el estado del repositorio. |
| `git commit -m "mensaje"` | Registra los cambios preparados con un mensaje. |
| `git remote add origin URL` | Registra el repositorio remoto con el nombre `origin`. |
| `git push -u origin main` | Publica `main` y configura su seguimiento remoto. |
| `git switch -c develop` | Crea `develop` a partir de la rama actual y cambia a ella. |
| `git switch -c rama base` | Crea una rama desde la base indicada y cambia a ella. |
| `git switch rama` | Cambia a una rama existente. |
| `git merge rama` | Integra los cambios de otra rama en la rama actual. |
| `git merge --no-ff rama` | Integra una rama creando un commit de merge aunque sea posible un avance directo. |
| `git branch -d rama` | Elimina una rama local si Git considera que sus cambios están integrados. |
| `git branch -D rama` | Fuerza la eliminación de una rama local. |
| `git push origin develop` | Publica la rama `develop` en el remoto. |
| `git push origin --delete rama` | Elimina la rama remota indicada. |
| `git push origin main develop --tags` | Publica ambas ramas y las etiquetas locales. |
| `git tag -a v1.0.0 -m "mensaje"` | Crea una etiqueta anotada para identificar una versión. |
| `git log --graph --oneline --all` | Muestra el historial resumido y las conexiones entre ramas. |
| `git log --graph --oneline --all --decorate` | Muestra el historial, los merges y las referencias de ramas y etiquetas. |
| `git branch -a` | Muestra las ramas locales y remotas conocidas. |
| `git tag` | Muestra las etiquetas del repositorio. |
| `git merge --abort` | Cancela el merge en curso y vuelve al estado anterior cuando es posible. |
| `git grep -n -E ...` | Busca patrones en los archivos que conoce Git y muestra las líneas coincidentes. |

---
