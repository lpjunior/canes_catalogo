from decimal import Decimal

from django.db.models.deletion import ProtectedError
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import PedidoForm
from .models import Pedido, Produto
from .services import calcular_indicadores_pedidos


class IndicadoresPedidosTests(SimpleTestCase):
    def test_calculo_com_decimais_sem_modificar_os_dados_originais(self):
        pedidos = [
            {"preco_unitario": Decimal("0.10"), "quantidade": 3, "situacao": "PENDENTE"},
            {"preco_unitario": Decimal("12.45"), "quantidade": 2, "situacao": "CONCLUIDO"},
        ]
        indicadores = calcular_indicadores_pedidos(pedidos)
        self.assertEqual(indicadores["total_pedidos"], 2)
        self.assertEqual(indicadores["pedidos_pendentes"], 1)
        self.assertEqual(indicadores["pedidos_concluidos"], 1)
        self.assertEqual(indicadores["valor_total"], Decimal("25.20"))
        self.assertEqual(indicadores["pedidos"][0]["valor_total"], Decimal("0.30"))
        self.assertNotIn("valor_total", pedidos[0])

    def test_lista_vazia(self):
        self.assertEqual(calcular_indicadores_pedidos([]), {
            "pedidos": [], "total_pedidos": 0, "pedidos_pendentes": 0,
            "pedidos_concluidos": 0, "valor_total": Decimal("0.00"),
        })


class PedidosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.produto = Produto.objects.create(nome="Produto CANES", preco="89.90", estoque=10)
        cls.pedido = Pedido.objects.create(
            numero="PED-001", cliente="Maria", produto=cls.produto,
            preco_unitario="89.90", quantidade=2, situacao="PENDENTE",
        )

    def dados_pedido(self, **alteracoes):
        dados = {
            "numero": "PED-002", "cliente": "João", "produto": self.produto.pk,
            "preco_unitario": "79.90", "quantidade": "3", "situacao": "CONCLUIDO",
        }
        dados.update(alteracoes)
        return dados

    def test_pagina_indicadores_e_acoes(self):
        response = self.client.get(reverse("pedidos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/pedidos.html")
        self.assertEqual(response.context["total_pedidos"], 1)
        self.assertEqual(response.context["pedidos_pendentes"], 1)
        self.assertEqual(response.context["pedidos_concluidos"], 0)
        self.assertEqual(response.context["valor_total"], Decimal("179.80"))
        self.assertContains(response, self.produto.nome)
        self.assertContains(response, "179,80")
        for nome, args in (
            ("cadastrar_pedido", []), ("editar_pedido", [self.pedido.pk]),
            ("excluir_pedido", [self.pedido.pk]),
        ):
            self.assertContains(response, reverse(nome, args=args))

    def test_formulario_de_cadastro(self):
        response = self.client.get(reverse("cadastrar_pedido"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/formulario_pedido.html")
        self.assertContains(response, self.produto.nome)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertEqual(Pedido.objects.count(), 1)

    def test_cadastrar_pedido(self):
        response = self.client.post(reverse("cadastrar_pedido"), self.dados_pedido())
        self.assertRedirects(response, reverse("pedidos"))
        pedido = Pedido.objects.get(numero="PED-002")
        self.assertEqual(pedido.cliente, "João")
        self.assertEqual(pedido.produto_id, self.produto.pk)
        self.assertEqual(pedido.preco_unitario, Decimal("79.90"))
        self.assertEqual(pedido.quantidade, 3)
        self.assertEqual(pedido.situacao, "CONCLUIDO")
        self.assertIsNone(pedido.excluido_em)

    def test_formulario_rejeita_dados_invalidos(self):
        casos = [
            ("preco_unitario", "0"), ("preco_unitario", "-1"),
            ("quantidade", "0"), ("quantidade", "-1"), ("quantidade", "1.5"),
            ("numero", "PED-001"), ("numero", ""), ("cliente", ""),
            ("produto", "999999"), ("produto", ""), ("situacao", "INVALIDA"),
        ]
        for campo, valor in casos:
            with self.subTest(campo=campo, valor=valor):
                response = self.client.post(
                    reverse("cadastrar_pedido"), self.dados_pedido(**{campo: valor})
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(campo, response.context["form"].errors)
        self.assertEqual(Pedido.objects.count(), 1)

    def test_editar_pedido(self):
        url = reverse("editar_pedido", args=[self.pedido.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].instance.pk, self.pedido.pk)
        outro_produto = Produto.objects.create(nome="Outro produto", preco="10.00")
        response = self.client.post(
            url, self.dados_pedido(numero="PED-001", produto=outro_produto.pk)
        )
        self.assertRedirects(response, reverse("pedidos"))
        self.pedido.refresh_from_db()
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(self.pedido.cliente, "João")
        self.assertEqual(self.pedido.produto_id, outro_produto.pk)
        self.assertEqual(self.pedido.preco_unitario, Decimal("79.90"))
        self.assertEqual(self.pedido.quantidade, 3)
        self.assertEqual(self.pedido.situacao, "CONCLUIDO")

    def test_edicao_invalida_preserva_dados(self):
        response = self.client.post(
            reverse("editar_pedido", args=[self.pedido.pk]),
            self.dados_pedido(quantidade="0"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("quantidade", response.context["form"].errors)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.cliente, "Maria")
        self.assertEqual(self.pedido.quantidade, 2)

    def test_get_exclusao_so_exibe_confirmacao(self):
        response = self.client.get(reverse("excluir_pedido", args=[self.pedido.pk]))
        self.assertTemplateUsed(response, "core/confirmar_exclusao_pedido.html")
        self.assertContains(response, self.pedido.numero)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.pedido.refresh_from_db()
        self.assertIsNone(self.pedido.excluido_em)

    def test_exclusao_logica_preserva_historico_e_remove_dos_indicadores(self):
        Pedido.objects.create(**{**self.dados_pedido(), "produto": self.produto})
        dados_antes = Pedido.objects.filter(pk=self.pedido.pk).values().get()
        antes = timezone.now()
        response = self.client.post(reverse("excluir_pedido", args=[self.pedido.pk]))
        self.assertRedirects(response, reverse("pedidos"))
        self.pedido.refresh_from_db()
        self.assertGreaterEqual(self.pedido.excluido_em, antes)
        self.assertEqual(Pedido.objects.count(), 2)
        dados_depois = Pedido.objects.filter(pk=self.pedido.pk).values().get()
        dados_antes.pop("excluido_em")
        dados_depois.pop("excluido_em")
        self.assertEqual(dados_antes, dados_depois)
        response = self.client.get(reverse("pedidos"))
        self.assertNotContains(response, "PED-001")
        self.assertContains(response, "PED-002")
        self.assertEqual(response.context["total_pedidos"], 1)
        self.assertEqual(response.context["pedidos_pendentes"], 0)
        self.assertEqual(response.context["pedidos_concluidos"], 1)
        self.assertEqual(response.context["valor_total"], Decimal("239.70"))

    def test_pagina_vazia_apos_exclusao(self):
        self.client.post(reverse("excluir_pedido", args=[self.pedido.pk]))
        response = self.client.get(reverse("pedidos"))
        self.assertContains(response, "Nenhum pedido encontrado")
        self.assertContains(response, "R$ 0,00")
        self.assertEqual(response.context["total_pedidos"], 0)

    def test_pedido_excluido_ou_inexistente_retorna_404(self):
        self.client.post(reverse("excluir_pedido", args=[self.pedido.pk]))
        for pk in (self.pedido.pk, self.pedido.pk + 100):
            for nome in ("editar_pedido", "excluir_pedido"):
                for metodo in (self.client.get, self.client.post):
                    with self.subTest(pk=pk, nome=nome, metodo=metodo.__name__):
                        self.assertEqual(metodo(reverse(nome, args=[pk])).status_code, 404)

    def test_numero_de_pedido_excluido_permanece_reservado(self):
        self.client.post(reverse("excluir_pedido", args=[self.pedido.pk]))
        form = PedidoForm(data=self.dados_pedido(numero="PED-001"))
        self.assertFalse(form.is_valid())
        self.assertIn("numero", form.errors)

    def test_csrf_obrigatorio_nas_mutacoes(self):
        client = Client(enforce_csrf_checks=True)
        for nome, args in (
            ("cadastrar_pedido", []), ("editar_pedido", [self.pedido.pk]),
            ("excluir_pedido", [self.pedido.pk]),
        ):
            with self.subTest(nome=nome):
                response = client.post(reverse(nome, args=args), self.dados_pedido())
                self.assertEqual(response.status_code, 403)
        self.pedido.refresh_from_db()
        self.assertIsNone(self.pedido.excluido_em)
        self.assertEqual(Pedido.objects.count(), 1)

    def test_preserva_pedidos_ao_tentar_excluir_produto(self):
        for excluido in (False, True):
            with self.subTest(excluido=excluido):
                if excluido:
                    self.client.post(reverse("excluir_pedido", args=[self.pedido.pk]))
                with self.assertRaises(ProtectedError):
                    self.produto.delete()
                response = self.client.post(reverse("excluir_produto", args=[self.produto.pk]))
                self.assertContains(response, "não pode ser excluído")
                self.assertTrue(Produto.objects.filter(pk=self.produto.pk).exists())
                self.assertTrue(Pedido.objects.filter(pk=self.pedido.pk).exists())

    def test_produto_sem_pedidos_pode_ser_excluido(self):
        produto = Produto.objects.create(nome="Sem pedidos", preco="10.00")
        response = self.client.post(reverse("excluir_produto", args=[produto.pk]))
        self.assertRedirects(response, reverse("catalogo"))
        self.assertFalse(Produto.objects.filter(pk=produto.pk).exists())

    def test_navegacao(self):
        for nome in ("inicio", "catalogo"):
            self.assertContains(self.client.get(reverse(nome)), reverse("pedidos"))
