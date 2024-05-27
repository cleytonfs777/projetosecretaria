from datetime import timedelta
from django import template
from django.db.models import Case, FloatField, Sum, When
from ..models import Empenho, Militar

register = template.Library()

# MEUS DICIONARIOS
MAP_VALUES = {
    'sd2cl': 'Sd 2ª Classe',
    'sd': 'Sd',
    'cb': 'Cb',
    '3sgt': '3º Sgt',
    '2sgt': '2º Sgt',
    '1sgt': '1º Sgt',
    'subten': 'Sub Ten',
    '2ten': '2º Ten',
    '1ten': '1º Ten',
    'cap': 'Cap',
    'maj': 'Maj',
    'tencel': 'Ten Cel',
    'cel': 'Cel'
}

MAP_LOCALS = {
    'acf': 'ACF',
    'acf1': 'ACF-1',
    'acf2': 'ACF-2',
    'acf3': 'ACF-3',
    'sdts1': 'SDTS 1',
    'sdts2': 'SDTS 2',
    'sdts3': 'SDTS 3',
    'nts': 'NTS',
    'gol': 'GOL',
    'sdal': 'SDAL',
    'sdal1': 'SDAL 1',
    'sdal2': 'SDAL 2',
    'sdal3': 'SDAL 3',
    'sdal4': 'SDAL 4',
    'sec': 'Secretaria'
}

MAP_MONTHS = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}


@register.filter(name="formatdatetime")
def formatdatetime(value):
    if value:
        # Formatar data e hora com timezone
        value -= timedelta(hours=3)
        return value.strftime("%d/%m/%Y %H:%M")
    else:
        return None


@register.filter(name="formattime")
def formattime(value):
    if value:
        return value.strftime("%H:%M")
    else:
        return "---"


@register.filter(name="formatinfo")
def formatinfo(value):
    if value:
        return value
    else:
        return "Não há"


@register.filter(name="formatdate")
def formatdate(value):
    if value:
        return value.strftime("%d/%m/%Y")
    else:
        return None


@register.filter(name="listranfpostgrad")
def listranfpostgrad(lista):
    return [MAP_VALUES.get(item, item) for item in lista]


@register.filter(name="formatpostgrad")
def formatpostgrad(value):
    return MAP_VALUES.get(value, value)


@register.filter(name="formatlocal")
def formatlocal(value):
    return MAP_LOCALS.get(value, value)


@register.filter(name="empenhos_por_militar")
def empenhos_por_militar(militar_id):
    try:
        militar = Militar.objects.get(id=militar_id)
        return militar.empenhos.all()
    except Militar.DoesNotExist:
        return []


@register.filter(name="militares_por_empenho")
def militares_por_empenho(empenho_id):
    try:
        empenho = Empenho.objects.get(id=empenho_id)
        return empenho.militares.all()
    except Empenho.DoesNotExist:
        return []


@register.filter(name="getyear")
def getyear(value):
    return value.strftime("%Y")


@register.filter(name="mestexto")
def mestexto(value):
    return MAP_MONTHS.get(value, value)


@register.filter(name="minutos_para_horas")
def minutos_para_horas(minutos):
    # Calcula as horas e os minutos restantes
    horas = minutos // 60
    minutos_rest = minutos % 60

    # Retorna a string formatada
    return f"{horas:02d}:{minutos_rest:02d}"
