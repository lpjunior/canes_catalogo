from django.db.models.deletion import ProtectedError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from core.models import Pedido, Produto

from .forms import PedidoForm, ProdutoForm
from .services import calcular_indicadores_pedidos, resumir_catalogo


def inicio(request: HttpRequest):
    contexto = {"titulo": "CANES | Início", "descricao": "Bem-vindo ao catálogo CANES!"}

    template = "core/index.html"

    return render(request, template, contexto)


def catalogo(request):
    produtos = list(
        Produto.objects.order_by("nome").values("id", "nome", "preco", "estoque")
    )

    contexto = resumir_catalogo(produtos)
    contexto["titulo"] = "Catálogo CANES"

    return render(request, "core/catalogo.html", contexto)


def pedidos(request: HttpRequest):
    lista_pedidos = list(
        Pedido.objects.filter(excluido_em__isnull=True).order_by("numero").values(
            "id", "numero", "cliente", "produto__nome", "preco_unitario", "quantidade", "situacao"
        )
    )

    contexto = {
        "titulo": "Painel de pedidos",
        "descricao": "Acompanhe os pedidos dos clientes, suas situações e os valores de cada compra.",
        "pedidos": lista_pedidos,
        **calcular_indicadores_pedidos(lista_pedidos),
    }
    
    return render(request, "core/pedidos.html", contexto)


@require_http_methods(["GET", "POST"])
def cadastrar_pedido(request: HttpRequest):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pedidos")
    else:
        form = PedidoForm()

    contexto = {
        "titulo": "Cadastrar Pedido",
        "descricao": "Preencha os campos para cadastrar um pedido na CANES.",
        "form": form,
        "texto_botao": "Salvar pedido",
    }
    return render(request, "core/formulario_pedido.html", contexto)


@require_http_methods(["GET", "POST"])
def editar_pedido(request: HttpRequest, pedido_id: int):
    pedido = get_object_or_404(Pedido, pk=pedido_id, excluido_em__isnull=True)
    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect("pedidos")
    else:
        form = PedidoForm(instance=pedido)

    contexto = {
        "titulo": f"Editar Pedido - {pedido.numero}",
        "descricao": "Atualize os dados do pedido na CANES.",
        "form": form,
        "texto_botao": "Salvar alterações",
    }
    return render(request, "core/formulario_pedido.html", contexto)


@require_http_methods(["GET", "POST"])
def excluir_pedido(request: HttpRequest, pedido_id: int):
    pedido = get_object_or_404(Pedido, pk=pedido_id, excluido_em__isnull=True)
    if request.method == "POST":
        pedido.excluido_em = timezone.now()
        pedido.save(update_fields=["excluido_em"])
        return redirect("pedidos")

    contexto = {
        "titulo": f"Excluir Pedido - {pedido.numero}",
        "pedido": pedido,
    }
    return render(request, "core/confirmar_exclusao_pedido.html", contexto)


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
        "form": form,
        "texto_botao": "Salvar produto",
        "descricao": "Preencha os campos para adicionar um produto ao catálogo da CANES."
    }

    return render(request, "core/formulario_produto.html", contexto)


def editar_produto(request: HttpRequest, produto_id: int):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)

        if form.is_valid():
            form.save()
            return redirect("catalogo")
    else:
        form = ProdutoForm(instance=produto)

    contexto = {
        "titulo": f"Editar Produto - {produto.nome}",
        "form": form,
        "texto_botao": "Salvar alterações",
        "descricao": "Preencha os campos para editar o produto no catálogo da CANES."
    }

    return render(request, "core/formulario_produto.html", contexto)

def excluir_produto(request: HttpRequest, produto_id: int):
    produto = get_object_or_404(Produto, pk=produto_id)
    erro = None

    if request.method == "POST":
        try:
            produto.delete()
        except ProtectedError:
            erro = "Este produto possui pedidos vinculados e não pode ser excluído, para preservar o histórico."
        else:
            return redirect("catalogo")

    contexto = {
        "titulo": f"Excluir Produto - {produto.nome}",
        "produto": produto,
        "erro": erro,
    }

    return render(request, "core/confirmar_exclusao.html", contexto)