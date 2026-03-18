# Tests de integración para aproximación de Poisson
"""
Tests de integración para aproximación de Poisson
"""

import pytest
from utils import AproximacionPoissonBinomial, AproximacionPoissonHiper


def test_integracion_binomial_poisson_completa():
    """Test flujo completo de aproximación Binomial → Poisson"""
    n, p = 100, 0.04
    k = 5

    # Validar condiciones
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(n, p)
    assert cumple is True  # n=100 ≥ 30, p=0.04 ≤ 0.05

    # Calcular lambda
    lam = AproximacionPoissonBinomial.calcular_lambda(n, p)
    assert lam == 4.0

    # Calcular probabilidades
    valores_k, probs_binom, probs_poisson = (
        AproximacionPoissonBinomial.calcular_probabilidades_rango(n, p)
    )

    assert len(valores_k) == 101
    assert k in valores_k
    assert len(probs_binom) == 101
    assert len(probs_poisson) == 101

    # Calcular estadísticas
    media, varianza, desviacion = AproximacionPoissonBinomial.calcular_estadisticas(
        n, p
    )
    assert media == 4.0
    assert varianza == 4.0
    assert desviacion == pytest.approx(2.0, rel=0.01)

    # Verificar que probabilidades suman aproximadamente 1
    assert sum(probs_binom) == pytest.approx(1.0, rel=0.01)
    assert sum(probs_poisson) == pytest.approx(1.0, rel=0.01)


def test_integracion_hipergeometrica_poisson_completa():
    """Test flujo completo de aproximación Hipergeométrica → Poisson"""
    N, K, n = 100, 20, 10
    k = 2

    # Validar condiciones
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(N, n)
    assert cumple is True  # N=100 ≥ 50, n/N=10% > 5% (pero continuamos)

    # Calcular lambda
    lam = AproximacionPoissonHiper.calcular_lambda(N, K, n)
    assert lam == 2.0  # 10 * (20/100)

    # Calcular probabilidades
    valores_k, probs_hiper, probs_poisson = (
        AproximacionPoissonHiper.calcular_probabilidades_rango(n, N, K)
    )

    max_k = min(K, n)
    assert len(valores_k) == max_k + 1
    assert k in valores_k
    assert len(probs_hiper) == max_k + 1
    assert len(probs_poisson) == max_k + 1

    # Calcular estadísticas
    media, varianza, desviacion = AproximacionPoissonHiper.calcular_estadisticas(
        n, N, K
    )
    assert media == 2.0
    assert varianza == 2.0
    assert desviacion == pytest.approx(1.414, rel=0.01)


def test_caso_prueba_binomial_ejercicio_8():
    """Test caso de ejercicio 8: n=200, K_amarillos=200, total=500, muestra=6"""
    # Nota: Este es el caso mencionado en el requerimiento
    n = 6  # muestra
    p = 200 / 500  # probabilidad
    lam = n * p

    valores_k, probs_binom, probs_poisson = (
        AproximacionPoissonBinomial.calcular_probabilidades_rango(n, p)
    )

    assert lam == 2.4
    assert len(valores_k) == 7  # 0 to 6

    # Verificar que ambas distribuciones son similares
    for i in range(len(valores_k)):
        diff = abs(probs_binom[i] - probs_poisson[i])
        # Diferencia debe ser razonablemente pequeña para buena aproximación
        # (esto depende de las condiciones específicas)
        assert diff < 0.1  # Tolerancia razonable


def test_advertencia_condiciones_no_ideales():
    """Test que se muestra advertencia cuando condiciones no son ideales"""
    # Caso: n pequeño
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(10, 0.03)
    assert cumple is False
    assert "n=10 < 30" in advertencia

    # Caso: p grande
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(100, 0.10)
    assert cumple is False
    assert "p=0.1000 > 0.05" in advertencia

    # Caso Hipergeométrica: N pequeño
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(30, 2)
    assert cumple is False
    assert "N=30 < 50" in advertencia

    # Caso Hipergeométrica: n/N grande
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(100, 10)
    assert cumple is False
    assert "n/N=10.0% > 5%" in advertencia
