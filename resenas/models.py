from django.db import models
from administracion.models import TimeStampedModel

# Create your models here.


class Resena(TimeStampedModel):
      resena = models.TextField()
      comunicacion = models.IntegerField()
      limpieza = models.IntegerField()
      locacion = models.IntegerField()
      check_in = models.IntegerField()
      precio = models.IntegerField()
      usuario = models.ForeignKey(
          "usuarios.usuario", on_delete=models.CASCADE, related_name='resenas')
      propiedad = models.ForeignKey(
          "propiedades.propiedad", on_delete=models.CASCADE, related_name='resenas')


      def __str__(self):
          return f'{self.resena} - {self.propiedad}'


      def puntaje_pomedio(self):
          prom = (self.comunicacion + self.limpieza +
                self.locacion + self.check_in + self.precio) / 5
          return round(prom)


      puntaje_pomedio.short_description = 'Prom.'
