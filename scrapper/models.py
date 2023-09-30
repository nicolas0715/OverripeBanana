from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
class Pelicula(models.Model):
    nombre_pelicula = models.CharField(max_length=255, verbose_name='Nombre_Pelicula')
    fecha_streaming = models.DateField(verbose_name='Fecha_Streaming')
    imagen = models.URLField(verbose_name='Imagen')
    critics_score = models.IntegerField(default='-', verbose_name='Critics_Score')
    audience_score = models.IntegerField(default='-', verbose_name='Audience_Score')
    user_score = models.IntegerField(blank=True, default='-', verbose_name='User Score')
        
class Serie(models.Model):
    nombre_serie = models.CharField(max_length=255, verbose_name='Nombre_Serie')
    ultimo_capitulo = models.DateField(verbose_name='Ultimo_Capitulo')
    imagen = models.URLField(verbose_name='Imagen_Serie')
    critics_score = models.IntegerField(default='-', verbose_name='Critics Score')
    audience_score = models.IntegerField(default='-', verbose_name='Audience Score')
    user_score = models.IntegerField(blank=True, default='-', verbose_name='User_Score')

class User(models.Model):
    nombre_completo = models.CharField(max_length=50)
    email = models.EmailField()
    contrasena = models.CharField(max_length=30)
'''
# =====================================================================================================

class Pelicula(models.Model):
    nombre_pelicula = models.CharField(max_length=255, verbose_name='Nombre_Pelicula')
    fecha_streaming = models.DateField(verbose_name='Fecha_Streaming')
    imagen = models.URLField(verbose_name='Imagen')
    critics_score = models.IntegerField(default=0, verbose_name='Critics Score')
    audience_score = models.IntegerField(default=0, verbose_name='Audience Score')
    user_score = models.IntegerField(blank=True, null=True, verbose_name='User Score')
    streaming = models.CharField(default=' ', max_length=30, verbose_name='Streaming')

class Serie(models.Model):
    nombre_serie = models.CharField(max_length=255, verbose_name='Nombre_Serie')
    ultimo_capitulo = models.DateField(verbose_name='Ultimo_Capitulo')
    imagen = models.URLField(verbose_name='Imagen_Serie')
    critics_score = models.IntegerField(default=0, verbose_name='Critics Score')
    audience_score = models.IntegerField(default=0, verbose_name='Audience Score')
    user_score = models.IntegerField(blank=True, null=True, verbose_name='User Score')
    streaming = models.CharField(default=' ', max_length=30, verbose_name='Streaming')

class Critica(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()

class ListaFavoritos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    peliculas = models.ManyToManyField(Pelicula, blank=True)
    series = models.ManyToManyField(Serie, blank=True)

class PeliculasVistas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    peliculas = models.ManyToManyField(Pelicula, blank=True)
    series = models.ManyToManyField(Serie, blank=True)

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="avatares", null=True, blank=True)