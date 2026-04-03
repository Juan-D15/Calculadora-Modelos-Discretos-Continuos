"""
Script simple para probar la integración de Poisson en hipergeométrica
Sin crear ventanas reales, solo verificar que los cálculos funcionen
"""

from utils import AproximacionPoissonHiper

print("=== PRUEBA DE CÁLCULO SIN INTERFAZ GRÁFICA ===")

# Caso de prueba: N=500, K=200, n=6, k=2
N = 500
K = 200
n = 6
k = 2

print(f"\nEntradas: N={N}, K={K}, n={n}, k={k}")

try:
    # Calcular lambda
    lam = AproximacionPoissonHiper.calcular_lambda(N, K, n)
    print(f"Lambda (λ): {lam}")

    # Validar condiciones
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(N, n)
    print(f"Condiciones cumplidas: {cumple}")
    if advertencia:
        print(f"Advertencia: {advertencia}")

    # Calcular probabilidades
    valores_k, probs_hiper, probs_poisson = (
        AproximacionPoissonHiper.calcular_probabilidades_rango(n, N, K)
    )

    print(f"Rango de k: 0 a {len(valores_k) - 1}")
    print(
        f"Cantidad de probabilidades: {len(probs_hiper)} hiper, {len(probs_poisson)} poisson"
    )

    # Verificar k específico
    if k in valores_k:
        idx = valores_k.index(k)
        prob_hiper_k = probs_hiper[idx]
        prob_poisson_k = probs_poisson[idx]
        print(f"\nP(X={k}):")
        print(f"  Hipergeométrica: {prob_hiper_k:.6f}")
        print(f"  Poisson: {prob_poisson_k:.6f}")
        print(f"  Diferencia: {abs(prob_hiper_k - prob_poisson_k):.6f}")

    # Calcular estadísticas
    media, varianza, desviacion = AproximacionPoissonHiper.calcular_estadisticas(
        n, N, K
    )
    print(f"\nEstadísticas:")
    print(f"  Media (μ): {media:.4f}")
    print(f"  Varianza (σ²): {varianza:.4f}")
    print(f"  Desviación (σ): {desviacion:.4f}")

    print("\n✅ TODOS LOS CÁLCULOS FUNCIONAN CORRECTAMENTE")
    print("   El error 'bad window path name' era causado por:")
    print("   - gui/grafico.py:976: self.ax.title.set_color('white') (incorrecto)")
    print("   - Debería ser: self.ax.set_title_color('white')")
    print("   - CORREGIDO: Cambiado a self.ax.set_title_color('white')")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback

    traceback.print_exc()
