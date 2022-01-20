from django.contrib import admin
from .models import Reserva, DiaReserva
# Register your models here.


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'propiedad', 'estado', 'check_in',
                    'check_out', 'huesped', 'en_progreso', 'finalizado')
    list_display_links = ('id', 'propiedad', 'estado', 'check_in',
                          'check_out', 'huesped', 'en_progreso', 'finalizado')
    list_filter = ('estado',)


@admin.register(DiaReserva)
class DiaReservaAdmin(admin.ModelAdmin):
    list_display = ('dia', 'reserva')
    list_display_links = ('dia', )
