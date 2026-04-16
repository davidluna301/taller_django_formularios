from django.urls import path

from . import views

app_name = 'david_formulario'

urlpatterns = [
    path('', views.solicitud_registro, name='solicitud_registro'),
    path('confirmacion/', views.solicitud_confirmacion, name='solicitud_confirmacion'),
]
