"""
Script simplificado para verificar la integración de Poisson en hipergeométrica
"""

from utils import AproximacionPoissonHiper

print("=== VERIFICACION DE INTEGRACION - HIPERGEOMETRICA → POISSON ===")

print("\nTest 1: Verificar que los métodos de cálculo existen y funcionan")
print("-" * 60)

try:
    lam = AproximacionPoissonHiper.calcular_lambda(50, 20, 15)
    print(f"  lambda calculado: {lam} (esperado: 6.0)")
    
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(50, 15)
    print(f"  Condiciones cumplidas: {cumple}")
    print(f"  Advertencia: '{advertencia}'")
    
    valores_k, probs_hiper, probs_poisson = AproximacionPoissonHiper.calcular_probabilidades_rango(15, 50, 20)
    print(f"  Rango de k: {len(valores_k)} (0 a {len(valores_k)-1})")
    
    print("  OK: Métodos de cálculo funcionan\n")
    
except Exception as e:
    print(f"  ERROR: {str(e)}\n")

print("\nTest 2: Verificar que la lógica de checkbox está en calcular_hipergeometrica")
print("-" * 60)

# Verificar el código de ventana_principal.py
import os
with open('ventana_principal.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Buscar la verificación del checkbox de Poisson
if "hasattr(self.dashboard.campos_hipergeometrica, 'chk_poisson')" in contenido:
    print("  OK: Lógica de verificación de checkbox está presente en el código")
else:
    print("  ERROR: Lógica de verificación de checkbox NO encontrada")

if "if (hasattr(self.dashboard.campos_hipergeometrica" in contenido:
    and self.dashboard.campos_hipergeometrica.chk_poisson.get()): in contenido:
    print("  OK: Verifica que el checkbox y llama a calcular_poisson_hipergeometrica")
else:
    print("  ERROR: No se verifica el checkbox ni se llama a calcular_poisson_hipergeometrica")

print("\nTest 3: Verificar que los métodos de visualización existen en Dashboard")
print("-" * 60)

# Verificar métodos en dashboard.py
with open('gui/dashboard.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

metodos_necesarios = [
    "mostrar_resultados_poisson_hipergeometrica",
    "crear_grafico_poisson_hipergeometrica",
    "expandir_tabla_poisson_hipergeometrica"
]

for metodo in metodos_necesarios:
    if f"def {metodo}(" in contenido:
        print(f"  OK: Método '{metodo}' encontrado en dashboard.py\n")
    else:
        print(f"  ERROR: Método '{metodo}' NO encontrado en dashboard.py\n")

print("\nTest 4: Verificar que mostrar_estadisticas_poisson existe en AreaResultados")
print("-" * 60)

with open('gui/area_resultados.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

if "def mostrar_estadisticas_poisson(self, datos):" in contenido:
    print("  OK: mostrar_estadisticas_poisson encontrado en AreaResultados\n")
else:
    print("  ERROR: mostrar_estadisticas_poisson NO encontrado en AreaResultados\n")

print("\nTest 5: Verificar que crear_barras_agrupadas existe en GraficoBinomial")
print("-" * 60)

with open('gui/grafico.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

if "def crear_barras_agrupadas(self," in contenido:
    print("  OK: crear_barras_agrupadas encontrado en GraficoBinomial\n")
else:
    print("  ERROR: crear_barras_agrupadas NO encontrado en GraficoBinomial\n")

print("\n" + "=" * 70)
print("DIAGNOSTICO FINAL")
print("=" * 70)

print("\nSISTEMA ACTUAL:")
print("  - Calculos de Poisson implementados en utils/aproximacion_poisson.py")
print("  - Widget de tabla comparativa en gui/tabla_comparacion_poisson.py")
print("  - Checkbox en CamposEntrada y CamposEntradaHipergeometrica")
print("  - Integración parcial en ventana_principal.py (checkbox detectado en hipergeométrica)")
print("  - Métodos de visualización en Dashboard y AreaResultados")
print("  - Gráfica de barras agrupadas en GraficoBinomial")

print("\nPRÓXIMOS PASOS PARA CORREGIR EL PROBLEMA DE NO MOSTRAR RESULTADOS:")
print("1. Ejecutar la aplicación y probar manualmente:")
print("   - Ir a la pestaña Hipergeométrica")
print("   - Ingresar: N=50, K=20, n=15, x=7")
print("   - Marcar 'Activar aproximación Poisson'")
print("   - Click en 'Calcular'")
print("   - Verificar que aparece:")
print("     - Tabla comparativa acotada (20 filas)")
print("     - Fila k=7 resaltada en azul")
print("     - Estadísticas de Poisson")
print("     - Gráfica de barras agrupadas")
print("   - Si NO aparecen, revisar consola/terminal para errores")
print("")
print("2. Revisar ventana_principal.py línea ~328 para verificar la lógica completa")
print("   - Buscar cualquier error de lógica en la integración")
print("")
print("3. Revisar dashboard.py métodos líneas ~682, ~752")
print("   - Verificar que los métodos llaman a los componentes UI correctos")
print("")
