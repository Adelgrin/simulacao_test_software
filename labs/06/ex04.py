import itertools

import pytest


def tem_frete_gratis(valor_compra, cliente_premium, peso):
    return valor_compra >= 200 and cliente_premium and peso <= 30


# a) Tabela de decisao completa (3 condicoes binarias -> 8 regras)
#
# Condicoes:
#   C1 = valor_compra >= 200
#   C2 = cliente_premium
#   C3 = peso <= 30
#
# | Regra | C1 | C2 | C3 | Acao            |
# |-------|----|----|----|-----------------|
# | R1    | V  | V  | V  | frete gratis    |
# | R2    | V  | V  | F  | frete cobrado   |
# | R3    | V  | F  | V  | frete cobrado   |
# | R4    | V  | F  | F  | frete cobrado   |
# | R5    | F  | V  | V  | frete cobrado   |
# | R6    | F  | V  | F  | frete cobrado   |
# | R7    | F  | F  | V  | frete cobrado   |
# | R8    | F  | F  | F  | frete cobrado   |

VALOR_ALTO = 250.0    # C1 = V
VALOR_BAIXO = 150.0   # C1 = F
PESO_LEVE = 20.0      # C3 = V
PESO_PESADO = 40.0    # C3 = F


@pytest.mark.parametrize(
    ("valor_compra", "cliente_premium", "peso", "esperado"),
    [
        (VALOR_ALTO, True, PESO_LEVE, True),
        (VALOR_ALTO, True, PESO_PESADO, False),
        (VALOR_ALTO, False, PESO_LEVE, False),
        (VALOR_ALTO, False, PESO_PESADO, False),
        (VALOR_BAIXO, True, PESO_LEVE, False),
        (VALOR_BAIXO, True, PESO_PESADO, False),
        (VALOR_BAIXO, False, PESO_LEVE, False),
        (VALOR_BAIXO, False, PESO_PESADO, False),
    ],
    ids=["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"],
)
def test_tabela_completa(valor_compra, cliente_premium, peso, esperado):
    assert tem_frete_gratis(valor_compra, cliente_premium, peso) is esperado


# b) Tabela reduzida por don't care ("-")
#
# | Regra | C1 | C2 | C3 | Acao          | Regras cobertas |
# |-------|----|----|----|---------------|-----------------|
# | RA    | V  | V  | V  | frete gratis  | R1              |
# | RB    | V  | V  | F  | frete cobrado | R2              |
# | RC    | V  | F  | -  | frete cobrado | R3, R4          |
# | RD    | F  | -  | -  | frete cobrado | R5, R6, R7, R8  |
#
# Justificativa de cada don't care:
#
# RC (C3 = -): com C1 = V e C2 = F o cliente nao e premium, e a assinatura
#   premium e obrigatoria para o frete gratis. A regra ja esta decidida como
#   "frete cobrado" antes de olhar o peso, entao C3 nao importa: R3 (peso <= 30)
#   e R4 (peso > 30) dao a mesma acao e se fundem numa unica regra.
#
# RD (C2 = - e C3 = -): com C1 = F a compra nao atinge R$200, e o valor minimo
#   tambem e obrigatorio. A acao ja e "frete cobrado" independentemente de o
#   cliente ser premium ou nao e de o pedido ser leve ou pesado, entao as quatro
#   combinacoes de C2/C3 (R5 a R8) colapsam numa unica regra.
#
# Observacao: em RA e RB nenhuma condicao vira don't care. Em RA as tres
# precisam ser V para liberar o frete, e em RB o unico motivo da cobranca e
# C3 = F, ou seja, o peso e justamente a condicao decisiva.

DONT_CARE = "-"

TABELA_REDUZIDA = [
    ("RA", True, True, True, True),
    ("RB", True, True, False, False),
    ("RC", True, False, DONT_CARE, False),
    ("RD", False, DONT_CARE, DONT_CARE, False),
]


def _expandir(condicao):
    return [True, False] if condicao is DONT_CARE else [condicao]


def _casos_reduzidos():
    casos = []
    ids = []
    for regra, c1, c2, c3, esperado in TABELA_REDUZIDA:
        for v1, v2, v3 in itertools.product(*map(_expandir, (c1, c2, c3))):
            valor = VALOR_ALTO if v1 else VALOR_BAIXO
            peso = PESO_LEVE if v3 else PESO_PESADO
            casos.append((valor, v2, peso, esperado))
            ids.append(f"{regra}_C1{'V' if v1 else 'F'}"
                       f"_C2{'V' if v2 else 'F'}_C3{'V' if v3 else 'F'}")
    return casos, ids


_CASOS_REDUZIDOS, _IDS_REDUZIDOS = _casos_reduzidos()


@pytest.mark.parametrize(
    ("valor_compra", "cliente_premium", "peso", "esperado"),
    _CASOS_REDUZIDOS,
    ids=_IDS_REDUZIDOS,
)
def test_tabela_reduzida(valor_compra, cliente_premium, peso, esperado):
    assert tem_frete_gratis(valor_compra, cliente_premium, peso) is esperado


@pytest.mark.parametrize(
    ("valor_compra", "peso", "esperado"),
    [
        (200.0, 30.0, True),
        (199.99, 30.0, False),
        (200.0, 30.01, False),
    ],
    ids=["limites_exatos", "valor_abaixo_do_limite", "peso_acima_do_limite"],
)
def test_limites(valor_compra, peso, esperado):
    assert tem_frete_gratis(valor_compra, True, peso) is esperado
