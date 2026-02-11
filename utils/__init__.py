"""
Módulo de utilidades para la aplicación de distribución binomial
"""

from utils.calculos import (
    factorial,
    combinatoria,
    binomial_pmf,
    calcular_media,
    calcular_desviacion_estandar,
    calcular_varianza,
    calcular_probabilidades,
    calcular_probabilidad_acumulada,
    calcular_probabilidad_mayor_que,
    calcular_probabilidad_entre,
    es_poblacion_infinita,
    calcular_factor_correccion,
    calcular_sesgo,
    calcular_curtosis
)

from utils.validaciones import (
    validar_parametros,
    validar_valores_x,
    parsear_valores_x
)

from utils.formato import (
    generar_texto_resultados,
    calcular_moda,
    generar_resumen_corto
)

__all__ = [
    # Cálculos
    'factorial',
    'combinatoria',
    'binomial_pmf',
    'calcular_media',
    'calcular_desviacion_estandar',
    'calcular_varianza',
    'calcular_probabilidades',
    'calcular_probabilidad_acumulada',
    'calcular_probabilidad_mayor_que',
    'calcular_probabilidad_entre',
    'es_poblacion_infinita',
    'calcular_factor_correccion',
    'calcular_sesgo',
    'calcular_curtosis',
    # Validaciones
    'validar_parametros',
    'validar_valores_x',
    'parsear_valores_x',
    # Formato
    'generar_texto_resultados',
    'calcular_moda',
    'generar_resumen_corto'
]
