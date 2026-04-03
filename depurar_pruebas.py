"""
Script de depuracion para ver valores calculados
"""

from utils import AproximacionPoissonBinomial, AproximacionPoissonHiper

print("=== DEPURACION PRUEBA B-01 ===")
print("Entradas: n=200, p=0.04, k=8")

lam = AproximacionPoissonBinomial.calcular_lambda(200, 0.04)
print(f"lambda calculado: {lam}")
print(f"lambda esperado: 8.0")
print(f"Diferencia: {abs(lam - 8.0)}")

cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(200, 0.04)
print(f"Cumple condiciones: {cumple}")
print(f"Advertencia: '{advertencia}'")

valores_k, probs_binom, probs_poisson = (
    AproximacionPoissonBinomial.calcular_probabilidades_rango(200, 0.04)
)
print(f"len(valores_k): {len(valores_k)}")
print(f"len(probs_binom): {len(probs_binom)}")
print(f"len(probs_poisson): {len(probs_poisson)}")

if 8 in valores_k:
    idx_8 = valores_k.index(8)
    prob_binom_8 = probs_binom[idx_8]
    prob_poisson_8 = probs_poisson[idx_8]

    print(f"prob_binom_8: {prob_binom_8}")
    print(f"prob_binom esperado: 0.13915")
    print(f"Diferencia: {abs(prob_binom_8 - 0.13915)}")

    print(f"prob_poisson_8: {prob_poisson_8}")
    print(f"prob_poisson esperado: 0.13960")
    print(f"Diferencia: {abs(prob_poisson_8 - 0.13960)}")
else:
    print("k=8 NO esta en valores_k!")

print("\n=== DEPURACION PRUEBA B-03 ===")
print("Entradas: n=10, p=0.077, k=2")

lam = AproximacionPoissonBinomial.calcular_lambda(10, 0.077)
print(f"lambda calculado: {lam}")
print(f"lambda esperado: 0.77")
print(f"Diferencia: {abs(lam - 0.77)}")

cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(10, 0.077)
print(f"Cumple condiciones: {cumple}")
print(f"Advertencia: '{advertencia}'")

valores_k, probs_binom, probs_poisson = (
    AproximacionPoissonBinomial.calcular_probabilidades_rango(10, 0.077)
)

if 2 in valores_k:
    idx_2 = valores_k.index(2)
    prob_binom_2 = probs_binom[idx_2]
    prob_poisson_2 = probs_poisson[idx_2]

    print(f"prob_binom_2: {prob_binom_2}")
    print(f"prob_binom esperado: 0.0988")
    print(f"Diferencia: {abs(prob_binom_2 - 0.0988)}")

    print(f"prob_poisson_2: {prob_poisson_2}")
    print(f"prob_poisson esperado: 0.1129")
    print(f"Diferencia: {abs(prob_poisson_2 - 0.1129)}")
else:
    print("k=2 NO esta en valores_k!")

print("\n=== DEPURACION PRUEBA H-01 ===")
print("Entradas: N=50, K=20, n=15, k=7")

lam = AproximacionPoissonHiper.calcular_lambda(50, 20, 15)
print(f"lambda calculado: {lam}")
print(f"lambda esperado: 6.0")
print(f"Diferencia: {abs(lam - 6.0)}")

cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(50, 15)
print(f"Cumple condiciones: {cumple}")
print(f"Advertencia: '{advertencia}'")

valores_k, probs_hiper, probs_poisson = (
    AproximacionPoissonHiper.calcular_probabilidades_rango(15, 50, 20)
)
print(f"len(valores_k): {len(valores_k)}")

if 7 in valores_k:
    idx_7 = valores_k.index(7)
    prob_hiper_7 = probs_hiper[idx_7]
    prob_poisson_7 = probs_poisson[idx_7]

    print(f"prob_hiper_7: {prob_hiper_7}")
    print(f"prob_hiper esperado: 0.1032")
    print(f"Diferencia: {abs(prob_hiper_7 - 0.1032)}")

    print(f"prob_poisson_7: {prob_poisson_7}")
    print(f"prob_poisson esperado: 0.1377")
    print(f"Diferencia: {abs(prob_poisson_7 - 0.1377)}")
else:
    print("k=7 NO esta en valores_k!")
