from django.urls import path
from . import views
app_name = 'usuarios'

urlpatterns = [
    path('signup', views.RegistroVista.as_view(), name='signup'),
    path('login', views.LoginVista.as_view(), name='login'),
    path('switch-hosting/', views.switch_hosting, name='switch-hosting'),
    path('logout', views.logout_vista, name='logout'),
    path('<int:pk>', views.PerfilUsuarioVista.as_view(), name='perfil'),
    path('actualizar-perfil', views.ActualizarPerfilVista.as_view(), name='actualizar'),
    path('actualizar-contrasena',views.ActualizarContrasenaVista.as_view(), name='contrasena'),
    path('verificar/<str:key>', views.completar_verificacion,
         name='verificacion-completa'),
]
