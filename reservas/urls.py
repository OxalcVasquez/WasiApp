from django.urls import path

from reservas import views

app_name = "reservas"
urlpatterns = [
    path("crear/<int:propiedad>/<int:anio>-<int:mes>-<int:dia>", views.crearReserva, name="crear"),
    path("<int:pk>", views.ReservaDetalleVista.as_view(), name="detail"),
    # path("<int:pk>/cancelar/", views.cancelarReserva, name="cancelar"),
    path("<int:pk>/editar/", views.EditarReserva, name="editar"),
    path("<int:pk>/editar/actualizar", views.editarReserva, name="actualizar"),
    path("<int:pk>/editar/cancelar", views.cancelarReserva, name="cancelar"),
    path("<int:pk>/editar/confirmar", views.confirmarReserva, name="confirmar"),

]
