"""
Verificar calculos manuales para entender el problema
"""

from scipy.stats import binom, poisson

print("=== PRUEBA B-01: n=200, p=0.04, k=8 ===")

# Calculo manual
from scipy.special import comb

print(f"Lambda = n * p = 200 * 0.04 = 8.0")

# Probabilidad binomial exacta
k = 8
n = 200
p = 0.04

# Usando scipy
prob_binom_scipy = binom.pmf(k, n, p)
print(f"Binomial scipy: {prob_binom_scipy}")

# Usando formula manual
prob_binom_manual = comb(n, k, exact=True) * (p**k) * ((1 - p) ** (n - k))
print(f"Binomial manual: {prob_binom_manual}")

# Poisson
lam = n * p
prob_poisson_scipy = poisson.pmf(k, lam)
print(f"Poisson scipy: {prob_poisson_scipy}")

# Formula manual
import math

prob_poisson_manual = (math.exp(-lam) * (lam**k)) / math.factorial(k)
print(f"Poisson manual: {prob_poisson_manual}")

print(
    f"\nBinomial scipy vs esperado (0.13915): diferencia = {abs(prob_binom_scipy - 0.13915)}"
)
print(
    f"Poisson scipy vs esperado (0.13960): diferencia = {abs(prob_poisson_scipy - 0.13960)}"
)

print("\n=== Verificacion PRUEBA B-03: n=10, p=0.077, k=2 ===")

n = 10
p = 0.077
k = 2
lam = n * p

prob_binom_scipy = binom.pmf(k, n, p)
print(f"Binomial scipy: {prob_binom_scipy}")
print(f"Esperado: 0.0988")
print(f"Diferencia: {abs(prob_binom_scipy - 0.0988)}")

prob_poisson_scipy = poisson.pmf(k, lam)
print(f"Poisson scipy: {prob_poisson_scipy}")
print(f"Esperado: 0.1129")
print(f"Diferencia: {abs(prob_poisson_scipy - 0.1129)}")
