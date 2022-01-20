from django.contrib import admin
from .models import Resena

# Register your models here.


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'puntaje_pomedio')
