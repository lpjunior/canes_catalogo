from django.urls import path

from . import views

urlpatterns = [
    path(route='', view=views.inicio, name='inicio'),
    path(route='catalogo/', view=views.catalogo, name='catalogo'),
    path(route='pedidos/', view=views.pedidos, name='pedidos'),
    path(route='produto/novo/', view=views.cadastrar_produto, name='cadastrar_produto'),
]
