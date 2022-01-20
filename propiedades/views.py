from django.shortcuts import render
from .models import FotosPropiedad, Propiedad,TipoPropiedad
from .forms import RegistroFotosForm,RegistroPropiedadForm
from django.contrib import messages
from usuarios.mixins import LoggedInOnlyView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.http import Http404
# Create your views here.


class PropiedadDetail(DetailView):
      model = Propiedad


class EditarPropiedadVista(LoggedInOnlyView, UpdateView):
    model = Propiedad
    fields = (
        "nombre",
        "descripcion",
        "pais",
        "ciudad",
        "precio",
        "direccion",
        "numMaxHuspedes",
        "numCamas",
        "numCuartos",
        "numBano",
        "tipoPropiedad",
        "conInternet",
        "permiteMascotas",
        "conEstacionamiento",
        "conCocina",
        "conSala",
        "conLavanderia",
        "conTvCable",
        "conAireAcondicionado",
        "otrasComodidades",
    )
    template_name = 'propiedades/editar_propiedad.html'

    def get_object(self, queryset=None):
        propiedad = super().get_object(queryset=queryset)
        if propiedad.host.pk != self.request.user.pk:
            raise Http404()
        return propiedad


class PropiedadFotosVista(LoggedInOnlyView, DetailView):
    model = Propiedad
    template_name = 'propiedades/propiedad_fotos.html'

    def get_object(self, queryset=None):
        propiedad = super().get_object(queryset=queryset)
        if propiedad.host.pk != self.request.user.pk:
            raise Http404()
        return propiedad


def detalleTipo(request):
    objTipo = TipoPropiedad.objects.all()
    return render(request, "propiedades/numTipoPropiedad.html", {"tipos": objTipo})


def propiedadPorTipo(request,tipo):
    objTipo = Propiedad.objects.filter(tipoPropiedad=tipo)
    return render(request, "propiedades/propiedadesTipo.html", {"propiedades": objTipo})


def buscarPropiedad(request):
    numCuartos = request.POST.get('numCuartos')
    numBanos = request.POST.get('numBanos')
    numHuespeds = request.POST.get('numHuespeds')
    tipo = request.POST.get('tipoProp')
    propiedades = Propiedad.objects.filter(
        numCuartos=numCuartos, numMaxHuspedes__gte=numHuespeds, numBano__gte=numBanos,tipoPropiedad=tipo)
    return render(request, "propiedades/propiedadesBusqueda.html", {"propiedades": propiedades})


@login_required
def eliminar_foto(request, propiedad_pk, foto_pk):
    user = request.user
    try:
        propiedad = Propiedad.objects.get(pk=propiedad_pk)
        if propiedad.host.pk != user.pk:
            messages.error(request, "No se puede eliminar esta foto")
        else:
            FotosPropiedad.objects.filter(pk=foto_pk).delete()
            messages.success(request, "Foto eliminada")
        return redirect(reverse("propiedades:fotos", kwargs={"pk": propiedad_pk}))
    except Propiedad.DoesNotExist:
        return request(reverse("home"))


class EditarFotosVista(LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = FotosPropiedad
    template_name = 'propiedades/editar_fotos.html'
    fields = ("descripcion","archivo")
    pk_url_kwarg = 'foto_pk'
    success_message = 'Foto Actualizada'

    def get_success_url(self):
        propiedad_pk = self.kwargs.get("propiedad_pk")
        return reverse("propiedades:fotos", kwargs={"pk": propiedad_pk})


class AddFotoVista(LoggedInOnlyView, FormView):
    template_name = 'propiedades/crear_foto.html'
    fields = ('descripcion', 'archivo',)
    form_class = RegistroFotosForm
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        pk = self.kwargs.get('pk')
        form.save(pk)
        messages.success(self.request, "Foto subida correctamenta")
        return redirect(reverse('propiedades:fotos', kwargs={'pk': pk}))

    def form_invalid(self, form, **kwargs):
        pk = self.kwargs.get('pk')
        messages.error(self.request, "Subida Fallida")
        return redirect(reverse('propiedades:fotos', kwargs={'pk': pk}))





class RegistroPropiedadVista(LoggedInOnlyView, FormView):
    form_class = RegistroPropiedadForm
    template_name = 'propiedades/registro_propiedad.html'


    def form_valid(self, form):
        propiedad = form.save()
        propiedad.host = self.request.user
        propiedad.save()
        form.save_m2m()
        messages.success(self.request, 'Propiedad subida')
        return redirect(reverse('propiedades:detail', kwargs={'pk': propiedad.pk}))
