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
    calcular_curtosis,
    calcular_probabilidades_acumuladas,
    calcular_probabilidad_acumulada_hipergeometrica,
    calcular_probabilidades_acumuladas_hipergeometrica,
    buscar_valor_tolerancia,
)

from utils.validaciones import (
    validar_parametros,
    validar_valores_x,
    parsear_valores_x,
    validar_parametros_comparacion,
    validar_tolerancia,
)

from utils.formato import generar_texto_resultados, calcular_moda, generar_resumen_corto

from utils.file_loader import (
    FileLoader,
    ErrorCargaArchivo,
    ArchivoNoSeleccionadoError,
    ArchivoVacioError,
    ArchivoSinEncabezadosError,
    FormatoNoSoportadoError,
    ColumnaNoEncontradaError,
)

__all__ = [
    # Cálculos
    "factorial",
    "combinatoria",
    "binomial_pmf",
    "calcular_media",
    "calcular_desviacion_estandar",
    "calcular_varianza",
    "calcular_probabilidades",
    "calcular_probabilidad_acumulada",
    "calcular_probabilidad_mayor_que",
    "calcular_probabilidad_entre",
    "es_poblacion_infinita",
    "calcular_factor_correccion",
    "calcular_sesgo",
    "calcular_curtosis",
    "calcular_probabilidades_acumuladas",
    "calcular_probabilidad_acumulada_hipergeometrica",
    "calcular_probabilidades_acumuladas_hipergeometrica",
    "buscar_valor_tolerancia",
    # Validaciones
    "validar_parametros",
    "validar_valores_x",
    "parsear_valores_x",
    "validar_parametros_comparacion",
    "validar_tolerancia",
    # Formato
    "generar_texto_resultados",
    "calcular_moda",
    "generar_resumen_corto",
    # FileLoader
    "FileLoader",
    "ErrorCargaArchivo",
    "ArchivoNoSeleccionadoError",
    "ArchivoVacioError",
    "ArchivoSinEncabezadosError",
    "FormatoNoSoportadoError",
    "ColumnaNoEncontradaError",
]
