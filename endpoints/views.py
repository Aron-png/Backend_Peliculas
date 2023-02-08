from django.http import HttpResponse
from django.shortcuts import render
import json
def login(request):
    if request.method == "POST":
        #La data q obtenemos de un servidor en forma de String "request.body".
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
def obtenerPeliculas(request):
    if request.method == "GET":
        categoria = request.GET.get("categoria")#Recogemos la info de la url del query
        
        peliculas = [
            {
                "id": 1,
                "nombre": "Avatar 2",
                "url": "https://i.blogs.es/6b43d1/avatar-edicion-especial-cartel/450_1000.jpg",
                "categoria": 1
            }, {
                "id": 2,
                "nombre": "El gato con botas",
                "url": "https://www.universalpictures-latam.com/tl_files/content/movies/puss_in_boots_2/posters/01.jpg",
                "categoria": 2
            }, {
                "id": 3,
                "nombre": "Transformer, el despertar de las bestias",
                "url": "https://es.web.img3.acsta.net/pictures/22/12/02/09/33/5399733.jpg",
                "categoria": 3
            }
        ]
        #Logica que filtra peliculas
        def logicaFiltrado(pelicula):
            if categoria == pelicula["categoria"]:
                return True
            else:
                return False
        #Peliculas filtradas lo pasamos en el response
        peliculasFiltradas = filter(logicaFiltrado,peliculas)
        # TODO: Consultas a bd
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
