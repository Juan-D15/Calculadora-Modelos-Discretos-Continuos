"""
Módulo de validación de datos de entrada
"""


def validar_parametros(n, p, N=None):
    if n <= 0:
        return False, "El número de ensayos (n) debe ser mayor a 0"
    if p < 0 or p > 1:
        return False, "La probabilidad (p) debe estar entre 0 y 1"
    if N is not None:
        if N <= 0:
            return False, "El tamaño de población (N) debe ser mayor a 0"
        if n >= N:
            return False, "El tamaño de muestra (n) debe ser menor que el tamaño de población (N)"
    return True, ""

def validar_valores_x(valores_x, n):
    """
    Valida que los valores de X estén dentro del rango válido
    
    Args:
        valores_x (list): Lista de valores de X
        n (int): Tamaño de muestra (valor máximo válido)
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    for x in valores_x:
        if x < 0 or x > n:
            return False, f"El valor X={x} debe estar entre 0 y {n}"
    
    return True, ""


def parsear_valores_x(texto, n):
    """
    Parsea el texto de entrada de valores X
    
    Args:
        texto (str): Texto con valores separados por coma o "todos"
        n (int): Tamaño de muestra
        
    Returns:
        list: Lista de valores enteros de X
    """
    texto = texto.strip().lower()
    
    if texto == "todos" or texto == "":
        return list(range(0, n + 1))
    
    valores_x = [int(x.strip()) for x in texto.split(",")]
    return valores_x