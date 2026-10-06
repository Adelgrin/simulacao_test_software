def isento(pcd, valor_compra, cadastro_app, minutos):
    if cadastro_app:
        return True
    if minutos > 240:
        return False
    return pcd or valor_compra >= 150.00
