from django.urls import path
from . import views

app_name = "conversaciones"

urlpatterns = [
    path("ir/<int:a_pk>/<int:b_pk>", views.ir_conversacion, name="ir"),
    path("<int:pk>/", views.ConversacionDetalleVista.as_view(), name="detail"),
]
