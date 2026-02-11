# AGENTS.md

This file provides guidelines for agentic coding agents working on this repository.

## Project Overview

Binomial Distribution Calculator - A Python GUI application for computing statistical distributions. Built with CustomTkinter for the UI and Matplotlib for visualizations.

## Running the Application

```bash
# Install dependencies (first time setup)
pip install -r requirements.txt

# Run the application
python main.py
```

## Build/Lint/Test Commands

This project currently has no formal test framework or linting configuration. When adding tests or linting:

- **Testing**: No test framework is set up. If adding tests, use pytest as the framework:
  ```bash
  pip install pytest pytest-mock
  pytest tests/                    # Run all tests
  pytest tests/test_calculos.py    # Run single test file
  pytest tests/test_calculos.py -k test_binomial  # Run specific test
  ```

- **Linting**: No linter configured. Recommended to add:
  ```bash
  pip install ruff
  ruff check .
  ruff check --fix .
  ```

- **Type checking**: No type checking configured. Recommended to add:
  ```bash
  pip install mypy
  mypy .
  ```

## Code Style Guidelines

### Naming Conventions

- **Classes**: PascalCase (e.g., `VentanaPrincipal`, `Dashboard`, `GraficoBinomial`, `AreaResultados`, `CamposEntrada`)
- **Functions**: snake_case (e.g., `calcular_media`, `validar_parametros`, `crear_interfaz`)
- **Variables**: snake_case (e.g., `valores_x`, `probabilidades`, `n_entry`)
- **Constants**: UPPER_SNAKE_CASE if needed (not currently used in codebase)
- **Private members**: Single underscore prefix (e.g., `_valor_interno`)

### Imports

- Standard library imports first, then third-party, then local modules
- Use alias for common imports: `import customtkinter as ctk`
- Group imports with blank lines between categories

```python
# Standard library
import math

# Third-party
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Local
from utils.calculos import calcular_media
from gui.dashboard import Dashboard
```

### Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length: ~100 characters (not strictly enforced)
- Blank lines between functions and classes
- Docstrings at module and class level

### Type Hints

Currently minimal. When adding type hints:
```python
def calcular_media(n: int, p: float) -> float:
    """Calcula la media (esperanza) de una distribución binomial"""
    return n * p
```

### Documentation

- Module-level docstrings in Spanish (as per existing code)
- Function docstrings with Args and Returns sections
- Comments should be in Spanish to match existing code

```python
def binomial_pmf(k, n, p):
    """
    Calcula P(X=k) para una distribución binomial
    
    Fórmula: P(X=k) = C(n,k) × p^k × (1-p)^(n-k)
    
    Args:
        k (int): Número de éxitos
        n (int): Número de ensayos
        p (float): Probabilidad de éxito en cada ensayo
    """
```

### Error Handling

- Use specific exception types
- Provide user-friendly error messages (shown via messagebox for GUI)
- Use try-except blocks for user input validation

```python
try:
    n = int(valores['n'])
    p = float(valores['p'])
except ValueError as e:
    messagebox.showerror("Error de Entrada", f"Valores inválidos: {str(e)}")
```

### GUI Conventions

- Use `ctk.CTkFrame` for container widgets
- Use `fg_color="transparent"` for nested layout frames
- Standard button colors: `#3b8ed0` (active), `gray` (secondary)
- Theme: Dark mode with `"blue"` color theme
- Window geometry: `1300x850`, minsize `1200x750`

### Project Structure

```
.
├── main.py                  # Entry point
├── ventana_principal.py     # Main window class
├── gui/                     # GUI components
│   ├── dashboard.py         # Main dashboard layout
│   ├── grafico.py           # Matplotlib chart wrapper
│   ├── campos_entrada.py    # Input field components
│   └── area_resultados.py   # Results display widget
└── utils/                   # Business logic
    ├── calculos.py          # Statistical calculations
    ├── validaciones.py     # Input validation
    └── formato.py          # Result formatting
```

### Additional Guidelines

- Mathematical functions use `math` module (e.g., `math.sqrt`, `math.factorial`)
- Matplotlib figures should be cleaned with `plt.close(figura)` to prevent memory leaks
- CustomTkinter widgets should be packed with appropriate padx/pady for spacing
- Use Spanish variable names when they represent domain concepts (e.g., `n`, `p`, `q`)
- Return tuples `(success, message)` for validation functions

### When Working with This Codebase

1. Maintain Spanish language in docstrings and user-facing strings
2. Follow the existing GUI color scheme and layout patterns
3. Ensure matplotlib figures are properly closed when cleaning up
4. Add type hints when modifying or adding new functions
5. Consider adding tests for new calculation or validation functions
