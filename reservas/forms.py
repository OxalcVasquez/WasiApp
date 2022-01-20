from django import forms
from .models import Reserva


class FromularioA(forms.Form):
    check_out = forms.DateField(widget=forms.DateInput())
