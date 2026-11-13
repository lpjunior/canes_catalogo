from decimal import Decimal

from django.template.loader import render_to_string
from django.test import SimpleTestCase
from django.urls import reverse

from .views import calcular_indicadores_pedidos


class PedidosTests(SimpleTestCase):
    def test_pagina_e_indicadores(self):
        response = self.client.get(reverse("pedidos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/pedidos.html")
        self.assertEqual(response.context["total_pedidos"], 5)
        self.assertEqual(response.context["pedidos_pendentes"], 3)
        self.assertEqual(response.context["pedidos_concluidos"], 2)
        self.assertEqual(response.context["valor_total"], Decimal("5125.50"))
        totais = ["179.80", "149.70", "799.00", "2999.00", "998.00"]
        for pedido, total in zip(response.context["pedidos"], totais):
            self.assertEqual(pedido["valor_total"], Decimal(total))
            for campo in ("numero", "cliente", "produto", "situacao"):
                self.assertContains(response, pedido[campo])
        self.assertContains(response, 'class="situacao pendente">Pendente')
        self.assertContains(response, 'class="situacao concluido">Concluído')
        self.assertContains(response, "5.125,50")
        self.assertContains(response, "179,80")

    def test_calculo_com_outros_dados(self):
        pedidos = [
            {"preco_unitario": Decimal("0.10"), "quantidade": 3, "situacao": "Pendente"},
            {"preco_unitario": Decimal("12.45"), "quantidade": 2, "situacao": "Concluído"},
        ]
        indicadores = calcular_indicadores_pedidos(pedidos)
        self.assertEqual(indicadores, {
            "total_pedidos": 2, "pedidos_pendentes": 1,
            "pedidos_concluidos": 1, "valor_total": Decimal("25.20"),
        })
        self.assertEqual(pedidos[0]["valor_total"], Decimal("0.30"))

    def test_lista_vazia(self):
        indicadores = calcular_indicadores_pedidos([])
        self.assertEqual(indicadores, {
            "total_pedidos": 0, "pedidos_pendentes": 0,
            "pedidos_concluidos": 0, "valor_total": Decimal("0.00"),
        })
        html = render_to_string("core/pedidos.html", {"pedidos": [], **indicadores})
        self.assertIn("Nenhum pedido encontrado", html)
        self.assertIn("R$ 0,00", html)
        self.assertNotIn('class="pedido-topo"', html)

    def test_navegacao(self):
        for nome in ("inicio", "catalogo"):
            self.assertContains(self.client.get(reverse(nome)), reverse("pedidos"))
