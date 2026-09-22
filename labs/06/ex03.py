import pytest
def classificar_por_faixa(valor,faixas):
    for limite_superior, rotulo in faixas:
        if valor <= limite_superior:
            return rotulo
    return faixas[-1][1]

def classificar_vento(velocidade):
    faixas = [
        (20,"calmo"),
        (40,"moderado"),
        (60,"forte"),
        (float("inf"),"tempestade")
    ]
    return classificar_por_faixa(velocidade, faixas)

@pytest.mark.parametrize(
("velocidade", "rotulo"),
    [
        (19,"calmo"),
        (20,"calmo"),
        (21,"moderado"),
        (30,"moderado"),
        (39,"moderado"),
        (40,"moderado"),
        (41,"forte"),
        (50,"forte"),
        (59,"forte"),
        (60,"forte"),
        (61,"tempestade"),
    ],
    ids=[
        "velocidade19_calmo",
        "velocidade20_calmo",
        "velocidade21_moderado",
        "velocidade30_moderado",
        "velocidade39_moderado",
        "velocidade40_moderado",
        "velocidade41_forte",
        "velocidade50_forte",
        "velocidade59_forte",
        "velocidade60_forte",
        "velocidade61_tempestade",
    ],
)
def test_classificar_vento_param(velocidade,rotulo):
    assert classificar_vento(velocidade) == rotulo
