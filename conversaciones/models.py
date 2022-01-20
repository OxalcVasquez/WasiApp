from django.db import models
from administracion.models import TimeStampedModel
# Create your models here.


class Conversacion(TimeStampedModel):
    participantes = models.ManyToManyField(
        "usuarios.Usuario", related_name="conversacion", blank=True
    )

    def __str__(self):
        usernames = []
        for usuario in self.participantes.all():
            usernames.append(usuario.first_name+" "+usuario.last_name)
        return " y ".join(usernames)

    def contar_mensajes(self):
        return self.mensajes.count()

    contar_mensajes.descripcion_corta = "Número mensajes"

    def contar_participantes(self):
        return self.participantes.count()


    contar_participantes.descripcion_corta = "Numero participanes"


class Mensajes(TimeStampedModel):
    mensaje = models.TextField()
    usuario = models.ForeignKey(
        "usuarios.Usuario", related_name="mensajes", on_delete=models.CASCADE
    )
    conversacion = models.ForeignKey(
        "Conversacion", related_name="mensajes", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.usuario} says: {self.mensaje}"
