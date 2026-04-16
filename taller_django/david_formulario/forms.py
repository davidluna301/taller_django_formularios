from django import forms

from .models import Solicitud


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'nombre_solicitante',
            'documento_identidad',
            'correo_electronico',
            'telefono_contacto',
            'tipo_solicitud',
            'asunto',
            'descripcion_detallada',
            'fecha_solicitud',
            'archivo_adjunto',
        ]
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_detallada': forms.Textarea(attrs={'rows': 5}),
        }
