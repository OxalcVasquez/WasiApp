from django.urls import path
from . import views
app_name = "resenas"
urlpatterns = [path("crear/<int:propiedad>",
                    views.crear_resena, name="crear")]
