import pytest

class CarteiraDigital05:
    def __init__(self, saldo=0):
        self.saldo = saldo
    
    def sacar(self, valor):
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= valor
    
    def depositar(self, valor):
        self.saldo += valor


def transferir(origem, destino, valor):
    origem.sacar(valor)
    destino.depositar(valor)


@pytest.fixture
def carteiras():
    origem = CarteiraDigital05(saldo=1000)
    destino = CarteiraDigital05(saldo=0)
    return origem, destino


@pytest.mark.parametrize("valor,ids", [
(100, "pequeno"),
(500, "medio"),
(1000, "total"),
])
def test_transferencia_bem_sucedida(carteiras, valor, ids):
    origem, destino = carteiras
    saldo_origem_antes = origem.saldo
    saldo_destino_antes = destino.saldo

    transferir(origem, destino, valor)
    
    assert origem.saldo == saldo_origem_antes - valor
    assert destino.saldo == saldo_destino_antes + valor


def test_transferencia_saldo_insuficiente(carteiras):
    origem, destino = carteiras
    saldo_origem_antes = origem.saldo
    saldo_destino_antes = destino.saldo
    
    with pytest.raises(ValueError):
        transferir(origem, destino, 1500)
    
    assert origem.saldo == saldo_origem_antes
    assert destino.saldo == saldo_destino_antes
