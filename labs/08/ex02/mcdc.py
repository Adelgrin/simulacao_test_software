from itertools import combinations, product


def regra(cartao, documento, grupo_chamado, prioridade):
    """Especificação: cartão E documento E (grupo chamado OU prioridade)."""
    return cartao and documento and (grupo_chamado or prioridade)


def tabela_verdade(n):
    """Linhas da tabela-verdade; a linha i é o número i em binário (F=0, V=1)."""
    return list(product((False, True), repeat=n))


def pares_independentes(decisao, n):
    """Para cada condição, os pares de linhas (i, j) que diferem só nela
    e mudam o resultado da decisão."""
    linhas = tabela_verdade(n)
    pares = {}
    for k in range(n):
        pares[k] = []
        for i, linha in enumerate(linhas):
            if linha[k]:
                continue
            j = i + 2 ** (n - 1 - k)  # mesma linha com a condição k em V
            if decisao(*linha) != decisao(*linhas[j]):
                pares[k].append((i, j))
    return pares


def conjuntos_mcdc_minimos(decisao, n):
    """Todos os conjuntos de linhas de tamanho mínimo que contêm
    pelo menos um par independente de cada condição."""
    pares = pares_independentes(decisao, n)
    for tamanho in range(n + 1, 2 ** n + 1):
        achados = [
            set(c)
            for c in combinations(range(2 ** n), tamanho)
            if all(any(i in c and j in c for i, j in pares[k]) for k in range(n))
        ]
        if achados:
            return achados
    return []
