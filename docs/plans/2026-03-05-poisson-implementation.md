# Distribución de Poisson Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a new "Distribución de Poisson" option to the statistical distributions calculator, implementing all calculation, validation, UI, and graph components following existing patterns.

**Architecture:** Create new Poisson-specific components in parallel with existing Binomial/Hypergeometric distributions. Each file gets a new class/function for Poisson support. Uses CustomTkinter for UI, Matplotlib for graphs, and standard math for calculations.

**Tech Stack:** Python, CustomTkinter, Matplotlib, NumPy, Math

---

## Task 1: Add Poisson Calculation Functions

**Files:**
- Modify: `utils/calculos.py` (add at end of file)

**Step 1: Add Poisson PMF function**

Add after line 612 in `utils/calculos.py`:

```python
def poisson_pmf(k: int, lam: float) -> float:
    """
    Calcula P(X=k) para una distribución de Poisson
    
    Fórmula: P(X=k) = (e^(-λ) × λ^k) / k!
    
    Args:
        k (int): Número de eventos/éxitos
        lam (float): Parámetro λ (media = n × p)
    
    Returns:
        float: Probabilidad de exactamente k eventos
    """
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def calcular_media_poisson(n: int, p: float) -> float:
    """
    Calcula la media (λ) de la distribución de Poisson
    
    Fórmula: λ = n × p
    
    Args:
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
    
    Returns:
        float: Media λ
    """
    return n * p


def calcular_desviacion_poisson(lam: float) -> float:
    """
    Calcula la desviación estándar de la distribución de Poisson
    
    Fórmula: σ = √λ
    
    Args:
        lam (float): Parámetro λ (media)
    
    Returns:
        float: Desviación estándar
    """
    return math.sqrt(lam)


def calcular_curtosis_poisson(lam: float) -> tuple[float, str]:
    """
    Calcula la curtosis de la distribución de Poisson
    
    Fórmula: Curtosis = 1 / λ
    
    Args:
        lam (float): Parámetro λ (media)
    
    Returns:
        tuple: (curtosis, interpretación)
    """
    if lam <= 0:
        return 0, "No definida"
    
    curtosis = 1 / lam
    
    return curtosis, "Leptocúrtica"


def calcular_sesgo_poisson(lam: float) -> tuple[float, str]:
    """
    Calcula el sesgo de la distribución de Poisson
    
    Fórmula: Sesgo = 1 / √λ
    
    Args:
        lam (float): Parámetro λ (media)
    
    Returns:
        tuple: (sesgo, interpretación)
    """
    if lam <= 0:
        return 0, "No definido"
    
    sesgo = 1 / math.sqrt(lam)
    
    return sesgo, "Sesgo positivo: Media > Mediana"


def calcular_probabilidades_poisson(valores_x: list[int], lam: float) -> list[float]:
    """
    Calcula las probabilidades para múltiples valores de X en Poisson
    
    Args:
        valores_x (list): Lista de valores para los cuales calcular P(X=x)
        lam (float): Parámetro λ (media)
    
    Returns:
        list: Lista de probabilidades correspondientes a cada valor de X
    """
    return [poisson_pmf(x, lam) for x in valores_x]
```

**Step 2: Verify the file was modified correctly**

Run: Check that the file compiles without errors
Expected: No syntax errors

**Step 3: Commit**

```bash
git add utils/calculos.py
git commit -m "feat: add Poisson distribution calculation functions"
```

---

## Task 2: Add Poisson Validation Functions

**Files:**
- Modify: `utils/validaciones.py` (add at end of file)

**Step 1: Add Poisson validation functions**

Add after line 282 in `utils/validaciones.py`:

```python
def validar_condiciones_poisson(n: int, p: float) -> tuple[bool, str, float]:
    """
    Valida que se cumplan las condiciones para usar distribución de Poisson
    como aproximación de la Binomial:
    - p < 0.10
    - λ = n × p < 10
    
    Args:
        n (int): Número de ensayos
        p (float): Probabilidad de éxito (ya normalizada 0-1)
    
    Returns:
        tuple: (cumple_condiciones, mensaje_error, lambda)
    """
    lam = n * p
    
    errores = []
    
    if p >= 0.10:
        errores.append(f"p debe ser menor a 0.10 (actual: {p:.4f})")
    
    if lam >= 10:
        errores.append(f"λ debe ser menor a 10 (actual: {lam:.2f})")
    
    if errores:
        mensaje = (
            "Las condiciones no se cumplen. Este problema debe resolverse "
            "mediante Distribución Binomial.\n\n"
            "Condiciones requeridas:\n"
            "• " + "\n• ".join(errores)
        )
        return False, mensaje, lam
    
    return True, "", lam


def parsear_valores_x_poisson(texto: str, lam: float) -> list[int]:
    """
    Parsea el texto de entrada de valores X para Poisson
    
    Args:
        texto (str): Texto con valores separados por coma, "todos", o un solo número
        lam (float): Parámetro λ para determinar rango máximo sugerido
    
    Returns:
        list: Lista de valores enteros de X
    """
    texto = texto.strip().lower()
    
    max_sugerido = int(lam + 4 * math.sqrt(lam)) if lam > 0 else 10
    
    if texto == "todos" or texto == "":
        return list(range(0, max_sugerido + 1))
    
    if "," not in texto:
        try:
            valor_max = int(texto)
            if valor_max < 0:
                return [0]
            return list(range(0, valor_max + 1))
        except ValueError:
            return [0]
    
    valores_x = [int(x.strip()) for x in texto.split(",")]
    return valores_x


import math
```

**Step 2: Move the import to the top of the file**

The `import math` should be at the top. Add it after line 1 if not already present.

**Step 3: Commit**

```bash
git add utils/validaciones.py
git commit -m "feat: add Poisson validation functions"
```

---

## Task 3: Export Poisson Functions from utils/__init__.py

**Files:**
- Modify: `utils/__init__.py`

**Step 1: Add Poisson imports**

Add after line 23 in the calculos imports section:

```python
    calcular_sesgo_poisson,
    calcular_curtosis_poisson,
    calcular_desviacion_poisson,
    calcular_media_poisson,
    calcular_probabilidades_poisson,
    poisson_pmf,
```

**Step 2: Add Poisson validation imports**

Add after line 31 in the validaciones imports section:

```python
    validar_condiciones_poisson,
    parsear_valores_x_poisson,
```

**Step 3: Add to __all__ list**

Add after line 65 in the `__all__` list:

```python
    "calcular_sesgo_poisson",
    "calcular_curtosis_poisson",
    "calcular_desviacion_poisson",
    "calcular_media_poisson",
    "calcular_probabilidades_poisson",
    "poisson_pmf",
    "validar_condiciones_poisson",
    "parsear_valores_x_poisson",
```

**Step 4: Commit**

```bash
git add utils/__init__.py
git commit -m "feat: export Poisson functions from utils module"
```

---

## Task 4: Create CamposEntradaPoisson Class

**Files:**
- Modify: `gui/campos_entrada.py` (add at end of file)

**Step 1: Add CamposEntradaPoisson class**

Add after line 249 in `gui/campos_entrada.py`:

```python
class CamposEntradaPoisson:
    """Clase para gestionar los campos de entrada de distribución Poisson"""

    def __init__(self, frame_contenedor):
        """
        Inicializa los campos de entrada para Poisson

        Args:
            frame_contenedor: Frame donde se colocarán los campos
        """
        self.frame = frame_contenedor
        self.n_entry = None
        self.p_entry = None
        self.x_entry = None

        self.crear_campos()

    def crear_campos(self):
        """Crea todos los campos de entrada para Poisson"""
        row1 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row1.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row1, text="Número de ensayos (n):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.n_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 100")
        self.n_entry.pack(side="left", padx=8)

        ctk.CTkLabel(
            row1, text="Probabilidad de éxito (p):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.p_entry = ctk.CTkEntry(
            row1, width=120, placeholder_text="Ej: 0.05 o 5"
        )
        self.p_entry.pack(side="left", padx=8)

        info_label = ctk.CTkLabel(
            row1,
            text="(acepta: 0.05 o 5 para 5%)",
            font=ctk.CTkFont(size=10),
            text_color="gray",
        )
        info_label.pack(side="left", padx=8)

        row2 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row2.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row2, text="Valores de X (separados por coma):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.x_entry = ctk.CTkEntry(
            row2,
            width=380,
            placeholder_text="Ej: 0,1,2,3 o 'todos' (vacío=rango sugerido)",
        )
        self.x_entry.pack(side="left", padx=8)

        condiciones_label = ctk.CTkLabel(
            row2,
            text="Condiciones: p < 0.10 y λ < 10",
            font=ctk.CTkFont(size=10),
            text_color="#3b8ed0",
        )
        condiciones_label.pack(side="left", padx=15)

    def obtener_valores(self):
        """
        Obtiene los valores de todos los campos

        Returns:
            dict: Diccionario con los valores de entrada
        """
        return {
            "n": self.n_entry.get().strip(),
            "p": self.p_entry.get().strip(),
            "x": self.x_entry.get().strip(),
        }

    def limpiar(self):
        """Limpia todos los campos de entrada"""
        self.n_entry.delete(0, "end")
        self.p_entry.delete(0, "end")
        self.x_entry.delete(0, "end")
```

**Step 2: Commit**

```bash
git add gui/campos_entrada.py
git commit -m "feat: add CamposEntradaPoisson class for Poisson input fields"
```

---

## Task 5: Add Poisson Graph Method

**Files:**
- Modify: `gui/grafico.py` (add at end of class, before the last method)

**Step 1: Add crear_grafico_poisson method**

Add after line 407 in `gui/grafico.py` (after `crear_grafico_hipergeometrica`):

```python
    def crear_grafico_poisson(
        self,
        valores_x: list[int],
        probabilidades: list[float],
        lam: float,
        n: int,
        p: float,
        x_destacado: int = None,
    ):
        """
        Crea y muestra el gráfico de barras de la distribución de Poisson

        Args:
            valores_x (list): Valores del eje X
            probabilidades (list): Probabilidades correspondientes
            lam (float): Parámetro λ (media)
            n (int): Número de ensayos original
            p (float): Probabilidad de éxito original
            x_destacado (int, optional): Valor X específico a resaltar
        """
        self.limpiar()

        desviacion = math.sqrt(lam)
        max_prob = max(probabilidades) if probabilidades else 1

        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")

        text_color = "#ffffff"
        grid_color = "#444444"
        bar_color_normal = "#27ae60"
        bar_color_destacado = "#e74c3c"
        curve_color = "#f39c12"
        normal_color = "#3498db"

        colores = []
        for x in valores_x:
            if x_destacado is not None and x == x_destacado:
                colores.append(bar_color_destacado)
            else:
                colores.append(bar_color_normal)

        bar_width = 0.7 if len(valores_x) <= 20 else 0.6

        bars = ax.bar(
            valores_x,
            probabilidades,
            color=colores,
            alpha=0.8,
            edgecolor="white",
            linewidth=0.5,
            width=bar_width,
            label="Distribución de Poisson",
        )

        if len(valores_x) > 1:
            x_suave = np.linspace(min(valores_x) - 0.5, max(valores_x) + 0.5, 300)
            y_suave = np.interp(x_suave, valores_x, probabilidades)
            ax.plot(
                x_suave,
                y_suave,
                color=curve_color,
                linewidth=2.5,
                alpha=0.9,
                label="Curva de distribución",
            )

        if desviacion > 0:
            x_normal = np.linspace(
                max(0, lam - 4 * desviacion), lam + 4 * desviacion, 200
            )
            y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * np.exp(
                -0.5 * ((x_normal - lam) / desviacion) ** 2
            )
            if max(y_normal) > 0:
                y_normal = y_normal * (max_prob / max(y_normal))
            ax.plot(
                x_normal,
                y_normal,
                color=normal_color,
                linewidth=2,
                linestyle="--",
                alpha=0.8,
                label="Curva Normal (referencia)",
            )

        for i, (x, prob) in enumerate(zip(valores_x, probabilidades)):
            if x_destacado is not None and x == x_destacado:
                ax.text(
                    x,
                    prob + max_prob * 0.05,
                    f"P(X={x})={prob:.4f}",
                    ha="center",
                    va="bottom",
                    color="#e74c3c",
                    fontsize=10,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor="#2b2b2b",
                        edgecolor="#e74c3c",
                    ),
                )
            elif prob > max_prob * 0.05:
                ax.text(
                    x,
                    prob + max_prob * 0.02,
                    f"{prob:.3f}",
                    ha="center",
                    va="bottom",
                    color="white",
                    fontsize=8,
                    fontweight="bold",
                )

        ax.set_xlabel(
            "Número de eventos (X)", fontsize=11, color=text_color, fontweight="bold"
        )
        ax.set_ylabel(
            "Probabilidad P(X)", fontsize=11, color=text_color, fontweight="bold"
        )

        ax.set_title(
            f"Distribución de Poisson (λ={lam:.2f})\n"
            f"Aproximación de Binomial (n={n}, p={p:.4f})",
            fontsize=11,
            color=text_color,
            fontweight="bold",
            pad=10,
        )

        legend = ax.legend(
            loc="upper right", facecolor="#3b3b3b", edgecolor="#555555", fontsize=9
        )
        for text in legend.get_texts():
            text.set_color(text_color)

        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines["bottom"].set_color(grid_color)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(grid_color)

        ax.grid(True, alpha=0.3, linestyle="--", color=grid_color, axis="y")
        ax.set_axisbelow(True)

        ax.axvline(x=lam, color="#2ecc71", linestyle=":", linewidth=2, alpha=0.7)
        ax.text(
            lam,
            max_prob * 0.85,
            f"λ={lam:.2f}",
            ha="center",
            va="bottom",
            color="#2ecc71",
            fontsize=10,
            fontweight="bold",
        )

        if len(valores_x) > 0:
            ax.set_xlim(min(valores_x) - 0.5, max(valores_x) + 0.5)

        ax.set_xticks(valores_x)

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
```

**Step 2: Add import for math at top of file**

Verify `import math` is at the top of `gui/grafico.py`. If not present, add it.

**Step 3: Commit**

```bash
git add gui/grafico.py
git commit -m "feat: add crear_grafico_poisson method for Poisson bar charts"
```

---

## Task 6: Add Poisson Results Display Method

**Files:**
- Modify: `gui/area_resultados.py` (add at end of class)

**Step 1: Add mostrar_resultados_poisson method**

Add after line 582 in `gui/area_resultados.py`:

```python
    def mostrar_resultados_poisson(self, datos):
        """
        Muestra resultados de distribución de Poisson con diseño visual

        Args:
            datos (dict): Diccionario con los datos:
                - n: número de ensayos
                - p: probabilidad de éxito
                - lambda: parámetro λ
                - valores_x: lista de valores X
                - probabilidades: lista de probabilidades
                - media: media (λ)
                - desviacion: desviación estándar
                - sesgo: valor del sesgo
                - interpretacion_sesgo: descripción del sesgo
                - curtosis: valor de curtosis
                - interpretacion_curtosis: descripción de curtosis
        """
        self.limpiar()
        self.resultados_data = datos

        row = 0

        titulo = ctk.CTkLabel(
            self.scrollable_frame,
            text="RESULTADOS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#27ae60", "#27ae60"),
        )
        titulo.grid(row=row, column=0, pady=(10, 15), sticky="ew")
        row += 1

        row = self._crear_seccion_condiciones_poisson(row, datos)
        row = self._crear_seccion_parametros_poisson(row, datos)
        row = self._crear_seccion_probabilidades(row, datos)
        row = self._crear_seccion_estadisticas(row, datos)
        row = self._crear_seccion_forma(row, datos)

    def _crear_seccion_condiciones_poisson(self, row, datos):
        """Crea la sección de condiciones de Poisson"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)

        lbl_titulo = ctk.CTkLabel(
            frame,
            text="APROXIMACIÓN DE POISSON",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))

        p = datos.get("p", 0)
        lam = datos.get("lambda", 0)

        cond_p = p < 0.10
        cond_lam = lam < 10

        frame_cond = ctk.CTkFrame(frame, fg_color="transparent")
        frame_cond.pack(fill="x", padx=10, pady=2)

        lbl_cond1 = ctk.CTkLabel(
            frame_cond,
            text=f"• p < 0.10: {p:.4f} {'✓' if cond_p else '✗'}",
            font=ctk.CTkFont(size=11),
            text_color="#2ecc71" if cond_p else "#e74c3c",
            anchor="w",
        )
        lbl_cond1.pack(anchor="w")

        lbl_cond2 = ctk.CTkLabel(
            frame_cond,
            text=f"• λ < 10: {lam:.2f} {'✓' if cond_lam else '✗'}",
            font=ctk.CTkFont(size=11),
            text_color="#2ecc71" if cond_lam else "#e74c3c",
            anchor="w",
        )
        lbl_cond2.pack(anchor="w")

        lbl_valido = ctk.CTkLabel(
            frame,
            text="Válido para aproximación de Poisson" if (cond_p and cond_lam) else "Condiciones no cumplidas",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#27ae60" if (cond_p and cond_lam) else "#e74c3c",
            anchor="w",
        )
        lbl_valido.pack(fill="x", padx=10, pady=(5, 10))

        return row + 1

    def _crear_seccion_parametros_poisson(self, row, datos):
        """Crea la sección de parámetros Poisson"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)

        lbl_titulo = ctk.CTkLabel(
            frame,
            text="PARÁMETROS",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))

        params = [
            ("Número de ensayos (n):", str(datos.get("n", "--"))),
            ("Probabilidad de éxito (p):", f"{datos.get('p', 0):.6f}"),
            ("Parámetro λ (media):", f"{datos.get('lambda', 0):.6f}"),
        ]

        for label, valor in params:
            frame_param = ctk.CTkFrame(frame, fg_color="transparent")
            frame_param.pack(fill="x", padx=10, pady=2)

            lbl = ctk.CTkLabel(
                frame_param,
                text=label,
                font=ctk.CTkFont(size=11),
                width=180,
                anchor="w",
            )
            lbl.pack(side="left")

            val = ctk.CTkLabel(
                frame_param,
                text=valor,
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w",
            )
            val.pack(side="left", padx=5)

        lbl_espacio = ctk.CTkLabel(frame, text="")
        lbl_espacio.pack(pady=(5, 0))

        return row + 1
```

**Step 2: Commit**

```bash
git add gui/area_resultados.py
git commit -m "feat: add mostrar_resultados_poisson method for Poisson results display"
```

---

## Task 7: Add Poisson Dashboard Interface

**Files:**
- Modify: `gui/dashboard.py`

**Step 1: Add Poisson import at top**

Add `CamposEntradaPoisson` to the imports on line 8:

```python
from gui.campos_entrada import CamposEntrada, CamposEntradaHipergeometrica, CamposEntradaPoisson
```

**Step 2: Add campos_poisson attribute in __init__**

Add after line 32 (`self.campos_hipergeometrica = None`):

```python
        self.campos_poisson = None
```

**Step 3: Add Poisson button in sidebar**

Add after line 67 (after `self.btn_binomial`):

```python
        self.btn_poisson = self.crear_boton_sidebar("Poisson", "poisson", False)
```

**Step 4: Update actualizar_botones_sidebar**

Modify the `botones` dictionary around line 166 to include Poisson:

```python
        botones = {
            "binomial": self.btn_binomial,
            "poisson": self.btn_poisson,
            "hipergeometrica": self.btn_hipergeometrica,
        }
```

**Step 5: Replace crear_interfaz_poisson method**

Replace the placeholder `crear_interfaz_poisson` method (lines 243-266) with:

```python
    def crear_interfaz_poisson(self):
        """Crea la interfaz para distribución Poisson"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN DE POISSON",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        titulo.pack(pady=(12, 8))

        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Aproximación de la Binomial cuando p < 0.10 y λ < 10",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        descripcion.pack(pady=(0, 12))

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=5)

        self.campos_poisson = CamposEntradaPoisson(input_frame)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=8)

        calc_btn = ctk.CTkButton(
            button_frame,
            text="CALCULAR",
            command=self.calcular_poisson,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=140,
            fg_color="#27ae60",
            hover_color="#219a52",
            corner_radius=8,
        )
        calc_btn.pack(side="left", padx=5, pady=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="LIMPIAR",
            command=self.limpiar_poisson,
            font=ctk.CTkFont(size=13),
            height=38,
            width=110,
            fg_color="gray",
            hover_color="darkgray",
            corner_radius=8,
        )
        clear_btn.pack(side="left", padx=5, pady=5)

        results_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, padx=12, pady=8)

        results_frame.grid_columnconfigure(0, weight=45)
        results_frame.grid_columnconfigure(1, weight=55)
        results_frame.grid_rowconfigure(0, weight=1)

        text_frame = ctk.CTkFrame(results_frame)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        graph_frame = ctk.CTkFrame(results_frame)
        graph_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=0)

        self.area_resultados = AreaResultados(text_frame)
        self.grafico = GraficoBinomial(graph_frame)
```

**Step 6: Add calcular_poisson and limpiar_poisson methods**

Add after line 393 (after `calcular_hipergeometrica` method):

```python
    def calcular_poisson(self):
        """Calcula la distribución de Poisson"""
        if self.ventana_principal:
            self.ventana_principal.calcular_poisson()

    def limpiar_poisson(self):
        """Limpia campos y resultados de Poisson"""
        if self.campos_poisson:
            self.campos_poisson.limpiar()
        if self.area_resultados:
            self.area_resultados.limpiar()
        if self.grafico:
            self.grafico.limpiar()
```

**Step 7: Add obtener_campos_poisson method**

Add after line 445 (after `obtener_campos_hipergeometrica` method):

```python
    def obtener_campos_poisson(self):
        """Obtiene los valores de los campos de entrada Poisson"""
        if self.campos_poisson:
            return self.campos_poisson.obtener_valores()
        return None
```

**Step 8: Add mostrar_resultados_poisson and crear_grafico_poisson methods**

Add after line 460 (after `mostrar_resultados_hipergeometrica` method):

```python
    def mostrar_resultados_poisson(self, datos):
        """Muestra resultados estructurados de distribución de Poisson"""
        if self.area_resultados:
            self.area_resultados.mostrar_resultados_poisson(datos)

    def crear_grafico_poisson(
        self, valores_x, probabilidades, lam, n, p, x_destacado=None
    ):
        """Crea el gráfico de distribución de Poisson"""
        if self.grafico:
            self.grafico.crear_grafico_poisson(
                valores_x, probabilidades, lam, n, p, x_destacado
            )
```

**Step 9: Commit**

```bash
git add gui/dashboard.py
git commit -m "feat: add Poisson interface to dashboard with button and methods"
```

---

## Task 8: Add calcular_poisson Orchestration Method

**Files:**
- Modify: `ventana_principal.py`

**Step 1: Add Poisson imports**

Add after line 25 in the imports from `utils`:

```python
    validar_condiciones_poisson,
    parsear_valores_x_poisson,
    calcular_probabilidades_poisson,
    calcular_desviacion_poisson,
    calcular_sesgo_poisson,
    calcular_curtosis_poisson,
```

**Step 2: Add calcular_poisson method**

Add after line 381 (after `calcular_hipergeometrica` method, before `abrir_analisis_archivo`):

```python
    def calcular_poisson(self):
        """Procesa los datos y realiza los cálculos de distribución de Poisson"""
        try:
            valores = self.dashboard.obtener_campos_poisson()

            if not valores:
                return

            n_str = valores.get("n", "").strip()
            p_str = valores.get("p", "").strip()
            x_str = valores.get("x", "").strip()

            if not n_str:
                messagebox.showerror(
                    "Error de Validación",
                    "El número de ensayos (n) es obligatorio",
                )
                return

            if not p_str:
                messagebox.showerror(
                    "Error de Validación",
                    "La probabilidad (p) es obligatoria",
                )
                return

            n = int(n_str)

            if n <= 0:
                messagebox.showerror(
                    "Error de Validación",
                    "El número de ensayos (n) debe ser mayor a 0",
                )
                return

            valido, p, error = normalizar_probabilidad(p_str)
            if not valido:
                messagebox.showerror("Error de Validación", error)
                return

            valido, mensaje, lam = validar_condiciones_poisson(n, p)
            if not valido:
                messagebox.showerror(
                    "Condiciones No Cumplidas",
                    mensaje,
                )
                return

            valores_x = parsear_valores_x_poisson(x_str, lam)

            probabilidades = calcular_probabilidades_poisson(valores_x, lam)
            media = lam
            desviacion = calcular_desviacion_poisson(lam)
            sesgo, interpretacion_sesgo = calcular_sesgo_poisson(lam)
            curtosis, interpretacion_curtosis = calcular_curtosis_poisson(lam)

            datos_resultados = {
                "n": n,
                "p": p,
                "lambda": lam,
                "valores_x": valores_x,
                "probabilidades": probabilidades,
                "media": media,
                "desviacion": desviacion,
                "sesgo": sesgo,
                "interpretacion_sesgo": interpretacion_sesgo,
                "curtosis": curtosis,
                "interpretacion_curtosis": interpretacion_curtosis,
            }

            self.dashboard.mostrar_resultados_poisson(datos_resultados)

            x_destacado = valores_x[0] if len(valores_x) == 1 else None
            self.dashboard.crear_grafico_poisson(
                valores_x, probabilidades, lam, n, p, x_destacado
            )

        except ValueError as e:
            messagebox.showerror(
                "Error de Entrada",
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}",
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al procesar los datos:\n\n{str(e)}",
            )
```

**Step 3: Commit**

```bash
git add ventana_principal.py
git commit -m "feat: add calcular_poisson orchestration method"
```

---

## Task 9: Final Verification and Integration Commit

**Step 1: Run the application to verify**

Run: `python main.py`

Expected: Application starts, Poisson button visible in sidebar, clicking it shows Poisson interface

**Step 2: Test Poisson calculation**

Test with these values:
- n = 100
- p = 0.05
- X = 0,1,2,3,4,5

Expected: Results displayed with λ = 5, probabilities calculated, graph shown

**Step 3: Test condition validation**

Test with these values:
- n = 100
- p = 0.5 (should fail: p >= 0.10)

Expected: Error message "Las condiciones no se cumplen..."

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat: complete Poisson distribution implementation

- Add Poisson calculation functions (PMF, media, desviacion, sesgo, curtosis)
- Add Poisson validation functions (condiciones, parsear valores)
- Add CamposEntradaPoisson for input fields
- Add crear_grafico_poisson for bar charts with normal curve
- Add mostrar_resultados_poisson for results display
- Add dashboard integration (button, interface, methods)
- Add calcular_poisson orchestration in ventana_principal

Conditions: p < 0.10 and λ < 10
Green color theme (#27ae60) to differentiate from other distributions"
```

---

## Summary

| Task | Description | Files Modified |
|------|-------------|----------------|
| 1 | Add calculation functions | `utils/calculos.py` |
| 2 | Add validation functions | `utils/validaciones.py` |
| 3 | Export from utils | `utils/__init__.py` |
| 4 | Add input fields class | `gui/campos_entrada.py` |
| 5 | Add graph method | `gui/grafico.py` |
| 6 | Add results display | `gui/area_resultados.py` |
| 7 | Add dashboard integration | `gui/dashboard.py` |
| 8 | Add orchestration method | `ventana_principal.py` |
| 9 | Verify and commit | All files |
