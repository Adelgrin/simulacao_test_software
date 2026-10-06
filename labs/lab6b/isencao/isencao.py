def isento(pcd, valor_compra, cadastro_app, minutos):
    if pcd:
        return True
    if minutos > 240:
        return False
    return valor_compra >= 150.00 or cadastro_app
