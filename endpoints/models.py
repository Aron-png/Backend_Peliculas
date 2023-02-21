from django.db import models

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

# Entre una categoria y una pelicula hay una relacion de uno a muchos, respectivamente.
class Pelicula(models.Model):
    #CharField para poner longitud del String y URLField hace lo mismo
    nombre = models.CharField(max_length=100)
    url = models.URLField()
    # on_delete=models.CASCADE --> cuando quiero borrar una categoria, borra TMB las peliculas
    # relacionadas a ella.
    
    # null=True --> No tener registros que tengan el campo vacio
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
#Creamos una nueva entidad categorias
    def __str__(self):
        return self.nombre#Pintar el archivo con su nombre como String
        
class Actor(models.Model):
    ACTOR_ESTADOS = (
        ("A", "Activo"),
        ("R", "Retirado")
    )
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=1, choices=ACTOR_ESTADOS)

    def __str__(self):
        return self.nombre
    
class PeliculaXActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)

    tiempo = models.IntegerField(verbose_name="Tiempo en pantalla", default=0)
    sueldo = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)

    def __str__(self):
        return f"{self.actor.nombre} - {self.pelicula.nombre}"
        












