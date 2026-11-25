from decimal import Decimal

from django import forms

from .models import Produto


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
