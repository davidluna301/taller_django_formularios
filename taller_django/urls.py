from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='inicio.html'), name='inicio'),
    path('asistencia/', include('taller_django.vale_formulario.urls')),
    path('solicitudes/', include('taller_django.david_formulario.urls')),
    path('panel-admin/login/', views.admin_login, name='panel_admin_login'),
    path('panel-admin/logout/', views.admin_logout, name='panel_admin_logout'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('panel-admin/descargas/asistencias/', views.descargar_asistencias_csv, name='descargar_asistencias_csv'),
    path('panel-admin/descargas/solicitudes/', views.descargar_solicitudes_csv, name='descargar_solicitudes_csv'),
    path('panel-admin/descargas/solicitud/<int:solicitud_id>/', views.descargar_adjunto_solicitud, name='descargar_adjunto_solicitud'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)