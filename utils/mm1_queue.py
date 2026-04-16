"""
Módulo de Colas de Espera Modelo M/M/1
Implementa el modelo de cola de un servidor con llegadas Poisson y servicio exponencial
"""

import math
from typing import Dict


class MM1Queue:
    """
    Clase para calcular métricas del modelo de cola M/M/1

    Fórmula general:
    - λ (lam): tasa de llegada de clientes
    - μ (mu): tasa de servicio
    - ρ = λ/μ: factor de utilización

    Args:
        lam (float): Tasa de llegada de clientes (clientes/unidad de tiempo)
        mu (float): Tasa de servicio (clientes/unidad de tiempo)
        n (int, optional): Número de clientes para calcular probabilidad P(N=n)
    """

    def __init__(self, lam: float, mu: float, n: int = 0):
        if not isinstance(lam, (int, float)):
            raise TypeError("λ (lam) debe ser un valor numérico")
        if not isinstance(mu, (int, float)):
            raise TypeError("μ (mu) debe ser un valor numérico")

        if lam <= 0:
            raise ValueError("λ (lam) debe ser mayor a 0")
        if mu <= 0:
            raise ValueError("μ (mu) debe ser mayor a 0")

        self._lam = float(lam)
        self._mu = float(mu)
        self._n = n

        self._rho = self._lam / self._mu

        if self._rho >= 1:
            raise ValueError(
                f"Sistema inestable: ρ = {self._rho:.4f} >= 1 (λ debe ser < μ)"
            )

        self._Ls = self._rho / (1 - self._rho)
        self._Lq = (self._rho**2) / (1 - self._rho)
        self._Ws = 1 / (self._mu - self._lam)
        self._Wq = self._lam / (self._mu * (self._mu - self._lam))
        self._P0 = 1 - self._rho

    @property
    def lambda_val(self) -> float:
        """Retorna λ (tasa de llegada)"""
        return self._lam

    @property
    def mu(self) -> float:
        """Retorna μ (tasa de servicio)"""
        return self._mu

    @property
    def rho(self) -> float:
        """Retorna ρ (factor de utilización)"""
        return self._rho

    @property
    def Ls(self) -> float:
        """Retorna Ls (longitud media en el sistema)"""
        return self._Ls

    @property
    def Lq(self) -> float:
        """Retorna Lq (longitud media en la cola)"""
        return self._Lq

    @property
    def Ws(self) -> float:
        """Retorna Ws (tiempo medio en el sistema)"""
        return self._Ws

    @property
    def Wq(self) -> float:
        """Retorna Wq (tiempo medio en la cola)"""
        return self._Wq

    @property
    def P0(self) -> float:
        """Retorna P0 (probabilidad de sistema vacío)"""
        return self._P0

    def summary(self) -> Dict[str, float]:
        """
        Retorna un diccionario con todos los resultados calculados

        Returns:
            dict: Diccionario con lambda, mu, rho, Ls, Lq, Ws, Wq, P0
        """
        return {
            "lambda": self._lam,
            "mu": self._mu,
            "rho": self._rho,
            "Ls": self._Ls,
            "Lq": self._Lq,
            "Ws": self._Ws,
            "Wq": self._Wq,
            "P0": self._P0,
        }

    def pn(self, n: int) -> float:
        """
        Calcula la probabilidad P(N=n) de tener n clientes en el sistema

        Fórmula: P(n) = (1 - ρ) × ρ^n

        Args:
            n (int): Número de clientes en el sistema (n >= 0)

        Returns:
            float: Probabilidad de tener exactamente n clientes
        """
        if n < 0:
            raise ValueError("n debe ser >= 0")
        if not isinstance(n, int):
            raise TypeError("n debe ser un entero")

        return (1 - self._rho) * (self._rho**n)

    def plot_results(self):
        """
        Genera los gráficos de resultados del modelo M/M/1
        - Gráfico 1: Pn vs n (distribución de probabilidad)
        - Gráfico 2: Lq y Ls vs ρ (como varía ρ de 0.01 a 0.99)
        """
        import matplotlib.pyplot as plt
        import numpy as np

        plt.style.use("dark_background")
        bg_color = "#2b2b2b"
        grid_color = "#444444"

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle("Modelo de Colas M/M/1", fontsize=14, fontweight="bold")

        valores_n = list(range(21))
        probabilidades = [self.pn(i) for i in valores_n]

        axes[0].bar(valores_n, probabilidades, color="#3b8ed0", edgecolor="#1a5a8a")
        axes[0].set_title("Distribución P(N=n)", fontweight="bold")
        axes[0].set_xlabel("Número de clientes (n)")
        axes[0].set_ylabel("Probabilidad P(N=n)")
        axes[0].set_facecolor(bg_color)
        axes[0].grid(True, color=grid_color, linestyle="--", alpha=0.5)

        rhos = np.linspace(0.01, 0.99, 50)
        mu_fijo = self._mu

        Lqs = [(r**2) / (1 - r) for r in rhos]
        Lss = [r / (1 - r) for r in rhos]

        axes[1].plot(rhos, Lqs, label="Lq (cola)", color="#e74c3c", linewidth=2)
        axes[1].plot(rhos, Lss, label="Ls (sistema)", color="#2ecc71", linewidth=2)
        axes[1].set_title("Longitud vs Factor de Utilización", fontweight="bold")
        axes[1].set_xlabel("Factor de utilización (ρ)")
        axes[1].set_ylabel("Longitud promedio")
        axes[1].legend()
        axes[1].set_facecolor(bg_color)
        axes[1].grid(True, color=grid_color, linestyle="--", alpha=0.5)

        for ax in axes:
            ax.spines["bottom"].set_color(grid_color)
            ax.spines["top"].set_color("none")
            ax.spines["left"].set_color(grid_color)
            ax.spines["right"].set_color("none")

        plt.tight_layout()
        plt.show()


def run_tests():
    """
    Ejecuta los tests de validación para el modelo M/M/1
    """
    print("=" * 60)
    print("EJECUTANDO TESTS - MODELO M/M/1")
    print("=" * 60)

    passed = 0
    total = 0

    def compare(name: str, expected: float, got: float, tolerance: float = 0.0001):
        nonlocal passed, total
        total += 1
        if abs(expected - got) <= tolerance:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name}: esperado {expected:.4f}, obtenido {got:.4f}")

    print("\n--- Caso 1: lambda=4, mu=6 ---")
    try:
        q1 = MM1Queue(4, 6)
        compare("rho", 0.6667, q1.rho)
        compare("Ls", 2.0000, q1.Ls)
        compare("Lq", 1.3333, q1.Lq)
        compare("Ws", 0.5000, q1.Ws)
        compare("Wq", 0.3333, q1.Wq)
        compare("P0", 0.3333, q1.P0)
        compare("P(n=0)", 0.3333, q1.pn(0))
        compare("P(n=1)", 0.2222, q1.pn(1))
        compare("P(n=2)", 0.1481, q1.pn(2))
    except Exception as e:
        print(f"  [ERROR] Caso 1: {e}")

    print("\n--- Caso 2: lambda=2, mu=5 ---")
    try:
        q2 = MM1Queue(2, 5)
        compare("rho", 0.4000, q2.rho)
        compare("Ls", 0.6667, q2.Ls)
        compare("Lq", 0.2667, q2.Lq)
        compare("Ws", 0.3333, q2.Ws)
        compare("Wq", 0.1333, q2.Wq)
        compare("P0", 0.6000, q2.P0)
    except Exception as e:
        print(f"  [ERROR] Caso 2: {e}")

    print("\n--- Casos de error esperado ---")

    total += 1
    try:
        q3 = MM1Queue(5, 3)
        print("  [FAIL] lambda=5, mu=3: deberia lanzar ValueError (sistema inestable)")
    except ValueError as e:
        print("  [PASS] lambda=5, mu=3: ValueError correctamente lanzado")
        passed += 1

    total += 1
    try:
        q4 = MM1Queue(0, 5)
        print("  [FAIL] lambda=0, mu=5: deberia lanzar ValueError (tasa invalida)")
    except ValueError as e:
        print("  [PASS] lambda=0, mu=5: ValueError correctamente lanzado")
        passed += 1

    print("\n" + "=" * 60)
    print(f"Tests pasados: {passed}/{total}")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
