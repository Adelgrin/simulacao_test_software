import pytest

import estacionamento
@pytest.mark.parametrize(
    ("minutos", "tarifa"),
    [
        (0,0.0),
        (15,0.0),
        (16,12.0),
        (17,12.0),
        (179,12.0),
        (180,12.0),
        (181,15.0),
        (182,15.0),
        (240,15.0),
        (241,18.0),
        (719,39.0),
        (720,39.0),
        (721,60.0),
    ],
    ids=[
        "gratis_min",
        "gratis_max",
        "baixa_min",
        "baixa_acima_min",
        "baixa_abaixo_max",
        "baixa_max",
        "media_min",
        "media_acima_min",
        "media_1_hora_exata",
        "media_2_horas",
        "media_abaixo_max",
        "media_max",
        "diaria_min",
    ],
)
def test_calcular(minutos,tarifa):
    assert estacionamento.calcular_tarifa(minutos) == tarifa


def test_minutos_negativo():
    with pytest.raises(ValueError):
        estacionamento.calcular_tarifa(-1)


@pytest.mark.parametrize(
    "minutos", [1.1, -1.5, "10", True],
    ids=["float", "float_negativo", "string", "bool"])
def test_minutos_nao_inteiro(minutos):
    with pytest.raises(TypeError):
        estacionamento.calcular_tarifa(minutos)
