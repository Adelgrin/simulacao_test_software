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


# print(classificar_pessoa(70,1.7))
# print(classificar_pessoa(60,1.6))
# print(classificar_pessoa(57,1.5))
# print(classificar_pessoa(88,1.9))

def test_pessoas():
    pess1 = classificar_pessoa(70, 1.7)
    assert pess1[0] == pytest.approx(24.2214532)
    assert pess1[1] == "peso normal"

    pess2 =  classificar_pessoa(40, 1.6)
    assert pess2[0] == pytest.approx(15.62499)
    assert pess2[1] == "abaixo do peso"

    pess3 = classificar_pessoa(57, 1.5)
    assert pess3[0] == pytest.approx(25.333333) 
    assert pess3[1] == "sobrepeso"

    pess4 = classificar_pessoa(88, 1.9)
    assert pess4[0] == pytest.approx(24.3767313)
    assert pess4[1] == "peso normal"
