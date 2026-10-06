import pytest

from isencao import isento
@pytest.mark.parametrize(
    ("pcd", "compra", "app", "minutos", "esperado"),
    [
        (True, 149.99, False, 241, True),
        (False, 150.00, True, 241, False),
        (False, 150.00, False, 240, True),
        (False, 149.99, True, 240, True),
        (False, 149.99, False, 240, False),
    ],
    ids=["R1", "R2", "R3", "R4", "R5"],
)
def test_isento(pcd, compra, app, minutos, esperado):
    assert isento(pcd, compra, app, minutos) is esperado
