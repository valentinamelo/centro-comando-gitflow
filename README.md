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