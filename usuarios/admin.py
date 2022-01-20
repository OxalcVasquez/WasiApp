from django.contrib import admin
from usuarios.models import Usuario
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'is_active',
        'is_staff', 'is_superuser', 'email_verificado', 'email_secreto', 'login_metodo')
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "genero",
                    "biografia",
                    "fechaNacimiento",
                    "login_metodo",
                )
            },
        ),
    )
