"""
Pruebas unitarias para funciones de cálculo y validación
"""

import pytest
import math
from utils.calculos import (
    calcular_probabilidades_acumuladas,
    calcular_probabilidad_acumulada_hipergeometrica,
    calcular_probabilidades_acumuladas_hipergeometrica,
    buscar_valor_tolerancia,
    es_poblacion_infinita,
    binomial_pmf,
    hipergeometrica_pmf,
)
from utils.validaciones import validar_parametros_comparacion, validar_tolerancia


class TestEsPoblacionInfinita:
    """Pruebas para la función es_poblacion_infinita"""

    def test_poblacion_none_es_infinita(self):
        assert es_poblacion_infinita(10, None) == True

    def test_muestra_menor_5porciento_es_infinita(self):
        assert es_poblacion_infinita(5, 200) == True
        assert es_poblacion_infinita(10, 500) == True

    def test_muestra_igual_5porciento_es_infinita(self):
        assert es_poblacion_infinita(10, 200) == True

    def test_muestra_mayor_5porciento_no_es_infinita(self):
        assert es_poblacion_infinita(15, 200) == False
        assert es_poblacion_infinita(50, 500) == False


class TestCalcularProbabilidadesAcumuladas:
    """Pruebas para calcular_probabilidades_acumuladas"""

    def test_probabilidades_acumuladas_binomial(self):
        valores_x = [0, 1, 2, 3]
        n = 3
        p = 0.5

        resultado = calcular_probabilidades_acumuladas(valores_x, n, p)

        assert len(resultado) == 4
        assert resultado[0] == pytest.approx(binomial_pmf(0, n, p), rel=1e-6)
        assert resultado[3] == pytest.approx(1.0, rel=1e-6)

    def test_probabilidades_acumuladas_crecientes(self):
        valores_x = [0, 1, 2]
        n = 2
        p = 0.5

        resultado = calcular_probabilidades_acumuladas(valores_x, n, p)

        for i in range(1, len(resultado)):
            assert resultado[i] >= resultado[i - 1]


class TestCalcularProbabilidadAcumuladaHipergeometrica:
    """Pruebas para calcular_probabilidad_acumulada_hipergeometrica"""

    def test_probabilidad_acumulada_hipergeometrica(self):
        n = 5
        N = 20
        K = 8
        x = 3

        resultado = calcular_probabilidad_acumulada_hipergeometrica(x, n, N, K)

        prob_manual = sum(hipergeometrica_pmf(k, n, N, K) for k in range(x + 1))
        assert resultado == pytest.approx(prob_manual, rel=1e-6)

    def test_probabilidad_acumulada_max(self):
        n = 3
        N = 10
        K = 5
        x = 3

        resultado = calcular_probabilidad_acumulada_hipergeometrica(x, n, N, K)
        assert resultado == pytest.approx(1.0, rel=1e-6)


class TestCalcularProbabilidadesAcumuladasHipergeometrica:
    """Pruebas para calcular_probabilidades_acumuladas_hipergeometrica"""

    def test_probabilidades_acumuladas_hipergeometrica(self):
        valores_x = [0, 1, 2]
        n = 3
        N = 10
        K = 5

        resultado = calcular_probabilidades_acumuladas_hipergeometrica(
            valores_x, n, N, K
        )

        assert len(resultado) == 3
        assert resultado[-1] <= 1.0

    def test_probabilidades_acumuladas_crecientes(self):
        valores_x = [0, 1, 2, 3]
        n = 4
        N = 15
        K = 6

        resultado = calcular_probabilidades_acumuladas_hipergeometrica(
            valores_x, n, N, K
        )

        for i in range(1, len(resultado)):
            assert resultado[i] >= resultado[i - 1]


class TestBuscarValorTolerancia:
    """Pruebas para buscar_valor_tolerancia"""

    def test_tolerancia_exacta(self):
        valores_x = [0, 1, 2, 3, 4]
        probabilidades = [0.1, 0.2, 0.4, 0.2, 0.1]
        acumuladas = [0.1, 0.3, 0.7, 0.9, 1.0]

        resultado = buscar_valor_tolerancia(valores_x, acumuladas, 70)
        assert resultado == 2

    def test_tolerancia_intermedia(self):
        valores_x = [0, 1, 2, 3]
        acumuladas = [0.2, 0.5, 0.8, 1.0]

        resultado = buscar_valor_tolerancia(valores_x, acumuladas, 60)
        assert resultado == 1

    def test_lista_vacia(self):
        resultado = buscar_valor_tolerancia([], [], 95)
        assert resultado is None

    def test_tolerancia_cero(self):
        valores_x = [0, 1, 2]
        acumuladas = [0.1, 0.5, 1.0]

        resultado = buscar_valor_tolerancia(valores_x, acumuladas, 0)
        assert resultado == 0


class TestValidarParametrosComparacion:
    """Pruebas para validar_parametros_comparacion"""

    def test_parametros_validos(self):
        valido, mensaje = validar_parametros_comparacion(10, 0.5, 100, 95)
        assert valido == True
        assert mensaje == ""

    def test_n_cero(self):
        valido, mensaje = validar_parametros_comparacion(0, 0.5, 100, 95)
        assert valido == False
        assert "n" in mensaje.lower()

    def test_p_fuera_rango(self):
        valido, mensaje = validar_parametros_comparacion(10, 1.5, 100, 95)
        assert valido == False
        assert "probabilidad" in mensaje.lower()

    def test_N_none(self):
        valido, mensaje = validar_parametros_comparacion(10, 0.5, None, 95)
        assert valido == False
        assert "población" in mensaje.lower()

    def test_n_mayor_N(self):
        valido, mensaje = validar_parametros_comparacion(150, 0.5, 100, 95)
        assert valido == False

    def test_tolerancia_fuera_rango(self):
        valido, mensaje = validar_parametros_comparacion(10, 0.5, 100, 150)
        assert valido == False
        assert "tolerancia" in mensaje.lower()


class TestValidarTolerancia:
    """Pruebas para validar_tolerancia"""

    def test_tolerancia_none(self):
        valido, valor, mensaje = validar_tolerancia(None)
        assert valido == True
        assert valor == 95.0

    def test_tolerancia_vacia(self):
        valido, valor, mensaje = validar_tolerancia("")
        assert valido == True
        assert valor == 95.0

    def test_tolerancia_valida(self):
        valido, valor, mensaje = validar_tolerancia("90")
        assert valido == True
        assert valor == 90.0

    def test_tolerancia_decimal(self):
        valido, valor, mensaje = validar_tolerancia("95.5")
        assert valido == True
        assert valor == 95.5

    def test_tolerancia_negativa(self):
        valido, valor, mensaje = validar_tolerancia("-5")
        assert valido == False

    def test_tolerancia_mayor_100(self):
        valido, valor, mensaje = validar_tolerancia("150")
        assert valido == False

    def test_tolerancia_no_numerica(self):
        valido, valor, mensaje = validar_tolerancia("abc")
        assert valido == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
