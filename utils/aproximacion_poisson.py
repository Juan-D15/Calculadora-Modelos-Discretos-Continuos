"""
Módulo de aproximación de Poisson para distribuciones Binomial e Hipergeométrica
"""

import math
from utils.calculos import binomial_pmf, poisson_pmf, hipergeometrica_pmf


class AproximacionPoissonBinomial:
    """Maneja aproximación Binomial → Poisson"""

    @staticmethod
    def calcular_lambda(n: int, p: float) -> float:
        """
        Calcula λ = n × p para aproximación de Poisson

        Args:
            n (int): Número de ensayos
            p (float): Probabilidad de éxito

        Returns:
            float: Parámetro λ
        """
        return n * p

    @staticmethod
    def validar_condiciones(n: int, p: float) -> tuple[bool, str]:
        """
        Valida condiciones ideales para aproximación Binomial → Poisson

        Condiciones: n ≥ 30 y p ≤ 0.05

        Args:
            n (int): Número de ensayos
            p (float): Probabilidad de éxito

        Returns:
            tuple: (cumple: bool, mensaje_advertencia: str)
        """
        condiciones = []

        if n < 30:
            condiciones.append(f"n={n} < 30")

        if p > 0.05:
            condiciones.append(f"p={p:.4f} > 0.05")

        if condiciones:
            mensaje = f"Advertencia: {', '.join(condiciones)}. Condiciones ideales: n≥30 y p≤0.05"
            return False, mensaje

        return True, ""

    @staticmethod
    def calcular_probabilidades_rango(
        n: int, p: float
    ) -> tuple[list[int], list[float], list[float]]:
        """
        Calcula P(X=k) para todo k=0..n en ambas distribuciones

        Args:
            n (int): Número de ensayos
            p (float): Probabilidad de éxito

        Returns:
            tuple: (valores_k, probs_binom, probs_poisson)
        """
        valores_k = list(range(n + 1))
        probs_binom = [binomial_pmf(k, n, p) for k in valores_k]
        lam = n * p
        probs_poisson = [poisson_pmf(k, lam) for k in valores_k]

        return valores_k, probs_binom, probs_poisson

    @staticmethod
    def calcular_estadisticas(n: int, p: float) -> tuple[float, float, float]:
        """
        Calcula estadísticas de distribución de Poisson

        Fórmulas: Media = λ, Varianza = λ, Desviación = √λ

        Args:
            n (int): Número de ensayos
            p (float): Probabilidad de éxito

        Returns:
            tuple: (media, varianza, desviacion)
        """
        lam = n * p
        media = lam
        varianza = lam
        desviacion = math.sqrt(lam)

        return media, varianza, desviacion


class AproximacionPoissonHiper:
    """Maneja aproximación Hipergeométrica → Poisson"""

    @staticmethod
    def calcular_lambda(N: int, K: int, n: int) -> float:
        """
        Calcula λ = n × (K/N) para aproximación de Poisson

        Args:
            N (int): Tamaño de población
            K (int): Elementos de interés en población
            n (int): Tamaño de muestra

        Returns:
            float: Parámetro λ
        """
        p = K / N
        return n * p

    @staticmethod
    def validar_condiciones(N: int, n: int) -> tuple[bool, str]:
        """
        Valida condiciones ideales para aproximación Hipergeométrica → Poisson

        Condiciones: N ≥ 50 y n/N ≤ 0.05

        Args:
            N (int): Tamaño de población
            n (int): Tamaño de muestra

        Returns:
            tuple: (cumple: bool, mensaje_advertencia: str)
        """
        condiciones = []
        porcentaje = (n / N) * 100

        if N < 50:
            condiciones.append(f"N={N} < 50")

        if porcentaje > 5:
            condiciones.append(f"n/N={porcentaje:.1f}% > 5%")

        if condiciones:
            mensaje = f"Advertencia: {', '.join(condiciones)}. Condiciones ideales: N≥50 y n/N≤5%"
            return False, mensaje

        return True, ""

    @staticmethod
    def calcular_probabilidades_rango(
        n: int, N: int, K: int
    ) -> tuple[list[int], list[float], list[float]]:
        """
        Calcula P(X=k) para k=0..min(K, n) en ambas distribuciones

        Args:
            n (int): Tamaño de muestra
            N (int): Tamaño de población
            K (int): Elementos de interés en población

        Returns:
            tuple: (valores_k, probs_hiper, probs_poisson)
        """
        max_k = min(K, n)
        valores_k = list(range(max_k + 1))

        probs_hiper = [hipergeometrica_pmf(k, n, N, K) for k in valores_k]
        lam = n * (K / N)
        probs_poisson = [poisson_pmf(k, lam) for k in valores_k]

        return valores_k, probs_hiper, probs_poisson

    @staticmethod
    def calcular_estadisticas(n: int, N: int, K: int) -> tuple[float, float, float]:
        """
        Calcula estadísticas de distribución de Poisson

        Fórmulas: Media = λ, Varianza = λ, Desviación = √λ
        donde λ = n × (K/N)

        Args:
            n (int): Tamaño de muestra
            N (int): Tamaño de población
            K (int): Elementos de interés en población

        Returns:
            tuple: (media, varianza, desviacion)
        """
        p = K / N
        lam = n * p
        media = lam
        varianza = lam
        desviacion = math.sqrt(lam)

        return media, varianza, desviacion
