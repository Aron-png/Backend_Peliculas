from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . models import Categoria, Pelicula, PeliculaXActor, Actor
import json

#/endpoint/login
@csrf_exempt
def login(request):
    if request.method == "POST":
        #La data q obtenemos de registrarse en forma de String "request.body".
        dictDataRequest = json.loads(request.body)#convertir a diccionario
        usuario = dictDataRequest["usuario"]
        password = dictDataRequest["password"]

        #TODO: Consultar a base de datos (un recordatorio de que falta algo por hacer=TODO)
        if usuario == "pw" and password == "123":
            #Correcto
            dictOk = {
                "error" : ""
            }
            return HttpResponse(json.dumps(dictOk))
        else:
            #Error login
            dictOk = {
                "error" : "No existe el usuario o contraseña"
            }
            strError = json.dumps(dictOk)
            return HttpResponse(strError)


    else:
        #Error en caso que la peticion no sea post
        dictError = {
            "error" : "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
        
@csrf_exempt#Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
def obtenerPeliculas(request):
    if request.method == "GET":
        idcategoria = request.GET.get("categoria")#Recogemos la info de la url del query, valor String
        if idcategoria == None:
            dictError = {
                "error": "Debe enviar una categoria como query paremeter."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)        
        # TODO: Consultas a base de datos -> HECHO
        #categoria__id=idCategoria
        #Un String con una categoria como comparacon no esta bien
        #Si al objeto quiero filtrar por su id
        #categoria__"valor"
        peliculasFiltradas = []

        if idcategoria == "-1":
            PeliculaQS = Pelicula.objects.all()
        else:
            PeliculaQS = Pelicula.objects.filter(categoria__id=idcategoria)
        
        for p in PeliculaQS:
            peliculasFiltradas.append(
              {
                "id":p.pk,
                "nombre":p.nombre,
                "url":p.url,
                "categoria":{
                "id":p.categoria.pk,
                "nombre":p.categoria.nombre
                }
              }
            )
            


        dictResponse = {
            "error": "",
            "peliculas": list(peliculasFiltradas)
        }
        strResponse = json.dumps(dictResponse)
        return HttpResponse(strResponse)
    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)


# /endpoinst/peliculas/listar_nombre?nombre=werwer
def obtenerPeliculasPorNombre(request):
    if request.method != "GET":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    nombreAFiltrar = request.GET.get("nombre")

    peliculasQS = Pelicula.objects.filter(nombre__contains=nombreAFiltrar)

    peliculas = []
    for p in peliculasQS:
        peliculas.append({
            "id" : p.id,
            "nombre" : p.nombre
        })

    dictOK = {
        "error" : "",
        "peliculas" : peliculas
    }
    return HttpResponse(json.dumps(dictOK))

#No vamos a recibir nada de request porque queremos todas las categorias
#El servicio nos va a devolver un String en forma de dicc de  (id y nombre)
def obtenerCategorias(request):
    if request.method=="GET":
        #Lista en formato QuerySet
        #Filtrar categorias cuyo estado sea A de Activo
                                                   #Comparacion: stado="A"
        ListaCategoriasQuerySet = Categoria.objects.filter(estado="A")
    #ListaCategorias = list(ListaCategoriasQuerySet)#convertido a lista de python (NO FUNCIONA)
        #En su reemplazo hacemos esto:
        ListaCategorias = []
        for c in ListaCategoriasQuerySet:
            ListaCategorias.append({
                "id":c.id,
                "nombre":c.nombre
            })#convertido a lista de python
        dictOK = {
            "error" : "",
            "categoria" : ListaCategorias
        }
        #Para retornarlo en el frondend, tengo que convertirlo a un String JSON y no dicc
        return HttpResponse(json.dumps(dictOK))
    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
"""
Path, POST:
/endpoints/categoria/crear
Request:
{
    "nombre":"...",
    "estado":"A"
}
"""

@csrf_exempt
#Te permite hacer una comunicacion de servidor al cliente, sin errores (403)
def registrarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    #El Request esta siendo llamado. Con "json.loads" convertirmos en la cadena de texto en
    #un diccionario para poder asi acceder a sus valores dictCategoria["nombre"].
    dictCategoria = json.loads(request.body)
    nombre = dictCategoria["nombre"]
    estado = dictCategoria["estado"]
    
    #En models, categoria tiene...
    #nombre = models.CharField(max_length=50)
    #estado = models.CharField(max_length=1, choices=CATEGORIA_ESTADOS)#1 xq solo hay 1 caracter
    #          Se declara el objet cat
    #Lo esta haciendo directamente porque son String
    #El valor se le esta asignando el argumento de entrada "nombre=nombre"
    
    cat = Categoria(nombre=nombre, estado=estado)
        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        #Queremos hacer lo contrario
    return HttpResponse(json.dumps(dictOK))
    
"""
Path, POST:
/endpoints/categorias/modificar
Request:
{
    "id": 1,
    "nombre"?: "...",
    "estado"? : "A"
}
Response:
{
    "error": ""
}
"""

def modificarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    dicctCategoria = json.loads(request.body)

    identificador = dicctCategoria["id"]
    #cat = Categoria.objects.all() --> Ya no se usa esto, porque el filter devuelve una querySet
    #luego el querySet lo convierto en lista.No quiero lista Sino un objeto Categoria.

    #                Para eso utilizamos esta funcion get de DJANGO
    #Obtener (objeto Categoria = cat) de base de datos --> .objects.get(pk=identificador) 
    cat = Categoria.objects.get(pk=identificador) 


    #Si hago una consulta de un elemento de categoria que no existe, "python" se cae
    #En otras palabras, si usamos esto "dicctCategoria["nombre"]" -> Sale Error
    #                Para eso utilizamos esta funcion get de PYTHON
    if dicctCategoria.get("nombre") != None:
        cat.nombre = dictCategoria.get("nombre")

    if dicctCategoria.get("estado") != None:
        cat.estado = dictCategoria.get("estado")
        #Codigo donde se registra la nueva categoria
    cat.save()
    dictOK = {
        "error" : ""
    }
        #Queremos hacer lo contrario
    return HttpResponse(json.dumps(dictOK))
"""
/endpoints/categorias/eliminar
"""
def eliminarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no valida"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    idCategoria = request.GET.get("id")

    if idCAtegoria == None:
        dictError = {
            "error": "Debe de enviar una categoria para eliminarlo"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    cat = Categoria.objects.get(pk=idCategoria)#Obtener la id de la Categoria
    cat.delete()#Elimino la categoria de la base de datos
    dictOK = {
        "error" : ""
    }
        #Queremos hacer lo contrario
    return HttpResponse(json.dumps(dictOK))
    
# /endpoints/actores/listar?pelicula=2
def obtenerActores(request):
    if request.method != "GET":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    peliculaId = request.GET.get("pelicula")

    actores = []
    if peliculaId == None:
        # Devolver todas los actores
        actoresQS = Actor.objects.all()
        for a in actoresQS:
            actores.append({
                "id" : a.pk,
                "nombre" : a.nombre
            })
    else :
        # Filtrar por id de pelicula
        peliculasxActorQS = PeliculaXActor.objects.filter(pelicula__pk=peliculaId)
        for pa in peliculasxActorQS:
            actores.append({
                "id" : pa.actor.pk,
                "nombre" : pa.actor.nombre
            })

    dictOK = {
        "error" : "",
        "actores" : actores
    }
    return HttpResponse(json.dumps(dictOK))




    