import csv
from pathlib import Path

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from taller_django.david_formulario.models import Solicitud
from taller_django.vale_formulario.models import Asistencia


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('panel_admin')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('panel_admin')

    return render(request, 'panel_admin/login.html', {'form': form})


@login_required(login_url='panel_admin_login')
def admin_logout(request):
    logout(request)
    return redirect('panel_admin_login')


@login_required(login_url='panel_admin_login')
def panel_admin(request):
    if not request.user.is_staff:
        raise PermissionDenied()

    asistencias = Asistencia.objects.order_by('-fecha_asistencia', '-id')
    solicitudes = Solicitud.objects.order_by('-fecha_solicitud', '-id')

    context = {
        'asistencias': asistencias,
        'solicitudes': solicitudes,
        'total_asistencias': asistencias.count(),
        'total_solicitudes': solicitudes.count(),
        'solicitudes_con_adjunto': solicitudes.exclude(archivo_adjunto='').exclude(archivo_adjunto__isnull=True).count(),
    }
    return render(request, 'panel_admin/dashboard.html', context)


@login_required(login_url='panel_admin_login')
def descargar_asistencias_csv(request):
    if not request.user.is_staff:
        raise PermissionDenied()

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="asistencias.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'Nombre completo',
        'Documento',
        'Correo',
        'Fecha asistencia',
        'Hora ingreso',
        'Hora salida',
        'Presente',
        'Observaciones',
    ])

    for asistencia in Asistencia.objects.order_by('-fecha_asistencia', '-id'):
        writer.writerow([
            asistencia.id,
            asistencia.nombre_completo,
            asistencia.documento_identidad,
            asistencia.correo_electronico,
            asistencia.fecha_asistencia,
            asistencia.hora_ingreso,
            asistencia.hora_salida,
            'Si' if asistencia.presente else 'No',
            asistencia.observaciones,
        ])

    return response


@login_required(login_url='panel_admin_login')
def descargar_solicitudes_csv(request):
    if not request.user.is_staff:
        raise PermissionDenied()

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="solicitudes.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'Solicitante',
        'Documento',
        'Correo',
        'Telefono',
        'Tipo',
        'Asunto',
        'Descripcion',
        'Fecha solicitud',
        'Adjunto',
    ])

    for solicitud in Solicitud.objects.order_by('-fecha_solicitud', '-id'):
        writer.writerow([
            solicitud.id,
            solicitud.nombre_solicitante,
            solicitud.documento_identidad,
            solicitud.correo_electronico,
            solicitud.telefono_contacto,
            solicitud.get_tipo_solicitud_display(),
            solicitud.asunto,
            solicitud.descripcion_detallada,
            solicitud.fecha_solicitud,
            request.build_absolute_uri(solicitud.archivo_adjunto.url) if solicitud.archivo_adjunto else '',
        ])

    return response


@login_required(login_url='panel_admin_login')
def descargar_adjunto_solicitud(request, solicitud_id):
    if not request.user.is_staff:
        raise PermissionDenied()

    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    if not solicitud.archivo_adjunto:
        raise Http404('La solicitud no tiene archivo adjunto.')

    return FileResponse(
        solicitud.archivo_adjunto.open('rb'),
        as_attachment=True,
        filename=Path(solicitud.archivo_adjunto.name).name,
    )