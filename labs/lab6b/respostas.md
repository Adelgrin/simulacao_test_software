## Exercício 1
b. classes de equivalência
    - -1
    - 1.1 
    - 0
    - 15
    - 16
    - 17
    - 179
    - 180
    - 181
    - 182
    - 719
    - 720
    - 721
A faixa 181 a 720 é dividida em 181, 182, 719, 720, 721. Porque o valor é variável e precisa ser validado se a lógica está correta.

## Exercício 2
a. Divergências em relação à especificação

| # | Defeito | Menor entrada | Devolve | Esperado | Correção |
|---|---------|---------------|---------|----------|----------|
| 1 | `minutos <= 0` | 0 | `ValueError` | 0.00 | `minutos < 0` |
| 2 | `minutos < 15` | 15 | 12.00 | 0.00 | `minutos <= 15` |
| 3 | `//` arredonda para baixo | 181 | 12.00 | 15.00 | `math.ceil((minutos - 180) / 60)` |
| 4 | `minutos < 720` | 720 | 60.00 | 39.00 | `minutos <= 720` |
| 5 | `bool` é subclasse de `int` | `False` | `ValueError` | `TypeError` | `isinstance(minutos, bool) or not isinstance(minutos, int)` |

No defeito 5, `True` devolve 0.00 em vez de lançar `TypeError`.

b. Sim. Rodando a suíte do Exercício 1 em `test_estagiario.py`, 8 testes falham e 10 passam. As falhas cobrem as 5 divergências, porque a suíte testa os valores-limite 0, 15, 181, 720 e `True`.

c. Não. Com 8, 100, 300 e 1000 minutos, as duas versões devolvem o mesmo valor (0.00, 12.00, 18.00 e 60.00). Em 300 minutos sobram 120 minutos, que são 2 horas exatas, então o `//` dá o mesmo resultado que o arredondamento para cima. Todos os defeitos estão nas fronteiras das faixas, e um representante no meio de cada classe nunca chega nelas.

## Exercício 3
a. Condições: C1 = credencial PCD/idoso, C2 = compras >= R$ 150,00, C3 = cadastro no aplicativo, C4 = permanência <= 240 minutos.

Tabela completa:

| Condição | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|----------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|
| C1 Credencial? | S | S | S | S | S | S | S | S | N | N | N | N | N | N | N | N |
| C2 Compras >= 150? | S | S | S | S | N | N | N | N | S | S | S | S | N | N | N | N |
| C3 Cadastro app? | S | S | N | N | S | S | N | N | S | S | N | N | S | S | N | N |
| C4 Permanência <= 240? | S | N | S | N | S | N | S | N | S | N | S | N | S | N | S | N |
| Isento? | S | S | S | S | S | S | S | S | S | N | S | N | S | N | N | N |

Tabela reduzida:

| Condição | R1 | R2 | R3 | R4 | R5 |
|----------|----|----|----|----|----|
| C1 Credencial? | S | N | N | N | N |
| C2 Compras >= 150? | X | X | S | N | N |
| C3 Cadastro app? | X | X | X | S | N |
| C4 Permanência <= 240? | X | N | S | S | S |
| Isento? | S | N | S | S | N |
| Regras da completa | 1-8 | 10, 12, 14, 16 | 9, 11 | 13 | 15 |

Justificativa dos X:
- R1: com credencial o veículo é sempre isento, então compras, cadastro e permanência não alteram o resultado (regras 1 a 8 têm todas a mesma ação).
- R2: sem credencial e com permanência acima de 240 minutos, o cliente paga mesmo com compras ou cadastro, porque a isenção por compras/cadastro exige permanência <= 240 (regras 10, 12, 14 e 16).
- R3: sem credencial, com permanência <= 240 e compras >= R$ 150,00, a condição "compras ou cadastro" já está satisfeita, então o cadastro não importa (regras 9 e 11).
- R4 e R5 não têm X: sem credencial, sem compras e com permanência <= 240, o cadastro decide o resultado.

b. Implementado em `isencao/isencao.py`.

c. Implementado em `isencao/test_isencao.py`, com uma linha por regra da tabela reduzida (R1 a R5). Compras usam R$ 150,00 / R$ 149,99 e permanência usa 240 / 241 minutos. Nos X, o valor escolhido é o que levaria ao resultado oposto caso a condição importasse.

## Exercício 4
a. Implementação errada em `isencao/isento_errado.py`:

```python
def isento(pcd, valor_compra, cadastro_app, minutos):
    if cadastro_app:
        return True
    if minutos > 240:
        return False
    return pcd or valor_compra >= 150.00
```

Ela passa nos cinco casos do colega, mas erra 4 regras da tabela completa:
- Regras 4 e 8 (credencial, sem cadastro, permanência > 240): devolve `False`, esperado `True`. A credencial deixa de valer acima de 240 minutos.
- Regras 10 e 14 (sem credencial, com cadastro, permanência > 240): devolve `True`, esperado `False`. O cadastro isenta sem olhar a permanência.

b. O teste do colega supôs que, se a tabela diz X, qualquer valor serve, e não verificou que a condição realmente não importa. Os valores escolhidos para os X empurram para o mesmo resultado esperado: no R1 a permanência é 100 (<= 240), e no R2 o cadastro é `False`. Assim, uma implementação que use a permanência no R1 ou o cadastro no R2 continua passando.

Casos corrigidos, mantendo cinco (em `test_colega.py`, função `test_isento_corrigido`):

| Regra | pcd | compra | app | minutos | esperado |
|-------|-----|--------|-----|---------|----------|
| R1 | True | 149.99 | False | 241 | True |
| R2 | False | 150.00 | True | 241 | False |
| R3 | False | 150.00 | False | 240 | True |
| R4 | False | 149.99 | True | 240 | True |
| R5 | False | 149.99 | False | 240 | False |

Com esses valores, R1 e R2 falham na implementação errada e passam na correta.

c. Regra geral: para cada condição marcada com X, escolha o valor concreto que, se a condição importasse, levaria ao resultado oposto ao esperado pela regra. Quando a condição é numérica, use o valor-limite desse lado da fronteira (por exemplo, 241 minutos ou R$ 150,00). Assim o teste só passa se a condição realmente não influenciar o resultado.
