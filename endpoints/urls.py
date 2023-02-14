from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login),
    path("peliculas/listar", views.obtenerPeliculas),
    path("categorias/listar",views.obtenerCategorias),
    path("/endpoints/categoria/crear", views.registrarCategoria),
    path("/endpoints/categorias/modificar", views.modificarCategoria),
    path("/endpoints/categorias/eliminar",views.eliminarCategoria)
]