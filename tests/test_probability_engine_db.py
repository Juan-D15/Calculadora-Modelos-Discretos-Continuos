"""
Pruebas para preparar parámetros importados desde ventas del simulador.
"""
import pytest

from probability_engine import ParametrosInvalidosError, ProbabilityEngine


def test_preparar_parametros_recomienda_binomial_hasta_5_por_ciento():
    """Si n es hasta 5% de N, recomienda Binomial sin corrección finita."""
    datos = ProbabilityEngine().preparar_parametros_desde_ventas(N=1000, K=80, n=50)

    assert datos["p"] == pytest.approx(0.08)
    assert datos["modelo_recomendado"] == "Binomial"
    assert datos["usa_correccion_finita"] is False


def test_preparar_parametros_recomienda_binomial_entre_5_y_20():
    """Si n está entre 5% y 20%, recomienda Binomial con corrección finita."""
    datos = ProbabilityEngine().preparar_parametros_desde_ventas(N=1000, K=80, n=100)

    assert datos["modelo_recomendado"] == "Binomial"
    assert datos["usa_correccion_finita"] is True


def test_preparar_parametros_recomienda_hipergeometrica_desde_20():
    """Si n es al menos 20% de N, recomienda Hipergeométrica."""
    datos = ProbabilityEngine().preparar_parametros_desde_ventas(N=1000, K=80, n=200)

    assert datos["modelo_recomendado"] == "Hipergeométrica"


def test_preparar_parametros_rechaza_k_mayor_que_n():
    """K no puede superar el inventario ficticio N."""
    with pytest.raises(ParametrosInvalidosError):
        ProbabilityEngine().preparar_parametros_desde_ventas(N=10, K=12, n=5)


def test_preparar_parametros_explica_inventario_insuficiente():
    """El error debe indicar cómo corregir N cuando K viene de ventas importadas."""
    with pytest.raises(ParametrosInvalidosError) as exc_info:
        ProbabilityEngine().preparar_parametros_desde_ventas(N=10, K=207, n=6)

    mensaje = str(exc_info.value)
    assert "unidades vendidas importadas" in mensaje
    assert "207" in mensaje
    assert "inventario" in mensaje.lower()


def test_preparar_parametros_permite_lambda_poisson_desde_ventas():
    """Poisson usa p=K/N y lambda=n*p desde ventas importadas."""
    datos = ProbabilityEngine().preparar_parametros_desde_ventas(N=1000, K=54, n=100)

    assert datos["p"] == pytest.approx(0.054)
    assert datos["lambda_poisson"] == pytest.approx(5.4)
