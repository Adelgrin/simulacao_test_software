import pytest

from senha import forca


# b/c) base de caminhos viáveis (o caminho P2, laço com 0 voltas, é inviável)
@pytest.mark.parametrize(
    "senha, esperado",
    [
        ("abc", "fraca"),       # P1: len < 8
        ("abcdefgh", "media"),  # P3: só letras (6 F -> 8 F)
        ("abcdefg1", "media"),  # P4: dígito (6 V)
        ("abcdefg!", "media"),  # P5: símbolo (8 V)
        ("abcdef!!", "forte"),  # P6: pontos >= 4 (10 V)
    ],
)
def test_caminhos_base(senha, esperado):
    assert forca(senha) == esperado


# d) teste de laços: o for dá len(senha) voltas, e só chega nele com len >= 8
@pytest.mark.parametrize(
    "senha, esperado",
    [
        ("abcdefg", "fraca"),            # 7 caracteres: não entra no laço
        ("12345678", "forte"),           # mínimo: exatamente 8 voltas
        ("abcdefgh1", "media"),          # mínimo + 1: 9 voltas
        ("abc123!xyz", "forte"),         # número típico de voltas (10)
        ("a" * 999 + "1", "media"),      # muitas voltas (1000)
        ("abcdefg" + "!" * 1000, "forte"),
        ("abcde123", "media"),           # fronteira: 3 pontos
        ("abcd1234", "forte"),           # fronteira: 4 pontos
    ],
)
def test_lacos(senha, esperado):
    assert forca(senha) == esperado
