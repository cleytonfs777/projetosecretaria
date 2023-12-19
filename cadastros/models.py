from django.db import models

postgrad_choices = (
    ('sd2cl', 'Sd 2ª Classe BM'),
    ('sd', 'Sd BM'),
    ('cb', 'Cb BM'),
    ('3sgt', '3º Sgt BM'),
    ('2sgt', '2º Sgt BM'),
    ('1sgt', '1º Sgt BM'),
    ('subten', 'Sub Ten BM'),
    ('2ten', '2º Ten BM'),
    ('1ten', '1º Ten BM'),
    ('cap', 'Cap BM'),
    ('maj', 'Maj BM'),
    ('tencel', 'Ten Cel BM'),
    ('cel', 'Cel BM'),
)

local_choices = (
    ('acf', 'ACF'),
    ('acf1', 'ACF-1'),
    ('acf2', 'ACF-2'),
    ('acf3', 'ACF-3'),
    ('sdts1', 'SDTS-1'),
    ('sdts2', 'SDTS-2'),
    ('sdts3', 'SDTS-3'),
    ('nts', 'NTS'),
    ('gol', 'GOL'),
    ('sdal', 'SDAL'),
    ('sdal1', 'SDAL-1'),
    ('sdal2', 'SDAL-2'),
    ('sdal3', 'SDAL-3'),
    ('sdal4', 'SDAL-4'),
    ('secretaria', 'Secretaria'),
    )

tipo_choices = (
    ('escala', 'Escala'),
    ('demanda', 'Demanda'),
    ('dsp', 'DSP'),
)




class Militar(models.Model):
    numero = models.CharField(max_length=100, blank=True, null=True)
    nome = models.CharField(max_length=100)
    postgrad = models.CharField(max_length=10, choices=postgrad_choices, blank=True, null=True)
    local = models.CharField(max_length=10, choices=local_choices, blank=True, null=True)
    qtd_empenhos = models.IntegerField(blank=True, null=True)
    empenhos_minutos_atipica = models.IntegerField(blank=True, null=True)
    empenhos_minutos_tipica = models.IntegerField(blank=True, null=True)
    empenhos = models.ManyToManyField(
        'Empenho', related_name='militares')

    def __str__(self):
        return f"{self.postgrad} {self.nome}"
    
class Empenho(models.Model):
    tipo = models.CharField(max_length=10, choices=tipo_choices, blank=True, null=True)
    nome = models.CharField(max_length=100)
    datahorainicial = models.DateTimeField(blank=True, null=True)
    datahorafinal = models.DateTimeField(blank=True, null=True)
    duracao_em_minutos_atipica = models.IntegerField(blank=True, null=True)
    duracao_em_minutos_tipica = models.IntegerField(blank=True, null=True)
    documentacao = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

