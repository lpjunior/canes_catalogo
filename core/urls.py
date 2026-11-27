from django.urls import path

from . import views

urlpatterns = [
    path(route='', view=views.inicio, name='inicio'),
    path(route='catalogo/', view=views.catalogo, name='catalogo'),
    path(route='pedidos/', view=views.pedidos, name='pedidos'),
    path(route='pedidos/novo/', view=views.cadastrar_pedido, name='cadastrar_pedido'),
    path(route='pedidos/<int:pedido_id>/editar/', view=views.editar_pedido, name='editar_pedido'),
    path(route='pedidos/<int:pedido_id>/excluir/', view=views.excluir_pedido, name='excluir_pedido'),

    path(route='produtos/novo/', view=views.cadastrar_produto, name='cadastrar_produto'),
    path(route='produtos/<int:produto_id>/editar/', view=views.editar_produto, name='editar_produto'),
    path(route='produtos/<int:produto_id>/excluir/', view=views.excluir_produto, name='excluir_produto'),
]
