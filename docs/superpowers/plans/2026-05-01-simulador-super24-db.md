# Simulador Super24 DB Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dashboard option that imports the latest Super24 simulation from PostgreSQL and uses those records to calculate and graph Binomial, Hipergeométrica, and M/M/1 distributions.

**Architecture:** Keep database access in a small `db_connector.py` module, keep statistical model selection in `ProbabilityEngine`, and add one focused dashboard panel for DB-driven analysis. `VentanaPrincipal` orchestrates imported data into the existing result and graph components.

**Tech Stack:** Python, CustomTkinter, Matplotlib, psycopg2, python-dotenv, pytest.

---

## File Structure

- Create `db_connector.py`: PostgreSQL connection, `.env` loading, queries for latest execution, scenarios, MM1 params, and sales totals.
- Modify `requirements.txt`: add `psycopg2-binary` and `python-dotenv`.
- Modify `probability_engine.py`: add DB-sales preparation and model recommendation using 5% and 20% thresholds.
- Modify `gui/dashboard.py`: add sidebar option `Simulador Super24` and a dedicated panel with DB selectors, controls, results, and graphs.
- Modify `ventana_principal.py`: add handlers that fetch DB data, populate dashboard controls, validate inputs, and call existing calculators/graph renderers.
- Create `tests/test_probability_engine_db.py`: tests for DB-sales model recommendation.
- Create `tests/test_db_connector.py`: tests connector behavior with mocked `psycopg2.connect`.

## Task 1: Dependencies and DB Connector

**Files:**
- Create: `db_connector.py`
- Modify: `requirements.txt`
- Test: `tests/test_db_connector.py`

- [ ] **Step 1: Write failing connector tests**

Create `tests/test_db_connector.py` with mocked DB calls:

```python
from unittest.mock import MagicMock, patch

import pytest

from db_connector import DatabaseConfigError, Super24DBConnector


def test_obtener_ultima_ejecucion_devuelve_diccionario():
    connector = Super24DBConnector()
    row = {"id": 2, "fecha": "2026-05-01", "modo": "normal", "tiempo_minutos": 60, "replicas": 3}

    with patch.object(connector, "_fetch_one", return_value=row):
        assert connector.obtener_ultima_ejecucion() == row


def test_obtener_escenarios_por_ejecucion_usa_parametro():
    connector = Super24DBConnector()
    rows = [{"id": 10, "nombre": "Mañana", "lambda_h": 4.0, "mu_h": 6.0, "servidores_c": 1}]

    with patch.object(connector, "_fetch_all", return_value=rows) as fetch_all:
        assert connector.obtener_escenarios_por_ejecucion(2) == rows
        assert fetch_all.call_args.args[1] == (2,)


def test_obtener_ventas_por_categoria_agrupa_totales():
    connector = Super24DBConnector()
    rows = [{"categoria": "Bebidas", "unidades_promedio": 12}]

    with patch.object(connector, "_fetch_all", return_value=rows):
        assert connector.obtener_ventas_por_categoria(10) == rows


def test_db_name_es_obligatorio(monkeypatch):
    monkeypatch.delenv("DB_NAME", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)

    with pytest.raises(DatabaseConfigError):
        Super24DBConnector()._build_config()
```

- [ ] **Step 2: Run connector tests to verify failure**

Run: `pytest tests/test_db_connector.py -v`

Expected: FAIL because `db_connector.py` does not exist.

- [ ] **Step 3: Implement connector and dependencies**

Add `psycopg2-binary` and `python-dotenv` to `requirements.txt`.

Create `db_connector.py` with:

```python
"""
Conector PostgreSQL para importar datos del simulador Super24.
"""
import os
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


class DatabaseConfigError(Exception):
    """Error cuando faltan variables de configuración de base de datos."""


class DatabaseQueryError(Exception):
    """Error al consultar la base de datos."""


class Super24DBConnector:
    """Conector para consultar corridas y resultados del simulador Super24."""

    def __init__(self) -> None:
        load_dotenv()

    def _build_config(self) -> Dict[str, Any]:
        db_name = os.getenv("DB_NAME") or os.getenv("POSTGRES_DB")
        if not db_name:
            raise DatabaseConfigError("Debe definir DB_NAME en el archivo .env")

        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "dbname": db_name,
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", ""),
        }

    def _connect(self):
        return psycopg2.connect(**self._build_config())

    def _fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        try:
            with self._connect() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params or ())
                    row = cursor.fetchone()
                    return dict(row) if row else None
        except DatabaseConfigError:
            raise
        except Exception as exc:
            raise DatabaseQueryError(f"Error al consultar la base de datos: {exc}") from exc

    def _fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        try:
            with self._connect() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params or ())
                    return [dict(row) for row in cursor.fetchall()]
        except DatabaseConfigError:
            raise
        except Exception as exc:
            raise DatabaseQueryError(f"Error al consultar la base de datos: {exc}") from exc

    def obtener_ultima_ejecucion(self) -> Optional[Dict[str, Any]]:
        query = """
            SELECT id, fecha, modo, tiempo_minutos, replicas
            FROM ejecucion_simulacion
            ORDER BY fecha DESC, id DESC
            LIMIT 1
        """
        return self._fetch_one(query)

    def obtener_escenarios_por_ejecucion(self, ejecucion_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT id, ejecucion_id, nombre, lambda_h, mu_h, servidores_c, rho, wq, w, lq
            FROM escenario_resultado
            WHERE ejecucion_id = %s
            ORDER BY id ASC
        """
        return self._fetch_all(query, (ejecucion_id,))

    def obtener_parametros_mm1(self, escenario_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT id, nombre, lambda_h, mu_h, servidores_c, rho, wq, w, lq
            FROM escenario_resultado
            WHERE id = %s
        """
        return self._fetch_one(query, (escenario_id,))

    def obtener_ventas_por_categoria(self, escenario_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT categoria, SUM(unidades_promedio)::integer AS unidades_promedio
            FROM ventas_escenario
            WHERE escenario_id = %s
            GROUP BY categoria
            ORDER BY categoria ASC
        """
        return self._fetch_all(query, (escenario_id,))
```

- [ ] **Step 4: Run connector tests to verify pass**

Run: `pytest tests/test_db_connector.py -v`
Expected: PASS.

## Task 2: Probability Engine DB Sales Recommendation

**Files:**
- Modify: `probability_engine.py`
- Test: `tests/test_probability_engine_db.py`

- [ ] **Step 1: Write failing engine tests**

Create `tests/test_probability_engine_db.py`:

```python
import pytest

from probability_engine import ParametrosInvalidosError, ProbabilityEngine


def test_preparar_parametros_recomienda_binomial_hasta_5_por_ciento():
    datos = ProbabilityEngine().preparar_parametros_desde_ventas(N=1000, K=80, n=50)
    assert datos["p"] == pytest.approx(0.08)
    assert datos["modelo_recomendado"] == "Binomial"
    assert datos["usa_correccion_finita"] is False


def test_preparar_parametros_recomienda_binomial_entre_5_y_20():
    datos = ProbabilityEngine().preparar_parametros_desde_ventas(N=1000, K=80, n=100)
    assert datos["modelo_recomendado"] == "Binomial"
    assert datos["usa_correccion_finita"] is True


def test_preparar_parametros_recomienda_hipergeometrica_desde_20():
    datos = ProbabilityEngine().preparar_parametros_desde_ventas(N=1000, K=80, n=200)
    assert datos["modelo_recomendado"] == "Hipergeométrica"


def test_preparar_parametros_rechaza_k_mayor_que_n():
    with pytest.raises(ParametrosInvalidosError):
        ProbabilityEngine().preparar_parametros_desde_ventas(N=10, K=12, n=5)
```

- [ ] **Step 2: Run engine tests to verify failure**

Run: `pytest tests/test_probability_engine_db.py -v`
Expected: FAIL because `preparar_parametros_desde_ventas` does not exist.

- [ ] **Step 3: Implement engine methods**

In `ProbabilityEngine`, add constants and methods:

```python
UMBRAL_POBLACION_INFINITA = 0.05
UMBRAL_HIPERGEOMETRICA = 0.20

def recomendar_modelo_por_umbral(self, n: int, N: int) -> Dict[str, object]:
    if N is None or N <= 0:
        raise ParametrosInvalidosError("El inventario/población (N) debe ser mayor a 0.")
    if n is None or n <= 0:
        raise ParametrosInvalidosError("El tamaño de muestra (n) debe ser mayor a 0.")
    if n > N:
        raise ParametrosInvalidosError(f"n ({n}) no puede ser mayor que N ({N}).")

    proporcion = n / N
    if proporcion >= self.UMBRAL_HIPERGEOMETRICA:
        return {"modelo_recomendado": "Hipergeométrica", "usa_correccion_finita": True, "porcentaje_muestra": proporcion * 100, "motivo": "n representa 20% o más de N"}
    if proporcion > self.UMBRAL_POBLACION_INFINITA:
        return {"modelo_recomendado": "Binomial", "usa_correccion_finita": True, "porcentaje_muestra": proporcion * 100, "motivo": "n supera 5% de N, pero no alcanza 20%"}
    return {"modelo_recomendado": "Binomial", "usa_correccion_finita": False, "porcentaje_muestra": proporcion * 100, "motivo": "n es menor o igual al 5% de N"}

def preparar_parametros_desde_ventas(self, N: int, K: int, n: int) -> Dict[str, object]:
    if K is None or K < 0:
        raise ParametrosInvalidosError("K no puede ser negativo.")
    if K > N:
        raise ParametrosInvalidosError(f"K ({K}) no puede ser mayor que N ({N}).")
    recomendacion = self.recomendar_modelo_por_umbral(n, N)
    return {"N": N, "K": K, "n": n, "p": K / N, **recomendacion}
```

- [ ] **Step 4: Run engine tests to verify pass**

Run: `pytest tests/test_probability_engine_db.py -v`
Expected: PASS.

## Task 3: Dashboard Panel for Super24

**Files:**
- Modify: `gui/dashboard.py`

- [ ] **Step 1: Add sidebar button and state fields**

Add fields for `campos_super24`, `datos_super24`, `combo_super24_escenario`, `combo_super24_categoria`, `combo_super24_distribucion`, entries for `N`, `n`, `x`, and optional MM1 `n`.

- [ ] **Step 2: Add `crear_interfaz_super24`**

Create a panel with buttons and entries. Commands should call `ventana_principal.cargar_datos_super24()` and `ventana_principal.calcular_super24()`.

- [ ] **Step 3: Add helper methods**

Add `actualizar_datos_super24`, `obtener_campos_super24`, `mostrar_resultados_super24`, and graph wrappers that reuse `AreaResultados`, `GraficoBinomial`, and `GraficoMM1`.

## Task 4: VentanaPrincipal Super24 Orchestration

**Files:**
- Modify: `ventana_principal.py`

- [ ] **Step 1: Import dependencies**

Import `Super24DBConnector`, connector errors, and `ProbabilityEngine`.

- [ ] **Step 2: Implement `cargar_datos_super24`**

Fetch latest execution, scenarios, and sales per scenario; pass normalized payload to `dashboard.actualizar_datos_super24`.

- [ ] **Step 3: Implement `calcular_super24`**

For `M/M/1`, use selected scenario `lambda_h` and `mu_h`. For Binomial/Hipergeométrica/Automática, use selected category units as `K`, user `N`, `n`, `x`, and `ProbabilityEngine.preparar_parametros_desde_ventas` to select or validate model.

- [ ] **Step 4: Render existing result and graph components**

For Binomial use existing `mostrar_resultados_binomial` and `crear_grafico`; for Hipergeométrica use existing `mostrar_resultados_hipergeometrica` and `crear_grafico_hipergeometrica`; for M/M/1 use existing `mostrar_resultados_mm1` and `GraficoMM1`.

## Task 5: Verification

**Files:**
- No new files.

- [ ] **Step 1: Run focused tests**

Run: `pytest tests/test_db_connector.py tests/test_probability_engine_db.py -v`
Expected: PASS.

- [ ] **Step 2: Run full tests**

Run: `pytest tests/ -v`
Expected: PASS or report unrelated pre-existing failures.

- [ ] **Step 3: Smoke-check imports**

Run: `python -m py_compile db_connector.py probability_engine.py ventana_principal.py gui/dashboard.py`
Expected: no output and exit code 0.

## Self-Review

- Spec coverage: connector, `.env`, latest execution, scenario/category selection, model recommendation, dashboard option, results, and graphs are covered.
- Placeholder scan: no TBD/TODO placeholders remain.
- Type consistency: DB rows are dictionaries; GUI selection values are strings; calculation inputs convert to `int`/`float` at orchestration boundary.
