# Exercício 3 — Preço com Desconto VIP


## a) Definições, usos e pares du

**Definições e usos**

| Variável | Definições (linha) | Usos (linha, tipo) |
| -------- | ------------------ | ------------------ |
| `total` | 2, 5, 7 | 5 (c-use), 6 (p-use), 8 (c-use) |
| `desconto` | 4 | 5 (c-use) |

Na linha 5, `total` é usado (lado direito) e depois redefinido. O p-use da linha 6
é associado às duas arestas da decisão: 6→7 (V) e 6→8 (F).

**Pares du de `total`.** Um par vale só se existe caminho livre de definição entre
a definição e o uso:

| # | Par (def, uso) | Tipo | Caminho que o percorre |
| - | -------------- | ---- | ---------------------- |
| T1 | (2, 5) | c-use | vip = V |
| T2 | (2, 6$\rightarrow$7) | p-use | vip = F e preco < 50 |
| T3 | (2, 6$\rightarrow$8) | p-use | vip = F e preco ≥ 50 |
| T4 | (2, 8) | c-use | vip = F e preco ≥ 50 |
| T5 | (5, 6$\rightarrow$7) | p-use | vip = V e total com desconto < 50 |
| T6 | (5, 6$\rightarrow$8) | p-use | vip = V e total com desconto ≥ 50 |
| T7 | (5, 8) | c-use | vip = V e total com desconto ≥ 50 |
| T8 | (7, 8) | c-use | total < 50 |

(2, 8) só vale com vip = F e sem passar pela 7, e (5, 8) só sem passar pela 7. Se
passar pela linha 7, ela redefine `total`.

**Pares du de `desconto`**

| # | Par (def, uso) | Tipo | Caminho |
| - | -------------- | ---- | ------- |
| D1 | (4, 5) | c-use | vip = V |

## b) Pares que a suíte atual não percorre

Suíte atual: `preco_final(60, True) == 50` e `preco_final(200, False) == 200`.

| Caso | Caminho | Pares percorridos |
| ---- | ------- | ----------------- |
| (60, True) | 2-3-4-5-6-7-8 (total = 36 na linha 5) | T1, T5, T8, D1 |
| (200, False) | 2-3-6-8 | T3, T4 |

**Não percorridos:**

- **T2 (2, 6→7):** cliente comum com preço abaixo de 50
- **T6 (5, 6→8)** e **T7 (5, 8):** cliente VIP cujo total com desconto fica
  acima de 50. O valor calculado na linha 5 nunca chega ao `return`.

## c) Casos que faltam para All-Uses

Valores esperados tirados da especificação (VIP tem 20% de desconto, mínimo de
R$ 50):

| Caso | Pares | Esperado (spec) | Original |
| ---- | ----- | --------------- | -------- |
| `preco_final(100, True)` | T6, T7 | 100 − 20% = **80** | **60.0** ✗ |
| `preco_final(40, False)` | T2 | **50** | 50 ✓ |

**O que acontece:** o caso VIP acima do mínimo **falha**. A linha 5 aplica o
desconto duas vezes. Primeiro `total * 0.8` já tira 20%, depois `- desconto` tira
mais 20% do preço: 100 · 0,8 − 20 = 60, um desconto de 40%.

**Por que a suíte atual não viu:** no único caso VIP, (60, True), o valor errado
(60 · 0,8 − 12 = **36**) e o valor certo (60 · 0,8 = **48**) estão ambos abaixo
de 50. A linha 7 sobrescreve os dois com 50, então o resultado da linha 5 nunca
chega a um uso observável (par (5, 8)). O piso de R$ 50 **mascara** o defeito. A
suíte passa por todos os ramos, mas não leva a definição da linha 5 ao `return`.
Por isso 100% de ramos não basta e o critério All-Uses encontra o defeito.

## d) Correção e suíte inteira

A linha 5 deve aplicar o desconto uma vez só (`preco.py`):

```python
def preco_final(preco, vip):
    total = preco
    if vip:
        desconto = preco * 0.2
        total = total - desconto
    if total < 50:
        total = 50
    return total
```

Suíte inteira: a atual mais os dois casos de All-Uses, e mais um teste que
registra o comportamento da original no caso (100, True):

```
$ pytest -q --cov=preco --cov-branch --cov-report=term-missing
preco.py       8      0      4      0   100%
4 passed
```

Com a correção, `preco_final(60, True)` continua 50 (48 → piso) e
`preco_final(100, True)` passa a 80.
