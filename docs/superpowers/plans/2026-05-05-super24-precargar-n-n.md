# Super24 Precargar N n Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preload editable `N` and `n` fields in Super24 using simulation-derived values.

**Architecture:** Reuse the existing observed lambda derivation in `VentanaPrincipal`. Compute `N = lambda_real * horas_simulacion`, `n = lambda_real`, clamp both to safe integer values, and preload dashboard entries when scenario changes.

**Tech Stack:** Python, CustomTkinter, pytest.

---

## File Structure

- Modify `ventana_principal.py`: add `precargar_parametros_super24` helper returning `N`, `n`, `lambda`, `mu`.
- Modify `gui/dashboard.py`: call helper when scenario changes and fill `N`, `n`, `lambda`, `mu` entries.
- Modify `tests/test_super24_mm1_tasas_observadas.py`: add tests for `N/n` derivation and safety clamps.

## Rules

- `lambda_real` comes from `_derivar_tasas_super24_mm1(escenario)`.
- Simulation hours come from `w`, `wq`, and `tipo_escenario`/`nombre` using the explicit hour in names like `Día (8h)` when present; otherwise default to `1` hour.
- `N = round(lambda_real * horas)`.
- `n = round(lambda_real)`.
- `N >= 1`, `n >= 1`, and `n <= N`.

## Tasks

- [ ] Add failing tests for `N/n` derivation.
- [ ] Implement helpers in `ventana_principal.py`.
- [ ] Update dashboard preloading to set `N`, `n`, `λ`, and `μ`.
- [ ] Verify syntax and run tests if dependencies exist.

## Self-Review

- The fields remain editable after preload.
- Existing calculation flow continues reading from entry fields.
- No database schema change is needed.
