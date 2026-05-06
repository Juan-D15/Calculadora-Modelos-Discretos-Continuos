"""
Pruebas para formateo de escenarios Super24 en el dashboard.
"""

from gui.dashboard import Dashboard


def test_formatear_escenario_super24_incluye_tipo_si_existe():
    """Debe prefijar la opción con la sección del escenario."""
    escenario = {"id": 166, "nombre": "Día (8h)", "tipo_escenario": "Día"}

    texto = Dashboard._formatear_escenario_super24(escenario)

    assert texto == "Día | 166 - Día (8h)"


def test_formatear_escenario_super24_mantiene_formato_si_no_hay_tipo():
    """Debe conservar compatibilidad si el escenario no trae tipo."""
    escenario = {"id": 166, "nombre": "Día (8h)"}

    texto = Dashboard._formatear_escenario_super24(escenario)

    assert texto == "166 - Día (8h)"
