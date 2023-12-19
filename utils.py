def hm_para_minutos(horas_minutos):
    horas, minutos = map(int, horas_minutos.split(':'))
    return horas * 60 + minutos

def minutos_para_hm(minutos):
    # Calcula as horas e os minutos restantes
    horas = minutos // 60
    minutos_rest = minutos % 60