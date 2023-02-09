from django.db import models

class Pelicula(models.Model):
    #CharField para poner longitud del String y URLField hace lo mismo
    nombre = models.CharField(max_length=100)
    url = models.URLField()
#Creamos una nueva entidad categorias
    def __str__(self):
        return self.nombre#Pintar el archivo con su nombre como String
        
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    #Cuando queremos una entidad que tenga 2 campos
        #Creamos un tupla, no se puede alterar sus valores
    CATEGORIA_ESTADOS = (
        ("A","Activo"), #Categoria 1
        ("I","Inactivo") #Categoria 2
    )
    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=CATEGORIA_ESTADOS)#1 xq solo hay 1 caracter
    
    def __str__(self):
        return self.nombre#Pintar el archivo con su nombre como String










