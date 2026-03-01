"""
Módulo de validación de datos de entrada
"""


def normalizar_probabilidad(valor):
    """
    Normaliza un valor de probabilidad, convirtiendo porcentajes a decimal

    Si el valor es mayor a 1, se asume que es un porcentaje (ej: 90 -> 0.9)
    Si el valor está entre 0 y 1, se usa tal cual

    Args:
        valor: String o número con el valor de probabilidad

    Returns:
        tuple: (es_valido, valor_normalizado, mensaje_error)
    """
    try:
        p = float(valor)
    except (ValueError, TypeError):
        return False, None, "La probabilidad debe ser un número válido"

    if p < 0:
        return False, None, "La probabilidad no puede ser negativa"

    if p > 100:
        return False, None, "La probabilidad no puede ser mayor a 100%"

    if p > 1:
        p = p / 100

    return True, p, ""


def validar_parametros(n, p, N=None):
    if n <= 0:
        return False, "El número de ensayos (n) debe ser mayor a 0"
    if p < 0 or p > 1:
        return False, "La probabilidad (p) debe estar entre 0 y 1"
    if N is not None:
        if N <= 0:
            return (
                False,
                "El tamaño de población (N) debe ser mayor a 0 (deje vacío para población infinita)",
            )
        if n >= N:
            return (
                False,
                "El tamaño de muestra (n) debe ser menor que el tamaño de población (N)",
            )
    return True, ""


def validar_parametros_comparacion(n, p, N, tolerancia, K=None):
    """
    Valida los parámetros para el modo comparación

    Args:
        n (int): Tamaño de muestra
        p (float): Probabilidad de éxito (puede ser None si K está definido)
        N (int): Tamaño de población (obligatorio para comparación)
        tolerancia (float): Porcentaje de tolerancia
        K (int, optional): Éxitos en población (si está definido, p puede ser None)

    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if n <= 0:
        return False, "El número de ensayos (n) debe ser mayor a 0"

    if K is None or K == "":
        if p is None or p == "":
            return (
                False,
                "Debe ingresar al menos p (probabilidad) o K (éxitos en población)",
            )
        if p < 0 or p > 1:
            return False, "La probabilidad (p) debe estar entre 0 y 1"
    else:
        try:
            K_val = int(K)
            if K_val <= 0:
                return False, "K debe ser mayor a 0"
        except (ValueError, TypeError):
            return False, "K debe ser un número entero válido"

    if N is None or N <= 0:
        return (
            False,
            "Para comparación, el tamaño de población (N) es obligatorio y debe ser mayor a 0",
        )
    if n >= N:
        return (
            False,
            "El tamaño de muestra (n) debe ser menor que el tamaño de población (N)",
        )
    if tolerancia is not None:
        try:
            tol = float(tolerancia)
            if tol < 0 or tol > 100:
                return False, "La tolerancia debe estar entre 0 y 100"
        except (ValueError, TypeError):
            return False, "La tolerancia debe ser un número válido"
    return True, ""


def validar_tolerancia(tolerancia):
    """
    Valida el valor de tolerancia

    Args:
        tolerancia: Valor de tolerancia (string o número)

    Returns:
        tuple: (es_valido, valor_float, mensaje_error)
    """
    if tolerancia is None or tolerancia == "":
        return True, 95.0, ""

    try:
        tol = float(tolerancia)
        if tol < 0 or tol > 100:
            return False, None, "La tolerancia debe estar entre 0 y 100"
        return True, tol, ""
    except (ValueError, TypeError):
        return False, None, "La tolerancia debe ser un número válido"


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
        if x < 0:
            return False, f"El valor X={x} no puede ser negativo"
        if x > n:
            return (
                False,
                f"El valor X={x} no puede ser mayor que el tamaño de la muestra (n={n})",
            )

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
        try:
            valor_max = int(texto)
            if valor_max < 0:
                return [0]
            return list(range(0, valor_max + 1))
        except ValueError:
            return [0]

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
        return (
            False,
            "El número de éxitos en población (K) es obligatorio y no puede ser negativo",
        )

    if K > N:
        return (
            False,
            f"El número de éxitos (K={K}) no puede ser mayor que la población (N={N})",
        )

    if n <= 0:
        return False, "El tamaño de muestra (n) debe ser mayor a 0"

    if n > N:
        return (
            False,
            f"El tamaño de muestra (n={n}) no puede ser mayor que la población (N={N})",
        )

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
        if x > n:
            return (
                False,
                f"El valor X={x} no puede ser mayor que el tamaño de la muestra (n={n})",
            )
        if x > max_x:
            return (
                False,
                f"El valor X={x} excede el máximo posible ({max_x} = min(n={n}, K={K}))",
            )

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
            return list(range(0, valor_max + 1))
        except ValueError:
            return [0]

    valores_x = [int(x.strip()) for x in texto.split(",")]
    return valores_x
