from django.db import models
from cadastros.models import Militar
tipo_choices = (
    ('ferias', 'Férias'),
    ('licenca', 'Licença'),
    ('dispensa', 'Dispensa'),
    ('outros', 'Outros'),
)

classe_choices = (
    ('feriado', 'Feriado'),
    ('pontof', 'Ponto Facultativo'),
    ('libaracao', 'Libaracao'),
)

class IndispMilitar(models.Model):
    tipo = models.CharField(max_length=10, choices=tipo_choices, blank=True, null=True)
    datainicial = models.DateTimeField(blank=True, null=True)
    datafinal = models.DateTimeField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    militar = models.ForeignKey(
        'cadastros.Militar', on_delete=models.CASCADE, related_name='indisp_militar', null=True)

    def __str__(self):
        return self.tipo


class DiaZero(models.Model):
    nome = models.CharField(max_length=100)
    classe = models.CharField(max_length=10, choices=classe_choices, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateTimeField(blank=True, null=True)
    horainicial = models.TimeField(blank=True, null=True)
    horafinal = models.TimeField(blank=True, null=True)
    all_day = models.BooleanField(default=True)

    def __str__(self):
        return self.nome