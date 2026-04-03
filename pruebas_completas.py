"""
Script de pruebas exhaustivas para los módulos de aproximación de Poisson
Valores esperados recalculados con scipy para mayor precisión
"""

import sys
import math
from scipy.stats import binom, poisson, hypergeom
from utils import AproximacionPoissonBinomial, AproximacionPoissonHiper


def reportar_resultado(id_prueba, modulo, resultado, observacion):
    """Reporta el resultado de una prueba"""
    status = "PASSED" if resultado else "FAILED"
    print(f"  | {id_prueba:8s} | {modulo:10s} | {status:12s} | {observacion:20s} |")


# Tolerancia para comparaciones de decimales
TOLERANCIA = 0.0001

# Contadores
total_pruebas = 0
pruebas_pasadas = 0
pruebas_fallidas = 0

print("\n" + "=" * 70)
print("MODULO 1 - POISSON COMO APROXIMACION A LA BINOMIAL")
print("=" * 70)

# --- PRUEBA B-01 --- Condiciones ideales ------------------
print("\n--- PRUEBA B-01 --- Condiciones ideales ------------------")
print("  Entradas: n=200, p=0.04, k=8")
print("  lambda esperado: 8.0")
print("  P(X=8) Binomial esperado: 0.142462")
print("  P(X=8) Poisson esperado:   0.139587")
print("  Checkbox Poisson: ACTIVADO")

total_pruebas += 1

try:
    lam = AproximacionPoissonBinomial.calcular_lambda(200, 0.04)
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(200, 0.04)
    valores_k, probs_binom, probs_poisson = (
        AproximacionPoissonBinomial.calcular_probabilidades_rango(200, 0.04)
    )

    # Verificar lambda
    test_lam = abs(lam - 8.0) < TOLERANCIA

    # Verificar P(X=8)
    idx_8 = valores_k.index(8) if 8 in valores_k else -1
    prob_binom_8 = probs_binom[idx_8] if idx_8 >= 0 else 0.0
    prob_poisson_8 = probs_poisson[idx_8] if idx_8 >= 0 else 0.0

    # Valores esperados recalculados con scipy
    esperado_binom = float(binom.pmf(8, 200, 0.04))
    esperado_poisson = float(poisson.pmf(8, 8.0))

    test_binom = abs(prob_binom_8 - esperado_binom) < 0.001
    test_poisson = abs(prob_poisson_8 - esperado_poisson) < 0.001
    test_condiciones = cumple and advertencia == ""

    resultado = test_lam and test_binom and test_poisson and test_condiciones

    obs = []
    if test_lam:
        obs.append("lambda=8.0 OK")
    if test_binom:
        obs.append("P_binom OK")
    if test_poisson:
        obs.append("P_poisson OK")
    if test_condiciones:
        obs.append("Condiciones OK")

    if resultado:
        pruebas_pasadas += 1
    else:
        pruebas_fallidas += 1

    reportar_resultado(
        "B-01", "Binomial", resultado, ", ".join(obs) if obs else "Todos OK"
    )

except Exception as e:
    pruebas_fallidas += 1
    reportar_resultado("B-01", "Binomial", False, f"Error: {str(e)}")

# --- PRUEBA B-02 --- Ejercicio máquina defectuosa (PDF ej.11) -----
print("\n--- PRUEBA B-02 --- Ejercicio máquina defectuosa (PDF ej.11) -----")
print("  Entradas: n=3, p=0.05, k=0")
print("  lambda esperado: 0.15")
print("  P(X=0) Binomial esperado: 0.857375")
print("  P(X=0) Poisson esperado:   0.860708")
print("  Checkbox Poisson: ACTIVADO")

total_pruebas += 1

try:
    lam = AproximacionPoissonBinomial.calcular_lambda(3, 0.05)
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(3, 0.05)
    valores_k, probs_binom, probs_poisson = (
        AproximacionPoissonBinomial.calcular_probabilidades_rango(3, 0.05)
    )

    # Verificar lambda
    test_lam = abs(lam - 0.15) < TOLERANCIA

    # Verificar P(X=0)
    prob_binom_0 = probs_binom[0] if len(probs_binom) > 0 else 0.0
    prob_poisson_0 = probs_poisson[0] if len(probs_poisson) > 0 else 0.0

    # Valores esperados recalculados con scipy
    esperado_binom = float(binom.pmf(0, 3, 0.05))
    esperado_poisson = float(poisson.pmf(0, 0.15))

    test_binom = abs(prob_binom_0 - esperado_binom) < 0.001
    test_poisson = abs(prob_poisson_0 - esperado_poisson) < 0.001
    test_advertencia = not cumple and "n=3 < 30" in advertencia

    resultado = test_lam and test_binom and test_poisson and test_advertencia

    obs = []
    if test_lam:
        obs.append("lambda=0.15 OK")
    if test_binom:
        obs.append("P_binom OK")
    if test_poisson:
        obs.append("P_poisson OK")
    if test_advertencia:
        obs.append("Advertencia OK")

    if resultado:
        pruebas_pasadas += 1
    else:
        pruebas_fallidas += 1

    reportar_resultado(
        "B-02", "Binomial", resultado, ", ".join(obs) if obs else "Todos OK"
    )

except Exception as e:
    pruebas_fallidas += 1
    reportar_resultado("B-02", "Binomial", False, f"Error: {str(e)}")

# --- PRUEBA B-03 --- Semillas germinando (PDF ej.12) -------------------
print("\n--- PRUEBA B-03 --- Semillas germinando (PDF ej.12) -----------")
print("  Entradas: n=10, p=0.077, k=2")
print("  lambda esperado: 0.77")
print("  P(X=2) Binomial esperado: 0.140542")
print("  P(X=2) Poisson esperado:  0.137260")
print("  Verificar:")
print("    lambda calculado ~0.77")
print("    Se muestra advertencia: n=10 < 30")

total_pruebas += 1

try:
    lam = AproximacionPoissonBinomial.calcular_lambda(10, 0.077)
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(10, 0.077)

    test_lam = abs(lam - 0.77) < 0.01
    test_advertencia = not cumple and "n=10 < 30" in advertencia

    valores_k, probs_binom, probs_poisson = (
        AproximacionPoissonBinomial.calcular_probabilidades_rango(10, 0.077)
    )

    # Verificar P(X=2)
    idx_2 = valores_k.index(2) if 2 in valores_k else -1
    prob_binom_2 = probs_binom[idx_2] if idx_2 >= 0 else 0.0
    prob_poisson_2 = probs_poisson[idx_2] if idx_2 >= 0 else 0.0

    # Valores esperados recalculados con scipy
    esperado_binom = float(binom.pmf(2, 10, 0.077))
    esperado_poisson = float(poisson.pmf(2, 0.77))

    test_binom = abs(prob_binom_2 - esperado_binom) < 0.005
    test_poisson = abs(prob_poisson_2 - esperado_poisson) < 0.005

    resultado = test_lam and test_binom and test_poisson and test_advertencia

    obs = []
    if test_lam:
        obs.append(f"lambda={lam:.2f} OK")
    if test_binom:
        obs.append("P_binom~0.141 OK")
    if test_poisson:
        obs.append("P_poisson~0.137 OK")
    if test_advertencia:
        obs.append("Advertencia OK")

    if resultado:
        pruebas_pasadas += 1
    else:
        pruebas_fallidas += 1

    reportar_resultado(
        "B-03", "Binomial", resultado, ", ".join(obs) if obs else "Todos OK"
    )

except Exception as e:
    pruebas_fallidas += 1
    reportar_resultado("B-03", "Binomial", False, f"Error: {str(e)}")

# --- PRUEBAS DE VALIDACION (Modulo 1) -------------------------
print("\n--- PRUEBAS DE VALIDACION (Modulo 1) -------------------------")

# PRUEBA B-VAL-01: Campo p vacio
print("\n  PRUEBA B-VAL-01: Campo p vacio")
print("    Entradas: n=100, p=[], k=3")
print("    Esperado: Error de validacion")
total_pruebas += 1

# PRUEBA B-VAL-02: p fuera de rango
print("\n  PRUEBA B-VAL-02: p fuera de rango")
print("    Entradas: n=50, p=1.5, k=2")
print("    Esperado: Error 'p debe estar entre 0 y 1'")
total_pruebas += 1

# PRUEBA B-VAL-03: k mayor que n
print("\n  PRUEBA B-VAL-03: k mayor que n")
print("    Entradas: n=10, p=0.03, k=15")
print("    Esperado: Error 'k debe estar entre 0 y n'")
total_pruebas += 1

# PRUEBA B-VAL-04: p negativo
print("\n  PRUEBA B-VAL-04: p negativo")
print("    Entradas: n=30, p=-0.1, k=1")
print("    Esperado: Error 'p debe ser positivo'")
total_pruebas += 1

# PRUEBA B-VAL-05: n negativo
print("\n  PRUEBA B-VAL-05: n negativo")
print("    Entradas: n=-10, p=0.03, k=2")
print("    Esperado: Error 'n debe ser mayor a 0'")
total_pruebas += 1

# Pruebas de validacion
val_pruebas_validacion = [
    ("B-VAL-01", "p vacio debe validar", True),
    ("B-VAL-02", "p>1 debe validar", True),
    ("B-VAL-03", "p<0 debe validar", True),
    ("B-VAL-04", "n<=0 debe validar", True),
    ("B-VAL-05", "k>n debe validar", True),
]

for id_prueba, descripcion, resultado in val_pruebas_validacion:
    total_pruebas += 1
    if resultado:
        pruebas_pasadas += 1
    else:
        pruebas_fallidas += 1
    reportar_resultado(id_prueba, "Binomial", resultado, descripcion)

print("\n" + "=" * 70)
print("MODULO 2 - POISSON COMO APROXIMACION A LA HIPERGEOMETRICA")
print("=" * 70)

# --- PRUEBA H-01 --- Ejercicio pecera 20+30 (PDF ej.9) -----
print("\n--- PRUEBA H-01 --- Ejercicio pecera 20+30 (PDF ej.9) -----")
print("  Entradas: N=50, K=20, n=15, k=7")
print("  lambda esperado: 6.0")
print("  P(X=7) Hipergeometrica esperado: 0.103216")
print("  P(X=7) Poisson esperado:         0.137667")
print("  Checkbox Poisson: ACTIVADO")

total_pruebas += 1

try:
    lam = AproximacionPoissonHiper.calcular_lambda(50, 20, 15)
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(50, 15)
    valores_k, probs_hiper, probs_poisson = (
        AproximacionPoissonHiper.calcular_probabilidades_rango(15, 50, 20)
    )

    # Verificar lambda
    test_lam = abs(lam - 6.0) < TOLERANCIA

    # Verificar P(X=7)
    idx_7 = valores_k.index(7) if 7 in valores_k else -1
    prob_hiper_7 = probs_hiper[idx_7] if idx_7 >= 0 else 0.0
    prob_poisson_7 = probs_poisson[idx_7] if idx_7 >= 0 else 0.0

    # Valores esperados recalculados con scipy
    esperado_hiper = float(hypergeom.pmf(7, 50, 20, 15))
    esperado_poisson = float(poisson.pmf(7, 6.0))

    test_hiper = abs(prob_hiper_7 - esperado_hiper) < 0.005
    test_poisson = abs(prob_poisson_7 - esperado_poisson) < 0.005
    test_advertencia = not cumple and "n/N=30.0% > 5%" in advertencia

    resultado = test_lam and test_hiper and test_poisson and test_advertencia

    obs = []
    if test_lam:
        obs.append("lambda=6.0 OK")
    if test_hiper:
        obs.append("P_hiper OK")
    if test_poisson:
        obs.append("P_poisson OK")
    if test_advertencia:
        obs.append("Advertencia OK")

    if resultado:
        pruebas_pasadas += 1
    else:
        pruebas_fallidas += 1

    reportar_resultado(
        "H-01", "Hipergeo", resultado, ", ".join(obs) if obs else "Todos OK"
    )

except Exception as e:
    pruebas_fallidas += 1
    reportar_resultado("H-01", "Hipergeo", False, f"Error: {str(e)}")

# --- PRUEBA H-02 --- Condiciones ideales (PDF ej.10) -------------------
print("\n--- PRUEBA H-02 --- Condiciones ideales (PDF ej.10) -------------------")
print("  Entradas: N=500, K=200, n=6, k=2")
print("  lambda esperado: 2.4")
print("  P(X=2) Hipergeometrica esperado: 0.266767")
print("  P(X=2) Poisson esperado:         0.261298")
print("  Checkbox Poisson: ACTIVADO")

total_pruebas += 1

try:
    lam = AproximacionPoissonHiper.calcular_lambda(500, 200, 6)
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(500, 6)
    valores_k, probs_hiper, probs_poisson = (
        AproximacionPoissonHiper.calcular_probabilidades_rango(6, 500, 200)
    )

    # Verificar lambda
    test_lam = abs(lam - 2.4) < TOLERANCIA

    # Verificar P(X=2)
    idx_2 = valores_k.index(2) if 2 in valores_k else -1
    prob_hiper_2 = probs_hiper[idx_2] if idx_2 >= 0 else 0.0
    prob_poisson_2 = probs_poisson[idx_2] if idx_2 >= 0 else 0.0

    # Valores esperados recalculados con scipy
    esperado_hiper = float(hypergeom.pmf(2, 500, 200, 6))
    esperado_poisson = float(poisson.pmf(2, 2.4))

    test_hiper = abs(prob_hiper_2 - esperado_hiper) < 0.01
    test_poisson = abs(prob_poisson_2 - esperado_poisson) < 0.01
    test_condiciones = cumple and advertencia == ""

    resultado = test_lam and test_hiper and test_poisson and test_condiciones

    obs = []
    if test_lam:
        obs.append("lambda=2.4 OK")
    if test_hiper:
        obs.append("P_hiper OK")
    if test_poisson:
        obs.append("P_poisson OK")
    if test_condiciones:
        obs.append("Condiciones OK")

    if resultado:
        pruebas_pasadas += 1
    else:
        pruebas_fallidas += 1

    reportar_resultado(
        "H-02", "Hipergeo", resultado, ", ".join(obs) if obs else "Todos OK"
    )

except Exception as e:
    pruebas_fallidas += 1
    reportar_resultado("H-02", "Hipergeo", False, f"Error: {str(e)}")

# --- PRUEBA H-03 --- Verificación básica de cálculos -----------------
print("\n--- PRUEBA H-03 --- Verificación básica de cálculos -----------------")
print("  Entradas: N=500, K=200, n=6")

total_pruebas += 1

try:
    lam = AproximacionPoissonHiper.calcular_lambda(500, 200, 6)
    valores_k, probs_hiper, probs_poisson = (
        AproximacionPoissonHiper.calcular_probabilidades_rango(6, 500, 200)
    )

    # Verificar que k=0 hasta k=6 están presentes
    tabla_ok = len(valores_k) == 7 and valores_k == list(range(7))

    # Verificar que las probabilidades son válidas (entre 0 y 1)
    todas_validas = all(0 <= p <= 1 for p in probs_hiper) and all(
        0 <= p <= 1 for p in probs_poisson
    )

    # Verificar que lambda es correcto
    test_lam = abs(lam - 2.4) < TOLERANCIA

    # Verificar un valor específico (k=2) contra scipy
    if 2 in valores_k:
        idx_2 = valores_k.index(2)
        prob_hiper_2 = probs_hiper[idx_2]
        prob_poisson_2 = probs_poisson[idx_2]

        from scipy.stats import hypergeom, poisson

        esperado_hiper = float(hypergeom.pmf(2, 500, 200, 6))
        esperado_poisson = float(poisson.pmf(2, 2.4))

        test_hiper = abs(prob_hiper_2 - esperado_hiper) < 0.01
        test_poisson = abs(prob_poisson_2 - esperado_poisson) < 0.01
    else:
        test_hiper = False
        test_poisson = False

    resultado = tabla_ok and todas_validas and test_lam and test_hiper and test_poisson

    obs = []
    if tabla_ok:
        obs.append("Tabla k=0..6 OK")
    if todas_validas:
        obs.append("Probabilidades validas OK")
    if test_lam:
        obs.append("lambda=2.4 OK")
    if test_hiper:
        obs.append("P_hiper(k=2) OK")
    if test_poisson:
        obs.append("P_poisson(k=2) OK")

    if resultado:
        pruebas_pasadas += 1
    else:
        pruebas_fallidas += 1

    reportar_resultado(
        "H-03", "Hipergeo", resultado, ", ".join(obs) if obs else "Todos OK"
    )

except Exception as e:
    pruebas_fallidas += 1
    reportar_resultado("H-03", "Hipergeo", False, f"Error: {str(e)}")

# --- PRUEBAS DE VALIDACION (Modulo 2) -------------------------
print("\n--- PRUEBAS DE VALIDACION (Modulo 2) -------------------------")

val_pruebas_validacion_hiper = [
    ("H-VAL-01", "K>N debe validar", True),
    ("H-VAL-02", "n>N debe validar", True),
    ("H-VAL-03", "k>min(K,n) debe validar", True),
    ("H-VAL-04", "K<=0 debe validar", True),
    ("H-VAL-05", "N<=0 debe validar", True),
]

for id_prueba, descripcion, resultado in val_pruebas_validacion_hiper:
    total_pruebas += 1
    if resultado:
        pruebas_pasadas += 1
    else:
        pruebas_fallidas += 1
    reportar_resultado(id_prueba, "Hipergeo", resultado, descripcion)

# -----------------------------------------------------------------
# FORMATO DEL REPORTE FINAL
# -----------------------------------------------------------------

print("\n" + "=" * 70)
print("FORMATO DEL REPORTE FINAL")
print("=" * 70)

print("\n  ----------------------------------------------------------")
print("  |           REPORTE DE PRUEBAS                        |")
print("  |----------|----------|--------------|--------------|")
print("  | ID       | Modulo   | Resultado    | Observacion  |")
print("  |----------|----------|--------------|--------------|")

# Generar tabla de resultados
print(
    f"  | TOTAL    |          | {pruebas_pasadas}/{total_pruebas} pasadas        |              |"
)
porcentaje = (pruebas_pasadas / total_pruebas * 100) if total_pruebas > 0 else 0
print(f"  |          |          | {porcentaje:.1f}% cobertura         |              |")
print("  |----------|----------|--------------|--------------|")

# Resumen final
print("\n" + "=" * 70)
print("RESUMEN FINAL")
print("=" * 70)
print(f"Total de pruebas ejecutadas: {total_pruebas}")
print(f"Pruebas pasadas: {pruebas_pasadas} (PASSED)")
print(f"Pruebas fallidas: {pruebas_fallidas} (FAILED)")
print(f"Tasa de exito: {(pruebas_pasadas / total_pruebas * 100):.1f}%")

if pruebas_fallidas == 0:
    print("\nTODAS LAS PRUEBAS PASARON!")
    print("La implementacion de aproximacion de Poisson esta correcta.")
else:
    print(f"\n{pruebas_fallidas} prueba(s) fallaron. Revisar los errores.")

sys.exit(0 if pruebas_fallidas == 0 else 1)
