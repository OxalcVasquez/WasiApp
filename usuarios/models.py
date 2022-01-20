import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


# Create your models here

class Usuario(AbstractUser):
  """Custom User Model"""
  usuarioID = models.AutoField(primary_key=True)
  GENERO_MASCULINO = "masculino"
  GENERO_FEMENINO = "femenino"
  GENERO_OTROS = "otros"

  GENDER_CHOICES = (
      (GENERO_MASCULINO, "Masculino"),
      (GENERO_FEMENINO, "Femenino"),
      (GENERO_OTROS, "Otros"),
  )


  LOGIN_EMAIL = 'email'


  LOGIN_CHOICES = (
      (LOGIN_EMAIL, 'Email'),
  )

  biografia = models.TextField(blank=True,null=True,max_length=200)
  # # username = models.TextField(max_length=30)
  # nombres = models.TextField(max_length=30)
  # apellidos = models.TextField(max_length=80)
  avatar = models.ImageField(blank=True, upload_to='avatares',null=True)
  genero = models.CharField(max_length=13, choices=GENDER_CHOICES, blank=True)
  fechaNacimiento = models.DateField(blank=True, null=True)
  email_verificado = models.BooleanField(default=False)
  email_secreto = models.CharField(max_length=120, blank=True, default="")
  login_metodo = models.CharField(
      max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

  def __str__(self):
      return self.username


  def get_absolute_url(self):
      return reverse("usuarios:perfil", kwargs={"pk": self.pk})


  def verificar_email(self):
      if not self.email_verificado:
          secret = uuid.uuid4().hex[:20]
          self.email_secreto = secret
          html_message = render_to_string(
              "emails/verificar_email.html", context={"secret": secret})
          send_mail(
              "Verifica tu cuenta de WASI",
              strip_tags(html_message),
              settings.EMAIL_HOST_USER,
              [self.email],
              fail_silently=False,
              html_message=html_message
          )
          self.save()
      return
