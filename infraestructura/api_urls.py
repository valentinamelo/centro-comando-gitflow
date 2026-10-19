from rest_framework.routers import DefaultRouter

from .api_views import (
    IncidenciaServidorViewSet,
    NodoServidorViewSet,
    RegistroAuditoriaViewSet,
)


router = DefaultRouter()
router.register('servidores', NodoServidorViewSet, basename='servidor')
router.register('auditorias', RegistroAuditoriaViewSet, basename='auditoria')
router.register('incidencias', IncidenciaServidorViewSet, basename='incidencia')

urlpatterns = router.urls