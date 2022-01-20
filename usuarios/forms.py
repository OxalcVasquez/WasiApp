from django import forms
from .models import Usuario


class FormularioLogin(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Contraseña"}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    'password', forms.ValidationError('Contraseña incorrecta'))
        except Usuario.DoesNotExist:
            self.add_error('email', forms.ValidationError(
                "Usuario no existe"))


class FormularioRegistro(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = {"first_name", "last_name", "email"}
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Nombres"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Apellidos"}),
        }

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Contraseña"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Confirme contraseña"}))
#Verificar existencia email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ingresado ya se encuentra registrado")
        else:
            return email
#Verificar contrasen
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password = self.cleaned_data.get('password')
        if password != password1:
            raise forms.ValidationError("Las contraseñas no coinciden")
        else:
            return password


    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user.username = email
        user.set_password(password)
        user.save()
