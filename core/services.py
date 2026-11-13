def calcular_valor_em_estoque(preco, estoque):
    """Calcula o valor em estoque de um produto."""
    return preco * estoque


def resumir_catalogo(produtos):
    """Calcula os totais em Python e acrescenta o valor de cada produto."""
    produtos_calculados = []
    quantidade_total_unidades = 0
    quantidade_indisponiveis = 0
    valor_total_estoque = 0.0

    for produto in produtos:
        item = produto.copy()  # Cria uma cópia do item para não modificar o original

        preco = item["preco"]
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