import calendar
from django.utils import timezone


class Dia:
    def __init__(self, numero, pasado, mes, anio):
        self.numero = numero
        self.pasado = pasado
        self.mes = mes
        self.anio = anio

    def __str__(self):
        return str(self.numero)


class Calendar(calendar.Calendar):

    def __init__(self, anio, mes):
        super().__init__(firstweekday=6)
        self.anio = anio
        self.mes = mes
        self.dia_nombres = ("Dom", "Lun", "Mar", "Mier", "Jue", "Vie", "Sab",)
        self.meses = (
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")

    def get_mes(self):
        return self.meses[self.mes - 1]

    def get_dias(self):
        semanas = self.monthdays2calendar(self.anio, self.mes)
        dias = []
        for semana in semanas:
            for dia, _ in semana:
                now = timezone.now()
                hoy = now.day
                mes = now.month
                pasado = False
                if mes == self.mes:
                    pasado = True if dia <= hoy else False
                new_dia = Dia(dia, pasado, self.mes, self.anio)
                dias.append(new_dia)
        return dias


# cal = Calendar(2020, 1)
# cal.get_dias()
