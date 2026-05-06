# Super24 Poisson Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Poisson as a selectable distribution in the Super24 database panel using imported sales data.

**Architecture:** Reuse the Super24 sales mapping already used for Binomial/Hipergeométrica: `K` comes from imported category sales, `N` comes from inventory, `p=K/N`, and `lambda=n*p`. The UI adds `Poisson` to the distribution combo and `VentanaPrincipal` routes to a new focused Poisson calculator that reuses existing Poisson utility, result, and graph methods.

**Tech Stack:** Python, CustomTkinter, Matplotlib, pytest.

---

## File Structure

- Modify `gui/dashboard.py`: include `Poisson` in the Super24 distribution selector.
- Modify `ventana_principal.py`: route Super24 `Poisson` to a new `_calcular_super24_poisson()` method.
- Modify `tests/test_probability_engine_db.py`: add a regression test proving sales data produces the expected Poisson lambda through `p=K/N` and `lambda=n*p`.

### Task 1: Poisson Parameter Regression Test

**Files:**
- Modify: `tests/test_probability_engine_db.py`

- [ ] **Step 1: Write failing/coverage test**

Add this test:

```python
def test_preparar_parametros_permite_lambda_poisson_desde_ventas():
    datos = ProbabilityEngine().preparar_parametros_desde_ventas(N=1000, K=54, n=100)
    assert datos["p"] == pytest.approx(0.054)
    assert datos["lambda_poisson"] == pytest.approx(5.4)
```

- [ ] **Step 2: Run test**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_probability_engine_db.py -v`

Expected: FAIL because `lambda_poisson` does not exist yet.

- [ ] **Step 3: Implement `lambda_poisson`**

In `ProbabilityEngine.preparar_parametros_desde_ventas`, include `"lambda_poisson": n * (K / N)` in the returned dict.

- [ ] **Step 4: Run test**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_probability_engine_db.py -v`

Expected: PASS.

### Task 2: Super24 UI Option

**Files:**
- Modify: `gui/dashboard.py`

- [ ] **Step 1: Add Poisson to selector**

Change the Super24 distribution combo values to:

```python
values=["Automática", "Binomial", "Hipergeométrica", "Poisson", "M/M/1"]
```

### Task 3: Super24 Poisson Calculation

**Files:**
- Modify: `ventana_principal.py`

- [ ] **Step 1: Route model**

In `calcular_super24`, add:

```python
elif modelo == "Poisson":
    self._calcular_super24_poisson(parametros, valores.get("x", ""))
```

- [ ] **Step 2: Implement calculator**

Add `_calcular_super24_poisson(self, parametros, x_texto)` that:

```python
n = int(parametros["n"])
p = float(parametros["p"])
lam = float(parametros["lambda_poisson"])
cumple, advertencia, _ = validar_condiciones_poisson(n, p)
if not cumple: messagebox.showwarning("Advertencia de Poisson", advertencia)
valores_x = parsear_valores_x_poisson(x_texto, lam, n)
valido, mensaje = validar_valores_x_poisson(valores_x, n)
probabilidades = calcular_probabilidades_poisson(valores_x, lam)
desviacion = calcular_desviacion_poisson(lam)
sesgo, interpretacion_sesgo = calcular_sesgo_poisson(lam)
curtosis, interpretacion_curtosis = calcular_curtosis_poisson(lam)
```

Then pass a result dict to `dashboard.mostrar_resultados_poisson()` and call `dashboard.crear_grafico_poisson()`.

### Task 4: Verification

**Files:**
- No new files.

- [ ] **Step 1: Run focused tests**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_probability_engine_db.py -v`

Expected: PASS.

- [ ] **Step 2: Compile modified files**

Run: `.\.venv\Scripts\python.exe -m py_compile probability_engine.py ventana_principal.py gui/dashboard.py`

Expected: no output.

- [ ] **Step 3: Run full suite**

Run: `.\.venv\Scripts\python.exe -m pytest tests -v`

Expected: PASS.

## Self-Review

- Spec coverage: Poisson appears in Super24 options and computes from sales `p=K/N`, `lambda=n*p`.
- Placeholder scan: no placeholders.
- Type consistency: `lambda_poisson` is float in `ProbabilityEngine` and consumed in `VentanaPrincipal`.
