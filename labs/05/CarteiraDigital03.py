import os
import pytest
class CarteiraDigital03:
    def __init__ (
        self,saldo_inicial=0 , log_path = "carteira.log"):
        self.saldo = saldo_inicial
        self.log_path = log_path
    def depositar (self,valor) :
        self.saldo += valor
        with open ( self.log_path , "a" ) as f :
            f . write (f"deposito:{valor}\n")
@pytest.fixture
def carteira_com_log():
    if os.path.exists("carteira.log"):
        os.remove("carteira.log")
def test_grava_log(carteira_com_log):
    carteira = CarteiraDigital03()
    carteira.depositar(50)
    with open("carteira.log","r",encoding="utf-8") as f:
        conteudo = f.read()
    assert conteudo == "deposito:50\n"
