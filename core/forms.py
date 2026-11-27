from decimal import Decimal

from django import forms

from .models import Pedido, Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "preco", "estoque"]

        labels = {
            "nome": "Nome do Produto",
            "preco": "Preço Unitário",
            "estoque": "Quantidade em Estoque"
        }

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "preco": forms.NumberInput(attrs={"class": "form-control", "min": "0.01", "step": "0.01"}),
            "estoque": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "1"})
        }

    def clean_preco(self):
        preco = self.cleaned_data["preco"]
        
        if preco <= Decimal("0.00"):
            raise forms.ValidationError("O preço unitário deve ser um valor positivo.")
        
        return preco


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["numero", "cliente", "produto", "preco_unitario", "quantidade", "situacao"]
        labels = {
            "numero": "Número do pedido",
            "cliente": "Cliente",
            "produto": "Produto",
            "preco_unitario": "Preço unitário",
            "quantidade": "Quantidade",
            "situacao": "Situação",
        }
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "cliente": forms.TextInput(attrs={"class": "form-control"}),
            "produto": forms.Select(attrs={"class": "form-control"}),
            "preco_unitario": forms.NumberInput(
                attrs={"class": "form-control", "min": "0.01", "step": "0.01"}
            ),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control", "min": "1", "step": "1"}
            ),
            "situacao": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["produto"].queryset = Produto.objects.order_by("nome")

    def clean_preco_unitario(self):
        preco = self.cleaned_data["preco_unitario"]
        if preco <= Decimal("0.00"):
            raise forms.ValidationError("O preço unitário deve ser um valor positivo.")
        return preco

    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        if quantidade < 1:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantidade
