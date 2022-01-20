from django.urls import path
from . import views

app_name = "propiedades"

urlpatterns = [
    path('registrar/', views.RegistroPropiedadVista.as_view(), name='registrar'),
    path("tipoPropiedad/", views.detalleTipo, name="tipo"),
    path("<int:pk>/", views.PropiedadDetail.as_view(), name="detail"),
    path("<int:pk>/editar/", views.EditarPropiedadVista.as_view(), name="editar"),
    path("<int:pk>/fotos/", views.PropiedadFotosVista.as_view(), name="fotos"),
    path("<int:pk>/fotos/add", views.AddFotoVista.as_view(), name="add-foto"),
    path("<int:propiedad_pk>/fotos/<int:foto_pk>/eliminar/",
         views.eliminar_foto, name="eliminar-foto"),
    path("<int:propiedad_pk>/fotos/<int:foto_pk>/editar/",
         views.EditarFotosVista.as_view(), name="edit-foto"),
    path("tipo/<str:tipo>", views.propiedadPorTipo, name="tipoPropiedad"),
    path("busqueda/", views.buscarPropiedad, name="busqueda"),
]
