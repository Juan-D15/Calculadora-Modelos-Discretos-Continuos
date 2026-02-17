"""
Módulo de cálculos para distribuciones estadísticas
Considera población infinita cuando no se especifica población
o cuando la muestra no excede el 5% de la población
"""
import math


def factorial(n):
    """
    Calcula el factorial de n
    
    Args:
        n (int): Número entero no negativo
        
    Returns:
        int: Factorial de n
    """
    if n <= 1:
        return 1
    return math.factorial(n)


def combinatoria(n, k):
    """
    Calcula la combinatoria C(n,k) = n! / (k! * (n-k)!)
    
    Args:
        n (int): Número total de pruebas
        k (int): Número de sucesos exitosos
        
    Returns:
        int: Valor de la combinatoria
    """
    if k > n or k < 0:
        return 0
    if k == 0 or k == n:
        return 1
    return factorial(n) // (factorial(k) * factorial(n - k))


def binomial_pmf(k, n, p):
    """
    Calcula P(X=k) para una distribución binomial
    
    Fórmula: P(X=k) = C(n,k) × p^k × (1-p)^(n-k)
    
    Args:
        k (int): Número de éxitos
        n (int): Número de ensayos
        p (float): Probabilidad de éxito en cada ensayo
        
    """
    return combinatoria(n, k) * (p ** k) * ((1 - p) ** (n - k))


def calcular_media(n, p):
    """
    Calcula la media (esperanza) de una distribución binomial
    
    Fórmula: μ = n × p
    
    Args:
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        
    """
    return n * p


def calcular_desviacion_estandar(n, p, N=None):
    """
    Calcula la desviación estándar de una distribución binomial
    Considera población finita si se especifica N
    
    Fórmula infinita: σ = √(n × p × (1-p))
    Fórmula finita: σ = √(n × p × (1-p) × √((N-n)/(N-1)))
    
    Args:
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        N (int, optional): Tamaño de la población
    """
    varianza = n * p * (1 - p)
    if N is not None and not es_poblacion_infinita(n, N):
        fpc = math.sqrt((N - n) / (N - 1))
        return math.sqrt(varianza) * fpc
    return math.sqrt(varianza)


def calcular_varianza(n, p, N=None):
    """
    Calcula la varianza de una distribución binomial
    Considera población finita si se especifica N
    
    Fórmula infinita: σ² = n × p × (1-p)
    Fórmula finita: σ² = n × p × (1-p) × ((N-n)/(N-1))
    
    Args:
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        N (int, optional): Tamaño de la población
        
    """
    varianza = n * p * (1 - p)
    if N is not None and not es_poblacion_infinita(n, N):
        fpc = (N - n) / (N - 1)
        return varianza * fpc
    return varianza


def es_poblacion_infinita(n, N=None):
    """
    Determina si la población se considera infinita
    
    La población se considera infinita cuando:
    1. No se especifica tamaño de población (N es None)
    2. La muestra (n) no excede el 5% de la población (n <= 0.05 * N)
    
    Args:
        n (int): Tamaño de la muestra
        N (int, optional): Tamaño de la población
        
    Returns:
        bool: True si la población se considera infinita
    """
    if N is None:
        # Sin población especificada -> población infinita
        return True
    
    # Verificar si n <= 5% de N
    return n <= (0.05 * N)


def calcular_probabilidades(valores_x, n, p):
    """
    Calcula las probabilidades para múltiples valores de X
    
    Args:
        valores_x (list): Lista de valores para los cuales calcular P(X=x)
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        
    Returns:
        list: Lista de probabilidades correspondientes a cada valor de X
    """
    probabilidades = []
    for x in valores_x:
        prob = binomial_pmf(x, n, p)
        probabilidades.append(prob)
    return probabilidades


def calcular_probabilidad_acumulada(x, n, p):
    """
    Calcula P(X <= x) - probabilidad acumulada hasta x
    
    Args:
        x (int): Valor máximo
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        
    Returns:
        float: Probabilidad acumulada
    """
    prob_acumulada = 0
    for k in range(0, x + 1):
        prob_acumulada += binomial_pmf(k, n, p)
    return prob_acumulada


def calcular_probabilidad_mayor_que(x, n, p):
    """
    Calcula P(X > x) - probabilidad de ser mayor que x
    
    Args:
        x (int): Valor de referencia
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        
    Returns:
        float: Probabilidad de X > x
    """
    return 1 - calcular_probabilidad_acumulada(x, n, p)


def calcular_probabilidad_entre(a, b, n, p):
    """
    Calcula P(a <= X <= b) - probabilidad entre dos valores
    
    Args:
        a (int): Límite inferior
        b (int): Límite superior
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        
    Returns:
        float: Probabilidad entre a y b
    """
    prob = 0
    for k in range(a, b + 1):
        prob += binomial_pmf(k, n, p)
    return prob


def calcular_factor_correccion(n, N):
    """
    Calcula el factor de corrección para población finita
    
    Fórmula: FPC = √((N-n)/(N-1))
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        
    Returns:
        float: Factor de corrección de población finita
    """
    return math.sqrt((N - n) / (N - 1))


def calcular_sesgo(n, p, N=None):
    """
    Calcula el sesgo (asimetría) de la distribución binomial
    Para población finita, aplica el factor de corrección
    
    Fórmula infinita: γ₁ = (1 - 2p) / √(n × p × (1-p)) = (q - p) / √(n × p × q)
    Fórmula finita: γ₁ = γ₁_infinita / FPC = γ₁_infinita × √((N-1)/(N-n))
    donde q = 1 - p y FPC = √((N-n)/(N-1))
    
    Args:
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        N (int, optional): Tamaño de la población
        
    Returns:
        float: Valor del sesgo
        str: Interpretación del sesgo (negativo, neutro, positivo)
    """
    q = 1 - p
    varianza_infinita = n * p * q
    
    if varianza_infinita == 0:
        return 0, "Neutro"
    
    # Calcular sesgo para población infinita
    sesgo = (1 - 2 * p) / math.sqrt(varianza_infinita)
    
    # Aplicar corrección para población finita
    if N is not None and not es_poblacion_infinita(n, N):
        fpc = math.sqrt((N - n) / (N - 1))
        # Para sesgo, dividimos por el FPC (equivalente a multiplicar por (N-1)/(N-n)^0.5)
        sesgo = sesgo / fpc
    
    if sesgo > 0.01:
        return sesgo, "Positivo (Asimetría a la derecha)"
    elif sesgo < -0.01:
        return sesgo, "Negativo (Asimetría a la izquierda)"
    else:
        return sesgo, "Neutro (Simétrica)"


def calcular_curtosis(n, p, N=None):
    """
    Calcula la curtosis (exceso de curtosis) de la distribución binomial
    Para población finita, aplica el factor de corrección
    
    Fórmula infinita: γ₂ = (1 - 6pq) / (n × p × q)
    Fórmula finita: γ₂ = γ₂_infinita / FPC² = γ₂_infinita × (N-1)/(N-n)
    donde q = 1 - p y FPC = √((N-n)/(N-1))
    
    Args:
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        N (int, optional): Tamaño de la población
        
    Returns:
        float: Valor de la curtosis (exceso de curtosis)
        str: Interpretación de la curtosis (platicúrtica, mesocúrtica, leptocúrtica)
    """
    q = 1 - p
    varianza_infinita = n * p * q
    
    if varianza_infinita == 0:
        return 0, "Mesocúrtica"
    
    # Calcular curtosis para población infinita (exceso de curtosis)
    curtosis = (1 - 6 * p * q) / varianza_infinita
    
    # Aplicar corrección para población finita (dividir por FPC al cuadrado)
    if N is not None and not es_poblacion_infinita(n, N):
        fpc_cuadrado = (N - n) / (N - 1)
        curtosis = curtosis / fpc_cuadrado
    
    if curtosis > 0.1:
        return curtosis, "Leptocúrtica (Curva elevada)"
    elif curtosis < -0.1:
        return curtosis, "Platicúrtica (Curva aplanada)"
    else:
        return curtosis, "Mesocúrtica (Campana de Gauss)"


def cumple_condicion_hipergeometrica(n, N):
    """
    Determina si se puede usar distribución hipergeométrica
    La condición es que la muestra sea >= 20% de la población
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        
    Returns:
        tuple: (cumple: bool, porcentaje: float)
    """
    if N is None or N <= 0:
        return False, 0.0
    porcentaje = (n / N) * 100
    return porcentaje >= 20, porcentaje


def hipergeometrica_pmf(k, n, N, K):
    """
    Calcula P(X=k) para una distribución hipergeométrica
    
    Fórmula: P(X=k) = C(K,k) × C(N-K, n-k) / C(N, n)
    
    Args:
        k (int): Número de éxitos en la muestra
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        
    Returns:
        float: Probabilidad P(X=k)
    """
    if k < 0 or k > n or k > K or (n - k) > (N - K):
        return 0.0
    
    numerador = combinatoria(K, k) * combinatoria(N - K, n - k)
    denominador = combinatoria(N, n)
    
    if denominador == 0:
        return 0.0
    
    return numerador / denominador


def calcular_media_hipergeometrica(n, N, K):
    """
    Calcula la media de la distribución hipergeométrica
    
    Fórmula: μ = n × K / N
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        
    Returns:
        float: Media de la distribución
    """
    if N == 0:
        return 0.0
    return n * K / N


def calcular_desviacion_hipergeometrica(n, N, K):
    """
    Calcula la desviación estándar de la distribución hipergeométrica
    
    Fórmula: σ = √(n × (K/N) × ((N-K)/N) × ((N-n)/(N-1)))
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        
    Returns:
        float: Desviación estándar
    """
    if N <= 1:
        return 0.0
    
    p = K / N
    q = (N - K) / N
    fpc = (N - n) / (N - 1)
    
    varianza = n * p * q * fpc
    return math.sqrt(varianza)


def calcular_sesgo_hipergeometrica(n, N, K):
    """
    Calcula el sesgo (asimetría) de la distribución hipergeométrica
    
    Fórmula: γ₁ = (N - 2K) × (N - 1)^½ × (N - 2n) / 
             [n × K × (N - K) × (N - n)]^½ × (N - 2)
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        
    Returns:
        tuple: (sesgo: float, interpretacion: str, tipo_sesgo_media_mediana: str)
    """
    if N <= 2 or K <= 0 or (N - K) <= 0 or n <= 0 or (N - n) <= 0:
        return 0, "Neutro", "Nulo"
    
    numerador = (N - 2 * K) * math.sqrt(N - 1) * (N - 2 * n)
    denominador = math.sqrt(n * K * (N - K) * (N - n)) * (N - 2)
    
    if denominador == 0:
        return 0, "Neutro", "Nulo"
    
    sesgo = numerador / denominador
    
    if sesgo > 0.01:
        return sesgo, "Positivo (Asimetría a la derecha)", "Positivo"
    elif sesgo < -0.01:
        return sesgo, "Negativo (Asimetría a la izquierda)", "Negativo"
    else:
        return sesgo, "Neutro (Simétrica)", "Nulo"


def calcular_curtosis_hipergeometrica(n, N, K):
    """
    Calcula la curtosis de la distribución hipergeométrica
    
    Fórmula simplificada para exceso de curtosis
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        
    Returns:
        tuple: (curtosis: float, interpretacion: str)
    """
    if N <= 3 or K <= 0 or (N - K) <= 0 or n <= 0 or (N - n) <= 0:
        return 0, "Mesocúrtica"
    
    p = K / N
    q = 1 - p
    
    varianza = n * p * q * (N - n) / (N - 1)
    
    if varianza == 0:
        return 0, "Mesocúrtica"
    
    numerador = (N - 1) * (N * (N + 1) - 6 * N * (N - n) * p * q + 
                          6 * n * (N - n) * (N - 2) * (N - 3) * p * p * q * q)
    denominador = n * (N - n) * (N - 2) * (N - 3) * p * q * varianza
    
    if denominador == 0:
        return 0, "Mesocúrtica"
    
    curtosis = numerador / denominador - 3
    
    if curtosis > 0.1:
        return curtosis, "Leptocúrtica (Curva elevada)"
    elif curtosis < -0.1:
        return curtosis, "Platicúrtica (Curva aplanada)"
    else:
        return curtosis, "Mesocúrtica (Campana de Gauss)"


def calcular_probabilidades_hipergeometrica(valores_x, n, N, K):
    """
    Calcula las probabilidades para múltiples valores de X en hipergeométrica
    
    Args:
        valores_x (list): Lista de valores para los cuales calcular P(X=x)
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        
    Returns:
        list: Lista de probabilidades correspondientes a cada valor de X
    """
    probabilidades = []
    for x in valores_x:
        prob = hipergeometrica_pmf(x, n, N, K)
        probabilidades.append(prob)
    return probabilidades


def calcular_mediana_hipergeometrica(n, N, K):
    """
    Calcula una aproximación de la mediana de la distribución hipergeométrica
    La mediana es el valor donde P(X ≤ m) ≥ 0.5
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        
    Returns:
        int: Mediana aproximada
    """
    max_k = min(n, K)
    prob_acumulada = 0
    
    for k in range(0, max_k + 1):
        prob_acumulada += hipergeometrica_pmf(k, n, N, K)
        if prob_acumulada >= 0.5:
            return k
    
    return max_k


def determinar_tipo_sesgo(media, mediana):
    """
    Determina el tipo de sesgo comparando media y mediana
    
    - Sesgo negativo: media < mediana
    - Sesgo nulo: media = mediana
    - Sesgo positivo: media > mediana
    
    Args:
        media (float): Valor de la media
        mediana (int): Valor de la mediana
        
    Returns:
        str: Descripción del tipo de sesgo
    """
    diferencia = media - mediana
    
    if abs(diferencia) < 0.001:
        return "Nulo (media = mediana)"
    elif diferencia < 0:
        return "Negativo (media < mediana)"
    else:
        return "Positivo (media > mediana)"

