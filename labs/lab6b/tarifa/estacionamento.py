import math
def calcular_tarifa(minutos):
    if isinstance(minutos,bool) or not isinstance(minutos,int):
        raise TypeError
    elif minutos < 0:
        raise ValueError
    if 0 <= minutos <= 15:
        return 0.0
    elif 16 <= minutos <= 180:
        return 12.0
    elif 181 <= minutos <= 720:
        horas_adicionais = math.ceil((minutos - 180) / 60)
        return 12.0 + horas_adicionais * 3
    elif minutos > 720:
        return 60.0
