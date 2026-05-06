# Super24 Escenarios Por Seccion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Show the latest five Super24 scenarios for each scenario type in the scenario combo, grouped by section.

**Architecture:** Classify scenarios in PostgreSQL using `CASE` on `nombre`, rank each section with `ROW_NUMBER()`, and return rows where rank is at most five. The dashboard keeps a flat `CTkComboBox` but prefixes each selectable option with its section.

**Tech Stack:** Python, PostgreSQL SQL window functions, CustomTkinter, pytest.

---

## File Structure

- Modify `db_connector.py`: add grouped query method for latest five per scenario type.
- Modify `ventana_principal.py`: load grouped scenarios instead of five global scenarios.
- Modify `gui/dashboard.py`: format scenario options with section prefix and resolve selected rows correctly.
- Modify `tests/test_db_connector.py`: assert query contains classification, partition ranking, and limit per section.
- Create `tests/test_dashboard_super24.py`: test scenario option formatting without constructing the UI.

## Tasks

- [ ] Add failing tests for grouped query and dashboard formatting.
- [ ] Implement grouped query with `CASE`, `ROW_NUMBER() OVER (PARTITION BY tipo_escenario ORDER BY id DESC)`, `rn <= %s`, and section ordering.
- [ ] Use grouped query in `cargar_datos_super24`.
- [ ] Prefix combo items as `Tipo | id - nombre`, using `tipo_escenario` from the query.
- [ ] Keep selection resolution working by comparing the new formatted string.
- [ ] Verify syntax and run tests if dependencies are available.

## Self-Review

- Scope is limited to the Super24 scenario list.
- Existing calculation behavior remains unchanged.
- The combo remains selectable; no non-selectable separator rows are introduced.
