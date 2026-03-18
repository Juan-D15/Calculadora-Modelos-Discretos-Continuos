# Tests de widget de tabla comparativa de Poisson
import customtkinter as ctk
from gui.tabla_comparacion_poisson import TablaComparacionPoisson


def test_tabla_comparacion_poisson_initialization():
    """Test widget initialization"""
    root = ctk.CTk()
    widget = TablaComparacionPoisson(root)

    assert widget.datos_completos is None
    assert widget.k_destacado is None
    assert widget.es_expandido is False

    root.destroy()


def test_tabla_comparacion_poisson_mostrar_acotada():
    """Test displaying bounded table"""
    root = ctk.CTk()
    widget = TablaComparacionPoisson(root)

    valores_k = list(range(100))  # 0 to 99
    probs_binom = [0.01] * 100
    probs_poisson = [0.01] * 100
    k_destacado = 50

    widget.mostrar_tabla_acotada(valores_k, probs_binom, probs_poisson, k_destacado)

    assert widget.k_destacado == 50
    assert widget.es_expandido is False
    assert widget.datos_completos is not None

    root.destroy()


def test_tabla_comparacion_poisson_expansion():
    """Test table expansion"""
    root = ctk.CTk()
    widget = TablaComparacionPoisson(root)

    valores_k = list(range(20))
    probs_binom = [0.05] * 20
    probs_poisson = [0.05] * 20

    widget.mostrar_tabla_acotada(valores_k, probs_binom, probs_poisson, 10)
    widget.mostrar_tabla_completa()

    assert widget.es_expandido is True

    root.destroy()
