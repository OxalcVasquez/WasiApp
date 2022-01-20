from django.shortcuts import render
from django.shortcuts import redirect, reverse, render
from django.views.generic import View
from usuarios.models import Usuario
from .models import Conversacion,Mensajes
from django.db.models import Q
from django.http import Http404

# Create your views here.


def ir_conversacion(request, a_pk, b_pk):
    usuario_uno = Usuario.objects.get(pk=a_pk)
    usuario_dos = Usuario.objects.get(pk=b_pk)
    if usuario_uno is not None and usuario_dos is not None:
        try:
            conversacion = Conversacion.objects.get(
                Q(participantes=usuario_uno) & Q(participantes=usuario_dos)
            )
        except Conversacion.DoesNotExist:
            conversacion = Conversacion.objects.create()
            conversacion.participantes.add(usuario_uno, usuario_dos)
        return redirect(reverse("conversaciones:detail", kwargs={"pk": conversacion.pk}))


class ConversacionDetalleVista(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversacion = Conversacion.objects.get(pk=pk)
        if not conversacion:
            raise Http404()
        return render(
            self.request,
            "conversaciones/converacion_detail.html",
            {"conversacion": conversacion},
        )

    def post(self, *args, **kwargs):
        mensaje = self.request.POST.get("mensaje", None)
        pk = kwargs.get("pk")
        conversacion = Conversacion.objects.get(pk=pk)
        if not conversacion:
            raise Http404()
        if mensaje is not None:
            Mensajes.objects.create(
                mensaje=mensaje, usuario=self.request.user, conversacion=conversacion
            )
        return redirect(reverse("conversaciones:detail", kwargs={"pk": pk}))
