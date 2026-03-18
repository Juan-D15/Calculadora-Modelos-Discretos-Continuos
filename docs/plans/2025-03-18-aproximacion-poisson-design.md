# Diseño: Aproximación de Poisson para Binomial e Hipergeométrica

**Fecha:** 2025-03-18
**Estado:** Aprobado
**Autor:** OpenCode

## Resumen

Implementar dos módulos de aproximación de Poisson para las distribuciones Binomial e Hipergeométrica en la Calculadora de Distribuciones. Los módulos permitirán comparar las probabilidades exactas con la aproximación de Poisson, mostrando tablas comparativas y gráficas de barras agrupadas.

## Objetivos

1. Implementar cálculo de aproximación Binomial → Poisson
2. Implementar cálculo de aproximación Hipergeométrica → Poisson
3. Mostrar tabla comparativa acotada (20 filas) con opción de expansión
4. Generar gráfica de barras agrupadas para todo el rango
5. Validar condiciones de aproximación y mostrar advertencias

## Requerimientos Funcionales

### Módulo 1: Binomial ≈ Poisson

**Entradas:**
- n: número de ensayos (entero positivo)
- p: probabilidad de éxito (0 < p < 1)
- k: valor específico de X (0 ≤ k ≤ n)

**Condiciones de aproximación:**
- n ≥ 30
- p ≤ 0.05
- λ = n × p

**Salidas:**
- λ calculado
- Tabla comparativa (k, P_binom, P_poisson)
- P(X=k) exacto en ambas distribuciones
- Media (λ), Varianza (λ), Desviación estándar (√λ)
- Gráfica de barras agrupadas (rango completo 0 a n)

### Módulo 2: Hipergeométrica ≈ Poisson

**Entradas:**
- N: tamaño de población (entero positivo)
- K: elementos de interés en población (K ≤ N)
- n: tamaño de muestra (n ≤ N)
- k: valor específico (0 ≤ k ≤ min(K, n))

**Condiciones de aproximación:**
- N ≥ 50
- n/N ≤ 0.05
- λ = n × (K/N) = n × p

**Salidas:**
- λ calculado
- Tabla comparativa (k, P_hiper, P_poisson)
- P(X=k) exacto en ambas distribuciones
- Media (λ), Varianza (λ), Desviación estándar (√λ)
- Gráfica de barras agrupadas (rango completo 0 a min(K, n))

## Requerimientos UI/UX

### Comportamiento del Checkbox
- Cuando está DESACTIVADO: solo se muestra la tabla de la distribución original
- Cuando está ACTIVADO: se muestra tabla comparativa paralela y gráfica comparativa
- Advertencia visual (no bloqueo) si no se cumplen condiciones ideales
- Checkbox ubicado en tabs Binomial e Hipergeométrica existentes

### Tabla Comparativa
- Muestra máximo 20 filas inicialmente
- Filas centradas en el valor k ingresado por el usuario
- Fila destacada con color azul para el k ingresado
- Botón "Ver tabla completa" para expandir
- Scroll nativo para visualización completa

### Gráfica Comparativa
- Barras agrupadas lado a lado
- Muestra rango completo (0 a n o 0 a min(K, n))
- Dos series: distribución original y Poisson
- Barra destacada para el valor k ingresado

## Arquitectura

### Estructura de Archivos

**Nuevos archivos:**
```
utils/
  └── aproximacion_poisson.py       # Lógica de cálculo para ambas aproximaciones

gui/
  └── tabla_comparacion_poisson.py  # Widget de tabla comparativa acotada
```

**Archivos modificados:**
```
ventana_principal.py                # Añadir métodos de cálculo de aproximación
gui/campos_entrada.py               # Añadir checkbox de aproximación
gui/area_resultados.py              # Añadir método para mostrar tabla comparativa
gui/grafico.py                      # Añadir método para graficar barras agrupadas
utils/__init__.py                   # Exportar nuevas funciones
```

### Componentes

#### 1. `utils/aproximacion_poisson.py`

Contiene dos clases principales:

**AproximacionPoissonBinomial**
- `calcular_lambda(n, p)`: Retorna n × p
- `validar_condiciones(n, p)`: Valida n≥30, p≤0.05, retorna advertencia si no cumple
- `calcular_probabilidades_rango(n, p)`: Calcula P(X=k) para k=0..n en ambas distribuciones
- `calcular_estadisticas(n, p)`: Retorna media, varianza, desviación de Poisson

**AproximacionPoissonHiper**
- `calcular_lambda(N, K, n)`: Retorna n × (K/N)
- `validar_condiciones(N, n)`: Valida N≥50, n/N≤0.05
- `calcular_probabilidades_rango(n, N, K)`: Calcula para k=0..min(K, n)
- `calcular_estadisticas(n, N, K)`: Retorna estadísticas de Poisson

#### 2. `gui/tabla_comparacion_poisson.py`

**Clase TablaComparacionPoisson(ctk.CTkFrame)**
- `mostrar_tabla_acotada()`: Muestra máximo 20 filas centradas en k_ingresado
- `mostrar_tabla_completa()`: Muestra todas las filas del rango
- `_render_filas()`: Renderiza filas con destacado para k_ingresado
- `expandir_tabla()`: Callback para expansión

#### 3. Modificaciones en archivos existentes

**ventana_principal.py**
- `calcular_poisson_binomial()`: Calcula aproximación cuando checkbox activado
- `calcular_poisson_hipergeometrica()`: Idem para hipergeométrica
- Modificar `calcular_desde_dashboard()` y `calcular_hipergeometrica()` para verificar checkbox

**gui/campos_entrada.py**
- Añadir `self.chk_poisson` en CamposEntrada y CamposEntradaHipergeometrica
- Método `on_poisson_toggle()` para recalcular al cambiar estado

**gui/area_resultados.py**
- `mostrar_resultados_poisson_binomial()`: Mostrar λ, estadísticas, tabla, advertencia
- `mostrar_resultados_poisson_hipergeometrica()`: Idem para hipergeométrica

**gui/grafico.py**
- `crear_grafico_barras_agrupadas()`: Generar gráfica comparativa con barras lado a lado

## Flujo de Datos

### Para Binomial → Poisson

1. Usuario ingresa n, p, k y activa checkbox
2. `calcular_desde_dashboard()` detecta checkbox activado
3. `calcular_poisson_binomial()` es llamado
4. `AproximacionPoissonBinomial.validar_condiciones()` verifica (n≥30, p≤0.05)
5. Si no cumple: muestra advertencia, continua
6. `calcular_probabilidades_rango()` genera arrays completos (k=0..n)
7. `calcular_estadisticas()` calcula media, varianza, desviación (Poisson)
8. Datos pasados a Dashboard
9. Dashboard muestra tabla acotada (20 filas) y gráfica completa

### Para Hipergeométrica → Poisson

1. Usuario ingresa N, K, n, k y activa checkbox
2. `calcular_hipergeometrica()` detecta checkbox activado
3. `calcular_poisson_hipergeometrica()` es llamado
4. `AproximacionPoissonHiper.validar_condiciones()` verifica (N≥50, n/N≤0.05)
5. Si no cumple: muestra advertencia, continua
6. `calcular_probabilidades_rango()` genera arrays (k=0..min(K, n))
7. `calcular_estadisticas()` calcula estadísticas (Poisson)
8. Datos pasados a Dashboard
9. Dashboard muestra tabla acotada y gráfica completa

## Fórmulas Matemáticas

### Binomial
- P(X=k) = C(n,k) × p^k × (1-p)^(n-k)
- λ = n × p

### Poisson
- P(X=k) = (e^(-λ) × λ^k) / k!
- Media = λ
- Varianza = λ
- Desviación estándar = √λ

### Hipergeométrica
- P(X=k) = [C(K,k)×C(N-K,n-k)] / C(N,n)
- λ = n × (K/N) = n × p

## Validaciones

### Módulo Binomial → Poisson
- n debe ser entero positivo
- 0 < p < 1
- 0 ≤ k ≤ n
- Advertencia si n < 30 o p > 0.05 (no bloqueo)

### Módulo Hipergeométrica → Poisson
- N, K, n enteros positivos
- K ≤ N, n ≤ N
- 0 ≤ k ≤ min(K, n)
- Advertencia si N < 50 o n/N > 0.05 (no bloqueo)

## Casos de Prueba

### Módulo Binomial → Poisson
- Caso A: n=200, p=0.4, k=5 → λ=80 (NO ideal, p>0.05, mostrar advertencia)
- Caso B: n=1000, p=0.02, k=15 → λ=20 (ideal, n≥30, p≤0.05)
- Caso C: n=10, p=0.03, k=2 → λ=0.3 (NO ideal, n<30, mostrar advertencia)

### Módulo Hipergeométrica → Poisson
- Caso A: N=50, K=20, n=15, k=7 → λ=6 (ideal)
- Caso B: N=30, K=10, n=5, k=2 → λ≈1.67 (NO ideal, N<50)
- Caso C: N=1000, K=100, n=100, k=20 → λ=10 (NO ideal, n/N=10% > 5%)

## Manejo de Errores

- Validaciones antes de cálculo
- `try-except` para capturar errores de cálculo
- Mensajes de error en español vía `messagebox.showerror()`
- Advertencias vía `messagebox.showwarning()` (no bloqueantes)

## Consideraciones de Rendimiento

- Para n grande (ej. n=1000), calcular probabilidades solo una vez y reutilizar
- Tabla acotada mejora rendimiento de UI
- Gráfica completa puede usar sub-sampling si n > 200 para mejorar rendimiento
- Usar funciones vectorizadas (NumPy/SciPy) cuando sea posible

## Limite de Rango Acotado

- Mostrar máximo 20 filas inicialmente
- Centrar en k_ingresado si existe
- Si k_ingresado está cerca de los bordes, ajustar rango
- Botón "Ver tabla completa" expande a todas las filas

## Próximos Pasos

1. Implementar módulo `aproximacion_poisson.py`
2. Implementar widget `TablaComparacionPoisson`
3. Modificar `campos_entrada.py` para añadir checkbox
4. Modificar `ventana_principal.py` para integrar cálculos
5. Modificar `area_resultados.py` para mostrar resultados
6. Modificar `grafico.py` para generar gráficas agrupadas
7. Actualizar `utils/__init__.py` para exportar nuevas funciones
8. Crear pruebas unitarias para cálculos
9. Crear pruebas de integración para UI
10. Documentación de usuario
