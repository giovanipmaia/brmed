from django.db import models

# Create your models here.
# api pra consultar as cotações com o dólar como base
# https://api.vatcomply.com/rates?base=USD&date=2000-04-05
class Moeda(models.Model):
    nome = models.CharField('Moeda', max_length=50)
    abreviatura = models.CharField('Sigla', max_length=3)

    def __str__(self):
        return self.abreviatura


class Cotacao(models.Model):
    moeda = models.ForeignKey(Moeda, on_delete=models.CASCADE)
    data = models.DateField('Data da cotação', auto_now_add=True)
    valor = models.DecimalField('Valor', decimal_places=16, max_digits=21, default=0)

    def __str__(self):
        return self.moeda