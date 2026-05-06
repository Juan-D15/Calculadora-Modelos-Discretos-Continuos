# Super24 M/M/1 Tasas Observadas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Super24 `M/M/1` option derive observed `lambda` and `mu` from simulation metrics instead of directly trusting theoretical `lambda_h` and `mu_h`.

**Architecture:** Add a private helper in `ventana_principal.py` close to `_calcular_super24_mm1` so the interpretation logic stays with the Super24 injection flow. Add focused tests that instantiate `VentanaPrincipal` via `__new__` to avoid opening the GUI.

**Tech Stack:** Python, pytest, CustomTkinter app code, existing `MM1Queue` model.

---

## File Structure

- Modify `ventana_principal.py`: add `_derivar_tasas_super24_mm1` and use it from `_calcular_super24_mm1`.
- Create `tests/test_super24_mm1_tasas_observadas.py`: unit tests for primary derivation and fallbacks.
- Keep `db_connector.py` unchanged because it already selects all required fields.

### Task 1: Add Failing Tests For Rate Derivation

**Files:**
- Create: `tests/test_super24_mm1_tasas_observadas.py`
- Test: `tests/test_super24_mm1_tasas_observadas.py`

- [ ] **Step 1: Write the failing tests**

```python
"""
Pruebas para derivar tasas observadas M/M/1 desde escenarios Super24.
"""
import pytest

from ventana_principal import VentanaPrincipal


def _ventana():
    return VentanaPrincipal.__new__(VentanaPrincipal)


def test_derivar_tasas_super24_mm1_usa_metricas_observadas():
    """Debe calcular mu desde W-Wq y lambda desde rho*c*mu."""
    escenario = {
        "lambda_h": 4.0,
        "mu_h": 5.0,
        "w": 12.0,
        "wq": 2.0,
        "rho": 0.5,
        "servidores_c": 2,
        "lq": 0.0,
    }

    lam, mu = _ventana()._derivar_tasas_super24_mm1(escenario)

    assert mu == pytest.approx(6.0)
    assert lam == pytest.approx(6.0)


def test_derivar_tasas_super24_mm1_usa_mu_teorico_si_servicio_no_es_valido():
    """Debe usar mu_h cuando W-Wq no permite calcular servicio real."""
    escenario = {
        "lambda_h": 4.0,
        "mu_h": 8.0,
        "w": 2.0,
        "wq": 2.0,
        "rho": 0.25,
        "servidores_c": 1,
        "lq": 0.0,
    }

    lam, mu = _ventana()._derivar_tasas_super24_mm1(escenario)

    assert mu == pytest.approx(8.0)
    assert lam == pytest.approx(2.0)


def test_derivar_tasas_super24_mm1_usa_little_si_lambda_principal_es_cero():
    """Debe usar lambda=(Lq/Wq)*60 cuando rho no aporta llegada observada."""
    escenario = {
        "lambda_h": 4.0,
        "mu_h": 20.0,
        "w": 20.0,
        "wq": 15.0,
        "rho": 0.0,
        "servidores_c": 1,
        "lq": 3.0,
    }

    lam, mu = _ventana()._derivar_tasas_super24_mm1(escenario)

    assert mu == pytest.approx(12.0)
    assert lam == pytest.approx(12.0)


def test_derivar_tasas_super24_mm1_usa_lambda_teorico_como_respaldo_final():
    """Debe usar lambda_h si rho y Ley de Little no producen lambda positiva."""
    escenario = {
        "lambda_h": 7.0,
        "mu_h": 10.0,
        "w": 1.0,
        "wq": 1.0,
        "rho": 0.0,
        "servidores_c": 1,
        "lq": 0.0,
    }

    lam, mu = _ventana()._derivar_tasas_super24_mm1(escenario)

    assert mu == pytest.approx(10.0)
    assert lam == pytest.approx(7.0)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_super24_mm1_tasas_observadas.py -v`

Expected: FAIL with `AttributeError: 'VentanaPrincipal' object has no attribute '_derivar_tasas_super24_mm1'`.

### Task 2: Implement Observed Rate Helper

**Files:**
- Modify: `ventana_principal.py`
- Test: `tests/test_super24_mm1_tasas_observadas.py`

- [ ] **Step 1: Add the helper near `_calcular_super24_mm1`**

```python
    def _derivar_tasas_super24_mm1(self, escenario) -> tuple[float, float]:
        """
        Deriva λ y μ reales desde métricas observadas del simulador Super24.

        Fórmulas:
        - μ_real = 60 / (W - Wq)
        - λ_real = ρ × c × μ_real
        - Respaldo: λ_real = (Lq / Wq) × 60

        Args:
            escenario (dict): Escenario importado desde Super24.

        Returns:
            tuple[float, float]: λ y μ en clientes por hora.
        """
        lambda_teorico = float(escenario.get("lambda_h") or 0)
        mu_teorico = float(escenario.get("mu_h") or 0)
        w = float(escenario.get("w") or 0)
        wq = float(escenario.get("wq") or 0)
        lq = float(escenario.get("lq") or 0)
        rho = float(escenario.get("rho") or 0)
        servidores = int(escenario.get("servidores_c") or 1)

        tiempo_servicio = w - wq
        if tiempo_servicio > 0:
            mu_real = 60 / tiempo_servicio
        else:
            mu_real = mu_teorico

        lambda_real = rho * servidores * mu_real
        if lambda_real <= 0 and wq > 0:
            lambda_real = (lq / wq) * 60
        if lambda_real <= 0:
            lambda_real = lambda_teorico

        return lambda_real, mu_real
```

- [ ] **Step 2: Run tests to verify helper passes**

Run: `pytest tests/test_super24_mm1_tasas_observadas.py -v`

Expected: PASS for all four tests.

### Task 3: Use Derived Rates In Super24 M/M/1 Calculation

**Files:**
- Modify: `ventana_principal.py`
- Test: `tests/test_super24_mm1_tasas_observadas.py`

- [ ] **Step 1: Replace theoretical rate reads in `_calcular_super24_mm1`**

Change:

```python
        lam = float(escenario.get("lambda_h") or 0)
        mu = float(escenario.get("mu_h") or 0)
```

To:

```python
        lam, mu = self._derivar_tasas_super24_mm1(escenario)
```

- [ ] **Step 2: Keep existing server warning unchanged**

Keep this block as-is so the user still knows when `servidores_c` is not `1`:

```python
        if servidores != 1:
            messagebox.showwarning(
                "Modelo M/M/1",
                f"El escenario tiene servidores_c={servidores}. "
                "Esta calculadora evalúa M/M/1 usando λ y μ del escenario.",
            )
```

- [ ] **Step 3: Run focused tests**

Run: `pytest tests/test_super24_mm1_tasas_observadas.py -v`

Expected: PASS.

### Task 4: Run Regression Tests

**Files:**
- Test: `tests/test_super24_mm1_tasas_observadas.py`
- Test: `tests/test_db_connector.py`
- Test: `tests/test_probability_engine_db.py`

- [ ] **Step 1: Run relevant pytest tests**

Run: `pytest tests/test_super24_mm1_tasas_observadas.py tests/test_db_connector.py tests/test_probability_engine_db.py -v`

Expected: PASS.

- [ ] **Step 2: If available, run the complete test suite**

Run: `pytest tests/ -v`

Expected: PASS or document any unrelated pre-existing failures with exact test names.

## Self-Review

- Spec coverage: Tasks implement observed `mu`, observed `lambda`, Little fallback, theoretical fallbacks, and multiple-server exact formula.
- Placeholder scan: No `TBD`, `TODO`, or unspecified implementation steps remain.
- Type consistency: Helper name `_derivar_tasas_super24_mm1` and return type `tuple[float, float]` are consistent across tests and implementation.
