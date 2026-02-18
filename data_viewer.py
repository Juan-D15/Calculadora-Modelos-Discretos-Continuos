"""
Ventana para visualizar y seleccionar datos de archivos cargados
"""
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from typing import Optional, Dict, Callable

import pandas as pd

from utils.file_loader import (
    FileLoader,
    ErrorCargaArchivo,
    ArchivoNoSeleccionadoError,
    ArchivoVacioError,
    ArchivoSinEncabezadosError,
    FormatoNoSoportadoError
)

from parameter_window import ParameterWindow
from base_window import BaseToplevelWindow


class DataViewerWindow(BaseToplevelWindow):
    """
    Ventana para cargar, visualizar y seleccionar datos de archivos.
    
    Permite cargar archivos CSV/Excel, visualizar los datos en una tabla,
    seleccionar una columna y ver sus frecuencias para continuar al análisis.
    
    Attributes:
        df: DataFrame con los datos cargados.
        loader: Instancia de FileLoader para cargar archivos.
        columna_seleccionada: Nombre de la columna seleccionada.
        frecuencias: Diccionario con frecuencias de la columna seleccionada.
    """
    
    def __init__(
        self, 
        master=None, 
        callback_continuar: Optional[Callable] = None
    ):
        """
        Inicializa la ventana de visualización de datos.
        
        Args:
            master: Ventana padre (opcional).
            callback_continuar: Función callback que se llama al presionar
                               "Continuar al Análisis". Recibe (df, columna, N, frecuencias).
        """
        super().__init__(master)
        
        if hasattr(self, '_skip_init') and self._skip_init:
            return
        
        self.df = None
        self.loader = FileLoader()
        self.columna_seleccionada = None
        self.frecuencias = None
        self.callback_continuar = callback_continuar
        
        self._configurar_ventana()
        self._crear_widgets()
        self._configurar_estilo_treeview()
        
        self.centrar_ventana(1100, 750)
    
    def _configurar_ventana(self):
        """Configura las propiedades de la ventana."""
        self.title("Visualizador de Datos")
        self.geometry("1100x750")
        self.minsize(900, 600)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def _configurar_estilo_treeview(self):
        """Configura el estilo oscuro para el Treeview."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        selected_color = "#3b8ed0"
        border_color = "#555555"
        
        self.style.configure(
            "Custom.Treeview",
            background=bg_color,
            foreground=fg_color,
            fieldbackground=bg_color,
            bordercolor=border_color,
            borderwidth=1
        )
        
        self.style.configure(
            "Custom.Treeview.Heading",
            background="#3b3b3b",
            foreground=fg_color,
            bordercolor=border_color,
            borderwidth=1,
            font=('Segoe UI', 10, 'bold')
        )
        
        self.style.map(
            "Custom.Treeview",
            background=[('selected', selected_color)],
            foreground=[('selected', '#ffffff')]
        )
        
        self.style.map(
            "Custom.Treeview.Heading",
            background=[('active', '#4a4a4a')]
        )
    
    def _crear_widgets(self):
        """Crea todos los widgets de la ventana."""
        self._crear_panel_superior()
        self._crear_panel_tabla()
        self._crear_panel_inferior()
    
    def _crear_panel_superior(self):
        """Crea el panel superior con el botón de cargar."""
        panel_superior = ctk.CTkFrame(self, fg_color="transparent")
        panel_superior.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        panel_superior.grid_columnconfigure(1, weight=1)
        
        titulo = ctk.CTkLabel(
            panel_superior,
            text="VISUALIZADOR DE DATOS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f6aa5", "#1f6aa5")
        )
        titulo.grid(row=0, column=0, sticky="w", padx=5)
        
        self.btn_cargar = ctk.CTkButton(
            panel_superior,
            text="Cargar Archivo",
            command=self._cargar_archivo,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=150,
            fg_color="#3b8ed0",
            hover_color="#3672a9"
        )
        self.btn_cargar.grid(row=0, column=1, sticky="e", padx=5)
        
        self.lbl_archivo = ctk.CTkLabel(
            panel_superior,
            text="Ningún archivo cargado",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.lbl_archivo.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=(5, 0))
    
    def _crear_panel_tabla(self):
        """Crea el panel con la tabla de datos."""
        panel_tabla = ctk.CTkFrame(self)
        panel_tabla.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        panel_tabla.grid_columnconfigure(0, weight=1)
        panel_tabla.grid_rowconfigure(0, weight=1)
        
        frame_tree = ctk.CTkFrame(panel_tabla, fg_color="transparent")
        frame_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame_tree.grid_columnconfigure(0, weight=1)
        frame_tree.grid_rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(frame_tree, style="Custom.Treeview", show='headings')
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        
        scrollbar_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.lbl_info_tabla = ctk.CTkLabel(
            panel_tabla,
            text="Cargue un archivo para ver los datos",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.lbl_info_tabla.grid(row=1, column=0, pady=5)
    
    def _crear_panel_inferior(self):
        """Crea el panel inferior con selección de columna y análisis."""
        panel_inferior = ctk.CTkFrame(self, fg_color="transparent")
        panel_inferior.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 15))
        panel_inferior.grid_columnconfigure(1, weight=1)
        
        frame_seleccion = ctk.CTkFrame(panel_inferior, fg_color="transparent")
        frame_seleccion.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        
        lbl_columna = ctk.CTkLabel(
            frame_seleccion,
            text="Seleccionar columna:",
            font=ctk.CTkFont(size=13)
        )
        lbl_columna.pack(side="left", padx=(0, 10))
        
        self.combo_columnas = ctk.CTkComboBox(
            frame_seleccion,
            values=["-- Cargue un archivo primero --"],
            command=self._on_columna_seleccionada,
            width=300,
            state="disabled"
        )
        self.combo_columnas.pack(side="left", padx=5)
        
        frame_info = ctk.CTkFrame(panel_inferior)
        frame_info.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
        
        self.lbl_total_registros = ctk.CTkLabel(
            frame_info,
            text="Total de registros (N): --",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.lbl_total_registros.pack(fill="x", padx=10, pady=(10, 5))
        
        lbl_frec_titulo = ctk.CTkLabel(
            frame_info,
            text="Frecuencias de categorías:",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        lbl_frec_titulo.pack(fill="x", padx=10, pady=(5, 2))
        
        frame_frecuencias = ctk.CTkScrollableFrame(
            frame_info,
            height=120,
            fg_color="transparent"
        )
        frame_frecuencias.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.frame_frecuencias = frame_frecuencias
        
        self.lbl_frecuencia_placeholder = ctk.CTkLabel(
            frame_frecuencias,
            text="Seleccione una columna para ver las frecuencias",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.lbl_frecuencia_placeholder.pack(pady=10)
        
        frame_botones = ctk.CTkFrame(panel_inferior, fg_color="transparent")
        frame_botones.grid(row=2, column=0, columnspan=2, sticky="e", pady=10)
        
        self.btn_continuar = ctk.CTkButton(
            frame_botones,
            text="Continuar al Análisis",
            command=self._continuar_analisis,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            width=180,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            state="disabled"
        )
        self.btn_continuar.pack(side="right", padx=5)
        
        self.btn_limpiar = ctk.CTkButton(
            frame_botones,
            text="Limpiar",
            command=self._limpiar_datos,
            font=ctk.CTkFont(size=13),
            height=40,
            width=100,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.btn_limpiar.pack(side="right", padx=5)
    
    def _cargar_archivo(self):
        """Maneja el evento de cargar archivo."""
        try:
            self.df = self.loader.cargar_archivo()
            
            if self.df is not None:
                self._mostrar_datos_tabla()
                self._actualizar_combo_columnas()
                
                nombre_archivo = self.loader.obtener_nombre_archivo()
                self.lbl_archivo.configure(
                    text=f"Archivo: {nombre_archivo} ({len(self.df)} filas, {len(self.df.columns)} columnas)"
                )
                
                self.btn_limpiar.configure(state="normal")
                
        except ArchivoNoSeleccionadoError:
            pass
        
        except FormatoNoSoportadoError as e:
            messagebox.showerror("Formato No Soportado", str(e))
        
        except ArchivoVacioError as e:
            messagebox.showerror("Archivo Vacío", str(e))
        
        except ArchivoSinEncabezadosError as e:
            messagebox.showerror("Sin Encabezados", str(e))
        
        except ErrorCargaArchivo as e:
            messagebox.showerror("Error de Carga", str(e))
        
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al cargar el archivo:\n\n{str(e)}"
            )
    
    def _mostrar_datos_tabla(self):
        """Muestra los datos del DataFrame en la tabla Treeview."""
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = []
        
        columnas = list(self.df.columns)
        self.tree['columns'] = columnas
        
        for col in columnas:
            self.tree.heading(col, text=str(col))
            max_width = max(
                len(str(col)) * 10,
                self.df[col].astype(str).str.len().max() * 10
            )
            self.tree.column(col, width=min(max(max_width, 80), 300), anchor='center')
        
        self.tree.delete(*self.tree.get_children())
        
        max_filas = 500
        df_mostrar = self.df.head(max_filas)
        
        for idx, row in df_mostrar.iterrows():
            valores = [str(v) if pd.notna(v) else "" for v in row]
            self.tree.insert('', 'end', values=valores)
        
        total_filas = len(self.df)
        if total_filas > max_filas:
            self.lbl_info_tabla.configure(
                text=f"Mostrando {max_filas} de {total_filas} filas"
            )
        else:
            self.lbl_info_tabla.configure(
                text=f"Total: {total_filas} filas | {len(columnas)} columnas"
            )
    
    def _actualizar_combo_columnas(self):
        """Actualiza el ComboBox con los encabezados de las columnas."""
        encabezados = self.loader.obtener_encabezados(self.df)
        self.combo_columnas.configure(values=encabezados, state="normal")
        self.combo_columnas.set("-- Seleccione una columna --")
    
    def _on_columna_seleccionada(self, columna: str):
        """Maneja el evento de selección de columna."""
        if columna.startswith("--") or self.df is None:
            self._limpiar_frecuencias()
            self.btn_continuar.configure(state="disabled")
            return
        
        try:
            self.columna_seleccionada = columna
            self.frecuencias = self.loader.obtener_frecuencias(self.df, columna)
            
            n_registros = len(self.df)
            self.lbl_total_registros.configure(
                text=f"Total de registros (N): {n_registros}"
            )
            
            self._mostrar_frecuencias()
            
            self.btn_continuar.configure(state="normal")
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al obtener frecuencias:\n{str(e)}"
            )
    
    def _mostrar_frecuencias(self):
        """Muestra las frecuencias en el panel correspondiente."""
        for widget in self.frame_frecuencias.winfo_children():
            widget.destroy()
        
        if not self.frecuencias:
            self.lbl_placeholder = ctk.CTkLabel(
                self.frame_frecuencias,
                text="No hay datos para mostrar",
                text_color="gray"
            )
            self.lbl_placeholder.pack(pady=5)
            return
        
        total = sum(self.frecuencias.values())
        
        for valor, conteo in sorted(self.frecuencias.items(), key=lambda x: -x[1]):
            porcentaje = (conteo / total) * 100 if total > 0 else 0
            
            frame_item = ctk.CTkFrame(self.frame_frecuencias, fg_color="transparent")
            frame_item.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(
                frame_item,
                text=f"• {valor}: {conteo} ({porcentaje:.1f}%)",
                font=ctk.CTkFont(size=11),
                anchor="w"
            )
            lbl.pack(side="left", padx=5)
    
    def _limpiar_frecuencias(self):
        """Limpia el panel de frecuencias."""
        for widget in self.frame_frecuencias.winfo_children():
            widget.destroy()
        
        self.lbl_frecuencia_placeholder = ctk.CTkLabel(
            self.frame_frecuencias,
            text="Seleccione una columna para ver las frecuencias",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.lbl_frecuencia_placeholder.pack(pady=10)
        
        self.lbl_total_registros.configure(text="Total de registros (N): --")
    
    def _continuar_analisis(self):
        """Maneja el evento de continuar al análisis."""
        if self.df is None:
            messagebox.showwarning(
                "Sin Datos",
                "Por favor, cargue un archivo antes de continuar."
            )
            return
        
        if not self.columna_seleccionada:
            messagebox.showwarning(
                "Sin Selección",
                "Por favor, seleccione una columna antes de continuar."
            )
            return
        
        n_registros = len(self.df)
        
        if self.callback_continuar:
            self.callback_continuar(
                self.df,
                self.columna_seleccionada,
                n_registros,
                self.frecuencias
            )
        else:
            ParameterWindow(
                master=self,
                df=self.df,
                columna=self.columna_seleccionada,
                N=n_registros,
                frecuencias=self.frecuencias
            )
    
    def _limpiar_datos(self):
        """Limpia todos los datos cargados."""
        self.df = None
        self.columna_seleccionada = None
        self.frecuencias = None
        
        self.tree.delete(*self.tree.get_children())
        columnas = list(self.tree['columns']) if self.tree['columns'] else []
        for col in columnas:
            self.tree.heading(col, text='')
        self.tree['columns'] = []
        
        self.combo_columnas.configure(
            values=["-- Cargue un archivo primero --"],
            state="disabled"
        )
        self.combo_columnas.set("-- Cargue un archivo primero --")
        
        self._limpiar_frecuencias()
        
        self.lbl_archivo.configure(text="Ningún archivo cargado")
        self.lbl_info_tabla.configure(text="Cargue un archivo para ver los datos")
        
        self.btn_continuar.configure(state="disabled")
        self.btn_limpiar.configure(state="disabled")
    
    def _al_cerrar(self):
        """Maneja el cierre de la ventana."""
        self._limpiar_datos()
        super()._al_cerrar()
    
    def obtener_datos_seleccionados(self) -> Optional[Dict]:
        """
        Retorna los datos seleccionados actualmente.
        
        Returns:
            Dict con df, columna, N y frecuencias, o None si no hay datos.
        """
        if self.df is None or not self.columna_seleccionada:
            return None
        
        return {
            'df': self.df,
            'columna': self.columna_seleccionada,
            'N': len(self.df),
            'frecuencias': self.frecuencias
        }
