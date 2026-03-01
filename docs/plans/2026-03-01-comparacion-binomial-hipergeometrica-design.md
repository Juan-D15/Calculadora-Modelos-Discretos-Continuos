# Diseño: Comparación Binomial vs Hipergeométrica

**Fecha:** 2026-03-01

## Resumen

Agregar funcionalidad de comparación entre distribuciones Binomial e Hipergeométrica mediante un checkbox en la interfaz binomial existente. Permite calcular ambas distribuciones en paralelo, mostrar tablas comparativas con probabilidades acumuladas, y graficar resultados.

## Requisitos

1. Checkbox "Comparar con Hipergeométrica" en interfaz binomial
2. Campos dinámicos: N (población) y Tolerancia (%) al activar checkbox
3. Cálculo automático de K = p × N (redondeado)
4. Validación de condición 20% (muestra ≥ 20% de población)
5. Tabla con toggle entre distribuciones: X | P(x) | P Acumulada
6. Resaltado de fila más cercana al % de tolerancia
7. Mensaje indicando valor encontrado para tolerancia
8. Gráficas con toggle: P(x) vs P Acumulada
9. Soporte para población finita e infinita (N vacío/0 = infinita)

## Arquitectura

### Enfoque: Extender CamposEntrada

Modificar componentes existentes en lugar de crear nuevos módulos principales.

### Archivos a Modificar

| Archivo | Cambios |
|---------|---------|
| `gui/campos_entrada.py` | Checkbox comparación, campos N y tolerancia dinámicos |
| `gui/area_resultados.py` | Integrar tabla con toggle y mensaje tolerancia |
| `gui/grafico.py` | Toggle para gráfica P(x) / P acumulada |
| `ventana_principal.py` | Nuevo método `calcular_comparacion()` |
| `utils/validaciones.py` | Validaciones para modo comparación |

### Archivo Nuevo

| Archivo | Propósito |
|---------|-----------|
| `gui/tabla_comparacion.py` | Componente de tabla con toggle entre distribuciones |

## Flujo de Datos

```
Usuario activa checkbox
    ↓
Aparecen campos N y Tolerancia
    ↓
Usuario completa n, p, x, N, tolerancia
    ↓
Click en Calcular
    ↓
1. Validar entrada
2. Calcular K = round(p × N)
3. Verificar condición 20%
   - Si n < 20% × N: mostrar advertencia (permitir continuar)
4. Calcular Binomial (P(x) y P acumulada)
5. Calcular Hipergeométrica (P(x) y P acumulada)
6. Buscar valor más cercano a tolerancia en cada distribución
7. Mostrar resultados:
   - Tabla con toggle
   - Gráfica con toggle
   - Mensaje de tolerancia con fila resaltada
```

## Componentes

### 1. CamposEntrada (modificación)

**Nuevos elementos:**
- `checkbox_comparacion`: CTkCheckBox
- `frame_comparacion`: CTkFrame (oculto por defecto)
- `entry_n_poblacion`: CTkEntry
- `entry_tolerancia`: CTkEntry (default: 95)

**Nuevos métodos:**
- `toggle_campos_comparacion()`: Muestra/oculta campos adicionales
- `obtener_valores()`: Retorna N y tolerancia cuando checkbox activo

### 2. TablaComparacion (nuevo)

```python
class TablaComparacion:
    def __init__(self, frame):
        self.toggle = CTkSegmentedButton(["Binomial", "Hipergeométrica"])
        self.tabla = CTkTextbox  # Formato tabla
        self.mensaje = CTkLabel
    
    def mostrar(datos_binomial, datos_hipergeometrica, tolerancia):
        # Mostrar tabla de distribución seleccionada
        # Resaltar fila más cercana a tolerancia
        # Mostrar mensaje de resultado
```

### 3. GraficoBinomial (modificación)

**Nuevos elementos:**
- `toggle_grafica`: CTkSegmentedButton(["P(x)", "P Acumulada"])

**Nuevos métodos:**
- `crear_grafico_acumulada()`: Gráfica de línea para probabilidad acumulada

### 4. VentanaPrincipal (modificación)

**Nuevo método:**
```python
def calcular_comparacion(self):
    # 1. Obtener n, p, x, N, tolerancia del dashboard
    # 2. Validar parámetros
    # 3. Calcular K = round(p * N)
    # 4. Verificar condición 20%
    # 5. Calcular probabilidades binomial
    # 6. Calcular probabilidades hipergeométrica
    # 7. Buscar valor más cercano a tolerancia
    # 8. Pasar datos a dashboard.mostrar_comparacion()
```

## Validaciones

### Población

| Condición | Resultado |
|-----------|-----------|
| N vacío o 0 | Población infinita |
| N > 0 | Población finita |
| n ≤ 5% × N | Se considera infinita (sin corrección) |
| n > 5% × N | Población finita (con corrección) |

### Muestra para Hipergeométrica

| Condición | Resultado |
|-----------|-----------|
| n < 20% × N | Advertencia: "Se recomienda usar solo Binomial" |
| n ≥ 20% × N | Cálculo normal de hipergeométrica |

### Valores de X

| Distribución | Restricción |
|--------------|-------------|
| Binomial | 0 ≤ x ≤ n |
| Hipergeométrica | 0 ≤ x ≤ min(n, K) |

### Tolerancia

| Condición | Resultado |
|-----------|-----------|
| Vacío | Usar default 95% |
| < 0 o > 100 | Error: "Tolerancia debe estar entre 0 y 100" |

## Manejo de Errores

```python
# Errores de validación
if checkbox_activo and N is None:
    return "Ingrese el tamaño de población (N) para comparación"

K = round(p * N)
if K <= 0 or K > N:
    return f"K calculado ({K}) es inválido para N={N}"

# Advertencias (no bloquean)
if n < 0.20 * N:
    advertencia = "La muestra no alcanza 20% de la población. Se recomienda usar solo Binomial."
```

## Estrategia de Pruebas

### Pruebas Unitarias

**`tests/test_calculos.py`:**
- `test_es_poblacion_infinita_none()`
- `test_es_poblacion_infinita_menor_5porciento()`
- `test_es_poblacion_infinita_mayor_5porciento()`
- `test_calcular_probabilidad_acumulada_binomial()`
- `test_calcular_probabilidad_acumulada_hipergeometrica()`
- `test_buscar_valor_tolerancia()`

**`tests/test_validaciones.py`:**
- `test_validar_parametros_comparacion_n_obligatorio()`
- `test_validar_tolerancia_rango()`
- `test_validar_x_hipergeometrica_limite()`

### Pruebas de Integración (Manuales)

| Caso | Pasos | Resultado Esperado |
|------|-------|-------------------|
| Modo normal | Calcular sin checkbox | Comportamiento actual sin cambios |
| Población infinita | Checkbox + N vacío | Error: N obligatorio |
| Muestra < 20% | Checkbox + n < 20% × N | Advertencia + cálculo completo |
| Muestra ≥ 20% | Checkbox + n ≥ 20% × N | Cálculo sin advertencia |
| Toggle tabla | Click en toggle | Cambia entre Binomial/Hipergeométrica |
| Toggle gráfica | Click en toggle | Cambia entre P(x)/P acumulada |
| Tolerancia | Ingresar 90% | Fila resaltada + mensaje correcto |

## Consideraciones de Implementación

1. **Compatibilidad:** El modo binomial normal (sin checkbox) debe funcionar exactamente igual que antes
2. **Rendimiento:** Calcular ambas distribuciones puede ser costoso para n grande, considerar límite
3. **UI:** Usar `CTkSegmentedButton` para toggles (consistente con diseño actual)
4. **Colores:** Mantener paleta actual (#3b8ed0 para binomial, #9b59b6 para hipergeométrica)

## Dependencias

Sin nuevas dependencias. Se usa CustomTkinter y Matplotlib existentes.
