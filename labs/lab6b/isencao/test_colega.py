import pytest

from isento_errado import isento
@pytest.mark.parametrize("pcd,compra,app,minutos,esperado", [
    (True, 0.00, False, 100, True),      # R1
    (False, 200.00, False, 300, False),  # R2
    (False, 200.00, False, 100, True),   # R3
    (False, 50.00, True, 100, True),     # R4
    (False, 50.00, False, 100, False),   # R5
], ids=["R1", "R2", "R3", "R4", "R5"])
def test_isento(pcd, compra, app, minutos, esperado):
    assert isento(pcd, compra, app, minutos) is esperado


detecta_errado = pytest.mark.xfail(
    strict=True, reason="caso corrigido detecta a implementacao errada")


@pytest.mark.parametrize("pcd,compra,app,minutos,esperado", [
    pytest.param(True, 149.99, False, 241, True, id="R1", marks=detecta_errado),
    pytest.param(False, 150.00, True, 241, False, id="R2", marks=detecta_errado),
    pytest.param(False, 150.00, False, 240, True, id="R3"),
    pytest.param(False, 149.99, True, 240, True, id="R4"),
    pytest.param(False, 149.99, False, 240, False, id="R5"),
])
def test_isento_corrigido(pcd, compra, app, minutos, esperado):
    assert isento(pcd, compra, app, minutos) is esperado
