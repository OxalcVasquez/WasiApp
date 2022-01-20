from django import forms
from django_countries.fields import CountryField
from .models import Propiedad,FotosPropiedad


class RegistroFotosForm(forms.ModelForm):
    class Meta:
        model = FotosPropiedad
        fields = ('descripcion', 'archivo')

    def save(self, pk, *args, **kwargs):
        fotos = super().save(commit=False)
        fotos.propiedad = Propiedad.objects.get(pk=pk)
        fotos.save()



class RegistroPropiedadForm(forms.ModelForm):
    class Meta:
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

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
