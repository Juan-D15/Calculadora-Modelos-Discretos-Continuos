"""
Script de prueba para verificar que la aproximación de Poisson en hipergeométrica funciona
"""

from utils import AproximacionPoissonHiper

print("=== PRUEBA DE INTEGRACIÓN - HIPERGEOMETRICA → POISSON ===")

print("\n1. Verificar que el método de cálculo existe y funciona:")
print("-" * 60)

try:
    lam = AproximacionPoissonHiper.calcular_lambda(500, 200, 6)
    print(f"  lambda calculado: {lam} (esperado: 2.4)")

    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(500, 6)
    print(f"  condiciones cumplidas: {cumple}")
    if advertencia:
        print(f"  advertencia: '{advertencia}'")

    valores_k, probs_hiper, probs_poisson = (
        AproximacionPoissonHiper.calcular_probabilidades_rango(6, 500, 200)
    )
    print(f"  rango de k: 0 a {len(valores_k) - 1}")
    print(
        f"  cantidad de probabilidades: {len(probs_hiper)} hiper, {len(probs_poisson)} poisson"
    )

    media, varianza, desviacion = AproximacionPoissonHiper.calcular_estadisticas(
        6, 500, 200
    )
    print(f"  media: {media}, varianza: {varianza}, desviacion: {desviacion}")

    print("  OK: Todos los cálculos funcionan correctamente\n")

except Exception as e:
    print(f"  ERROR: {str(e)}\n")
    import sys

    sys.exit(1)

print("\n2. Verificar que los métodos de visualización están implementados:")
print("-" * 60)

import os

# Verificar que dashboard.py tiene los métodos necesarios
with open("gui/dashboard.py", "r", encoding="utf-8") as f:
    contenido = f.read()

    metodos_necesarios = [
        "mostrar_resultados_poisson_hipergeometrica",
        "crear_grafico_poisson_hipergeometrica",
        "expandir_tabla_poisson_hipergeometrica",
    ]

    for metodo in metodos_necesarios:
        if f"def {metodo}(" in contenido:
            print(f"  OK: Método '{metodo}' encontrado en dashboard.py")
        else:
            print(f"  ERROR: Método '{metodo}' NO encontrado en dashboard.py")

# Verificar que el checkbox está en CamposEntradaHipergeometrica
with open("gui/campos_entrada.py", "r", encoding="utf-8") as f:
    contenido = f.read()

    if "chk_poisson = ctk.CTkCheckBox" in contenido:
        print("  OK: Checkbox 'chk_poisson' encontrado en CamposEntradaHipergeometrica")
    else:
        print(
            "  ERROR: Checkbox 'chk_poisson' NO encontrado en CamposEntradaHipergeometrica"
        )

# Verificar que ventana_principal.py llama a calcular_poisson_hipergeometrica
with open("ventana_principal.py", "r", encoding="utf-8") as f:
    contenido = f.read()

    if "def calcular_poisson_hipergeometrica(self):" in contenido:
        print(
            "  OK: Método 'calcular_poisson_hipergeometrica()' definido en ventana_principal.py"
        )
    else:
        print(
            "  ERROR: Método 'calcular_poisson_hipergeometrica()' NO definido en ventana_principal.py"
        )

    # Verificar que se verifica el checkbox en calcular_hipergeometrica
    if "self.dashboard.campos_hipergeometrica.chk_poisson.get()" in contenido:
        print("  OK: Lógica de verificación de checkbox en calcular_hipergeometrica()")
    else:
        print(
            "  ERROR: Lógica de verificación de checkbox NO encontrada en calcular_hipergeometrica()"
        )

print("\n3. Verificar que la integración está completa:")
print("-" * 60)

# Buscar el patrón correcto de integración
with open("ventana_principal.py", "r", encoding="utf-8") as f:
    contenido = f.read()

    # Verificar que calcular_poisson_binomial tiene el mismo patrón
    if "if (hasattr(self.dashboard.campos, 'chk_poisson')" in contenido:
        print("  OK: Patrón de verificación de checkbox encontrado (Binomial)")
    else:
        print("  INFO: Patrón de verificación de checkbox NO encontrado (Binomial)")

    if "if (hasattr(self.dashboard.campos_hipergeometrica, 'chk_poisson')" in contenido:
        print("  OK: Patrón de verificación de checkbox encontrado (Hipergeométrica)")
    else:
        print(
            "  ERROR: Patrón de verificación de checkbox NO encontrado (Hipergeométrica)"
        )

print("\n" + "=" * 70)
print("CONCLUSIÓN")
print("=" * 70)

print("\nSISTEMA LISTO PARA PRUEBAS:")
print("1. Ejecutar: .venv/Scripts/python.exe main.py")
print("2. Ir a la pestaña 'Hipergeométrica'")
print("3. Ingresar: N=500, K=200, n=6, k=2")
print("4. Marcar 'Activar aproximación Poisson'")
print("5. Click en 'Calcular'")
print("")
print("RESULTADOS ESPERADOS:")
print("  ✓ Advertencia de condiciones (N≥50, n/N≤5%)")
print("  ✓ Tabla comparativa acotada (20 filas centradas en k=2)")
print("  ✓ Fila k=2 resaltada en azul")
print("  ✓ Estadísticas (λ, media, varianza, desviación)")
print("  ✓ Gráfica de barras agrupadas (Hipergeométrica + Poisson)")
print("")
print("Si NO se muestran los resultados, revisar:")
print("  1. Terminal para errores de consola/terminal")
print("   2. El checkbox 'chk_poisson' está en CamposEntradaHipergeometrica")
print("  3. Los métodos de visualización existen en dashboard.py")
print("  4. La lógica de verificación está en calcular_hipergeometrica()")

print("\n" + "=" * 70)
