from decimal import Decimal

from django.http import HttpRequest
from django.shortcuts import render

from .services import resumir_catalogo


def inicio(request: HttpRequest):
    contexto = {"titulo": "CANES | Início", "descricao": "Bem-vindo ao catálogo CANES!"}

    template = "core/index.html"

    return render(request, template, contexto)


def somar():
    resultado = 0
    for a in range(1, 11):
        resultado += a

    return resultado

def catalogo(request):
    produtos = [
        {"nome": "Teclado", "preco": 89.90, "estoque": 5},
        {"nome": "Mouse", "preco": 49.90, "estoque": 0},
        {"nome": "Monitor", "preco": 799.00, "estoque": 2},
        {"nome": "Notebook", "preco": 2999.00, "estoque": 1},
        {"nome": "Cadeira Gamer", "preco": 499.00, "estoque": 0},
        {"nome": "Memória DDR5", "preco": 599.00, "estoque": 0},
        {"nome": "Placa de Vídeo", "preco": 899.00, "estoque": 0},
        {"nome": "Processador", "preco": 1299.00, "estoque": 0},
        {"nome": "Gabinete", "preco": 299.00, "estoque": 0},
        {"nome": "Fonte de Alimentação", "preco": 199.00, "estoque": 0},
    ]

    contexto = resumir_catalogo(produtos)
    contexto["titulo"] = "Catálogo CANES"

    return render(request, "core/catalogo.html", contexto)


def saudacao(request: HttpRequest, nome: str):
    contexto = {"nome": nome}
    return render(request, "core/saudacao.html", contexto)


def calcular_indicadores_pedidos(pedidos):
    """Calcula os totais em Python e acrescenta o valor de cada pedido."""
    total_pedidos = 0
    pedidos_pendentes = 0
    pedidos_concluidos = 0
    valor_total = Decimal("0.00")

    for pedido in pedidos:
        pedido["valor_total"] = pedido["preco_unitario"] * pedido["quantidade"]
        total_pedidos += 1
        valor_total += pedido["valor_total"]
        if pedido["situacao"] == "Pendente":
            pedidos_pendentes += 1
        elif pedido["situacao"] == "Concluído":
            pedidos_concluidos += 1

    return {
        "total_pedidos": total_pedidos,
        "pedidos_pendentes": pedidos_pendentes,
        "pedidos_concluidos": pedidos_concluidos,
        "valor_total": valor_total,
    }


def pedidos(request: HttpRequest):
    lista_pedidos = [
        {"numero": "CAN-001", "cliente": "Ana Silva", "produto": "Teclado", "preco_unitario": Decimal("89.90"), "quantidade": 2, "situacao": "Pendente"},
        {"numero": "CAN-002", "cliente": "Bruno Santos", "produto": "Mouse", "preco_unitario": Decimal("49.90"), "quantidade": 3, "situacao": "Concluído"},
        {"numero": "CAN-003", "cliente": "Carla Oliveira", "produto": "Monitor", "preco_unitario": Decimal("799.00"), "quantidade": 1, "situacao": "Pendente"},
        {"numero": "CAN-004", "cliente": "Diego Costa", "produto": "Notebook", "preco_unitario": Decimal("2999.00"), "quantidade": 1, "situacao": "Concluído"},
        {"numero": "CAN-005", "cliente": "Elisa Souza", "produto": "Cadeira Gamer", "preco_unitario": Decimal("499.00"), "quantidade": 2, "situacao": "Pendente"},
    ]
    contexto = {
        "titulo": "Painel de pedidos",
        "descricao": "Acompanhe os pedidos dos clientes, suas situações e os valores de cada compra.",
        "pedidos": lista_pedidos,
        **calcular_indicadores_pedidos(lista_pedidos),
    }
    return render(request, "core/pedidos.html", contexto)
