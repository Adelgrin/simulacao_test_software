import pytest

import embarque_original
from embarque import pode_embarcar
from mcdc import conjuntos_mcdc_minimos, pares_independentes, regra, tabela_verdade

LINHAS = tabela_verdade(4)


# b) pares independentes e conjuntos MC/DC mínimos
def test_pares_independentes():
    assert pares_independentes(regra, 4) == {
        0: [(5, 13), (6, 14), (7, 15)],  # cartao
        1: [(9, 13), (10, 14), (11, 15)],  # documento
        2: [(12, 14)],  # grupo_chamado
        3: [(12, 13)],  # prioridade
    }


def test_conjuntos_mcdc_minimos():
    assert sorted(map(sorted, conjuntos_mcdc_minimos(regra, 4))) == [
        [5, 9, 12, 13, 14],
        [5, 10, 12, 13, 14],
        [6, 9, 12, 13, 14],
        [6, 10, 12, 13, 14],
    ]


# c) todos V e todos F: a versão original passa
@pytest.mark.parametrize("linha", [(True,) * 4, (False,) * 4])
def test_todos_v_todos_f(linha):
    assert embarque_original.pode_embarcar(*linha) == regra(*linha)


# d) em cada conjunto MC/DC mínimo, a original diverge da regra?
@pytest.mark.parametrize(
    "conjunto, acha_defeito",
    [
        ({5, 9, 12, 13, 14}, True),
        ({5, 10, 12, 13, 14}, True),
        ({6, 9, 12, 13, 14}, True),
        ({6, 10, 12, 13, 14}, False),
    ],
)
def test_mcdc_na_original(conjunto, acha_defeito):
    divergentes = [
        i for i in conjunto
        if embarque_original.pode_embarcar(*LINHAS[i]) != regra(*LINHAS[i])
    ]
    assert bool(divergentes) == acha_defeito


# d) MCC: as 16 combinações acham o defeito na original...
def test_mcc_acha_defeito_na_original():
    divergentes = [
        i for i, linha in enumerate(LINHAS)
        if embarque_original.pode_embarcar(*linha) != regra(*linha)
    ]
    assert divergentes == [1, 3, 5, 7, 9, 11]


# ...e a versão corrigida concorda com a regra em todas elas
@pytest.mark.parametrize("linha", LINHAS)
def test_corrigida_mcc(linha):
    assert pode_embarcar(*linha) == regra(*linha)
