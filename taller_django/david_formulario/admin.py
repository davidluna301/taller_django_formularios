from django.contrib import admin

from .models import Solicitud


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('nombre_solicitante', 'tipo_solicitud', 'fecha_solicitud')
    search_fields = ('nombre_solicitante', 'documento_identidad', 'correo_electronico', 'asunto')
    list_filter = ('tipo_solicitud', 'fecha_solicitud')
