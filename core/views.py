
from django.http import HttpRequest
from django.shortcuts import redirect, render

from core.models import Pedido, Produto

from .forms import ProdutoForm
from .services import calcular_indicadores_pedidos, resumir_catalogo


def inicio(request: HttpRequest):
    contexto = {"titulo": "CANES | Início", "descricao": "Bem-vindo ao catálogo CANES!"}

    template = "core/index.html"

    return render(request, template, contexto)


def catalogo(request):
    produtos = list(
        Produto.objects.order_by("nome").values("nome", "preco", "estoque")
    )

    contexto = resumir_catalogo(produtos)
    contexto["titulo"] = "Catálogo CANES"

    return render(request, "core/catalogo.html", contexto)


def pedidos(request: HttpRequest):
    lista_pedidos = list(
        Pedido.objects.order_by("numero").values("numero", "cliente", "produto", "preco_unitario", "quantidade", "situacao")
    )

    contexto = {
        "titulo": "Painel de pedidos",
        "descricao": "Acompanhe os pedidos dos clientes, suas situações e os valores de cada compra.",
        "pedidos": lista_pedidos,
        **calcular_indicadores_pedidos(lista_pedidos),
    }
    return render(request, "core/pedidos.html", contexto)


def cadastrar_produto(request: HttpRequest):

    if request.method == "POST":
        form = ProdutoForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("catalogo")
    else:
        form = ProdutoForm()

    contexto = {
        "titulo": "Cadastrar Produto",
        "form": form
    }

    return render(request, "core/cadastrar_produto.html", contexto)