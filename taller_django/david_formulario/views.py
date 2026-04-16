from django.shortcuts import redirect, render

from .forms import SolicitudForm


def solicitud_registro(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('david_formulario:solicitud_confirmacion')
    else:
        form = SolicitudForm()

    return render(request, 'david_formulario/solicitud_form.html', {'form': form})


def solicitud_confirmacion(request):
    return render(request, 'david_formulario/solicitud_confirmacion.html')
