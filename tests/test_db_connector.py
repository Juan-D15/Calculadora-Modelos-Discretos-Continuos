"""
Pruebas unitarias para el conector PostgreSQL del simulador Super24.
"""
from unittest.mock import patch

import pytest

from db_connector import DatabaseConfigError, Super24DBConnector


def test_obtener_ultima_ejecucion_devuelve_diccionario():
    """Debe retornar la última ejecución como diccionario."""
    connector = Super24DBConnector()
    row = {
        "id": 2,
        "fecha": "2026-05-01",
        "modo": "normal",
        "tiempo_minutos": 60,
        "replicas": 3,
    }

    with patch.object(connector, "_fetch_one", return_value=row):
        assert connector.obtener_ultima_ejecucion() == row


def test_obtener_escenarios_por_ejecucion_usa_parametro():
    """Debe consultar escenarios usando el id de ejecución como parámetro."""
    connector = Super24DBConnector()
    rows = [
        {
            "id": 10,
            "nombre": "Mañana",
            "lambda_h": 4.0,
            "mu_h": 6.0,
            "servidores_c": 1,
        }
    ]

    with patch.object(connector, "_fetch_all", return_value=rows) as fetch_all:
        assert connector.obtener_escenarios_por_ejecucion(2) == rows
        assert fetch_all.call_args.args[1] == (2,)


def test_obtener_escenarios_por_ejecucion_incluye_serie_cola():
    """Debe traer serie_cola porque el esquema actual la guarda en escenario_resultado."""
    connector = Super24DBConnector()

    with patch.object(connector, "_fetch_all", return_value=[]) as fetch_all:
        connector.obtener_escenarios_por_ejecucion(2)

    query = fetch_all.call_args.args[0]
    assert "serie_cola" in query


def test_obtener_escenarios_por_ejecucion_ordena_ultimo_primero():
    """Debe listar escenarios del más reciente al más antiguo."""
    connector = Super24DBConnector()

    with patch.object(connector, "_fetch_all", return_value=[]) as fetch_all:
        connector.obtener_escenarios_por_ejecucion(2)

    query = fetch_all.call_args.args[0]
    assert "ORDER BY id DESC" in query


def test_obtener_escenarios_por_ejecucion_limita_a_ultimos_cinco():
    """Debe consultar solo los últimos cinco escenarios registrados."""
    connector = Super24DBConnector()

    with patch.object(connector, "_fetch_all", return_value=[]) as fetch_all:
        connector.obtener_escenarios_por_ejecucion(2)

    query = fetch_all.call_args.args[0]
    assert "LIMIT 5" in query


def test_obtener_ultimos_escenarios_no_filtra_por_ejecucion():
    """Debe traer los últimos cinco escenarios globales, no solo de una corrida."""
    connector = Super24DBConnector()

    with patch.object(connector, "_fetch_all", return_value=[]) as fetch_all:
        connector.obtener_ultimos_escenarios(limite=5)

    query = fetch_all.call_args.args[0]
    assert "WHERE ejecucion_id" not in query
    assert "ORDER BY id DESC" in query
    assert "LIMIT %s" in query
    assert fetch_all.call_args.args[1] == (5,)


def test_obtener_ultimos_escenarios_por_tipo_limita_cinco_por_seccion():
    """Debe traer los últimos cinco escenarios por cada tipo reconocido."""
    connector = Super24DBConnector()

    with patch.object(connector, "_fetch_all", return_value=[]) as fetch_all:
        connector.obtener_ultimos_escenarios_por_tipo(limite_por_tipo=5)

    query = fetch_all.call_args.args[0]
    assert "tipo_escenario" in query
    assert "ROW_NUMBER() OVER" in query
    assert "PARTITION BY tipo_escenario" in query
    assert "rn <= %s" in query
    assert "Mañana" in query
    assert "Mediodía" in query
    assert "Noche" in query
    assert fetch_all.call_args.args[1] == (5,)


def test_obtener_ultimos_escenarios_por_tipo_escapa_porcentajes_psycopg2():
    """Debe escapar % literales para que psycopg2 no los trate como parámetros."""
    connector = Super24DBConnector()

    with patch.object(connector, "_fetch_all", return_value=[]) as fetch_all:
        connector.obtener_ultimos_escenarios_por_tipo(limite_por_tipo=5)

    query = fetch_all.call_args.args[0]
    assert "ILIKE '%%día%%'" in query
    assert "ILIKE '%%mes%%'" in query
    assert "ILIKE '%%noche%%'" in query


def test_obtener_ultimos_escenarios_por_tipo_reconoce_mensual():
    """Debe clasificar nombres mensual/mensuales dentro de la sección Mes."""
    connector = Super24DBConnector()

    with patch.object(connector, "_fetch_all", return_value=[]) as fetch_all:
        connector.obtener_ultimos_escenarios_por_tipo(limite_por_tipo=5)

    query = fetch_all.call_args.args[0]
    assert "ILIKE '%%mensual%%'" in query
    assert "ILIKE '%%mensuales%%'" in query


def test_obtener_parametros_mm1_incluye_serie_cola():
    """Debe traer serie_cola al consultar un escenario puntual."""
    connector = Super24DBConnector()

    with patch.object(connector, "_fetch_one", return_value=None) as fetch_one:
        connector.obtener_parametros_mm1(10)

    query = fetch_one.call_args.args[0]
    assert "serie_cola" in query


def test_obtener_ventas_por_categoria_agrupa_totales():
    """Debe devolver ventas agregadas por categoría para el escenario."""
    connector = Super24DBConnector()
    rows = [{"categoria": "Bebidas", "unidades_promedio": 12}]

    with patch.object(connector, "_fetch_all", return_value=rows):
        assert connector.obtener_ventas_por_categoria(10) == rows


def test_db_name_es_obligatorio(monkeypatch):
    """Debe exigir nombre de base de datos en variables de entorno."""
    monkeypatch.delenv("DB_NAME", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)

    with pytest.raises(DatabaseConfigError):
        Super24DBConnector.__new__(Super24DBConnector)._build_config()
