from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Mensajes)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created")


@admin.register(models.Conversacion)
class ConversacionAdmin(admin.ModelAdmin):

    list_display = ("__str__", "contar_mensajes", "contar_participantes")
