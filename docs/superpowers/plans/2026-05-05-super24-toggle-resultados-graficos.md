# Super24 Toggle Resultados Graficos Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `Resultados / Gráficos` selector to Simulador Super24 so every Super24 distribution can show results and graphs in full-width alternate views.

**Architecture:** Reuse the existing M/M/1 segmented-button pattern in `gui/dashboard.py`, but scope it to Super24. Keep result rendering through `AreaResultados` and graph rendering through the existing `GraficoBinomial`/`GraficoMM1` instances.

**Tech Stack:** Python, CustomTkinter, Matplotlib wrappers.

---

## File Structure

- Modify `gui/dashboard.py`: add Super24 toggle state, two alternate frames, and a view switcher.
- Modify `ventana_principal.py`: after each Super24 calculation, switch the Super24 view back to `Resultados`.

### Task 1: Add Super24 Toggle Layout

**Files:**
- Modify: `gui/dashboard.py`

- [ ] Add instance attributes for `toggle_super24`, `results_super24_frame`, and `graph_super24_frame`.
- [ ] Replace the split `results_frame` grid with one full-width container and two stacked frames.
- [ ] Create `AreaResultados` in the results frame and both graph objects in the graph frame.

### Task 2: Add Super24 View Switching

**Files:**
- Modify: `gui/dashboard.py`

- [ ] Add `_cambiar_vista_super24(self, valor)` to show one frame and hide the other.
- [ ] Add `mostrar_vista_resultados_super24(self)` to reset the segmented button to `Resultados` after calculation.

### Task 3: Reset View After Super24 Calculation

**Files:**
- Modify: `ventana_principal.py`

- [ ] Call `self.dashboard.mostrar_vista_resultados_super24()` before/after rendering Super24 results for Binomial, Hipergeométrica, Poisson, and M/M/1.

### Task 4: Verify

**Files:**
- Test: `gui/dashboard.py`, `ventana_principal.py`

- [ ] Run `python -m py_compile ventana_principal.py gui/dashboard.py`.
- [ ] Run focused tests if `pytest` is installed; otherwise document the missing dependency.

## Self-Review

- Scope is only Super24, matching user choice.
- The existing main M/M/1 screen remains unchanged.
- Results and graph widgets keep existing responsibilities.
