"""
Módulo para formatear y presentar resultados
Mejorada la presentación con información sobre población infinita
"""


def generar_texto_resultados(n, p, valores_x, probabilidades, media, desviacion, 
                               N=None, factor_correccion=None, sesgo=None, 
                               interpretacion_sesgo=None, curtosis=None, 
                               interpretacion_curtosis=None):
    """
    Genera el texto formateado con los resultados del cálculo
    
    """
    q = 1 - p
    varianza = desviacion ** 2
    es_infinita = (N is None) or (n <= 0.05 * N)
    
    resultado = "╔" + "═" * 56 + "╗\n"
    resultado += "║" + " " * 10 + "RESULTADOS DEL CÁLCULO" + " " * 20 + "║\n"
    resultado += "╚" + "═" * 56 + "╝\n\n"
    
    # Información de población
    resultado += "TIPO DE POBLACIÓN\n"
    resultado += "─" * 58 + "\n"
    if N is None:
        resultado += f"   • Tipo: INFINITA (no se especificó población)\n"
    elif es_infinita:
        resultado += f"   • Tipo: INFINITA (muestra ≤ 5% de población)\n"
        resultado += f"   • Población (N): {N}\n"
        resultado += f"   • Proporción muestra/población: {(n/N)*100:.2f}%\n"
    else:
        resultado += f"   • Tipo: FINITA (muestra > 5% de población)\n"
        resultado += f"   • Población (N): {N}\n"
        resultado += f"   • Proporción muestra/población: {(n/N)*100:.2f}%\n"
        if factor_correccion is not None:
            resultado += f"   • Factor de corrección (FPC): {factor_correccion:.6f}\n"
    resultado += "\n"
    
    # Parámetros
    resultado += "PARÁMETROS DE LA DISTRIBUCIÓN\n"
    resultado += "─" * 58 + "\n"
    resultado += f"   • Tamaño de muestra (n): {n}\n"
    resultado += f"   • Probabilidad de éxito (p): {p:.6f}\n"
    resultado += f"   • Probabilidad de fracaso (q): {q:.6f}\n\n"
    
    # Estadísticas
    resultado += "ESTADÍSTICAS\n"
    resultado += "─" * 58 + "\n"
    resultado += f"   • Media (μ = n × p): {media:.6f}\n"
    if not es_infinita and N is not None:
        resultado += f"   • Varianza (σ² = n × p × q × FPC²): {varianza:.6f}\n"
        resultado += f"   • Desviación estándar (σ = √(n × p × q) × FPC): {desviacion:.6f}\n"
    else:
        resultado += f"   • Varianza (σ² = n × p × q): {varianza:.6f}\n"
        resultado += f"   • Desviación estándar (σ = √(n × p × q)): {desviacion:.6f}\n"
    resultado += f"   • Coeficiente de variación: {(desviacion/media)*100:.2f}%\n\n"
    
    # Sesgo y Curtosis
    if sesgo is not None and curtosis is not None:
        resultado += "FORMA DE LA DISTRIBUCIÓN\n"
        resultado += "─" * 58 + "\n"
        resultado += f"   • Sesgo (Asimetría): {sesgo:.6f}\n"
        resultado += f"   • Interpretación: {interpretacion_sesgo}\n"
        resultado += f"   • Curtosis: {curtosis:.6f}\n"
        resultado += f"   • Interpretación: {interpretacion_curtosis}\n\n"
    
    # Probabilidades individuales
    resultado += "PROBABILIDADES CALCULADAS\n"
    resultado += "─" * 58 + "\n"
    resultado += "   Valores   Probabilidad    Porcentaje     Visual\n"
    resultado += "─" * 58 + "\n"
    
    for x, prob in zip(valores_x, probabilidades):
        porcentaje = prob * 100
        # Crear barra visual mejorada
        barra_length = int(porcentaje / 1.5) if porcentaje <= 100 else 67
        barra = "█" * barra_length
        
        # Formatear valores
        resultado += f"   P(X={x:2d})    {prob:.8f}    {porcentaje:6.3f}%     {barra}\n"
    
    resultado += "─" * 58 + "\n"
    
    # Resumen de probabilidades
    suma_prob = sum(probabilidades)
    resultado += f"\nSuma de probabilidades calculadas: {suma_prob:.10f}\n"
    
    # Probabilidad máxima
    prob_max = max(probabilidades)
    x_max = valores_x[probabilidades.index(prob_max)]
    resultado += f"Probabilidad máxima: P(X={x_max}) = {prob_max:.8f} ({prob_max*100:.3f}%)\n"
    
    
    return resultado


def calcular_moda(n, p):
    """
    Calcula la moda de la distribución binomial
    
    La moda es el valor más probable de X.
    
    Args:
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
        
    Returns:
        int or str: Moda de la distribución
    """
    if (n + 1) * p == int((n + 1) * p):
        # Dos modas
        k = int((n + 1) * p)
        return f"{k-1} y {k}"
    else:
        # Una moda
        return int((n + 1) * p)


def generar_resumen_corto(n, p, media, desviacion, N=None):
    """
    Genera un resumen corto de los resultados
    
    Args:
        n (int): Tamaño de muestra
        p (float): Probabilidad de éxito
        media (float): Media
        desviacion (float): Desviación estándar
        N (int, optional): Tamaño de población
        
    Returns:
        str: Resumen corto
    """
    poblacion_tipo = "Infinita" if N is None or n <= 0.05 * N else f"Finita(N={N})"
    return (f"Binomial(n={n}, p={p:.4f}) | "
            f"μ={media:.4f} | σ={desviacion:.4f} | "
            f"{poblacion_tipo}")


def generar_texto_resultados_hipergeometrica(n, N, K, valores_x, probabilidades, 
                                              media, desviacion, sesgo=None,
                                              interpretacion_sesgo=None, 
                                              tipo_sesgo_media_mediana=None,
                                              curtosis=None, interpretacion_curtosis=None,
                                              mediana=None, cumple_condicion=True,
                                              porcentaje_muestra=0.0):
    """
    Genera el texto formateado con los resultados del cálculo hipergeométrico
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        valores_x (list): Lista de valores de X
        probabilidades (list): Lista de probabilidades
        media (float): Media
        desviacion (float): Desviación estándar
        sesgo (float): Valor del sesgo
        interpretacion_sesgo (str): Interpretación del sesgo
        tipo_sesgo_media_mediana (str): Tipo de sesgo según media vs mediana
        curtosis (float): Valor de la curtosis
        interpretacion_curtosis (str): Interpretación de la curtosis
        mediana (int): Mediana de la distribución
        cumple_condicion (bool): Si la muestra es >= 20% de la población
        porcentaje_muestra (float): Porcentaje que representa la muestra
        
    Returns:
        str: Texto formateado con resultados
    """
    varianza = desviacion ** 2
    p = K / N if N > 0 else 0
    q = 1 - p
    
    resultado = "╔" + "═" * 56 + "╗\n"
    resultado += "║" + " " * 6 + "RESULTADOS - DISTRIBUCIÓN HIPERGEOMÉTRICA" + " " * 6 + "║\n"
    resultado += "╚" + "═" * 56 + "╝\n\n"
    
    resultado += "CONDICIÓN DE APLICABILIDAD\n"
    resultado += "─" * 58 + "\n"
    if cumple_condicion:
        resultado += f"   ✓ VÁLIDO: La muestra representa {porcentaje_muestra:.2f}% de la población\n"
        resultado += "   (≥ 20%) - Se puede usar distribución hipergeométrica\n"
    else:
        resultado += f"   ✗ ADVERTENCIA: La muestra representa {porcentaje_muestra:.2f}% de la población\n"
        resultado += "   (< 20%) - Se recomienda usar distribución BINOMIAL\n\n"
        resultado += "   La distribución hipergeométrica es apropiada cuando\n"
        resultado += "   la muestra es grande respecto a la población.\n"
    resultado += "\n"
    
    resultado += "PARÁMETROS DE LA DISTRIBUCIÓN\n"
    resultado += "─" * 58 + "\n"
    resultado += f"   • Población total (N): {N}\n"
    resultado += f"   • Éxitos en población (K): {K}\n"
    resultado += f"   • Tamaño de muestra (n): {n}\n"
    resultado += f"   • Probabilidad implícita (p = K/N): {p:.6f}\n"
    resultado += f"   • Probabilidad implícita (q = 1-p): {q:.6f}\n\n"
    
    resultado += "ESTADÍSTICAS\n"
    resultado += "─" * 58 + "\n"
    resultado += f"   • Media (μ = nK/N): {media:.6f}\n"
    resultado += f"   • Varianza (σ²): {varianza:.6f}\n"
    resultado += f"   • Desviación estándar (σ): {desviacion:.6f}\n"
    resultado += f"   • Coeficiente de variación: {(desviacion/media)*100:.2f}%\n" if media > 0 else "   • Coeficiente de variación: N/A\n"
    
    if mediana is not None:
        resultado += f"   • Mediana: {mediana}\n"
    resultado += "\n"
    
    if sesgo is not None:
        resultado += "FORMA DE LA DISTRIBUCIÓN\n"
        resultado += "─" * 58 + "\n"
        resultado += f"   • Sesgo (Asimetría): {sesgo:.6f}\n"
        resultado += f"   • Interpretación: {interpretacion_sesgo}\n"
        if tipo_sesgo_media_mediana:
            resultado += f"   • Tipo por media vs mediana: {tipo_sesgo_media_mediana}\n"
        if curtosis is not None:
            resultado += f"   • Curtosis: {curtosis:.6f}\n"
            resultado += f"   • Interpretación: {interpretacion_curtosis}\n"
        resultado += "\n"
    
    resultado += "PROBABILIDADES CALCULADAS\n"
    resultado += "─" * 58 + "\n"
    resultado += "   Valores   Probabilidad    Porcentaje     Visual\n"
    resultado += "─" * 58 + "\n"
    
    for x, prob in zip(valores_x, probabilidades):
        porcentaje = prob * 100
        barra_length = int(porcentaje / 1.5) if porcentaje <= 100 else 67
        barra = "█" * barra_length
        resultado += f"   P(X={x:2d})    {prob:.8f}    {porcentaje:6.3f}%     {barra}\n"
    
    resultado += "─" * 58 + "\n"
    
    suma_prob = sum(probabilidades)
    resultado += f"\nSuma de probabilidades calculadas: {suma_prob:.10f}\n"
    
    prob_max = max(probabilidades)
    x_max = valores_x[probabilidades.index(prob_max)]
    resultado += f"Probabilidad máxima: P(X={x_max}) = {prob_max:.8f} ({prob_max*100:.3f}%)\n"
    
    return resultado


def generar_mensaje_usar_binomial(n, N, K, porcentaje):
    """
    Genera un mensaje indicando que se debe usar distribución binomial
    
    Args:
        n (int): Tamaño de la muestra
        N (int): Tamaño de la población
        K (int): Número de éxitos en la población
        porcentaje (float): Porcentaje que representa la muestra
        
    Returns:
        str: Mensaje formateado
    """
    resultado = "╔" + "═" * 56 + "╗\n"
    resultado += "║" + " " * 12 + "USAR DISTRIBUCIÓN BINOMIAL" + " " * 14 + "║\n"
    resultado += "╚" + "═" * 56 + "╝\n\n"
    
    resultado += "ANÁLISIS DE CONDICIONES\n"
    resultado += "─" * 58 + "\n"
    resultado += f"   • Tamaño de población (N): {N}\n"
    resultado += f"   • Tamaño de muestra (n): {n}\n"
    resultado += f"   • Porcentaje de muestra: {porcentaje:.2f}%\n\n"
    
    resultado += "CONCLUSIÓN\n"
    resultado += "─" * 58 + "\n"
    resultado += "   La muestra representa menos del 20% de la población.\n"
    resultado += "   Por lo tanto, se DEBE resolver mediante DISTRIBUCIÓN\n"
    resultado += "   BINOMIAL en lugar de Hipergeométrica.\n\n"
    
    resultado += "   Razón: Cuando la muestra es pequeña respecto a la\n"
    resultado += "   población (< 20%), el muestreo sin reemplazo se\n"
    resultado += "   aproxima bien al muestreo con reemplazo (binomial).\n\n"
    
    p = K / N if N > 0 else 0
    resultado += "PARÁMETROS PARA BINOMIAL\n"
    resultado += "─" * 58 + "\n"
    resultado += f"   • n = {n} (tamaño de muestra)\n"
    resultado += f"   • p = {p:.6f} (K/N = {K}/{N})\n"
    
    return resultado

