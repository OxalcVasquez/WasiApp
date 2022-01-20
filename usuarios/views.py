from django.shortcuts import render
from .models import Usuario
from .forms import FormularioRegistro, FormularioLogin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView, DetailView, UpdateView
from . import mixins
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView

# Create your views here.


class LoginVista(mixins.LoggedOutOnlyView, FormView):
    template_name = 'usuarios/login.html'
    form_class = FormularioLogin

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Bienvenido de vuelta {user.first_name}')
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get('next')
        if next_arg is not None:
            return next_arg
        else:
            return reverse("home")


def logout_vista(request):
    logout(request)
    messages.info(request, "Nos vemos luego")
    return redirect(reverse('home'))



class RegistroVista(mixins.LoggedOutOnlyView, FormView):
    template_name = 'usuarios/registro.html'
    form_class = FormularioRegistro
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        usuario = authenticate(self.request, username=email, password=password)
        if usuario is not None:
            login(self.request, usuario)
            messages.success(self.request, f'Bienvenido {usuario.first_name}')
        usuario.verificar_email()
        return super().form_valid(form)


def completar_verificacion(request, key):
    try:
        user = Usuario.objects.get(email_secreto=key)
        user.email_verificado = True
        user.email_secreto = ""
        user.save()
    except Usuario.DoesNotExist:
        pass
    return redirect(reverse("home"))


class PerfilUsuarioVista(DetailView):
    model = Usuario
    context_object_name = 'user_obj'


class ActualizarPerfilVista(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = Usuario
    fields = ("avatar","email", "first_name", "last_name", "genero", "biografia", "fechaNacimiento")
    template_name = "usuarios/actualizar_perfil.html"

    success_url = reverse_lazy("home")
    success_message = "Perfil Actualizado"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["email"].widget.attrs = {"placeholder": "Email"}
        form.fields["first_name"].widget.attrs = {"placeholder": "Nombre"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Apellidos"}
        form.fields["biografia"].widget.attrs = {"placeholder": "Biografia"}
        form.fields["fechaNacimiento"].widget.attrs = {"placeholder": "Fecha Nacimiento"}
        return form

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        self.object.username = email
        self.object.save()
        return super().form_valid(form)

class ActualizarContrasenaVista(mixins.LoggedInOnlyView, mixins.EmailLoginOnlyView, SuccessMessageMixin, PasswordChangeView):
        template_name = 'usuarios/actualizar_contrasena.html'
        success_message = 'Contraseña actualizada'

        def get_form(self, form_class=None):
            form = super().get_form(form_class=form_class)
            form.fields["old_password"].widget.attrs = {
                "placeholder": "Contraseña actual"}
            form.fields["new_password1"].widget.attrs = {
                "placeholder": "Nueva contraseña"}
            form.fields["new_password2"].widget.attrs = {
                "placeholder": "Confirme contraseña"}
            return form


        def get_success_url(self):
            return self.request.user.get_absolute_url()



@login_required
def switch_hosting(request):
    try:
        del request.session['is_hosting']
    except KeyError:
        request.session['is_hosting'] = True
    return redirect(reverse("home"))
