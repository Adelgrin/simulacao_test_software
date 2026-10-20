def preco_final(preco, vip):
    total = preco
    if vip:
        desconto = preco * 0.2
        total = total - desconto
    if total < 50:
        total = 50
    return total
