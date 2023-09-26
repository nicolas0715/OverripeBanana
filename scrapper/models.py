from django.db import models

# Create your models here.

class Pelicula():
    
    def __init__(self, peli_nombre, fecha_streamming, ):
        self.nombre = peli_nombre
        self.fecha = fecha_streamming
        