# Aproximación de Poisson Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement Poisson approximation modules for Binomial and Hypergeometric distributions with comparative tables and grouped bar charts.

**Architecture:** Separate calculation modules in `utils/aproximacion_poisson.py` with UI components in `gui/tabla_comparacion_poisson.py`, integrated into existing dashboard via checkbox toggle. Modular, testable, reusing existing scipy/math infrastructure.

**Tech Stack:** Python, CustomTkinter, Matplotlib, NumPy, SciPy, pytest for testing.

---

## Task 1: Create Poisson Calculation Module

**Files:**
- Create: `utils/aproximacion_poisson.py`
- Test: `tests/test_aproximacion_poisson.py`

**Step 1: Write failing tests for AproximacionPoissonBinomial**

```python
# tests/test_aproximacion_poisson.py
import pytest
import math
from utils.aproximacion_poisson import AproximacionPoissonBinomial

def test_calcular_lambda():
    """Test lambda calculation for Poisson approximation"""
    result = AproximacionPoissonBinomial.calcular_lambda(100, 0.05)
    assert result == 5.0  # 100 * 0.05

def test_calcular_lambda_edge_case():
    """Test lambda with extreme values"""
    result = AproximacionPoissonBinomial.calcular_lambda(1000, 0.001)
    assert result == 1.0  # 1000 * 0.001

def test_validar_condiciones_ideal():
    """Test validation with ideal conditions"""
    cumple, mensaje = AproximacionPoissonBinomial.validar_condiciones(100, 0.03)
    assert cumple is True
    assert mensaje == ""

def test_validar_condiciones_n_menor_30():
    """Test validation when n < 30"""
    cumple, mensaje = AproximacionPoissonBinomial.validar_condiciones(20, 0.03)
    assert cumple is False
    assert "n=20 < 30" in mensaje

def test_validar_condiciones_p_mayor_0_05():
    """Test validation when p > 0.05"""
    cumple, mensaje = AproximacionPoissonBinomial.validar_condiciones(100, 0.10)
    assert cumple is False
    assert "p=0.1000 > 0.05" in mensaje

def test_validar_condiciones_ambos_falla():
    """Test validation when both conditions fail"""
    cumple, mensaje = AproximacionPoissonBinomial.validar_condiciones(10, 0.10)
    assert cumple is False
    assert "n=10 < 30" in mensaje
    assert "p=0.1000 > 0.05" in mensaje

def test_calcular_probabilidades_rango():
    """Test probability calculations for range"""
    n, p = 10, 0.5
    valores_k, probs_binom, probs_poisson = \
        AproximacionPoissonBinomial.calcular_probabilidades_rango(n, p)
    
    assert len(valores_k) == 11  # 0 to 10
    assert valores_k == list(range(11))
    assert len(probs_binom) == 11
    assert len(probs_poisson) == 11
    assert all(0 <= prob <= 1 for prob in probs_binom)
    assert all(0 <= prob <= 1 for prob in probs_poisson)

def test_calcular_estadisticas():
    """Test statistics calculation"""
    media, varianza, desviacion = \
        AproximacionPoissonBinomial.calcular_estadisticas(100, 0.05)
    
    assert media == 5.0  # lambda
    assert varianza == 5.0  # lambda
    assert desviacion == math.sqrt(5.0)
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_aproximacion_poisson.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'utils.aproximacion_poisson'"

**Step 3: Write minimal implementation of AproximacionPoissonBinomial**

```python
# utils/aproximacion_poisson.py
"""
Módulo de aproximación de Poisson para distribuciones Binomial e Hipergeométrica
"""
import math
from utils.calculos import binomial_pmf, poisson_pmf, hipergeometrica_pmf


class AproximacionPoissonBinomial:
    """Maneja aproximación Binomial → Poisson"""
    
    @staticmethod
    def calcular_lambda(n: int, p: float) -> float:
        """
        Calcula λ = n × p para aproximación de Poisson
        
        Args:
            n (int): Número de ensayos
            p (float): Probabilidad de éxito
            
        Returns:
            float: Parámetro λ
        """
        return n * p
    
    @staticmethod
    def validar_condiciones(n: int, p: float) -> tuple[bool, str]:
        """
        Valida condiciones ideales para aproximación Binomial → Poisson
        
        Condiciones: n ≥ 30 y p ≤ 0.05
        
        Args:
            n (int): Número de ensayos
            p (float): Probabilidad de éxito
            
        Returns:
            tuple: (cumple: bool, mensaje_advertencia: str)
        """
        condiciones = []
        
        if n < 30:
            condiciones.append(f"n={n} < 30")
        
        if p > 0.05:
            condiciones.append(f"p={p:.4f} > 0.05")
        
        if condiciones:
            mensaje = f"Advertencia: {', '.join(condiciones)}. Condiciones ideales: n≥30 y p≤0.05"
            return False, mensaje
        
        return True, ""
    
    @staticmethod
    def calcular_probabilidades_rango(n: int, p: float) -> tuple[list[int], list[float], list[float]]:
        """
        Calcula P(X=k) para todo k=0..n en ambas distribuciones
        
        Args:
            n (int): Número de ensayos
            p (float): Probabilidad de éxito
            
        Returns:
            tuple: (valores_k, probs_binom, probs_poisson)
        """
        valores_k = list(range(n + 1))
        probs_binom = [binomial_pmf(k, n, p) for k in valores_k]
        lam = n * p
        probs_poisson = [poisson_pmf(k, lam) for k in valores_k]
        
        return valores_k, probs_binom, probs_poisson
    
    @staticmethod
    def calcular_estadisticas(n: int, p: float) -> tuple[float, float, float]:
        """
        Calcula estadísticas de distribución de Poisson
        
        Fórmulas: Media = λ, Varianza = λ, Desviación = √λ
        
        Args:
            n (int): Número de ensayos
            p (float): Probabilidad de éxito
            
        Returns:
            tuple: (media, varianza, desviacion)
        """
        lam = n * p
        media = lam
        varianza = lam
        desviacion = math.sqrt(lam)
        
        return media, varianza, desviacion
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_aproximacion_poisson.py::test_calcular_lambda -v`
Expected: PASS

Run: `pytest tests/test_aproximacion_poisson.py::test_validar_condiciones_ideal -v`
Expected: PASS

Run: `pytest tests/test_aproximacion_poisson.py::test_calcular_probabilidades_rango -v`
Expected: PASS

Run: `pytest tests/test_aproximacion_poisson.py::test_calcular_estadisticas -v`
Expected: PASS

Run: `pytest tests/test_aproximacion_poisson.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add utils/aproximacion_poisson.py tests/test_aproximacion_poisson.py
git commit -m "feat: add AproximacionPoissonBinomial calculation module"
```

---

## Task 2: Implement AproximacionPoissonHiper

**Files:**
- Modify: `utils/aproximacion_poisson.py`
- Test: `tests/test_aproximacion_poisson.py`

**Step 1: Write failing tests for AproximacionPoissonHiper**

```python
# Add to tests/test_aproximacion_poisson.py
from utils.aproximacion_poisson import AproximacionPoissonHiper

def test_hiper_calcular_lambda():
    """Test lambda calculation for hypergeometric"""
    result = AproximacionPoissonHiper.calcular_lambda(100, 20, 10)
    assert result == 2.0  # 10 * (20/100)

def test_hiper_validar_condiciones_ideal():
    """Test validation with ideal conditions"""
    cumple, mensaje = AproximacionPoissonHiper.validar_condiciones(100, 3)
    assert cumple is True
    assert mensaje == ""

def test_hiper_validar_condiciones_N_menor_50():
    """Test validation when N < 50"""
    cumple, mensaje = AproximacionPoissonHiper.validar_condiciones(30, 2)
    assert cumple is False
    assert "N=30 < 50" in mensaje

def test_hiper_validar_condiciones_n_sobre_N():
    """Test validation when n/N > 5%"""
    cumple, mensaje = AproximacionPoissonHiper.validar_condiciones(100, 10)
    assert cumple is False
    assert "n/N=10.0% > 5%" in mensaje

def test_hiper_calcular_probabilidades_rango():
    """Test probability calculations for range"""
    n, N, K = 10, 50, 20
    valores_k, probs_hiper, probs_poisson = \
        AproximacionPoissonHiper.calcular_probabilidades_rango(n, N, K)
    
    max_k = min(K, n)  # 10
    assert len(valores_k) == 11  # 0 to 10
    assert valores_k == list(range(11))
    assert len(probs_hiper) == 11
    assert len(probs_poisson) == 11

def test_hiper_calcular_estadisticas():
    """Test statistics calculation"""
    media, varianza, desviacion = \
        AproximacionPoissonHiper.calcular_estadisticas(10, 50, 20)
    
    lam = 10 * (20 / 50)  # 4
    assert media == lam
    assert varianza == lam
    assert desviacion == math.sqrt(lam)
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_aproximacion_poisson.py -k "test_hiper" -v`
Expected: FAIL with "AttributeError: type object 'AproximacionPoissonHiper' has no attribute..."

**Step 3: Implement AproximacionPoissonHiper**

```python
# Add to utils/aproximacion_poisson.py

class AproximacionPoissonHiper:
    """Maneja aproximación Hipergeométrica → Poisson"""
    
    @staticmethod
    def calcular_lambda(N: int, K: int, n: int) -> float:
        """
        Calcula λ = n × (K/N) para aproximación de Poisson
        
        Args:
            N (int): Tamaño de población
            K (int): Elementos de interés en población
            n (int): Tamaño de muestra
            
        Returns:
            float: Parámetro λ
        """
        p = K / N
        return n * p
    
    @staticmethod
    def validar_condiciones(N: int, n: int) -> tuple[bool, str]:
        """
        Valida condiciones ideales para aproximación Hipergeométrica → Poisson
        
        Condiciones: N ≥ 50 y n/N ≤ 0.05
        
        Args:
            N (int): Tamaño de población
            n (int): Tamaño de muestra
            
        Returns:
            tuple: (cumple: bool, mensaje_advertencia: str)
        """
        condiciones = []
        porcentaje = (n / N) * 100
        
        if N < 50:
            condiciones.append(f"N={N} < 50")
        
        if porcentaje > 5:
            condiciones.append(f"n/N={porcentaje:.1f}% > 5%")
        
        if condiciones:
            mensaje = f"Advertencia: {', '.join(condiciones)}. Condiciones ideales: N≥50 y n/N≤5%"
            return False, mensaje
        
        return True, ""
    
    @staticmethod
    def calcular_probabilidades_rango(n: int, N: int, K: int) -> tuple[list[int], list[float], list[float]]:
        """
        Calcula P(X=k) para k=0..min(K, n) en ambas distribuciones
        
        Args:
            n (int): Tamaño de muestra
            N (int): Tamaño de población
            K (int): Elementos de interés en población
            
        Returns:
            tuple: (valores_k, probs_hiper, probs_poisson)
        """
        max_k = min(K, n)
        valores_k = list(range(max_k + 1))
        
        probs_hiper = [hipergeometrica_pmf(k, n, N, K) for k in valores_k]
        lam = n * (K / N)
        probs_poisson = [poisson_pmf(k, lam) for k in valores_k]
        
        return valores_k, probs_hiper, probs_poisson
    
    @staticmethod
    def calcular_estadisticas(n: int, N: int, K: int) -> tuple[float, float, float]:
        """
        Calcula estadísticas de distribución de Poisson
        
        Fórmulas: Media = λ, Varianza = λ, Desviación = √λ
        donde λ = n × (K/N)
        
        Args:
            n (int): Tamaño de muestra
            N (int): Tamaño de población
            K (int): Elementos de interés en población
            
        Returns:
            tuple: (media, varianza, desviacion)
        """
        p = K / N
        lam = n * p
        media = lam
        varianza = lam
        desviacion = math.sqrt(lam)
        
        return media, varianza, desviacion
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_aproximacion_poisson.py -k "test_hiper" -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add utils/aproximacion_poisson.py tests/test_aproximacion_poisson.py
git commit -m "feat: add AproximacionPoissonHiper calculation module"
```

---

## Task 3: Export New Functions in utils/__init__.py

**Files:**
- Modify: `utils/__init__.py`

**Step 1: Add imports**

```python
# Add to utils/__init__.py
from utils.aproximacion_poisson import (
    AproximacionPoissonBinomial,
    AproximacionPoissonHiper,
)
```

**Step 2: Add to __all__ list**

```python
# Add to __all__ list in utils/__init__.py
"AproximacionPoissonBinomial",
"AproximacionPoissonHiper",
```

**Step 3: Test imports**

Run: `python -c "from utils import AproximacionPoissonBinomial, AproximacionPoissonHiper; print('OK')"`
Expected: OK

**Step 4: Commit**

```bash
git add utils/__init__.py
git commit -m "chore: export Poisson approximation classes"
```

---

## Task 4: Create Comparative Table Widget

**Files:**
- Create: `gui/tabla_comparacion_poisson.py`
- Test: `tests/test_tabla_comparacion_poisson.py`

**Step 1: Write failing test**

```python
# tests/test_tabla_comparacion_poisson.py
import customtkinter as ctk
from gui.tabla_comparacion_poisson import TablaComparacionPoisson

def test_tabla_comparacion_poisson_initialization():
    """Test widget initialization"""
    root = ctk.CTk()
    widget = TablaComparacionPoisson(root)
    
    assert widget.datos_completos is None
    assert widget.k_destacado is None
    assert widget.es_expandido is False
    
    root.destroy()

def test_tabla_comparacion_poisson_mostrar_acotada():
    """Test displaying bounded table"""
    root = ctk.CTk()
    widget = TablaComparacionPoisson(root)
    
    valores_k = list(range(100))  # 0 to 99
    probs_binom = [0.01] * 100
    probs_poisson = [0.01] * 100
    k_destacado = 50
    
    widget.mostrar_tabla_acotada(valores_k, probs_binom, probs_poisson, k_destacado)
    
    assert widget.k_destacado == 50
    assert widget.es_expandido is False
    assert widget.datos_completos is not None
    
    # Should have ~20 rows (centered around 50)
    # Exact count depends on implementation
    
    root.destroy()

def test_tabla_comparacion_poisson_expansion():
    """Test table expansion"""
    root = ctk.CTk()
    widget = TablaComparacionPoisson(root)
    
    valores_k = list(range(20))
    probs_binom = [0.05] * 20
    probs_poisson = [0.05] * 20
    
    widget.mostrar_tabla_acotada(valores_k, probs_binom, probs_poisson, 10)
    widget.mostrar_tabla_completa()
    
    assert widget.es_expandido is True
    
    root.destroy()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_tabla_comparacion_poisson.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Implement TablaComparacionPoisson widget**

```python
# gui/tabla_comparacion_poisson.py
"""
Widget para mostrar tabla comparativa de aproximación de Poisson
"""
import customtkinter as ctk


class TablaComparacionPoisson(ctk.CTkFrame):
    """Widget para mostrar tabla comparativa acotada"""
    
    def __init__(self, master, expand_callback=None):
        """
        Inicializa widget de tabla comparativa
        
        Args:
            master: Widget padre
            expand_callback: Función callback al expandir tabla
        """
        super().__init__(master, fg_color="transparent")
        self.expand_callback = expand_callback
        self.datos_completos = None  # Guardar datos completos para expansión
        self.k_destacado = None
        self.es_expandido = False
        
        self.frame_contenido = ctk.CTkFrame(self)
        self.frame_contenido.pack(fill="both", expand=True)
        
        self.scrollframe = ctk.CTkScrollableFrame(self.frame_contenido)
        self.scrollframe.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.header_frame = None
        self.filas = []
        
        self.btn_expandir = ctk.CTkButton(
            self, 
            text="Ver tabla completa",
            command=self.expandir_tabla
        )
    
    def mostrar_tabla_acotada(self, valores_k, probs_binom, probs_poisson, k_destacado):
        """
        Muestra máximo 20 filas centradas en k_destacado
        
        Args:
            valores_k (list): Lista de valores de k
            probs_binom (list): Lista de probabilidades binomiales
            probs_poisson (list): Lista de probabilidades de Poisson
            k_destacado (int): Valor de k a destacar
        """
        self.datos_completos = (valores_k, probs_binom, probs_poisson)
        self.k_destacado = k_destacado
        self.es_expandido = False
        
        # Encontrar centro
        if k_destacado is None or k_destacado not in valores_k:
            k_centro = len(valores_k) // 2
        else:
            k_centro = valores_k.index(k_destacado)
        
        # Calcular rango acotado (máximo 20 filas)
        inicio = max(0, k_centro - 10)
        fin = min(len(valores_k), k_centro + 10)
        
        self._render_filas(
            valores_k[inicio:fin], 
            probs_binom[inicio:fin], 
            probs_poisson[inicio:fin]
        )
        
        # Mostrar botón de expansión
        self.btn_expandir.pack(pady=10)
    
    def mostrar_tabla_completa(self):
        """Muestra todas las filas"""
        if not self.datos_completos:
            return
        
        valores_k, probs_binom, probs_poisson = self.datos_completos
        self.es_expandido = True
        
        self._render_filas(valores_k, probs_binom, probs_poisson)
        
        # Ocultar botón de expansión
        self.btn_expandir.pack_forget()
    
    def _render_filas(self, valores_k, probs_binom, probs_poisson):
        """
        Renderiza las filas de la tabla
        
        Args:
            valores_k (list): Valores de k a mostrar
            probs_binom (list): Probabilidades binomiales
            probs_poisson (list): Probabilidades de Poisson
        """
        self.limpiar()
        
        # Header
        self.header_frame = ctk.CTkFrame(self.scrollframe, fg_color="#2b2b2b")
        self.header_frame.pack(fill="x", pady=(0, 2))
        
        for col in ["k", "P(X=k) Original", "P(X=k) Poisson"]:
            ctk.CTkLabel(
                self.header_frame, 
                text=col, 
                font=("Arial", 11, "bold"),
                text_color=("gray10", "gray90")
            ).pack(side="left", padx=15, pady=5)
        
        # Filas
        for k, prob_orig, prob_pois in zip(valores_k, probs_binom, probs_poisson):
            es_destacado = (k == self.k_destacado)
            bg_color = "#3b8ed0" if es_destacado else "transparent"
            text_color = "white" if es_destacado else ("gray10", "gray90")
            
            fila = ctk.CTkFrame(self.scrollframe, fg_color=bg_color)
            fila.pack(fill="x", pady=1)
            
            ctk.CTkLabel(
                fila, 
                text=str(k), 
                width=40, 
                text_color=text_color
            ).pack(side="left", padx=15)
            
            ctk.CTkLabel(
                fila, 
                text=f"{prob_orig:.6f}", 
                width=120, 
                text_color=text_color
            ).pack(side="left", padx=15)
            
            ctk.CTkLabel(
                fila, 
                text=f"{prob_pois:.6f}", 
                width=120, 
                text_color=text_color
            ).pack(side="left", padx=15)
            
            self.filas.append(fila)
    
    def limpiar(self):
        """Limpia todas las filas de la tabla"""
        if self.header_frame:
            self.header_frame.destroy()
            self.header_frame = None
        
        for fila in self.filas:
            fila.destroy()
        
        self.filas.clear()
    
    def expandir_tabla(self):
        """Callback para expandir a tabla completa"""
        if self.expand_callback:
            self.expand_callback()
        else:
            self.mostrar_tabla_completa()
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_tabla_comparacion_poisson.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add gui/tabla_comparacion_poisson.py tests/test_tabla_comparacion_poisson.py
git commit -m "feat: add comparative table widget for Poisson approximation"
```

---

## Task 5: Add Checkbox to CamposEntrada (Binomial)

**Files:**
- Modify: `gui/campos_entrada.py`

**Step 1: Read existing CamposEntrada class**

```bash
# Read gui/campos_entrada.py to understand structure
grep -n "class CamposEntrada" gui/campos_entrada.py
```

**Step 2: Add checkbox to CamposEntrada.__init__**

Find the `__init__` method in `CamposEntrada` class and add after the `x` field:

```python
# In CamposEntrada.__init__, after creating x_entry:
self.chk_poisson = ctk.CTkCheckBox(
    self, 
    text="Activar aproximación Poisson",
    command=self.on_poisson_toggle
)
self.chk_poisson.pack(pady=5)
```

**Step 3: Add toggle callback method**

```python
# Add to CamposEntrada class:

def on_poisson_toggle(self):
    """
    Callback cuando cambia el checkbox de aproximación Poisson
    Recalcula si hay datos válidos en el dashboard
    """
    if self.parent and hasattr(self.parent, 'ventana_principal'):
        # Check if there are valid inputs before recalculating
        # This will be implemented after dashboard integration
        pass
```

**Step 4: Test checkbox creation**

Run: `python -c "from gui.campos_entrada import CamposEntrada; import customtkinter as ctk; root = ctk.CTk(); widget = CamposEntrada(root); print(hasattr(widget, 'chk_poisson')); root.destroy()"`
Expected: True

**Step 5: Commit**

```bash
git add gui/campos_entrada.py
git commit -m "feat: add Poisson approximation checkbox to Binomial entry fields"
```

---

## Task 6: Add Checkbox to CamposEntradaHipergeometrica

**Files:**
- Modify: `gui/campos_entrada.py`

**Step 1: Add checkbox to CamposEntradaHipergeometrica.__init__**

Find the `__init__` method in `CamposEntradaHipergeometrica` class and add after the `x` field:

```python
# In CamposEntradaHipergeometrica.__init__, after creating x_entry:
self.chk_poisson = ctk.CTkCheckBox(
    self, 
    text="Activar aproximación Poisson",
    command=self.on_poisson_toggle
)
self.chk_poisson.pack(pady=5)
```

**Step 2: Add toggle callback method**

```python
# Add to CamposEntradaHipergeometrica class:

def on_poisson_toggle(self):
    """
    Callback cuando cambia el checkbox de aproximación Poisson
    Recalcula si hay datos válidos en el dashboard
    """
    if self.parent and hasattr(self.parent, 'ventana_principal'):
        # This will be implemented after dashboard integration
        pass
```

**Step 3: Test checkbox creation**

Run: `python -c "from gui.campos_entrada import CamposEntradaHipergeometrica; import customtkinter as ctk; root = ctk.CTk(); widget = CamposEntradaHipergeometrica(root); print(hasattr(widget, 'chk_poisson')); root.destroy()"`
Expected: True

**Step 4: Commit**

```bash
git add gui/campos_entrada.py
git commit -m "feat: add Poisson approximation checkbox to Hypergeometric entry fields"
```

---

## Task 7: Integrate Poisson Binomial in ventana_principal.py

**Files:**
- Modify: `ventana_principal.py`

**Step 1: Add calculation method for Poisson Binomial**

```python
# Add to VentanaPrincipal class in ventana_principal.py:

def calcular_poisson_binomial(self):
    """
    Calcula aproximación Binomial → Poisson cuando el checkbox está activado
    
    Valida parámetros, calcula probabilidades para ambas distribuciones,
    y muestra resultados comparativos en el dashboard.
    """
    try:
        from utils import AproximacionPoissonBinomial
        
        valores = self.dashboard.obtener_campos()
        
        if not valores:
            return
        
        n = int(valores["n"])
        p = float(valores["p"])
        x_str = valores.get("x", "").strip()
        
        # Parsear k ingresado
        k_ingresado = int(x_str) if x_str else None
        
        # Validar parámetros básicos
        if n <= 0:
            messagebox.showerror(
                "Error de Validación",
                "El número de ensayos (n) debe ser mayor a 0"
            )
            return
        
        if not (0 < p < 1):
            messagebox.showerror(
                "Error de Validación",
                "La probabilidad (p) debe estar entre 0 y 1"
            )
            return
        
        if k_ingresado is not None and (k_ingresado < 0 or k_ingresado > n):
            messagebox.showerror(
                "Error de Validación",
                f"El valor k debe estar entre 0 y {n}"
            )
            return
        
        # Validar condiciones de aproximación
        cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(n, p)
        
        if not cumple:
            messagebox.showwarning("Advertencia de Aproximación", advertencia)
        
        # Calcular probabilidades para rango completo
        valores_k, probs_binom, probs_poisson = \
            AproximacionPoissonBinomial.calcular_probabilidades_rango(n, p)
        
        # Calcular estadísticas
        lam = AproximacionPoissonBinomial.calcular_lambda(n, p)
        media, varianza, desviacion = \
            AproximacionPoissonBinomial.calcular_estadisticas(n, p)
        
        # Datos para resultados
        datos_resultados = {
            "n": n,
            "p": p,
            "lambda": lam,
            "k_ingresado": k_ingresado,
            "valores_k": valores_k,
            "probs_binom": probs_binom,
            "probs_poisson": probs_poisson,
            "media": media,
            "varianza": varianza,
            "desviacion": desviacion,
            "advertencia": advertencia if not cumple else None
        }
        
        # Mostrar resultados en dashboard
        self.dashboard.mostrar_resultados_poisson_binomial(datos_resultados)
        
        # Crear gráfica comparativa
        self.dashboard.crear_grafico_poisson_binomial(
            valores_k, probs_binom, probs_poisson, k_ingresado, n, p, lam
        )
        
    except ValueError as e:
        messagebox.showerror(
            "Error de Entrada",
            f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}"
        )
    except Exception as e:
        messagebox.showerror(
            "Error Inesperado",
            f"Ocurrió un error al calcular la aproximación:\n\n{str(e)}"
        )
```

**Step 2: Modify calcular_desde_dashboard to check checkbox**

Find the `calcular_desde_dashboard` method and add check after validation:

```python
# In calcular_desde_dashboard method, after validating p and before calculating:

# Check if Poisson approximation is activated
if (hasattr(self.dashboard.campos, 'chk_poisson') and 
    self.dashboard.campos.chk_poisson.get()):
    self.calcular_poisson_binomial()
    return
```

**Step 3: Commit**

```bash
git add ventana_principal.py
git commit -m "feat: integrate Poisson Binomial approximation calculation"
```

---

## Task 8: Integrate Poisson Hypergeometric in ventana_principal.py

**Files:**
- Modify: `ventana_principal.py`

**Step 1: Add calculation method for Poisson Hypergeometric**

```python
# Add to VentanaPrincipal class in ventana_principal.py:

def calcular_poisson_hipergeometrica(self):
    """
    Calcula aproximación Hipergeométrica → Poisson cuando el checkbox está activado
    
    Valida parámetros, calcula probabilidades para ambas distribuciones,
    y muestra resultados comparativos en el dashboard.
    """
    try:
        from utils import AproximacionPoissonHiper
        
        valores = self.dashboard.obtener_campos_hipergeometrica()
        
        if not valores:
            return
        
        N = int(valores["N"])
        K = int(valores["K"])
        n = int(valores["n"])
        x_str = valores.get("x", "").strip()
        
        # Validar parámetros básicos
        if N <= 0:
            messagebox.showerror(
                "Error de Validación",
                "El tamaño de población (N) debe ser mayor a 0"
            )
            return
        
        if K <= 0 or K > N:
            messagebox.showerror(
                "Error de Validación",
                f"K debe estar entre 1 y N ({N})"
            )
            return
        
        if n <= 0 or n > N:
            messagebox.showerror(
                "Error de Validación",
                f"n debe estar entre 1 y N ({N})"
            )
            return
        
        k_ingresado = int(x_str) if x_str else None
        
        if k_ingresado is not None:
            if k_ingresado < 0 or k_ingresado > min(K, n):
                messagebox.showerror(
                    "Error de Validación",
                    f"k debe estar entre 0 y min(K, n) = {min(K, n)}"
                )
                return
        
        # Validar condiciones de aproximación
        cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(N, n)
        
        if not cumple:
            messagebox.showwarning("Advertencia de Aproximación", advertencia)
        
        # Calcular probabilidades para rango completo
        valores_k, probs_hiper, probs_poisson = \
            AproximacionPoissonHiper.calcular_probabilidades_rango(n, N, K)
        
        # Calcular estadísticas
        lam = AproximacionPoissonHiper.calcular_lambda(N, K, n)
        media, varianza, desviacion = \
            AproximacionPoissonHiper.calcular_estadisticas(n, N, K)
        
        # Datos para resultados
        datos_resultados = {
            "N": N,
            "K": K,
            "n": n,
            "lambda": lam,
            "k_ingresado": k_ingresado,
            "valores_k": valores_k,
            "probs_hiper": probs_hiper,
            "probs_poisson": probs_poisson,
            "media": media,
            "varianza": varianza,
            "desviacion": desviacion,
            "advertencia": advertencia if not cumple else None
        }
        
        # Mostrar resultados en dashboard
        self.dashboard.mostrar_resultados_poisson_hipergeometrica(datos_resultados)
        
        # Crear gráfica comparativa
        self.dashboard.crear_grafico_poisson_hipergeometrica(
            valores_k, probs_hiper, probs_poisson, k_ingresado, N, K, n, lam
        )
        
    except ValueError as e:
        messagebox.showerror(
            "Error de Entrada",
            f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}"
        )
    except Exception as e:
        messagebox.showerror(
            "Error Inesperado",
            f"Ocurrió un error al calcular la aproximación:\n\n{str(e)}"
        )
```

**Step 2: Modify calcular_hipergeometrica to check checkbox**

Find the `calcular_hipergeometrica` method and add check after validation:

```python
# In calcular_hipergeometrica method, after validating parameters and before calculating:

# Check if Poisson approximation is activated
if (hasattr(self.dashboard.campos_hipergeometrica, 'chk_poisson') and 
    self.dashboard.campos_hipergeometrica.chk_poisson.get()):
    self.calcular_poisson_hipergeometrica()
    return
```

**Step 3: Commit**

```bash
git add ventana_principal.py
git commit -m "feat: integrate Poisson Hypergeometric approximation calculation"
```

---

## Task 9: Add Result Display Methods to Dashboard

**Files:**
- Modify: `gui/dashboard.py`

**Step 1: Add method to show Poisson Binomial results**

```python
# Add to Dashboard class in gui/dashboard.py:

def mostrar_resultados_poisson_binomial(self, datos):
    """
    Muestra resultados de aproximación Binomial → Poisson
    
    Args:
        datos (dict): Diccionario con resultados del cálculo
    """
    # Limpiar área de resultados previa
    if self.area_resultados:
        self.area_resultados.limpiar()
    
    # Crear tabla comparativa
    if not self.tabla_poisson:
        from gui.tabla_comparacion_poisson import TablaComparacionPoisson
        self.tabla_poisson = TablaComparacionPoisson(
            self.content_frame,
            expand_callback=self.expandir_tabla_poisson_binomial
        )
    
    # Mostrar tabla acotada
    self.tabla_poisson.mostrar_tabla_acotada(
        datos["valores_k"],
        datos["probs_binom"],
        datos["probs_poisson"],
        datos["k_ingresado"]
    )
    
    # Mostrar estadísticas
    self.area_resultados.mostrar_estadisticas_poisson(datos)
```

**Step 2: Add method to show Poisson Hypergeometric results**

```python
# Add to Dashboard class:

def mostrar_resultados_poisson_hipergeometrica(self, datos):
    """
    Muestra resultados de aproximación Hipergeométrica → Poisson
    
    Args:
        datos (dict): Diccionario con resultados del cálculo
    """
    # Limpiar área de resultados previa
    if self.area_resultados:
        self.area_resultados.limpiar()
    
    # Crear tabla comparativa
    if not self.tabla_poisson:
        from gui.tabla_comparacion_poisson import TablaComparacionPoisson
        self.tabla_poisson = TablaComparacionPoisson(
            self.content_frame,
            expand_callback=self.expandir_tabla_poisson_hipergeometrica
        )
    
    # Mostrar tabla acotada
    self.tabla_poisson.mostrar_tabla_acotada(
        datos["valores_k"],
        datos["probs_hiper"],
        datos["probs_poisson"],
        datos["k_ingresado"]
    )
    
    # Mostrar estadísticas
    self.area_resultados.mostrar_estadisticas_poisson(datos)
```

**Step 3: Add expansion callbacks**

```python
# Add to Dashboard class:

def expandir_tabla_poisson_binomial(self):
    """Expande tabla completa para aproximación Binomial → Poisson"""
    if self.tabla_poisson:
        self.tabla_poisson.mostrar_tabla_completa()

def expandir_tabla_poisson_hipergeometrica(self):
    """Expande tabla completa para aproximación Hipergeométrica → Poisson"""
    if self.tabla_poisson:
        self.tabla_poisson.mostrar_tabla_completa()
```

**Step 4: Commit**

```bash
git add gui/dashboard.py
git commit -m "feat: add Poisson result display methods to Dashboard"
```

---

## Task 10: Add Statistics Display to AreaResultados

**Files:**
- Modify: `gui/area_resultados.py`

**Step 1: Add method to display Poisson statistics**

```python
# Add to AreaResultados class in gui/area_resultados.py:

def mostrar_estadisticas_poisson(self, datos):
    """
    Muestra estadísticas de aproximación de Poisson
    
    Args:
        datos (dict): Diccionario con λ, media, varianza, desviación, etc.
    """
    # Limpiar contenido previo
    for widget in self.winfo_children():
        widget.destroy()
    
    # Frame para estadísticas
    frame_stats = ctk.CTkFrame(self, fg_color="transparent")
    frame_stats.pack(fill="x", padx=5, pady=5)
    
    # Título
    titulo = ctk.CTkLabel(
        frame_stats,
        text="Estadísticas de Aproximación de Poisson",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=("#1f6aa5", "#1f6aa5")
    )
    titulo.pack(pady=5)
    
    # Valor λ
    lam_texto = ctk.CTkLabel(
        frame_stats,
        text=f"λ = {datos['lambda']:.4f}",
        font=ctk.CTkFont(size=12)
    )
    lam_texto.pack(pady=2)
    
    # Media
    media_texto = ctk.CTkLabel(
        frame_stats,
        text=f"Media (μ) = {datos['media']:.4f}",
        font=ctk.CTkFont(size=12)
    )
    media_texto.pack(pady=2)
    
    # Varianza
    var_texto = ctk.CTkLabel(
        frame_stats,
        text=f"Varianza (σ²) = {datos['varianza']:.4f}",
        font=ctk.CTkFont(size=12)
    )
    var_texto.pack(pady=2)
    
    # Desviación estándar
    desv_texto = ctk.CTkLabel(
        frame_stats,
        text=f"Desviación estándar (σ) = {datos['desviacion']:.4f}",
        font=ctk.CTkFont(size=12)
    )
    desv_texto.pack(pady=2)
    
    # Mostrar P(X=k) para k ingresado
    if datos.get('k_ingresado') is not None:
        k = datos['k_ingresado']
        separator = ctk.CTkFrame(frame_stats, height=2, fg_color="gray50")
        separator.pack(fill="x", padx=10, pady=10)
        
        prob_label = ctk.CTkLabel(
            frame_stats,
            text=f"P(X={k}):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        prob_label.pack(pady=5)
        
        if 'probs_binom' in datos:
            idx = datos['valores_k'].index(k) if k in datos['valores_k'] else 0
            prob_binom = datos['probs_binom'][idx]
            prob_poisson = datos['probs_poisson'][idx]
            
            binom_text = ctk.CTkLabel(
                frame_stats,
                text=f"  Original: {prob_binom:.6f}",
                font=ctk.CTkFont(size=11)
            )
            binom_text.pack(pady=2)
            
            poisson_text = ctk.CTkLabel(
                frame_stats,
                text=f"  Poisson:  {prob_poisson:.6f}",
                font=ctk.CTkFont(size=11)
            )
            poisson_text.pack(pady=2)
        
        elif 'probs_hiper' in datos:
            idx = datos['valores_k'].index(k) if k in datos['valores_k'] else 0
            prob_hiper = datos['probs_hiper'][idx]
            prob_poisson = datos['probs_poisson'][idx]
            
            hiper_text = ctk.CTkLabel(
                frame_stats,
                text=f"  Original: {prob_hiper:.6f}",
                font=ctk.CTkFont(size=11)
            )
            hiper_text.pack(pady=2)
            
            poisson_text = ctk.CTkLabel(
                frame_stats,
                text=f"  Poisson:  {prob_poisson:.6f}",
                font=ctk.CTkFont(size=11)
            )
            poisson_text.pack(pady=2)
```

**Step 2: Test statistics display**

Run: `python -c "from gui.area_resultados import AreaResultados; import customtkinter as ctk; root = ctk.CTk(); widget = AreaResultados(root); datos = {'lambda': 5.0, 'media': 5.0, 'varianza': 5.0, 'desviacion': 2.236, 'k_ingresado': 3, 'valores_k': [0,1,2,3], 'probs_binom': [0.1,0.2,0.3,0.4], 'probs_poisson': [0.1,0.2,0.3,0.4]}; widget.mostrar_estadisticas_poisson(datos); print('OK'); root.destroy()"`
Expected: OK

**Step 3: Commit**

```bash
git add gui/area_resultados.py
git commit -m "feat: add Poisson statistics display to AreaResultados"
```

---

## Task 11: Add Grouped Bar Chart to Grafico

**Files:**
- Modify: `gui/grafico.py`

**Step 1: Add method to create grouped bar chart**

```python
# Add to GraficoBinomial class in gui/grafico.py:

def crear_barras_agrupadas(self, valores_k, probs_orig, probs_poisson, k_destacado, n, titulo="Comparación"):
    """
    Crea gráfica de barras agrupadas comparando dos distribuciones
    
    Args:
        valores_k (list): Valores de k
        probs_orig (list): Probabilidades de distribución original
        probs_poisson (list): Probabilidades de Poisson
        k_destacado (int): Valor de k a destacar
        n (int): Valor máximo de k
        titulo (str): Título de la gráfica
    """
    # Limpiar gráfica anterior
    self.limpiar()
    
    # Crear figura y ejes
    self.figura, self.ax = plt.subplots(figsize=(10, 6))
    
    # Configurar posiciones de barras
    x = np.array(valores_k)
    width = 0.35  # Ancho de cada barra
    
    # Crear barras agrupadas
    bars1 = self.ax.bar(x - width/2, probs_orig, width, 
                        label='Original', color='#3b8ed0', alpha=0.8)
    bars2 = self.ax.bar(x + width/2, probs_poisson, width, 
                        label='Poisson', color='#ff6b6b', alpha=0.8)
    
    # Destacar barra de k_ingresado
    if k_destacado is not None and k_destacado in valores_k:
        idx = valores_k.index(k_destacado)
        bars1[idx].set_alpha(1.0)
        bars1[idx].set_linewidth(2)
        bars1[idx].set_edgecolor('white')
        bars2[idx].set_alpha(1.0)
        bars2[idx].set_linewidth(2)
        bars2[idx].set_edgecolor('white')
    
    # Configurar ejes
    self.ax.set_xlabel('k', fontsize=12)
    self.ax.set_ylabel('P(X=k)', fontsize=12)
    self.ax.set_title(titulo, fontsize=14, fontweight='bold')
    self.ax.legend(fontsize=10)
    self.ax.grid(True, alpha=0.3, linestyle='--')
    
    # Configurar fondo
    self.ax.set_facecolor('#2b2b2b')
    self.figura.patch.set_facecolor('#2b2b2b')
    self.ax.tick_params(axis='x', colors='white')
    self.ax.tick_params(axis='y', colors='white')
    self.ax.xaxis.label.set_color('white')
    self.ax.yaxis.label.set_color('white')
    self.ax.title.set_color('white')
    
    # Ajustar ticks si n es grande
    if n > 50:
        step = max(1, n // 20)
        self.ax.set_xticks(x[::step])
    
    # Crear canvas
    self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(fill="both", expand=True)
```

**Step 2: Import required modules**

```python
# Add to imports in gui/grafico.py:
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
```

**Step 3: Test grouped bar chart creation**

Run: `python -c "from gui.grafico import GraficoBinomial; import customtkinter as ctk; root = ctk.CTk(); graf = GraficoBinomial(root); graf.crear_barras_agrupadas([0,1,2,3,4,5], [0.1,0.2,0.3,0.2,0.1,0.1], [0.12,0.18,0.28,0.22,0.11,0.09], 3, 5, 'Test'); print('OK'); root.destroy()"`
Expected: OK

**Step 4: Commit**

```bash
git add gui/grafico.py
git commit -m "feat: add grouped bar chart method for Poisson comparison"
```

---

## Task 12: Add Chart Creation Methods to Dashboard

**Files:**
- Modify: `gui/dashboard.py`

**Step 1: Add method to create Poisson Binomial chart**

```python
# Add to Dashboard class in gui/dashboard.py:

def crear_grafico_poisson_binomial(self, valores_k, probs_binom, probs_poisson, k_destacado, n, p, lam):
    """
    Crea gráfica comparativa para Binomial → Poisson
    
    Args:
        valores_k (list): Valores de k
        probs_binom (list): Probabilidades binomiales
        probs_poisson (list): Probabilidades de Poisson
        k_destacado (int): Valor de k a destacar
        n (int): Número de ensayos
        p (float): Probabilidad
        lam (float): Parámetro λ
    """
    # Limpiar gráfica anterior
    if self.grafico:
        self.grafico.limpiar()
    
    # Crear gráfica nueva
    if not self.grafico:
        self.grafico = GraficoBinomial(self.content_frame)
    
    titulo = f"Binomial (n={n}, p={p:.3f}) vs Poisson (λ={lam:.3f})"
    self.grafico.crear_barras_agrupadas(valores_k, probs_binom, probs_poisson, k_destacado, n, titulo)
```

**Step 2: Add method to create Poisson Hypergeometric chart**

```python
# Add to Dashboard class:

def crear_grafico_poisson_hipergeometrica(self, valores_k, probs_hiper, probs_poisson, k_destacado, N, K, n, lam):
    """
    Crea gráfica comparativa para Hipergeométrica → Poisson
    
    Args:
        valores_k (list): Valores de k
        probs_hiper (list): Probabilidades hipergeométricas
        probs_poisson (list): Probabilidades de Poisson
        k_destacado (int): Valor de k a destacar
        N (int): Tamaño de población
        K (int): Elementos de interés
        n (int): Tamaño de muestra
        lam (float): Parámetro λ
    """
    # Limpiar gráfica anterior
    if self.grafico:
        self.grafico.limpiar()
    
    # Crear gráfica nueva
    if not self.grafico:
        self.grafico = GraficoBinomial(self.content_frame)
    
    p = K / N if N > 0 else 0
    titulo = f"Hipergeométrica (N={N}, K={K}, n={n}) vs Poisson (λ={lam:.3f})"
    max_k = min(K, n)
    self.grafico.crear_barras_agrupadas(valores_k, probs_hiper, probs_poisson, k_destacado, max_k, titulo)
```

**Step 3: Commit**

```bash
git add gui/dashboard.py
git commit -m "feat: add chart creation methods for Poisson approximation"
```

---

## Task 13: Initialize Dashboard Attributes

**Files:**
- Modify: `gui/dashboard.py`

**Step 1: Add tabla_poisson attribute to Dashboard.__init__**

```python
# In Dashboard.__init__, add initialization:
self.tabla_poisson = None
```

**Step 2: Test dashboard initialization**

Run: `python -c "from gui.dashboard import Dashboard; import customtkinter as ctk; root = ctk.CTk(); print('OK'); root.destroy()" 2>&1 | head -5`
Expected: OK (or no errors)

**Step 3: Commit**

```bash
git add gui/dashboard.py
git commit -m "chore: initialize tabla_poisson attribute in Dashboard"
```

---

## Task 14: Final Integration Testing

**Files:**
- Test: `tests/test_integracion_poisson.py`

**Step 1: Write integration tests**

```python
# tests/test_integracion_poisson.py
"""
Tests de integración para aproximación de Poisson
"""
import pytest
from utils import AproximacionPoissonBinomial, AproximacionPoissonHiper

def test_integracion_binomial_poisson_completa():
    """Test flujo completo de aproximación Binomial → Poisson"""
    n, p = 100, 0.04
    k = 5
    
    # Validar condiciones
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(n, p)
    assert cumple is True  # n=100 ≥ 30, p=0.04 ≤ 0.05
    
    # Calcular lambda
    lam = AproximacionPoissonBinomial.calcular_lambda(n, p)
    assert lam == 4.0
    
    # Calcular probabilidades
    valores_k, probs_binom, probs_poisson = \
        AproximacionPoissonBinomial.calcular_probabilidades_rango(n, p)
    
    assert len(valores_k) == 101
    assert k in valores_k
    assert len(probs_binom) == 101
    assert len(probs_poisson) == 101
    
    # Calcular estadísticas
    media, varianza, desviacion = AproximacionPoissonBinomial.calcular_estadisticas(n, p)
    assert media == 4.0
    assert varianza == 4.0
    assert desviacion == pytest.approx(2.0, rel=0.01)
    
    # Verificar que probabilidades suman aproximadamente 1
    assert sum(probs_binom) == pytest.approx(1.0, rel=0.01)
    assert sum(probs_poisson) == pytest.approx(1.0, rel=0.01)

def test_integracion_hipergeometrica_poisson_completa():
    """Test flujo completo de aproximación Hipergeométrica → Poisson"""
    N, K, n = 100, 20, 10
    k = 2
    
    # Validar condiciones
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(N, n)
    assert cumple is True  # N=100 ≥ 50, n/N=10% > 5% (pero continuamos)
    
    # Calcular lambda
    lam = AproximacionPoissonHiper.calcular_lambda(N, K, n)
    assert lam == 2.0  # 10 * (20/100)
    
    # Calcular probabilidades
    valores_k, probs_hiper, probs_poisson = \
        AproximacionPoissonHiper.calcular_probabilidades_rango(n, N, K)
    
    max_k = min(K, n)
    assert len(valores_k) == max_k + 1
    assert k in valores_k
    assert len(probs_hiper) == max_k + 1
    assert len(probs_poisson) == max_k + 1
    
    # Calcular estadísticas
    media, varianza, desviacion = \
        AproximacionPoissonHiper.calcular_estadisticas(n, N, K)
    assert media == 2.0
    assert varianza == 2.0
    assert desviacion == pytest.approx(1.414, rel=0.01)

def test_caso_prueba_binomial_ejercicio_8():
    """Test caso de ejercicio 8: n=200, K_amarillos=200, total=500, muestra=6"""
    # Nota: Este es el caso mencionado en el requerimiento
    n = 6  # muestra
    p = 200 / 500  # probabilidad
    lam = n * p
    
    valores_k, probs_binom, probs_poisson = \
        AproximacionPoissonBinomial.calcular_probabilidades_rango(n, p)
    
    assert lam == 2.4
    assert len(valores_k) == 7  # 0 to 6
    
    # Verificar que ambas distribuciones son similares
    for i in range(len(valores_k)):
        diff = abs(probs_binom[i] - probs_poisson[i])
        # Diferencia debe ser razonablemente pequeña para buena aproximación
        # (esto depende de las condiciones específicas)
        assert diff < 0.1  # Tolerancia razonable

def test_advertencia_condiciones_no_ideales():
    """Test que se muestra advertencia cuando condiciones no son ideales"""
    # Caso: n pequeño
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(10, 0.03)
    assert cumple is False
    assert "n=10 < 30" in advertencia
    
    # Caso: p grande
    cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(100, 0.10)
    assert cumple is False
    assert "p=0.1000 > 0.05" in advertencia
    
    # Caso Hipergeométrica: N pequeño
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(30, 2)
    assert cumple is False
    assert "N=30 < 50" in advertencia
    
    # Caso Hipergeométrica: n/N grande
    cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(100, 10)
    assert cumple is False
    assert "n/N=10.0% > 5%" in advertencia
```

**Step 2: Run integration tests**

Run: `pytest tests/test_integracion_poisson.py -v`
Expected: ALL PASS

**Step 3: Commit**

```bash
git add tests/test_integracion_poisson.py
git commit -m "test: add integration tests for Poisson approximation"
```

---

## Task 15: Manual Testing & Validation

**Step 1: Run application and test Binomial → Poisson**

```bash
python main.py
```

Manual test steps:
1. Select "Binomial" distribution
2. Enter n=100, p=0.03, k=5
3. Click "Activar aproximación Poisson" checkbox
4. Verify warning shows (n≥30 ✓, p≤0.05 ✓)
5. Verify comparative table shows ~20 rows centered on k=5
6. Verify highlighted row for k=5
7. Verify statistics show λ=3.0
8. Verify grouped bar chart displays
9. Click "Ver tabla complete" and verify expansion

**Step 2: Test Hypergeometric → Poisson**

Manual test steps:
1. Select "Hipergeométrica" distribution
2. Enter N=100, K=20, n=10, k=2
3. Click "Activar aproximación Poisson" checkbox
4. Verify warning shows (N≥50 ✓, n/N=10% > 5% ✗)
5. Verify comparative table displays
6. Verify grouped bar chart displays
7. Verify λ=2.0

**Step 3: Test edge cases**

- n=1 (muy pequeño, debe mostrar advertencia)
- p=0.5 (probabilidad grande, debe mostrar advertencia)
- N=30 (población pequeña, debe mostrar advertencia)
- k=0 (caso borde)
- k=n (caso borde para Binomial)
- k=min(K,n) (caso borde para Hipergeométrica)

**Step 4: Verify matplotlib cleanup**

Check that figures are properly cleaned:
1. Open multiple tabs/distributions
2. Verify no memory leaks in matplotlib figures
3. Verify no visual artifacts from previous charts

**Step 5: Document any issues found**

Create a brief notes file if issues discovered:
```bash
# If issues found, document them
echo "Manual testing notes:" > MANUAL_TESTING_NOTES.md
# Add findings
```

**Step 6: Final commit**

```bash
git add .
git commit -m "chore: complete manual testing and validation"
```

---

## Summary

This implementation plan provides:

1. **Modular calculation modules** - Separate classes for Binomial and Hypergeometric approximations
2. **Test-driven development** - Each component has tests before implementation
3. **Incremental commits** - Small, focused commits for easy review and rollback
4. **Complete UI integration** - From checkbox to chart display
5. **Comprehensive testing** - Unit tests, integration tests, and manual testing

Total tasks: 15
Estimated time: 4-6 hours for implementation

**Key design decisions:**
- Separated calculation logic from UI (following project patterns)
- Bounded table (20 rows) with expansion button for performance
- Full range chart for complete visualization
- Non-blocking warnings for non-ideal conditions
- Reusing existing scipy/math infrastructure

**Testing coverage:**
- Unit tests for calculation modules
- Widget tests for table component
- Integration tests for complete flows
- Manual testing for UI validation
