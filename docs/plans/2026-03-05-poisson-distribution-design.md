# Design: Distribución de Poisson

**Date:** 2026-03-05
**Status:** Approved

## Overview

Add a new "Distribución de Poisson" option to the existing statistical distributions calculator. The Poisson distribution will be available as an approximation to the Binomial distribution when certain conditions are met.

## Architecture

### Files to Modify/Create

| File | Change |
|------|--------|
| `gui/dashboard.py` | Add "Poisson" button and `crear_interfaz_poisson()` method |
| `gui/campos_entrada.py` | Add `CamposEntradaPoisson` class |
| `utils/calculos.py` | Add Poisson calculation functions |
| `utils/validaciones.py` | Add `validar_parametros_poisson()` function |
| `utils/__init__.py` | Export new functions |
| `gui/grafico.py` | Add `crear_grafico_poisson()` method |
| `gui/area_resultados.py` | Add `mostrar_resultados_poisson()` method |
| `ventana_principal.py` | Add `calcular_poisson()` method |

### Data Flow

```
User inputs (n, p, x) → Validación condiciones → 
Si falla: Error "Usar Binomial"
Si pasa: Cálculos Poisson → Resultados + Gráfica
```

## Input Fields

### Class: `CamposEntradaPoisson`

Location: `gui/campos_entrada.py`

```python
class CamposEntradaPoisson(ctk.CTkFrame):
    def __init__(self, master, **kwargs)
    def crear_campos(self) -> None
    def obtener_valores(self) -> dict
    def limpiar(self) -> None
```

### Input Fields

| Field | Type | Label | Placeholder |
|-------|------|-------|-------------|
| `n_entry` | CTkEntry | "Número de ensayos (n):" | "Ej: 100" |
| `p_entry` | CTkEntry | "Probabilidad de éxito (p):" | "Ej: 0.05" |
| `x_entry` | CTkEntry | "Valores de X (separados por coma):" | "Ej: 0, 1, 2, 3" |

### Probability Field Conversion

The `p` field accepts two formats:

| Input | Converted To | Example |
|-------|--------------|---------|
| Value >= 1 | Divide by 100 | 89 → 0.89, 90.2 → 0.902 |
| Value < 1 | Use as-is | 0.05 → 0.05, 0.2 → 0.2 |

## Validation

### Condition Validation

Location: `utils/validaciones.py`

```python
def validar_condiciones_poisson(n: int, p: float) -> tuple[bool, str]:
    """
    Valida que se cumplan las condiciones para usar Poisson:
    - p < 0.10
    - λ = n × p < 10
    
    Returns:
        (cumple_condiciones, mensaje_error)
    """
```

### Validation Flow

1. Convert p (if p >= 1, divide by 100)
2. Check: p < 0.10 ?
   - No → Error
3. Calculate λ = n × p
4. Check: λ < 10 ?
   - No → Error
5. Both pass → Return (True, "")

### Error Message (when conditions fail)

```
"Las condiciones no se cumplen. Este problema debe resolverse 
mediante Distribución Binomial.

Condiciones requeridas:
• p < 0.10 (actual: {p})
• λ < 10 (actual: {λ})"
```

## Calculations

### Functions to Add

Location: `utils/calculos.py`

| Function | Formula | Description |
|----------|---------|-------------|
| `poisson_pmf(k, lam)` | (e^(-λ) × λ^k) / k! | Probabilidad P(X=k) |
| `calcular_media_poisson(n, p)` | n × p | Media λ |
| `calcular_desviacion_poisson(lam)` | √λ | Desviación estándar |
| `calcular_curtosis_poisson(lam)` | 1 / λ | Curtosis |
| `calcular_sesgo_poisson(lam)` | 1 / √λ | Sesgo |
| `calcular_probabilidades_poisson(valores_x, lam)` | Vectorized PMF | Lista de probabilidades |

### Implementation

```python
def poisson_pmf(k: int, lam: float) -> float:
    """
    Calcula P(X=k) para distribución de Poisson.
    Fórmula: P(X=k) = (e^(-λ) × λ^k) / k!
    
    Args:
        k: Número de éxitos
        lam: Parámetro λ (media)
    Returns:
        Probabilidad de exactamente k éxitos
    """
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)
```

### Interpretation

- **Curtosis**: Always positive (1/λ > 0) → "Leptocúrtica"
- **Sesgo**: Always positive (1/√λ > 0) → "Sesgo positivo: Media > Mediana"

## Graph

### Method: `crear_grafico_poisson()`

Location: `gui/grafico.py`

### Specifications

| Element | Specification |
|---------|---------------|
| Type | Bar chart |
| X-axis | Valores de X ingresados |
| Y-axis | Probabilidades P(X=k) |
| Title | "Distribución de Poisson" |
| Background | `#2b2b2b` (dark theme) |
| Bar color | `#27ae60` (green) |
| Highlight color | `#e74c3c` (red) |
| Normal curve | `#f39c12` (orange) |
| Grid | `#444444` |

### Features

1. Bars: One bar per X value with probability height
2. Normal curve overlay: Reference distribution
3. Media indicator: Vertical line at λ
4. Value labels: Probability value on top of each bar

### Color Scheme

| Distribution | Bar Color |
|--------------|-----------|
| Binomial | `#3b8ed0` (blue) |
| Hypergeometric | `#9b59b6` (purple) |
| Poisson | `#27ae60` (green) |

## Results Display

### Method: `mostrar_resultados_poisson(datos)`

Location: `gui/area_resultados.py`

### Data Structure

```python
datos = {
    "n": int,
    "p": float,
    "lambda": float,
    "valores_x": list[int],
    "probabilidades": list[float],
    "media": float,
    "desviacion": float,
    "curtosis": float,
    "interpretacion_curtosis": str,
    "sesgo": float,
    "interpretacion_sesgo": str
}
```

### Display Sections

| Section | Content |
|---------|---------|
| **Parámetros** | n, p, λ (lambda) |
| **Tabla de Probabilidades** | X \| P(X=k) |
| **Estadísticas** | Media (λ), Desviación estándar (σ) |
| **Forma** | Curtosis + "Leptocúrtica", Sesgo + "Sesgo positivo" |

## Orchestration

### Method: `calcular_poisson()`

Location: `ventana_principal.py`

### Calculation Flow

1. Obtener valores de CamposEntradaPoisson
2. Validar que n, p, x no estén vacíos
3. Normalizar p (si p >= 1, dividir entre 100)
4. Parsear valores_x (separados por coma)
5. Validar condiciones Poisson (p < 0.10 y λ < 10)
6. Si falla: Error "Usar Distribución Binomial"
7. Si pasa: Calcular λ = n × p
8. Calcular probabilidades para cada X
9. Calcular estadísticas (σ, curtosis, sesgo)
10. Mostrar resultados en AreaResultados
11. Generar gráfica en GraficoBinomial

## Dashboard Integration

### Sidebar Button

Location: `gui/dashboard.py`

```python
# In crear_sidebar()
self.btn_poisson = self.crear_boton_sidebar("Poisson", "poisson", False)

# In cargar_distribucion()
elif distribucion == "poisson":
    self.crear_interfaz_poisson()

# In actualizar_botones_sidebar()
"poisson": self.btn_poisson
```

### Interface Creation

```python
def crear_interfaz_poisson(self):
    self.limpiar_contenido()
    self.campos = CamposEntradaPoisson(self.frame_contenido)
    self.campos.pack(...)
    self.btn_calcular.configure(command=self.master.calcular_poisson)
```
