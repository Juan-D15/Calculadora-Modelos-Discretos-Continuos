# Tests de aproximación de Poisson
import pytest
import math
from utils.aproximacion_poisson import (
    AproximacionPoissonBinomial,
    AproximacionPoissonHiper,
)


def test_calcular_lambda():
    """Test lambda calculation for Poisson approximation"""
    result = AproximacionPoissonBinomial.calcular_lambda(100, 0.05)
    assert result == 5.0  # 100 * 0.05


def test_calcular_lambda_edge_case():
    """Test lambda with extreme values"""
    result = AproximacionPoissonBinomial.calcular_lambda(1000, 0.001)
    assert result == 1.0  # 1000 * 0.001


def test_validar_condiciones_ideal():
    """Test validation with ideal conditions"""
    cumple, mensaje = AproximacionPoissonBinomial.validar_condiciones(100, 0.03)
    assert cumple is True
    assert mensaje == ""


def test_validar_condiciones_n_menor_30():
    """Test validation when n < 30"""
    cumple, mensaje = AproximacionPoissonBinomial.validar_condiciones(20, 0.03)
    assert cumple is False
    assert "n=20 < 30" in mensaje


def test_validar_condiciones_p_mayor_0_05():
    """Test validation when p > 0.05"""
    cumple, mensaje = AproximacionPoissonBinomial.validar_condiciones(100, 0.10)
    assert cumple is False
    assert "p=0.1000 > 0.05" in mensaje


def test_validar_condiciones_ambos_falla():
    """Test validation when both conditions fail"""
    cumple, mensaje = AproximacionPoissonBinomial.validar_condiciones(10, 0.10)
    assert cumple is False
    assert "n=10 < 30" in mensaje
    assert "p=0.1000 > 0.05" in mensaje


def test_calcular_probabilidades_rango():
    """Test probability calculations for range"""
    n, p = 10, 0.5
    valores_k, probs_binom, probs_poisson = (
        AproximacionPoissonBinomial.calcular_probabilidades_rango(n, p)
    )

    assert len(valores_k) == 11  # 0 to 10
    assert valores_k == list(range(11))
    assert len(probs_binom) == 11
    assert len(probs_poisson) == 11
    assert all(0 <= prob <= 1 for prob in probs_binom)
    assert all(0 <= prob <= 1 for prob in probs_poisson)


def test_calcular_estadisticas():
    """Test statistics calculation"""
    media, varianza, desviacion = AproximacionPoissonBinomial.calcular_estadisticas(
        100, 0.05
    )

    assert media == 5.0  # lambda
    assert varianza == 5.0  # lambda
    assert desviacion == math.sqrt(5.0)


def test_hiper_calcular_lambda():
    """Test lambda calculation for hypergeometric"""
    result = AproximacionPoissonHiper.calcular_lambda(100, 20, 10)
    assert result == 2.0  # 10 * (20/100)


def test_hiper_validar_condiciones_ideal():
    """Test validation with ideal conditions"""
    cumple, mensaje = AproximacionPoissonHiper.validar_condiciones(100, 3)
    assert cumple is True
    assert mensaje == ""


def test_hiper_validar_condiciones_N_menor_50():
    """Test validation when N < 50"""
    cumple, mensaje = AproximacionPoissonHiper.validar_condiciones(30, 2)
    assert cumple is False
    assert "N=30 < 50" in mensaje


def test_hiper_validar_condiciones_n_sobre_N():
    """Test validation when n/N > 5%"""
    cumple, mensaje = AproximacionPoissonHiper.validar_condiciones(100, 10)
    assert cumple is False
    assert "n/N=10.0% > 5%" in mensaje


def test_hiper_calcular_probabilidades_rango():
    """Test probability calculations for range"""
    n, N, K = 10, 50, 20
    valores_k, probs_hiper, probs_poisson = (
        AproximacionPoissonHiper.calcular_probabilidades_rango(n, N, K)
    )

    max_k = min(K, n)  # 10
    assert len(valores_k) == 11  # 0 to 10
    assert valores_k == list(range(11))
    assert len(probs_hiper) == 11
    assert len(probs_poisson) == 11


def test_hiper_calcular_estadisticas():
    """Test statistics calculation"""
    media, varianza, desviacion = AproximacionPoissonHiper.calcular_estadisticas(
        10, 50, 20
    )

    lam = 10 * (20 / 50)  # 4
    assert media == lam
    assert varianza == lam
    assert desviacion == math.sqrt(lam)
