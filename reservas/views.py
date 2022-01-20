import datetime
from django.contrib import messages
from django.http import Http404, request
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.views.generic import View
from reservas.models import DiaReserva, Reserva
from propiedades.models import Propiedad
from usuarios.mixins import LoggedInOnlyView
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from .forms import FromularioA
from resenas.forms import CrearResenaForm

def crearReserva(request, propiedad, anio, mes, dia):
    try:
        obj_fecha = datetime.datetime(year=anio, month=mes, day=dia)
        propiedad = Propiedad.objects.get(pk=propiedad)
        DiaReserva.objects.get(dia=obj_fecha, reserva__propiedad=propiedad)
    except Propiedad.DoesNotExist:
        messages.error(request, "No se puede reservar esta propiedad")
        return redirect(reverse("home"))
    except DiaReserva.DoesNotExist:
        reserva = Reserva.objects.create(huesped=request.user, propiedad=propiedad,check_in=obj_fecha,check_out=obj_fecha + datetime.timedelta(days=1))
        return redirect(reverse("reservas:detail", kwargs={'pk': reserva.pk}))

def EditarReserva(request,pk):
    reserva = Reserva.objects.get(pk=pk)
    return render(request, "reservas/editar_reserva.html",{"reserva":reserva})


def editarReserva(request,pk):
   reserva = Reserva.objects.get(pk=pk)
   if request.method == "POST":
        form = FromularioA(request.POST)
        if form.is_valid():
         fecha = request.POST['check_out'].split('-')
         reserva.check_out = datetime.date(
             year=int(fecha[0]), month=int(fecha[1]), day=int(fecha[2]))
         reserva.update()
        return redirect(reverse("reservas:detail", kwargs={'pk': reserva.pk}))


def cancelarReserva(request, pk):
   reserva = Reserva.objects.get(pk=pk)
   if request.method == "POST":
      reserva.estado = "cancelado";
      reserva.save()
      reserva.cancelar()
      return redirect(reverse("reservas:detail", kwargs={'pk': reserva.pk}))


def confirmarReserva(request, pk):
   reserva = Reserva.objects.get(pk=pk)
   if request.method == "GET":
      reserva.estado = "confirmado"
      reserva.save()
      return redirect(reverse("reservas:detail", kwargs={'pk': reserva.pk}))


class ReservaDetalleVista(View):
    def get(self, request, pk):
        reserva = Reserva.objects.get_or_none(pk=pk)
        if not reserva or (reserva.huesped != request.user and reserva.propiedad.host != request.user):
            raise Http404()
        form = CrearResenaForm()
        return render(request, "reservas/detail.html", {"reserva": reserva, "form": form})
