"""
Depuración específica de la prueba H-03
"""

from utils import AproximacionPoissonHiper
from scipy.stats import hypergeom, poisson

print("=== DEPURACION PRUEBA H-03 ===")
print("Entradas: N=500, K=200, n=6")

valores_k, probs_hiper, probs_poisson = (
    AproximacionPoissonHiper.calcular_probabilidades_rango(6, 500, 200)
)

print(f"valores_k: {valores_k}")
print(f"len(valores_k): {len(valores_k)}")
print(f"len(probs_hiper): {len(probs_hiper)}")
print(f"len(probs_poisson): {len(probs_poisson)}")

# Verificar tabla contiene k=0 hasta k=6
print(f"valores_k == list(range(7)): {valores_k == list(range(7))}")

# Verificar valores individuales con scipy
print("\nVerificar valores individuales:")
for k in valores_k:
    idx = valores_k.index(k)
    prob_hiper = probs_hiper[idx]
    prob_poisson = probs_poisson[idx]

    # Calcular esperado con scipy
    esperado_hiper = float(hypergeom.pmf(k, 500, 200, 6))
    esperado_poisson = float(poisson.pmf(k, 2.4))

    print(
        f"k={k}: hiper={prob_hiper:.6f} (esperado={esperado_hiper:.6f}), poisson={prob_poisson:.6f} (esperado={esperado_poisson:.6f})"
    )

# Verificar sumas
suma_hiper = sum(probs_hiper)
suma_poisson = sum(probs_poisson)

print(f"\nSumas:")
print(f"  suma_hiper: {suma_hiper}")
print(f"  suma_poisson: {suma_poisson}")
print(f"  suma_hiper esperada ~1.0: {abs(suma_hiper - 1.0)}")
print(f"  suma_poisson esperada ~1.0: {abs(suma_poisson - 1.0)}")

# Verificar con scipy directo para validar
valores_k_direct = list(range(7))
probs_hiper_scipy = [float(hypergeom.pmf(k, 500, 200, 6)) for k in valores_k_direct]
probs_poisson_scipy = [float(poisson.pmf(k, 2.4)) for k in valores_k_direct]

suma_hiper_scipy = sum(probs_hiper_scipy)
suma_poisson_scipy = sum(probs_poisson_scipy)

print(f"\nSumas scipy directo:")
print(f"  suma_hiper_scipy: {suma_hiper_scipy}")
print(f"  suma_poisson_scipy: {suma_poisson_scipy}")
print(f"  suma_hiper_scipy esperada ~1.0: {abs(suma_hiper_scipy - 1.0)}")
print(f"  suma_poisson_scipy esperada ~1.0: {abs(suma_poisson_scipy - 1.0)}")

# Comparar
print(f"\nDiferencia hiper: {abs(suma_hiper - suma_hiper_scipy)}")
print(f"Diferencia poisson: {abs(suma_poisson - suma_poisson_scipy)}")
