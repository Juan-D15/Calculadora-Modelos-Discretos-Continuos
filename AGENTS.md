# AGENTS.md

This file provides guidelines for agentic coding agents working in this repository.

## Project Overview

Binomial Distribution Calculator - Python GUI for statistical distributions (Binomial/Hypergeometric). Built with CustomTkinter and Matplotlib.

## Running

```bash
pip install -r requirements.txt
python main.py
```

## Build/Lint/Test Commands

No formal test/lint framework configured. When adding:

- **Testing**: `pytest tests/` or `pytest tests/test_calculos.py::test_name`
- **Linting**: `ruff check .` or `ruff check --fix .`
- **Type checking**: `mypy .`

## Code Style

### Naming

- **Classes**: PascalCase (`VentanaPrincipal`, `Dashboard`, `GraficoBinomial`, `BaseToplevelWindow`)
- **Functions/Variables**: snake_case (`calcular_media`, `valores_x`, `n_entry`)
- **Private members**: Single underscore (`_al_cerrar`, `_limpiar_recursos`)

### Imports

Standard library → Third-party → Local, grouped with blank lines:

```python
import math
from typing import Optional, Dict, Type

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np

from utils.calculos import calcular_media
from gui.dashboard import Dashboard
from base_window import BaseToplevelWindow
```

### Formatting & Types

- 4 spaces indentation, ~100 char line length
- Module-level docstrings in Spanish, use f-strings
- Add type hints for new functions:

```python
def centrar_ventana(self, ancho: int, alto: int) -> None: ...
def validar_parametros(n: int, p: float, N: Optional[int] = None) -> tuple[bool, str]: ...
```

### Documentation

Spanish docstrings with Args/Returns. Include formulas for math functions:

```python
def binomial_pmf(k, n, p):
    """
    Calcula P(X=k) para una distribución binomial
    Fórmula: P(X=k) = C(n,k) × p^k × (1-p)^(n-k)
    
    Args:
        k (int): Número de éxitos
        n (int): Número de ensayos
        p (float): Probabilidad de éxito
    Returns:
        float: Probabilidad de exactamente k éxitos
    """
```

### Error Handling

- Use `messagebox.showerror()` for GUI errors in Spanish
- Return `(success: bool, message: str)` tuples for validation:

```python
def validar_parametros(n, p, N=None):
    if n <= 0:
        return False, "El número de ensayos (n) debe ser mayor a 0"
    if p < 0 or p > 1:
        return False, "La probabilidad (p) debe estar entre 0 y 1"
    return True, ""
```

### GUI Conventions

- `ctk.CTkFrame` for containers, `fg_color="transparent"` for nested frames
- Button colors: `#3b8ed0` (primary), `gray` (secondary)
- Dark mode with `"blue"` theme, Window: `1300x850`, minsize `1200x750`
- Chart background: `#2b2b2b`, grid: `#444444`

### Matplotlib Cleanup

CRITICAL: Always clean up to prevent memory leaks:

```python
def limpiar(self):
    for widget in self.frame.winfo_children():
        widget.destroy()
    if self.figura is not None:
        try:
            plt.close(self.figura)
        except Exception:
            pass
        self.figura = None
    self.canvas = None
```

### Base Window Pattern

Inherit from `BaseToplevelWindow` for secondary windows:

```python
class DataViewerWindow(BaseToplevelWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Visor de Datos")
        self.centrar_ventana(800, 600)
```

Provides: automatic centering, single instance control, modal behavior, matplotlib cleanup.

### Project Structure

```
├── main.py                  # Entry point
├── ventana_principal.py     # Main window, calculation orchestration
├── base_window.py           # Base class for secondary windows
├── gui/
│   ├── dashboard.py         # Main dashboard with sidebar
│   ├── grafico.py           # Matplotlib chart wrapper
│   ├── campos_entrada.py    # Input field components
│   └── area_resultados.py   # Results display widget
└── utils/
    ├── calculos.py          # Statistical calculations
    ├── validaciones.py      # Input validation
    └── formato.py           # Result formatting
```

### Key Points

- Use `math` module (`math.sqrt`, `math.factorial`) and `numpy` for arrays (`np.linspace`, `np.interp`)
- Statistical params: `n` (trials), `p` (probability), `N` (population), `K` (successes in pop), `x/k` (value)
- Spanish for user-facing strings and docstrings
- Always clean up matplotlib figures with `plt.close(figura)`
