# Exercício 2 — Controle de Embarque


## a) `regra` e `pares_independentes`

A especificação diz "cartão **e** documento, **e** (grupo chamado **ou**
prioridade)":

```python
def regra(cartao, documento, grupo_chamado, prioridade):
    return cartao and documento and (grupo_chamado or prioridade)
```

`pares_independentes(decisao, n)` percorre a tabela-verdade gerada por
`itertools.product((False, True), repeat=n)`. A linha `i` é o número `i` em
binário (C é o bit mais significativo, F = 0, V = 1). Para cada condição `k` e cada
linha em que ela é F, a linha "gêmea" com `k` em V é `i + 2**(n-1-k)`. O par entra
na lista se a decisão muda entre as duas linhas.

## b) Pares e conjuntos MC/DC mínimos

Linhas relevantes da tabela-verdade de `regra` (C D G P):

| Linha | C | D | G | P | regra |
| ----- | - | - | - | - | ----- |
| 5  | F | V | F | V | F |
| 6  | F | V | V | F | F |
| 7  | F | V | V | V | F |
| 9  | V | F | F | V | F |
| 10 | V | F | V | F | F |
| 11 | V | F | V | V | F |
| 12 | V | V | F | F | F |
| 13 | V | V | F | V | **V** |
| 14 | V | V | V | F | **V** |
| 15 | V | V | V | V | **V** |

| Condição | Pares independentes | Quantidade |
| -------- | ------------------- | ---------- |
| C (cartao) | (5, 13), (6, 14), (7, 15) | **3** |
| D (documento) | (9, 13), (10, 14), (11, 15) | **3** |
| G (grupo_chamado) | (12, 14) | **1** |
| P (prioridade) | (12, 13) | **1** |

G e P só têm um par cada, então as linhas **12, 13 e 14** são obrigatórias. Para
C e D, os pares que reaproveitam 13 ou 14 custam uma linha só: C escolhe entre 5
ou 6 e D entre 9 ou 10 (usar o par com a 15 custaria duas linhas).

**Existem 4 conjuntos MC/DC mínimos, cada um com 5 casos (n + 1):**

| Conjunto | Linhas |
| -------- | ------ |
| M1 | {5, 9, 12, 13, 14} |
| M2 | {5, 10, 12, 13, 14} |
| M3 | {6, 9, 12, 13, 14} |
| M4 | {6, 10, 12, 13, 14} |

`conjuntos_mcdc_minimos` confirma por força bruta (`test_conjuntos_mcdc_minimos`).

## c) Todos V e todos F

| Entrada | `pode_embarcar` original | `regra` |
| ------- | ------------------------ | ------- |
| (V, V, V, V) | True | True |
| (F, F, F, F) | False | False |

Os dois testes **passam**, e a cobertura da versão original fica em **100%**:

```
$ pytest -q --cov=embarque_original --cov-branch   (só os dois testes)
embarque_original.py       4      0      2      0   100%
2 passed
```

Dois testes já cobrem os dois ramos do `if`, mas nenhum deles separa
`(C and D and G) or P` de `C and D and (G or P)`. 100% de ramos não encontrou o
defeito.

## d) Comparação em cada conjunto MC/DC mínimo

A original calcula `(C and D and G) or P`. Ela diverge da especificação sempre que
**P = V e falta cartão ou documento**, porque aí a prioridade sozinha libera o
embarque. Na tabela, essas são as linhas **1, 3, 5, 7, 9 e 11**.

| Conjunto | Linha que diverge | Acha o defeito? |
| -------- | ----------------- | --------------- |
| M1 {5, 9, 12, 13, 14} | 5 e 9 | **Sim** |
| M2 {5, 10, 12, 13, 14} | 5 | **Sim** |
| M3 {6, 9, 12, 13, 14} | 9 | **Sim** |
| M4 {6, 10, 12, 13, 14} | nenhuma | **Não** |

**Por quê:** as linhas 12, 13 e 14 têm C = D = V e dão o mesmo resultado nas duas
versões. O defeito só aparece numa linha com P = V e C ou D falso. A linha 5
(sem cartão, com prioridade) e a linha 9 (sem documento, com prioridade) servem.
M4 mostra a independência de C e D com as linhas 6 e 10, que têm **P = F**. Nelas a
prioridade não entra em jogo e a original devolve False, como a regra. Todo
conjunto MC/DC é válido para a especificação, mas cada um escolhe pares
diferentes, e só os que usam P = V com C ou D falso expõem o erro de precedência.

**Por que o MCC sempre acharia:** o teste de múltiplas condições executa as
2⁴ = 16 combinações. Duas funções booleanas diferentes discordam em pelo menos uma
combinação de entradas, e o MCC testa todas elas, então essa combinação está
sempre lá (aqui são seis: 1, 3, 5, 7, 9, 11).
`test_mcc_acha_defeito_na_original` confirma.

**Correção** (`embarque.py`): faltavam os parênteses, porque `and` tem precedência
maior que `or`.

```python
def pode_embarcar(cartao, documento, grupo_chamado, prioridade):
    if cartao and documento and (grupo_chamado or prioridade):
        return True
    return False
```

`test_corrigida_mcc` compara a versão corrigida com `regra` nas 16 linhas:

```
$ pytest -q --cov=embarque --cov=mcdc --cov-branch --cov-report=term-missing
embarque.py       4      0      2      0   100%
25 passed
```
