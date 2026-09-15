class SaldoInsuficienteError(Exception):
    pass
class CarteiraDigital02:
    def __init__(self,saldo_inicial=0):
        self.saldo = saldo_inicial

    def depositar(self,valor):
        self.saldo += valor

    def sacar(self,valor):
        if valor > self.saldo:
            raise SaldoInsuficienteError("Saldo insuficiente para realizar o saque")
        else:
            self.saldo -= valor

def test_saldo_insuficiente():
    carteira = CarteiraDigital02(100)
    try:
        carteira.sacar(200)
    except SaldoInsuficienteError as e:
        assert type(e) is SaldoInsuficienteError
        assert str(e) == "Saldo insuficiente para realizar o saque"

