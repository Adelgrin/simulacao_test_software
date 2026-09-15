class CarteiraDigital:
    def __init__(self,saldo_inicial=0):
        self.saldo = saldo_inicial

    def depositar(self,valor):
        self.saldo += valor

    def sacar(self,valor):
        self.saldo -= valor

def test_saldo_inicial_padrao_zero():
    carteira = CarteiraDigital()

    saldo = carteira.saldo

    assert saldo == 0


def test_saldo_inicial_personalizado():
    saldo_inicial = 150.0

    carteira = CarteiraDigital(saldo_inicial)

    assert carteira.saldo == saldo_inicial


def test_depositar_aumenta_o_saldo():
    carteira = CarteiraDigital(100)
    valor = 50

    carteira.depositar(valor)

    assert carteira.saldo == 150


def test_sacar_dentro_do_saldo_disponivel():
    carteira = CarteiraDigital(200)
    valor = 75

    carteira.sacar(valor)

    assert carteira.saldo == 125


def test_deposito_e_saque_em_sequencia():
    carteira = CarteiraDigital(50)

    carteira.depositar(30)
    carteira.sacar(20)

    assert carteira.saldo == 60
