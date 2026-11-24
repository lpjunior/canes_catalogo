from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=120, null=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco} - Estoque: {self.estoque}"

class Pedido(models.Model):
    SITUACAO_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("CONCLUIDO", "Concluído"),
    ]

    numero = models.CharField(max_length=20, unique=True)
    cliente = models.CharField(max_length=120)

    # constraint - restrição de integridade referencial
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=1)
    
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default="PENDENTE")

    def __str__(self):
        return f"Pedido {self.numero} - Cliente: {self.cliente} - Produto: {self.produto.nome} - Situação: {self.situacao}"
