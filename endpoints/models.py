from django.db import models

class Pelicula(models.Model):
    #CharField para poner longitud del String y URLField hace lo mismo
    nombre = models.CharField(max_length=100)
    url = models.URLField()
