from decimal import Decimal


def calcular_valor_em_estoque(preco, estoque):
    """Calcula o valor em estoque de um produto."""
    return preco * estoque


def resumir_catalogo(produtos):
    """Calcula os totais em Python e acrescenta o valor de cada produto."""
    produtos_calculados = []
    quantidade_total_unidades = 0
    quantidade_indisponiveis = 0
    valor_total_estoque = Decimal("0.00")

    for produto in produtos:
        item = produto.copy()  # Cria uma cópia do item para não modificar o original

        preco = Decimal(str(item["preco"]))
        estoque = item["estoque"]
        valor = calcular_valor_em_estoque(preco, estoque)
        item["valor_em_estoque"] = valor

        produtos_calculados.append(item)

        quantidade_total_unidades += estoque
        valor_total_estoque += item["valor_em_estoque"]
        
        if item["estoque"] == 0:
            quantidade_indisponiveis += 1

    return {
        "produtos": produtos_calculados,
        "quantidade_produtos": len(produtos),
        "quantidade_total_unidades": quantidade_total_unidades,
        "quantidade_indisponiveis": quantidade_indisponiveis,
        "valor_total_estoque": valor_total_estoque,
    }



def calcular_indicadores_pedidos(pedidos):
    """Calcula os totais em Python e acrescenta o valor de cada pedido."""
    pedidos_processados = []
    total_pedidos = 0
    pedidos_pendentes = 0
    pedidos_concluidos = 0
    valor_total = Decimal("0.00")

    for pedido in pedidos:
        item = pedido.copy()
        preco = Decimal(str(item["preco_unitario"]))
        item["valor_total"] = preco * item["quantidade"]

        total_pedidos += 1
        valor_total += item["valor_total"]

        if pedido["situacao"] == "PENDENTE":
            pedidos_pendentes += 1
        elif pedido["situacao"] == "CONCLUIDO":
            pedidos_concluidos += 1

        pedidos_processados.append(item)

    return {
        "pedidos": pedidos_processados,
        "total_pedidos": total_pedidos,
        "pedidos_pendentes": pedidos_pendentes,
        "pedidos_concluidos": pedidos_concluidos,
        "valor_total": valor_total,
    }
