# Generated by Django 3.2.7 on 2021-11-20 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('propiedades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resena',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('resena', models.TextField()),
                ('comunicacion', models.IntegerField()),
                ('limpieza', models.IntegerField()),
                ('locacion', models.IntegerField()),
                ('check_in', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resenas', to='propiedades.propiedad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resenas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
