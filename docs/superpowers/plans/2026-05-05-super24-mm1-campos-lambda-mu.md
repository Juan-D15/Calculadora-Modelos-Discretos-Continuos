# Super24 M/M/1 Campos Lambda Mu Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add editable `λ` and `μ` fields to Super24 `M/M/1`, preloaded from database-derived values and used for calculation.

**Architecture:** Keep derivation in `VentanaPrincipal` and expose a small callback from `Dashboard` to preload fields without duplicating formulas. `Dashboard` owns UI fields and returns their text values through `obtener_campos_super24`.

**Tech Stack:** Python, CustomTkinter, pytest.

---

## File Structure

- Modify `gui/dashboard.py`: add `super24_mm1_lambda_entry` and `super24_mm1_mu_entry`, return values, and preload them when scenario changes.
- Modify `ventana_principal.py`: expose preloading through `precargar_tasas_super24_mm1` and use manual field values when present.
- Modify `tests/test_super24_mm1_tasas_observadas.py`: add test for manual override helper.

### Task 1: Test Manual Rate Selection

**Files:**
- Modify: `tests/test_super24_mm1_tasas_observadas.py`

- [ ] **Step 1: Add test**

```python
def test_obtener_tasas_super24_mm1_prefiere_campos_manual():
    """Debe usar lambda y mu escritos por el usuario cuando existan."""
    escenario = {
        "lambda_h": 4.0,
        "mu_h": 5.0,
        "w": 12.0,
        "wq": 2.0,
        "rho": 0.5,
        "servidores_c": 2,
        "lq": 0.0,
    }
    valores = {"mm1_lambda": "3.5", "mm1_mu": "9.5"}

    lam, mu = _ventana()._obtener_tasas_super24_mm1(escenario, valores)

    assert lam == pytest.approx(3.5)
    assert mu == pytest.approx(9.5)
```

- [ ] **Step 2: Expected RED**

Run: `python -m pytest tests/test_super24_mm1_tasas_observadas.py -v`

Expected: fail because `_obtener_tasas_super24_mm1` does not exist.

### Task 2: Implement Rate Selection Helper

**Files:**
- Modify: `ventana_principal.py`

- [ ] **Step 1: Add helper**

```python
def _obtener_tasas_super24_mm1(self, escenario, valores) -> tuple[float, float]:
    lambda_texto = str(valores.get("mm1_lambda") or "").strip()
    mu_texto = str(valores.get("mm1_mu") or "").strip()
    if lambda_texto and mu_texto:
        return float(lambda_texto), float(mu_texto)
    return self._derivar_tasas_super24_mm1(escenario)
```

- [ ] **Step 2: Use it in `_calcular_super24_mm1`**

Change `lam, mu = self._derivar_tasas_super24_mm1(escenario)` to `lam, mu = self._obtener_tasas_super24_mm1(escenario, valores)`.

### Task 3: Add Dashboard Fields And Preload

**Files:**
- Modify: `gui/dashboard.py`

- [ ] **Step 1: Add instance attrs**

Add `self.super24_mm1_lambda_entry = None` and `self.super24_mm1_mu_entry = None` near existing Super24 attrs.

- [ ] **Step 2: Add entries in Super24 row4**

Add labels and entries for `λ M/M/1` and `μ M/M/1` before `Clientes n M/M/1`.

- [ ] **Step 3: Return values**

Return `mm1_lambda` and `mm1_mu` from `obtener_campos_super24`.

- [ ] **Step 4: Preload values**

When `_actualizar_categorias_super24` or `actualizar_datos_super24` updates the selected scenario, call `ventana_principal.precargar_tasas_super24_mm1(escenario)` and write formatted values into the entries.

### Task 4: Verify

**Files:**
- Test: changed files

- [ ] **Step 1: Compile**

Run: `python -m py_compile ventana_principal.py gui/dashboard.py tests/test_super24_mm1_tasas_observadas.py`

Expected: no output.

- [ ] **Step 2: Run pytest if installed**

Run: `python -m pytest tests/test_super24_mm1_tasas_observadas.py -v`

Expected: pass. If pytest is not installed, document that limitation.

## Self-Review

- Spec coverage: fields are editable, preloaded from DB-derived values, and used for M/M/1 calculation.
- Placeholder scan: no placeholders.
- Type consistency: `mm1_lambda` and `mm1_mu` are consistent in dashboard and ventana principal.
