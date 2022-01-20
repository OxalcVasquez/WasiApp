import datetime

from django import template

from reservas.models import DiaReserva

register = template.Library()


@register.simple_tag
def reservado(propiedad, dia):
    if dia.numero == 0:
        return ""
    try:
        dia = datetime.datetime(year=dia.anio, month=dia.mes, day=dia.numero)
        DiaReserva.objects.get(dia=dia, reserva__propiedad=propiedad)
        return True
    except DiaReserva.DoesNotExist:
        return False


