"""
Script de diagnóstico para simular el flujo de Poisson en hipergeométrica
Simula el flujo completo desde la entrada de datos hasta la visualización
"""

import sys

print("=== DIAGNÓSTICO - SIMULACIÓN DE FLUJO HIPERGEOMÉTRICA → POISSON ===")

print("\nPaso 1: Simular obtención de datos de hipergeométrica")
print("-" * 60)

try:
    # Verificar que el checkbox existe
    print("  Verificación: Existe checkbox chk_poisson en CamposEntradaHipergeometrica")
    print("  Resultado: SIMULADO (se asume que existe)\n")

    # Verificar que el checkbox está marcado
    print("  Verificación: Checkbox está ACTIVADO")
    print("  Resultado: SIMULADO\n")

    # Simular el cálculo
    from utils import AproximacionPoissonHiper

    N = 50
    K = 20
    n = 15
    k = 7

    print(f"\nPaso 2: Simular cálculo con:")
    print(f"  N={N}, K={K}, n={n}, k={k}")

    lam = AproximacionPoissonHiper.calcular_lambda(N, K, n)
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(N, n)
    valores_k, probs_hiper, probs_poisson = (
        AproximacionPoissonHiper.calcular_probabilidades_rango(n, N, K)
    )

    print(f"\n  lambda: {lam}")
    print(f"  Condiciones cumplidas: {cumple}")
    if advertencia:
        print(f"  Advertencia: {advertencia}")

    print(f"  Rango de k: 0 a {len(valores_k) - 1}")
    print(f"  Probabilidades calculadas: {len(probs_hiper)} valores")

    print(
        "\nPaso 3: Simular llamada a dashboard.mostrar_resultados_poisson_hipergeometrica"
    )
    print("-" * 60)

    datos_resultados = {
        "N": N,
        "K": K,
        "n": n,
        "lambda": lam,
        "k_ingresado": k,
        "valores_k": valores_k,
        "probs_hiper": probs_hiper,
        "probs_poisson": probs_poisson,
        "media": lam,
        "varianza": lam,
        "desviacion": lam**0.5 if lam > 0 else 0,
    }

    print("  Datos preparados (simulado):")
    print(f"    - λ: {datos_resultados['lambda']}")
    print(f"    - Rango k: 0 a {len(datos_resultados['valores_k']) - 1}")
    print(f"    - k_ingresado: {k}")
    print(f"    - Cantidad de probabilidades: {len(datos_resultados['probs_hiper'])}")

    print("\n  Resultado: SIMULADO (sin verificar implementación real)")
    print("  Los métodos de visualización DEBERÍAN ser llamados:")
    print("  1. dashboard.mostrar_resultados_poisson_hipergeometrica(datos)")
    print(
        "  2. dashboard.crear_grafico_poisson_hipergeometrica(valores_k, probs_hiper, probs_poisson, k, N, K, n, lam)"
    )
    print("  3. dashboard.expandir_tabla_poisson_hipergeometrica()")
    print("")
    print("DIAGNÓSTICO:")
    print("-" * 60)
    print(
        "  Si al ejecutar la aplicación y marcar el checkbox de Poisson en hipergeométrica:"
    )
    print("  con los mismos datos N=50, K=20, n=15, x=7:")
    print("")
    print("  Y no se muestran resultados ni gráfica, entonces:")
    print(
        "  1. Revisar que self.dashboard.campos_hipergeometrica.chk_poisson.get() devuelve True"
    )
    print("  2. Revisar que se llama a calcular_poisson_hipergeometrica()")
    print("  3. Revisar que se llaman a los métodos de visualización:")
    print("     - mostrar_resultados_poisson_hipergeometrica()")
    print("     - crear_grafico_poisson_hipergeometrica()")
    print("  4. Revisar si hay errores en consola/terminal durante la ejecución")
    print("")
    print("  Posibles causas:")
    print(
        "  - El método calcular_poisson_hipergeometrica() no existe en ventana_principal.py"
    )
    print("  - Los métodos de visualización no están conectados correctamente")
    print("  - Hay un error en la integración que previene la ejecución")
    print(
        "  - Los métodos en dashboard.py están intentando acceder a atributos inexistentes en self.dashboard"
    )
    print(
        "  - Requiere agregar el método calcular_poisson_hipergeometrica() a ventana_principal.py"
    )
    print("")
    print("  SOLUCIÓN INMEDIATA:")
    print(
        "  El método calcular_poisson_hipergeometrica() ya existe en ventana_principal.py"
    )
    print(
        "  Revisar si está conectado correctamente con la lógica del checkbox (línea 332-334)"
    )
    print(
        "  Si está, verificar que los métodos de visualización se llaman desde ese método"
    )
    print("  Si no, revisar la integración y corregir")

    sys.exit(0)

except Exception as e:
    print(f"\n  ERROR inesperado: {str(e)}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
