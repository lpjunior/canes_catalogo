from django.urls import path

from . import views

urlpatterns = [
    path(route='', view=views.inicio, name='inicio'),
    path(route='catalogo/', view=views.catalogo, name='catalogo'),
    path(route='pedidos/', view=views.pedidos, name='pedidos'),
    path(route='ola/<str:nome>/', view=views.saudacao, name='saudacao'),
]
