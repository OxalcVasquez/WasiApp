# Generated by Django 3.2.7 on 2021-11-22 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propiedades', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propiedad',
            name='reserva_instantanea',
        ),
    ]
