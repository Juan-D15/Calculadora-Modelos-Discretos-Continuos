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
            return False, "El tamaño de población (N) debe ser mayor a 0 (deje vacío para población infinita)"
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
        texto (str): Texto con valores separados por coma, "todos", o un solo número
        n (int): Tamaño de muestra
        
    Returns:
        list: Lista de valores enteros de X
    """
    texto = texto.strip().lower()
    
    if texto == "todos" or texto == "":
        return list(range(0, n + 1))
    
    if "," not in texto:
        # Es un solo número, calcular rango desde 0 hasta ese número
        try:
            valor_max = int(texto)
            if valor_max < 0:
                return [0]
            if valor_max > n:
                return list(range(0, n + 1))
            return list(range(0, valor_max + 1))
        except ValueError:
            return [0]
    
    # Son múltiples valores separados por coma
    valores_x = [int(x.strip()) for x in texto.split(",")]
    return valores_x


def validar_parametros_hipergeometrica(n, N, K):
    """
    Valida los parámetros para distribución hipergeométrica
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if N is None or N <= 0:
        return False, "El tamaño de población (N) es obligatorio y debe ser mayor a 0"
    
    if K is None or K < 0:
        return False, "El número de éxitos en población (K) es obligatorio y no puede ser negativo"
    
    if K > N:
        return False, f"El número de éxitos (K={K}) no puede ser mayor que la población (N={N})"
    
    if n <= 0:
        return False, "El tamaño de muestra (n) debe ser mayor a 0"
    
    if n > N:
        return False, f"El tamaño de muestra (n={n}) no puede ser mayor que la población (N={N})"
    
    return True, ""


def validar_valores_x_hipergeometrica(valores_x, n, K):
    """
    Valida que los valores de X estén dentro del rango válido para hipergeométrica
    
    El rango válido es: 0 ≤ x ≤ min(n, K)
    
    Args:
        valores_x (list): Lista de valores de X
        n (int): Tamaño de muestra
        K (int): Número de éxitos en población
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    max_x = min(n, K)
    
    for x in valores_x:
        if x < 0:
            return False, f"El valor X={x} no puede ser negativo"
        if x > max_x:
            return False, f"El valor X={x} excede el máximo posible ({max_x} = min(n={n}, K={K}))"
    
    return True, ""


def parsear_valores_x_hipergeometrica(texto, n, K):
    """
    Parsea el texto de entrada de valores X para hipergeométrica
    
    Args:
        texto (str): Texto con valores separados por coma, "todos", o un solo número
        n (int): Tamaño de muestra
        K (int): Número de éxitos en población
        
    Returns:
        list: Lista de valores enteros de X
    """
    max_x = min(n, K)
    texto = texto.strip().lower()
    
    if texto == "todos" or texto == "":
        return list(range(0, max_x + 1))
    
    if "," not in texto:
        try:
            valor_max = int(texto)
            if valor_max < 0:
                return [0]
            if valor_max > max_x:
                return list(range(0, max_x + 1))
            return list(range(0, valor_max + 1))
        except ValueError:
            return [0]
    
    valores_x = [int(x.strip()) for x in texto.split(",")]
    return valores_x