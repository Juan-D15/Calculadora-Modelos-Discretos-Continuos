"""
Ventana para ingresar parámetros de la distribución hipergeométrica
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Callable, Any

import pandas as pd

from results_window import ResultsWindow
from base_window import BaseToplevelWindow


class ParameterWindow(BaseToplevelWindow):
    """
    Ventana para configurar los parámetros de la distribución hipergeométrica.
    
    Permite al usuario seleccionar la categoría de éxito e ingresar el tamaño
    de muestra y número de éxitos deseados.
    
    Attributes:
        df: DataFrame con los datos originales.
        columna: Nombre de la columna seleccionada.
        N: Total de registros en la población.
        frecuencias: Diccionario con frecuencias de cada categoría.
        K: Número de éxitos en la población (frecuencia de categoría seleccionada).
        callback_calcular: Función a llamar cuando se presiona calcular.
    """
    
    def __init__(
        self,
        master=None,
        df: pd.DataFrame = None,
        columna: str = None,
        N: int = None,
        frecuencias: Dict[str, int] = None,
        callback_calcular: Optional[Callable[[int, int, int, int], None]] = None
    ):
        """
        Inicializa la ventana de parámetros.
        
        Args:
            master: Ventana padre.
            df: DataFrame con los datos.
            columna: Nombre de la columna seleccionada.
            N: Total de registros (población).
            frecuencias: Diccionario {categoría: frecuencia}.
            callback_calcular: Función que recibe (N, K, n, x) al calcular.
        """
        super().__init__(master)
        
        if hasattr(self, '_skip_init') and self._skip_init:
            return
        
        self.df = df
        self.columna = columna
        self.N = N
        self.frecuencias = frecuencias or {}
        self.K = 0
        self.categoria_exito = None
        self.callback_calcular = callback_calcular
        
        self._configurar_ventana()
        self._crear_widgets()
        
        self.centrar_ventana(520, 530)
    
    def _configurar_ventana(self):
        """Configura las propiedades de la ventana."""
        self.title("Parámetros de Distribución Hipergeométrica")
        self.geometry("520x530")
        self.minsize(500, 500)
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
    
    def _crear_widgets(self):
        """Crea todos los widgets de la ventana."""
        self._crear_titulo()
        self._crear_panel_info()
        self._crear_panel_parametros()
        self._crear_panel_errores()
        self._crear_panel_botones()
    
    def _crear_titulo(self):
        """Crea el título de la ventana."""
        frame_titulo = ctk.CTkFrame(self, fg_color="transparent")
        frame_titulo.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))
        
        titulo = ctk.CTkLabel(
            frame_titulo,
            text="CONFIGURACIÓN DE PARÁMETROS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1f6aa5", "#1f6aa5")
        )
        titulo.pack()
        
        if self.columna:
            lbl_columna = ctk.CTkLabel(
                frame_titulo,
                text=f"Columna: {self.columna}",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            lbl_columna.pack(pady=(2, 0))
    
    def _crear_panel_info(self):
        """Crea el panel con información de la población."""
        frame_info = ctk.CTkFrame(self)
        frame_info.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        
        lbl_info_titulo = ctk.CTkLabel(
            frame_info,
            text="DATOS DE LA POBLACIÓN",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        lbl_info_titulo.pack(anchor="w", padx=10, pady=(8, 5))
        
        frame_n = ctk.CTkFrame(frame_info, fg_color="transparent")
        frame_n.pack(fill="x", padx=10, pady=2)
        
        lbl_n_label = ctk.CTkLabel(
            frame_n,
            text="Tamaño de población (N):",
            font=ctk.CTkFont(size=11),
            width=160,
            anchor="w"
        )
        lbl_n_label.pack(side="left")
        
        self.lbl_n_valor = ctk.CTkLabel(
            frame_n,
            text=str(self.N) if self.N else "--",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#3b8ed0"
        )
        self.lbl_n_valor.pack(side="left", padx=5)
        
        frame_k = ctk.CTkFrame(frame_info, fg_color="transparent")
        frame_k.pack(fill="x", padx=10, pady=2)
        
        lbl_k_label = ctk.CTkLabel(
            frame_k,
            text="Éxitos en población (K):",
            font=ctk.CTkFont(size=11),
            width=160,
            anchor="w"
        )
        lbl_k_label.pack(side="left")
        
        self.lbl_k_valor = ctk.CTkLabel(
            frame_k,
            text="-- (seleccione categoría)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#2ecc71"
        )
        self.lbl_k_valor.pack(side="left", padx=5)
        
        lbl_espacio = ctk.CTkLabel(frame_info, text="")
        lbl_espacio.pack(pady=(3, 0))
    
    def _crear_panel_parametros(self):
        """Crea el panel para ingresar parámetros."""
        frame_params = ctk.CTkFrame(self)
        frame_params.grid(row=2, column=0, sticky="ew", padx=15, pady=5)
        
        lbl_params_titulo = ctk.CTkLabel(
            frame_params,
            text="PARÁMETROS DE ENTRADA",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        lbl_params_titulo.pack(anchor="w", padx=10, pady=(8, 5))
        
        frame_categoria = ctk.CTkFrame(frame_params, fg_color="transparent")
        frame_categoria.pack(fill="x", padx=10, pady=5)
        
        lbl_categoria = ctk.CTkLabel(
            frame_categoria,
            text="Categoría de éxito:",
            font=ctk.CTkFont(size=11),
            width=140,
            anchor="w"
        )
        lbl_categoria.pack(side="left")
        
        categorias = list(self.frecuencias.keys()) if self.frecuencias else []
        self.combo_categoria = ctk.CTkComboBox(
            frame_categoria,
            values=categorias,
            command=self._on_categoria_seleccionada,
            width=220,
            state="readonly" if categorias else "disabled"
        )
        self.combo_categoria.pack(side="left", padx=5)
        if categorias:
            self.combo_categoria.set("-- Seleccione --")
        
        frame_n_muestra = ctk.CTkFrame(frame_params, fg_color="transparent")
        frame_n_muestra.pack(fill="x", padx=10, pady=5)
        
        lbl_n_muestra = ctk.CTkLabel(
            frame_n_muestra,
            text="Tamaño de muestra (n):",
            font=ctk.CTkFont(size=11),
            width=140,
            anchor="w"
        )
        lbl_n_muestra.pack(side="left")
        
        self.entry_n = ctk.CTkEntry(
            frame_n_muestra,
            width=80,
            placeholder_text="Ej: 20"
        )
        self.entry_n.pack(side="left", padx=5)
        
        lbl_n_info = ctk.CTkLabel(
            frame_n_muestra,
            text=f"(max: {self.N})" if self.N else "",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        lbl_n_info.pack(side="left")
        
        frame_x = ctk.CTkFrame(frame_params, fg_color="transparent")
        frame_x.pack(fill="x", padx=10, pady=5)
        
        lbl_x = ctk.CTkLabel(
            frame_x,
            text="Éxitos deseados (x):",
            font=ctk.CTkFont(size=11),
            width=140,
            anchor="w"
        )
        lbl_x.pack(side="left")
        
        self.entry_x = ctk.CTkEntry(
            frame_x,
            width=80,
            placeholder_text="Ej: 5"
        )
        self.entry_x.pack(side="left", padx=5)
        
        self.lbl_x_info = ctk.CTkLabel(
            frame_x,
            text="(seleccione categoría primero)",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.lbl_x_info.pack(side="left")
        
        lbl_espacio = ctk.CTkLabel(frame_params, text="")
        lbl_espacio.pack(pady=(3, 0))
    
    def _crear_panel_errores(self):
        """Crea el panel para mostrar errores de validación."""
        self.frame_errores = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_errores.grid(row=3, column=0, sticky="ew", padx=15, pady=3)
        
        self.lbl_error = ctk.CTkLabel(
            self.frame_errores,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#e74c3c",
            wraplength=420
        )
        self.lbl_error.pack(pady=2)
    
    def _crear_panel_botones(self):
        """Crea el panel con los botones de acción."""
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.grid(row=4, column=0, sticky="sew", padx=15, pady=(5, 15))
        
        self.btn_calcular = ctk.CTkButton(
            frame_botones,
            text="CALCULAR",
            command=self._calcular,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            width=130,
            fg_color="#3b8ed0",
            hover_color="#3672a9"
        )
        self.btn_calcular.pack(side="right", padx=5)
        
        self.btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="CANCELAR",
            command=self._al_cerrar,
            font=ctk.CTkFont(size=13),
            height=40,
            width=100,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.btn_cancelar.pack(side="right", padx=5)
    
    def _on_categoria_seleccionada(self, categoria: str):
        """Maneja el evento de selección de categoría de éxito."""
        if categoria.startswith("--"):
            self.K = 0
            self.categoria_exito = None
            self.lbl_k_valor.configure(text="-- (seleccione categoría)")
            self.lbl_x_info.configure(text="(seleccione categoría primero)")
            return
        
        self.categoria_exito = categoria
        self.K = self.frecuencias.get(categoria, 0)
        
        self.lbl_k_valor.configure(text=f"{self.K}")
        self.lbl_x_info.configure(text=f"(max: min({self.K}, n))")
        
        self._limpiar_error()
    
    def _validar_campos(self) -> tuple:
        """
        Valida todos los campos de entrada.
        
        Returns:
            tuple: (es_valido, mensaje_error, valores_dict)
        """
        if self.categoria_exito is None:
            return False, "Debe seleccionar una categoría de éxito.", None
        
        n_str = self.entry_n.get().strip()
        x_str = self.entry_x.get().strip()
        
        if not n_str:
            return False, "El campo 'Tamaño de muestra (n)' no puede estar vacío.", None
        
        if not x_str:
            return False, "El campo 'Éxitos deseados (x)' no puede estar vacío.", None
        
        try:
            n = int(n_str)
        except ValueError:
            return False, "El tamaño de muestra (n) debe ser un número entero.", None
        
        try:
            x = int(x_str)
        except ValueError:
            return False, "Los éxitos deseados (x) deben ser un número entero.", None
        
        if n <= 0:
            return False, "El tamaño de muestra (n) debe ser mayor a 0.", None
        
        if x < 0:
            return False, "Los éxitos deseados (x) no pueden ser negativos.", None
        
        if n > self.N:
            return False, f"El tamaño de muestra (n={n}) no puede ser mayor que la población (N={self.N}).", None
        
        if x > self.K:
            return False, f"Los éxitos deseados (x={x}) no pueden ser mayores que los éxitos en la población (K={self.K}).", None
        
        if x > n:
            return False, f"Los éxitos deseados (x={x}) no pueden ser mayores que el tamaño de muestra (n={n}).", None
        
        return True, "", {'N': self.N, 'K': self.K, 'n': n, 'x': x}
    
    def _mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error."""
        self.lbl_error.configure(text=f"❌ {mensaje}")
    
    def _limpiar_error(self):
        """Limpia el mensaje de error."""
        self.lbl_error.configure(text="")
    
    def _calcular(self):
        """Maneja el evento de calcular."""
        self._limpiar_error()
        
        es_valido, mensaje, valores = self._validar_campos()
        
        if not es_valido:
            self._mostrar_error(mensaje)
            return
        
        N = valores['N']
        K = valores['K']
        n = valores['n']
        x = valores['x']
        
        if self.callback_calcular:
            self.callback_calcular(N, K, n, x)
        else:
            self._abrir_resultados(N, K, n, x)
    
    def _abrir_resultados(self, N: int, K: int, n: int, x: int):
        """Abre la ventana de resultados con los parámetros configurados."""
        ResultsWindow(
            master=self,
            N=N,
            K=K,
            n=n,
            x=x
        )
    
    def _al_cerrar(self):
        """Maneja el cierre de la ventana."""
        super()._al_cerrar()
    
    def obtener_parametros(self) -> Optional[Dict[str, Any]]:
        """
        Retorna los parámetros configurados actualmente.
        
        Returns:
            Dict con N, K, n, x y categoria_exito, o None si no están completos.
        """
        es_valido, _, valores = self._validar_campos()
        
        if not es_valido:
            return None
        
        valores['categoria_exito'] = self.categoria_exito
        return valores
