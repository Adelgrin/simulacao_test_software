import pytest
def calcular_imc(peso, altura):
    if altura <=0:
        raise ValueError("altura não pode ser negativa ou 0")
    elif peso <= 0:
        raise ValueError("peso não pode ser negativo ou 0")
    imc = peso/altura**2
    return imc
def categorizar_imc(imc):
    if imc < 18.5:
        return("abaixo do peso")
    elif 18.5 <= imc < 25:
        return "peso normal"
    elif 25<= imc < 30:
        return "sobrepeso"
    elif imc >=30:
        return "obesidade"
    else:
        raise ValueError("valor fora do escopo")
def classificar_pessoa(peso,altura):
    imc = calcular_imc(peso, altura)
    classe = categorizar_imc(imc)
    return imc, classe
@pytest.mark.parametrize(
    ("imc", "categoria"),
    [
        (18.5,"peso normal"),
        (25,"sobrepeso"),
        (30,"obesidade"),
        (15,"abaixo do peso"),
        (35,"obesidade")
    ],
    ids=[
        "igual_limite_inferior",
        "igual_limite_intermediario",
        "igual_limite_superior",
        "abaixo_limite_inferior",
        "acima_limite_superior",
    ],
)
def test_classificar(imc,categoria):
    assert categorizar_imc(imc) == categoria

def test_calcular():
    with pytest.raises(ValueError):
        calcular_imc(-1,-15)
