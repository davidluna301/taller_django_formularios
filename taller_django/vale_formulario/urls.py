from django.urls import path

from . import views

app_name = 'vale_formulario'

urlpatterns = [
    path('', views.asistencia_registro, name='asistencia_registro'),
    path('confirmacion/', views.asistencia_confirmacion, name='asistencia_confirmacion'),
]
