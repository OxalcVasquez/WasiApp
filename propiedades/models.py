from django.db import models
from administracion.models import TimeStampedModel
from django_countries.fields import CountryField
from django.urls import reverse
from django.utils import timezone
from cal import Calendar

# Create your models here. tipo propiedades,tipo alojamiento,


class AbstractItem(TimeStampedModel):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class TipoPropiedad(AbstractItem):
  class Meta:
      verbose_name = "Tipo Propiedad"


class FotosPropiedad(TimeStampedModel):
    descripcion = models.CharField(max_length=80)
    archivo = models.ImageField(upload_to="propiedad_fotos")
    propiedad = models.ForeignKey(  "Propiedad", on_delete=models.CASCADE, related_name="fotos")


    def __str__(self):
        return self.descripcion


class Propiedad(TimeStampedModel):
      propiedadID = models.AutoField(primary_key=True)
      nombre = models.CharField(max_length=140)
      descripcion = models.TextField()
      pais = CountryField()
      ciudad = models.CharField(max_length=80)
      precio = models.DecimalField(max_digits=12, decimal_places=2)
      direccion = models.CharField(max_length=140)
      numCuartos = models.IntegerField()
      numMaxHuspedes = models.IntegerField()
      numCamas = models.IntegerField()
      numBano = models.IntegerField()
      conInternet = models.BooleanField()
      permiteMascotas = models.BooleanField()
      conEstacionamiento = models.BooleanField()
      conCocina = models.BooleanField()
      conSala = models.BooleanField()
      conLavanderia = models.BooleanField()
      conTvCable = models.BooleanField()
      conAireAcondicionado = models.BooleanField()
      otrasComodidades = models.CharField(max_length=200, null=True)
      host = models.ForeignKey(
          "usuarios.Usuario", on_delete=models.CASCADE, related_name="Propiedads"
      )
      tipoPropiedad = models.ForeignKey(
          "TipoPropiedad", on_delete=models.SET_NULL, null=True, related_name="Propiedades"
      )


      class Meta:
          ordering = ['-pk']


      def __str__(self):
          return self.nombre


      def puntaje_total(self):
          resenas_propiedad = self.resenas.all()
          propiedad_puntajes = 0
          if len(resenas_propiedad) > 0:
              for resena in resenas_propiedad:
                  propiedad_puntajes += resena.puntaje_pomedio()
              return round(propiedad_puntajes / len(resenas_propiedad), 2)
          return 0


      def primera_foto(self):
          try:
              foto = self.fotos.first()
              return foto
          except Exception:
              return None


      def get_siguientes_cuatro(self):
          fotos = self.fotos.all()[1:5]
          return fotos


      def get_absolute_url(self):
          return reverse("propiedades:detail", kwargs={"pk": self.pk})


      def get_cuartos(self):
          return "1 cama" if self.numCuartos == 1 else f'{self.numCuartos} cuartos'

      def get_calendars(self):
        year = timezone.now().year
        month = timezone.now().month
        next_month = month + 1
        if month == 12:
            next_month = 1
        this_month_cal = Calendar(year, month)
        next_month_cal = Calendar(year, next_month)
        return [this_month_cal, next_month_cal]


      def save(self, *args, **kwargs):
          self.ciudad = str.title(self.ciudad)
          super().save(*args, **kwargs)
