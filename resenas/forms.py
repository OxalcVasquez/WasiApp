from django import forms
from . import models

class CrearResenaForm(forms.ModelForm):
    comunicacion = forms.IntegerField(max_value=5, min_value=1)
    limpieza = forms.IntegerField(max_value=5, min_value=1)
    locacion =forms.IntegerField(max_value=5, min_value=1)
    check_in = forms.IntegerField(max_value=5, min_value=1)
    precio = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = models.Resena
        fields = (
            "resena",
            "comunicacion",
            "limpieza",
            "locacion",
            "check_in",
            "precio",
        )

    def save(self):
        resena = super().save(commit=False)
        return resena
