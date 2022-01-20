from django.contrib import messages
from django.shortcuts import redirect, reverse
from propiedades.models import Propiedad
from . import forms


def crear_resena(request, propiedad):
    if request.method == "POST":
        form = forms.CrearResenaForm(request.POST)
        propiedad = Propiedad.objects.get(pk=propiedad)
        if not propiedad:
            return redirect(reverse("home"))
        if form.is_valid():
            resena = form.save()
            resena.propiedad = propiedad
            resena.usuario = request.user
            resena.save()
            messages.success(request, "Propiedad reseñada")
            return redirect(reverse("propiedades:detail", kwargs={"pk": propiedad.pk}))
