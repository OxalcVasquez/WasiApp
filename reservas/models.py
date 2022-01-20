import datetime
from django.db import models
from administracion.models import TimeStampedModel
from reservas.managers import CustomReservationManager
from django.utils import timezone

# Create your models here.

class Reserva(TimeStampedModel):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_CONFIRMADO = 'confirmado'
    ESTADO_CANCELADO = 'cancelado'
    ESTADO_ELECCIONES = (
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_CONFIRMADO, 'Confirmado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    )

    estado = models.CharField(
        max_length=12, choices=ESTADO_ELECCIONES, default=ESTADO_PENDIENTE)
    huesped = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.CASCADE, related_name='reservas')
    propiedad = models.ForeignKey(
        "propiedades.Propiedad", on_delete=models.CASCADE, related_name='reservas')
    check_in = models.DateField()
    check_out = models.DateField()

    objects = CustomReservationManager()

    def __str__(self):
        return f'{self.propiedad}: {self.check_in}'

    def en_progreso(self):
        now = timezone.now().date()
        return self.check_in <= now < self.check_out

    en_progreso.boolean = True

    def finalizado(self):
        now = timezone.now().date()
        finalizado=  now > self.check_out
        if finalizado:
           DiaReserva.objects.filter(reserva=self).delete()
        return finalizado

    finalizado.boolean = True

    def save(self, *args, **kwargs):
        inicio = self.check_in
        fin = self.check_out
        diferencia = fin - inicio
        dia_existente_reserva = DiaReserva.objects.filter(
            dia__range=(inicio, fin), reserva__propiedad=self.propiedad).exists()
        if not dia_existente_reserva:
            super().save(*args, **kwargs)
            for i in range(diferencia.days + 1):
                dia = inicio + datetime.timedelta(days=i)
                DiaReserva.objects.create(dia=dia, reserva=self)
        else:
            return super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        inicio = self.check_in
        fin = self.check_out
        diferencia = fin - inicio
        # dia_existente_reserva = DiaReserva.objects.filter(
        #     dia__range=(inicio, fin), reserva__propiedad=self.propiedad).exists()
        for i in range(diferencia.days + 1):
            dia = inicio + datetime.timedelta(days=i)
            dia_existente_reserva = DiaReserva.objects.filter(
                dia=dia, reserva__propiedad=self.propiedad).exists()
            if not dia_existente_reserva:
                DiaReserva.objects.create(dia=dia, reserva=self)

        return super().save(*args, **kwargs)

    def cancelar(self, *args, **kwargs):
        registros = DiaReserva.objects.filter(
            reserva=self)
        registros.delete()
        return super().save(*args, **kwargs)








class DiaReserva(TimeStampedModel):
    dia = models.DateField()
    reserva = models.ForeignKey(
        Reserva, on_delete=models.CASCADE, related_name='reservado')

    class Meta:
        verbose_name = "Dia Reservado"
        verbose_name_plural = "Dias Reservados"

    def __str__(self):
        return str(self.dia)
