from django import forms


class AgregarComentarioForm(forms.Form):
    mensaje = forms.CharField(
    required=True, widget=forms.TextInput(attrs={"placeholder": "Agregar mensaje"})
)
