import pytest
def classificar_transacao(valor):
    if valor < 100:
        return "pequena"
    elif valor < 1000:
        return "media"
    else:
        return "grande"
@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0,"pequena"),
        (99,"pequena"),
        (100, "media"),
        (999,"media"),
        (1000,"grande"),
        (1001,"grande"),
    ],
    ids=[
        "valor_zero_pequeno",
        "valor_abaixo_do_limite",
        "valor_exatamente_100_media",
        "valor_abaixo_de_1000_grande",
        "valor_exatamente_1000_grande",
        "valor_acima_de_1000_grande",
    ],
)
def test_classifier_transacao_parametrizado(valor,esperado):
    assert classificar_transacao(valor) == esperado
