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


def test_precargar_parametros_super24_deriva_n_y_n_desde_lambda_y_horas():
    """Debe calcular N=lambda*horas y n=lambda para precargar campos editables."""
    escenario = {
        "nombre": "Día (8h)",
        "lambda_h": 4.0,
        "mu_h": 5.0,
        "w": 12.0,
        "wq": 2.0,
        "rho": 0.5,
        "servidores_c": 2,
        "lq": 0.0,
    }

    parametros = _ventana().precargar_parametros_super24(escenario)

    assert parametros["lambda"] == pytest.approx(6.0)
    assert parametros["mu"] == pytest.approx(6.0)
    assert parametros["N"] == 48
    assert parametros["n"] == 6


def test_precargar_parametros_super24_no_permite_n_mayor_que_n_total():
    """Debe ajustar n para que no supere N cuando la duración sea menor a una hora."""
    escenario = {
        "nombre": "Escenario corto (0.5h)",
        "lambda_h": 10.0,
        "mu_h": 20.0,
        "w": 1.0,
        "wq": 1.0,
        "rho": 0.0,
        "servidores_c": 1,
        "lq": 0.0,
    }

    parametros = _ventana().precargar_parametros_super24(escenario)

    assert parametros["N"] == 5
    assert parametros["n"] == 5


def test_derivar_horas_usa_tipo_escenario_cuando_no_hay_horas_en_nombre():
    """Debe usar tipo_escenario para derivar horas cuando el nombre no tiene formato Xh."""
    ventana = _ventana()
    
    assert ventana._derivar_horas_simulacion_super24({"nombre": "Día", "tipo_escenario": "Día"}) == 8.0
    assert ventana._derivar_horas_simulacion_super24({"nombre": "Semana", "tipo_escenario": "Semana"}) == 40.0
    assert ventana._derivar_horas_simulacion_super24({"nombre": "Mes", "tipo_escenario": "Mes"}) == 160.0
    assert ventana._derivar_horas_simulacion_super24({"nombre": "Mañana", "tipo_escenario": "Mañana"}) == 4.0
    assert ventana._derivar_horas_simulacion_super24({"nombre": "Mediodía", "tipo_escenario": "Mediodía"}) == 4.0
    assert ventana._derivar_horas_simulacion_super24({"nombre": "Noche", "tipo_escenario": "Noche"}) == 8.0


def test_precargar_parametros_super24_usa_tipo_escenario():
    """Debe calcular N=λ*8 y n=λ cuando el tipo es Día sin horas en el nombre."""
    escenario = {
        "nombre": "Día",
        "tipo_escenario": "Día",
        "lambda_h": 4.0,
        "mu_h": 5.0,
        "w": 12.0,
        "wq": 2.0,
        "rho": 0.5,
        "servidores_c": 2,
        "lq": 0.0,
    }

    parametros = _ventana().precargar_parametros_super24(escenario)

    assert parametros["lambda"] == pytest.approx(6.0)
    assert parametros["mu"] == pytest.approx(6.0)
    assert parametros["N"] == 48
    assert parametros["n"] == 6
