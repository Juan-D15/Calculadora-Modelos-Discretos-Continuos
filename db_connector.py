"""
Conector PostgreSQL para importar datos del simulador Super24.
"""
import os
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


class DatabaseConfigError(Exception):
    """Error cuando faltan variables de configuración de base de datos."""


class DatabaseQueryError(Exception):
    """Error al consultar la base de datos."""


class Super24DBConnector:
    """Conector para consultar corridas y resultados del simulador Super24."""

    def __init__(self) -> None:
        load_dotenv()

    def _build_config(self) -> Dict[str, Any]:
        """
        Construye la configuración de conexión desde variables de entorno.

        Returns:
            dict: Parámetros aceptados por psycopg2.connect.
        """
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
        """Crea una conexión PostgreSQL."""
        return psycopg2.connect(**self._build_config())

    def _fetch_one(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> Optional[Dict[str, Any]]:
        """Ejecuta una consulta y retorna una fila."""
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

    def _fetch_all(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> List[Dict[str, Any]]:
        """Ejecuta una consulta y retorna todas las filas."""
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
        """
        Extrae la última corrida de simulación.

        Returns:
            dict | None: Registro de ejecucion_simulacion más reciente.
        """
        query = """
            SELECT id, fecha, modo, tiempo_minutos, replicas
            FROM ejecucion_simulacion
            ORDER BY fecha DESC, id DESC
            LIMIT 1
        """
        return self._fetch_one(query)

    def obtener_escenarios_por_ejecucion(self, ejecucion_id: int) -> List[Dict[str, Any]]:
        """
        Extrae escenarios asociados a una ejecución.

        Args:
            ejecucion_id (int): Identificador de la corrida.

        Returns:
            list[dict]: Escenarios con parámetros de cola y métricas.
        """
        query = """
            SELECT id, ejecucion_id, nombre, lambda_h, mu_h, servidores_c, rho, wq, w, lq,
                   serie_cola
            FROM escenario_resultado
            WHERE ejecucion_id = %s
            ORDER BY id DESC
            LIMIT 5
        """
        return self._fetch_all(query, (ejecucion_id,))

    def obtener_ultimos_escenarios(self, limite: int = 5) -> List[Dict[str, Any]]:
        """
        Extrae los últimos escenarios registrados, sin filtrar por corrida.

        Args:
            limite (int): Cantidad máxima de escenarios a retornar.

        Returns:
            list[dict]: Escenarios más recientes con parámetros de cola y métricas.
        """
        query = """
            SELECT id, ejecucion_id, nombre, lambda_h, mu_h, servidores_c, rho, wq, w, lq,
                   serie_cola
            FROM escenario_resultado
            ORDER BY id DESC
            LIMIT %s
        """
        return self._fetch_all(query, (limite,))

    def obtener_ultimos_escenarios_por_tipo(
        self, limite_por_tipo: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Extrae los últimos escenarios registrados por tipo de periodo.

        Args:
            limite_por_tipo (int): Cantidad máxima de escenarios por tipo.

        Returns:
            list[dict]: Escenarios recientes agrupados por tipo.
        """
        query = """
            WITH escenarios_clasificados AS (
                SELECT
                    id,
                    ejecucion_id,
                    nombre,
                    lambda_h,
                    mu_h,
                    servidores_c,
                    rho,
                    wq,
                    w,
                    lq,
                    serie_cola,
                    CASE
                        WHEN nombre ILIKE '%%día%%' OR nombre ILIKE '%%dia%%' THEN 'Día'
                        WHEN nombre ILIKE '%%mes%%'
                            OR nombre ILIKE '%%mensual%%'
                            OR nombre ILIKE '%%mensuales%%' THEN 'Mes'
                        WHEN nombre ILIKE '%%semana%%' THEN 'Semana'
                        WHEN nombre ILIKE '%%mañana%%' OR nombre ILIKE '%%manana%%' THEN 'Mañana'
                        WHEN nombre ILIKE '%%mediodía%%' OR nombre ILIKE '%%mediodia%%' THEN 'Mediodía'
                        WHEN nombre ILIKE '%%noche%%' THEN 'Noche'
                        ELSE 'Otros'
                    END AS tipo_escenario
                FROM escenario_resultado
            ), escenarios_numerados AS (
                SELECT
                    *,
                    ROW_NUMBER() OVER (
                        PARTITION BY tipo_escenario
                        ORDER BY id DESC
                    ) AS rn
                FROM escenarios_clasificados
            )
            SELECT
                id,
                ejecucion_id,
                nombre,
                lambda_h,
                mu_h,
                servidores_c,
                rho,
                wq,
                w,
                lq,
                serie_cola,
                tipo_escenario
            FROM escenarios_numerados
            WHERE rn <= %s
            ORDER BY
                CASE tipo_escenario
                    WHEN 'Día' THEN 1
                    WHEN 'Mes' THEN 2
                    WHEN 'Semana' THEN 3
                    WHEN 'Mañana' THEN 4
                    WHEN 'Mediodía' THEN 5
                    WHEN 'Noche' THEN 6
                    ELSE 7
                END,
                id DESC
        """
        return self._fetch_all(query, (limite_por_tipo,))

    def obtener_parametros_mm1(self, escenario_id: int) -> Optional[Dict[str, Any]]:
        """
        Extrae λ y μ para alimentar el modelo M/M/1.

        Args:
            escenario_id (int): Identificador del escenario.

        Returns:
            dict | None: Parámetros y métricas del escenario.
        """
        query = """
            SELECT id, nombre, lambda_h, mu_h, servidores_c, rho, wq, w, lq, serie_cola
            FROM escenario_resultado
            WHERE id = %s
        """
        return self._fetch_one(query, (escenario_id,))

    def obtener_ventas_por_categoria(self, escenario_id: int) -> List[Dict[str, Any]]:
        """
        Extrae sumatorias de unidades vendidas por categoría.

        Args:
            escenario_id (int): Identificador del escenario.

        Returns:
            list[dict]: Categoría y unidades promedio agregadas como K esperado.
        """
        query = """
            SELECT categoria, SUM(unidades_promedio)::integer AS unidades_promedio
            FROM ventas_escenario
            WHERE escenario_id = %s
            GROUP BY categoria
            ORDER BY categoria ASC
        """
        return self._fetch_all(query, (escenario_id,))
