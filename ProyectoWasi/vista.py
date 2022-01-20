
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from propiedades.models import Propiedad,TipoPropiedad
from usuarios.models import Usuario


def inicio(request):
    obj_propiedades = Propiedad.objects.select_related('host')
    obj_tipo = TipoPropiedad.objects.all()
    return render(request, "home.html", {"propiedades": obj_propiedades,"tipos":obj_tipo})


def contacto(request):
    return render(request, "contacto.html")


def about(request):
    return render(request, "sobreNosotros.html")


def listadoPropiedad(request):
    obj_propiedades = Propiedad.objects.select_related('host')
    return render(request, "propiedades.html", {"propiedades": obj_propiedades})

