import pytest

import preco_original
from preco import preco_final


# suíte atual: 100% de ramos
def test_suite_atual():
    assert preco_final(60, True) == 50
    assert preco_final(200, False) == 200


# c) casos que faltam para All-Uses
def test_vip_acima_do_minimo():
    # pares (5, 6-F) e (5, 8) de total: o valor com desconto chega ao return
    assert preco_final(100, True) == pytest.approx(80)


def test_comum_abaixo_do_minimo():
    # par (2, 6-V) de total: o valor sem desconto é testado e fica abaixo de 50
    assert preco_final(40, False) == 50


# c) o mesmo caso VIP na versão original expõe o desconto duplo
def test_original_desconta_duas_vezes():
    assert preco_original.preco_final(100, True) == pytest.approx(60)
