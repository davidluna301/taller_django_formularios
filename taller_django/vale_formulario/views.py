from django.shortcuts import redirect, render

from .forms import AsistenciaForm


def asistencia_registro(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vale_formulario:asistencia_confirmacion')
    else:
        form = AsistenciaForm()

    return render(request, 'vale_formulario/asistencia_form.html', {'form': form})


def asistencia_confirmacion(request):
    return render(request, 'vale_formulario/asistencia_confirmacion.html')
