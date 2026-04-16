"""
Módulo del Dashboard de la aplicación
Permite navegar entre diferentes distribuciones estadísticas
Diseño mejorado y centrado
"""

import customtkinter as ctk
from gui.campos_entrada import (
    CamposEntrada,
    CamposEntradaHipergeometrica,
    CamposEntradaPoisson,
    CamposEntradaMM1,
)
from gui.area_resultados import AreaResultados
from gui.grafico import GraficoBinomial
from gui.grafico import GraficoMM1
from gui.tabla_comparacion import TablaComparacion
from gui.tabla_comparacion_poisson import TablaComparacionPoisson


class Dashboard:
    """Clase principal del Dashboard de distribuciones estadísticas"""

    def __init__(self, frame_contenedor, ventana_principal):
        """
        Inicializa el dashboard

        Args:
            frame_contenedor: Frame donde se mostrará el dashboard
            ventana_principal: Referencia a la ventana principal para callbacks
        """
        self.frame = frame_contenedor
        self.ventana_principal = ventana_principal
        self.distribucion_actual = "binomial"

        self.sidebar = None
        self.content_frame = None
        self.campos = None
        self.campos_hipergeometrica = None
        self.campos_poisson = None
        self.area_resultados = None
        self.grafico = None
        self.tabla_comparacion = None
        self.tabla_poisson = None
        self.modo_comparacion = False
        self.datos_comparacion_binomial = None
        self.datos_comparacion_hipergeometrica = None

        self.campos_mm1 = None
        self.grafico_mm1 = None
        self.toggle_mm1_frame = None
        self.toggle_mm1 = None
        self.results_mm1_frame = None
        self.graph_mm1_frame = None

        self.ventana_analisis_archivo = None

        self.crear_dashboard()

    def crear_dashboard(self):
        """Crea la estructura del dashboard con sidebar y contenido"""
        self.dashboard_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.dashboard_frame.pack(fill="both", expand=True)

        self.crear_sidebar()
        self.crear_area_contenido()
        self.cargar_distribucion("binomial")

    def crear_sidebar(self):
        """Crea la barra lateral con opciones de distribuciones"""
        self.sidebar = ctk.CTkFrame(self.dashboard_frame, width=180, corner_radius=10)
        self.sidebar.pack(side="left", fill="y", padx=8, pady=8)
        self.sidebar.pack_propagate(False)

        titulo = ctk.CTkLabel(
            self.sidebar,
            text="DISTRIBUCIONES",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("gray10", "gray90"),
        )
        titulo.pack(pady=(15, 15))

        self.btn_binomial = self.crear_boton_sidebar("Binomial", "binomial", True)

        self.btn_poisson = self.crear_boton_sidebar("Poisson", "poisson", False)

        self.btn_hipergeometrica = self.crear_boton_sidebar(
            "Hipergeométrica", "hipergeometrica", False
        )

        self.btn_mm1 = self.crear_boton_sidebar("M/M/1", "mm1", False, color="#3b8ed0")

        separador = ctk.CTkFrame(self.sidebar, height=2, fg_color="gray50")
        separador.pack(fill="x", padx=10, pady=15)

        titulo_analisis = ctk.CTkLabel(
            self.sidebar,
            text="ANÁLISIS",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("gray10", "gray90"),
        )
        titulo_analisis.pack(pady=(0, 10))

        self.btn_analisis_archivo = ctk.CTkButton(
            self.sidebar,
            text="📂 Desde Archivo",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            text_color=("gray10", "gray90"),
            anchor="w",
            height=38,
            corner_radius=8,
            command=self.abrir_analisis_archivo,
        )
        self.btn_analisis_archivo.pack(fill="x", padx=8, pady=4)

    def abrir_analisis_archivo(self):
        """Abre la ventana de análisis desde archivo"""
        if self.ventana_principal:
            self.ventana_principal.abrir_analisis_archivo()

    def crear_boton_sidebar(self, texto, distribucion, es_activo, color=None):
        """
        Crea un botón de navegación en el sidebar

        Args:
            texto: Texto del botón
            distribucion: Nombre de la distribución
            es_activo: Si es la distribución activa
            color: Color personalizado del botón (opcional)
        """
        default_color = "#3b8ed0"
        btn_color = color if color else default_color
        hover_color = "#3672a9" if es_activo else ("gray70", "gray30")

        btn = ctk.CTkButton(
            self.sidebar,
            text=texto,
            font=ctk.CTkFont(size=12),
            fg_color=btn_color,
            hover_color=hover_color,
            text_color=("white", "gray10") if es_activo else ("gray10", "gray90"),
            anchor="w",
            height=38,
            corner_radius=8,
            command=lambda: self.cargar_distribucion(distribucion),
        )
        btn.pack(fill="x", padx=8, pady=4)
        return btn

    def crear_area_contenido(self):
        """Crea el área de contenido principal"""
        self.content_frame = ctk.CTkFrame(self.dashboard_frame, corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=8, pady=8)

    def cargar_distribucion(self, distribucion):
        """
        Carga la interfaz de la distribución seleccionada

        Args:
            distribucion: Nombre de la distribución a cargar
        """
        self.distribucion_actual = distribucion

        self.actualizar_botones_sidebar(distribucion)

        try:
            if self.content_frame is not None and self.content_frame.winfo_exists():
                for widget in self.content_frame.winfo_children():
                    widget.destroy()
        except Exception:
            pass

        if distribucion == "binomial":
            self.crear_interfaz_binomial()
        elif distribucion == "poisson":
            self.crear_interfaz_poisson()
        elif distribucion == "normal":
            self.crear_interfaz_normal()
        elif distribucion == "geometrica":
            self.crear_interfaz_geometrica()
        elif distribucion == "hipergeometrica":
            self.crear_interfaz_hipergeometrica()
        elif distribucion == "mm1":
            self.crear_interfaz_mm1()

    def actualizar_botones_sidebar(self, distribucion_activo):
        """Actualiza el estado visual de los botones del sidebar"""
        botones = {
            "binomial": self.btn_binomial,
            "poisson": self.btn_poisson,
            "hipergeometrica": self.btn_hipergeometrica,
            "mm1": self.btn_mm1,
        }

        for dist, btn in botones.items():
            es_activo = dist == distribucion_activo
            btn.configure(
                fg_color="#3b8ed0" if es_activo else "transparent",
                hover_color="#3672a9" if es_activo else ("gray70", "gray30"),
                text_color=("white", "gray10") if es_activo else ("gray10", "gray90"),
            )

    def crear_interfaz_binomial(self):
        """Crea la interfaz para distribución binomial"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN BINOMIAL",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        titulo.pack(pady=(12, 8))

        descripcion = ctk.CTkLabel(
            self.content_frame, text="", font=ctk.CTkFont(size=11), text_color="gray"
        )
        descripcion.pack(pady=(0, 12))

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=5)

        self.campos = CamposEntrada(input_frame)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=8)

        calc_btn = ctk.CTkButton(
            button_frame,
            text="CALCULAR",
            command=self.calcular_binomial,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=140,
            fg_color="#3b8ed0",
            hover_color="#3672a9",
            corner_radius=8,
        )
        calc_btn.pack(side="left", padx=5, pady=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="LIMPIAR",
            command=self.limpiar,
            font=ctk.CTkFont(size=13),
            height=38,
            width=110,
            fg_color="gray",
            hover_color="darkgray",
            corner_radius=8,
        )
        clear_btn.pack(side="left", padx=5, pady=5)

        results_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, padx=12, pady=8)

        results_frame.grid_columnconfigure(0, weight=45)
        results_frame.grid_columnconfigure(1, weight=55)
        results_frame.grid_rowconfigure(0, weight=1)

        text_frame = ctk.CTkFrame(results_frame)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        graph_frame = ctk.CTkFrame(results_frame)
        graph_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=0)

        self.area_resultados = AreaResultados(text_frame)
        self.grafico = GraficoBinomial(graph_frame)

    def crear_interfaz_poisson(self):
        """Crea la interfaz para distribución Poisson"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN DE POISSON",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        titulo.pack(pady=(12, 8))

        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Aproximación de la Binomial cuando p < 0.10 y λ < 10",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        descripcion.pack(pady=(0, 12))

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=5)

        self.campos_poisson = CamposEntradaPoisson(input_frame)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=8)

        calc_btn = ctk.CTkButton(
            button_frame,
            text="CALCULAR",
            command=self.calcular_poisson,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=140,
            fg_color="#27ae60",
            hover_color="#219a52",
            corner_radius=8,
        )
        calc_btn.pack(side="left", padx=5, pady=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="LIMPIAR",
            command=self.limpiar_poisson,
            font=ctk.CTkFont(size=13),
            height=38,
            width=110,
            fg_color="gray",
            hover_color="darkgray",
            corner_radius=8,
        )
        clear_btn.pack(side="left", padx=5, pady=5)

        results_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, padx=12, pady=8)

        results_frame.grid_columnconfigure(0, weight=45)
        results_frame.grid_columnconfigure(1, weight=55)
        results_frame.grid_rowconfigure(0, weight=1)

        text_frame = ctk.CTkFrame(results_frame)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        graph_frame = ctk.CTkFrame(results_frame)
        graph_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=0)

        self.area_resultados = AreaResultados(text_frame)
        self.grafico = GraficoBinomial(graph_frame)

    def crear_interfaz_normal(self):
        """Crea la interfaz para distribución Normal"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN NORMAL",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        titulo.pack(pady=(12, 8))

        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Distribución continua más importante en estadística",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        descripcion.pack(pady=(0, 12))

        info = ctk.CTkLabel(
            self.content_frame,
            text="🚧 Próximamente disponible",
            font=ctk.CTkFont(size=15),
            text_color="#3b8ed0",
        )
        info.pack(pady=50)

    def crear_interfaz_geometrica(self):
        """Crea la interfaz para distribución Geométrica"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN GEOMÉTRICA",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        titulo.pack(pady=(12, 8))

        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Modela el número de ensayos hasta el primer éxito",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        descripcion.pack(pady=(0, 12))

        info = ctk.CTkLabel(
            self.content_frame,
            text="🚧 Próximamente disponible",
            font=ctk.CTkFont(size=15),
            text_color="#3b8ed0",
        )
        info.pack(pady=50)

    def crear_interfaz_hipergeometrica(self):
        """Crea la interfaz para distribución Hipergeométrica"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN HIPERGEOMÉTRICA",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        titulo.pack(pady=(12, 8))

        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Modela muestreo sin reemplazo de una población finita (muestra ≥ 20% de población)",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        descripcion.pack(pady=(0, 12))

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=5)

        self.campos_hipergeometrica = CamposEntradaHipergeometrica(input_frame)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=8)

        calc_btn = ctk.CTkButton(
            button_frame,
            text="CALCULAR",
            command=self.calcular_hipergeometrica,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=140,
            fg_color="#3b8ed0",
            hover_color="#3672a9",
            corner_radius=8,
        )
        calc_btn.pack(side="left", padx=5, pady=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="LIMPIAR",
            command=self.limpiar_hipergeometrica,
            font=ctk.CTkFont(size=13),
            height=38,
            width=110,
            fg_color="gray",
            hover_color="darkgray",
            corner_radius=8,
        )
        clear_btn.pack(side="left", padx=5, pady=5)

        results_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, padx=12, pady=8)

        results_frame.grid_columnconfigure(0, weight=45)
        results_frame.grid_columnconfigure(1, weight=55)
        results_frame.grid_rowconfigure(0, weight=1)

        text_frame = ctk.CTkFrame(results_frame)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        graph_frame = ctk.CTkFrame(results_frame)
        graph_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=0)

        self.area_resultados = AreaResultados(text_frame)
        self.grafico = GraficoBinomial(graph_frame)

    def crear_interfaz_mm1(self):
        """Crea la interfaz para modelo de colas M/M/1"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="MODELO DE COLAS M/M/1",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        titulo.pack(pady=(12, 8))

        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Cola de un servidor con llegadas Poisson y servicio exponencial",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        descripcion.pack(pady=(0, 12))

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=5)

        self.campos_mm1 = CamposEntradaMM1(input_frame)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=8)

        calc_btn = ctk.CTkButton(
            button_frame,
            text="CALCULAR",
            command=self.calcular_mm1,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=140,
            fg_color="#3b8ed0",
            hover_color="#3672a9",
            corner_radius=8,
        )
        calc_btn.pack(side="left", padx=5, pady=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="LIMPIAR",
            command=self.limpiar_mm1,
            font=ctk.CTkFont(size=13),
            height=38,
            width=110,
            fg_color="gray",
            hover_color="darkgray",
            corner_radius=8,
        )
        clear_btn.pack(side="left", padx=5, pady=5)

        self.toggle_mm1_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.toggle_mm1_frame.pack(fill="x", padx=15, pady=(0, 5))

        self.toggle_mm1 = ctk.CTkSegmentedButton(
            self.toggle_mm1_frame,
            values=["Resultados", "Gráficos"],
            command=self._cambiar_vista_mm1,
            selected_color="#3b8ed0",
            selected_hover_color="#3672a9",
        )
        self.toggle_mm1.set("Resultados")
        self.toggle_mm1.pack()

        results_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        results_container.pack(fill="both", expand=True, padx=12, pady=8)

        results_container.grid_columnconfigure(0, weight=1)
        results_container.grid_rowconfigure(0, weight=1)

        self.results_mm1_frame = ctk.CTkFrame(results_container)
        self.results_mm1_frame.grid(row=0, column=0, sticky="nsew")

        self.graph_mm1_frame = ctk.CTkFrame(results_container)
        self.graph_mm1_frame.grid(row=0, column=0, sticky="nsew")
        self.graph_mm1_frame.grid_remove()

        self.area_resultados = AreaResultados(self.results_mm1_frame)
        self.grafico_mm1 = GraficoMM1(self.graph_mm1_frame)

    def _cambiar_vista_mm1(self, valor):
        """Cambia entre vista de resultados y gráficos"""
        if valor == "Resultados":
            self.results_mm1_frame.grid()
            self.graph_mm1_frame.grid_remove()
        else:
            self.results_mm1_frame.grid_remove()
            self.graph_mm1_frame.grid()

    def calcular_mm1(self):
        """Calcula el modelo M/M/1"""
        if self.ventana_principal:
            self.ventana_principal.calcular_mm1()

    def limpiar_mm1(self):
        """Limpia campos y resultados de M/M/1"""
        if self.campos_mm1:
            self.campos_mm1.limpiar()
        if self.area_resultados:
            self.area_resultados.limpiar()
        if self.grafico_mm1:
            self.grafico_mm1.limpiar()

    def calcular_binomial(self):
        """Calcula la distribución binomial"""
        if self.ventana_principal:
            self.ventana_principal.calcular_desde_dashboard()

    def calcular_hipergeometrica(self):
        """Calcula la distribución hipergeométrica"""
        if self.ventana_principal:
            self.ventana_principal.calcular_hipergeometrica()

    def limpiar(self):
        """Limpia todos los campos y resultados"""
        if self.campos:
            self.campos.limpiar()
        if self.area_resultados:
            self.area_resultados.limpiar()
            if self.modo_comparacion:
                self.area_resultados.scrollable_frame.grid(
                    row=0, column=0, sticky="nsew", padx=5, pady=5
                )
        if self.grafico:
            self.grafico.limpiar()
        if self.tabla_comparacion:
            self.tabla_comparacion.limpiar()
            self.tabla_comparacion.frame.grid_forget()
        self.modo_comparacion = False

    def limpiar_hipergeometrica(self):
        """Limpia campos y resultados de hipergeométrica"""
        if self.campos_hipergeometrica:
            self.campos_hipergeometrica.limpiar()
        if self.area_resultados:
            self.area_resultados.limpiar()
        if self.grafico:
            self.grafico.limpiar()

    def calcular_poisson(self):
        """Calcula la distribución de Poisson"""
        if self.ventana_principal:
            self.ventana_principal.calcular_poisson()

    def limpiar_poisson(self):
        """Limpia campos y resultados de Poisson"""
        if self.campos_poisson:
            self.campos_poisson.limpiar()
        if self.area_resultados:
            self.area_resultados.limpiar()
        if self.grafico:
            self.grafico.limpiar()

    def limpiar_comparacion(self):
        """Limpia solo la tabla de comparación y restaura la vista normal"""
        if self.tabla_comparacion:
            self.tabla_comparacion.limpiar()
            self.tabla_comparacion.frame.grid_forget()
        if self.area_resultados:
            self.area_resultados.limpiar()
            self.area_resultados.scrollable_frame.grid(
                row=0, column=0, sticky="nsew", padx=5, pady=5
            )
        if self.grafico:
            self.grafico.limpiar()
        self.modo_comparacion = False

    def obtener_campos(self):
        """Obtiene los valores de los campos de entrada"""
        if self.campos:
            return self.campos.obtener_valores()
        return None

    def obtener_campos_hipergeometrica(self):
        """Obtiene los valores de los campos de entrada hipergeométrica"""
        if self.campos_hipergeometrica:
            return self.campos_hipergeometrica.obtener_valores()
        return None

    def obtener_campos_poisson(self):
        """Obtiene los valores de los campos de entrada Poisson"""
        if self.campos_poisson:
            return self.campos_poisson.obtener_valores()
        return None

    def obtener_campos_mm1(self):
        """Obtiene los valores de los campos de entrada M/M/1"""
        if self.campos_mm1:
            return self.campos_mm1.obtener_valores()
        return None

    def mostrar_resultados(self, texto):
        """Muestra los resultados en el área de texto (compatibilidad)"""
        if self.area_resultados:
            self.area_resultados.mostrar_texto(texto)

    def mostrar_resultados_binomial(self, datos):
        """Muestra resultados estructurados de distribución binomial"""
        if self.area_resultados:
            self.area_resultados.mostrar_resultados_binomial(datos)

    def mostrar_resultados_hipergeometrica(self, datos):
        """Muestra resultados estructurados de distribución hipergeométrica"""
        if self.area_resultados:
            self.area_resultados.mostrar_resultados_hipergeometrica(datos)

    def mostrar_resultados_poisson(self, datos):
        """Muestra resultados estructurados de distribución de Poisson"""
        if self.area_resultados:
            self.area_resultados.mostrar_resultados_poisson(datos)

    def mostrar_resultados_mm1(self, datos):
        """Muestra resultados del modelo M/M/1"""
        if self.area_resultados:
            self.area_resultados.mostrar_resultados_mm1(datos)

    def crear_grafico(
        self,
        valores_x,
        probabilidades,
        n,
        p,
        N=None,
        es_infinita=True,
        x_destacado=None,
    ):
        """Crea el gráfico de distribución binomial"""
        if self.grafico:
            self.grafico.crear_grafico(
                valores_x, probabilidades, n, p, N, es_infinita, x_destacado
            )

    def crear_grafico_hipergeometrica(
        self, valores_x, probabilidades, n, N, K, p=None, x_destacado=None
    ):
        """Crea el gráfico de distribución hipergeométrica"""
        if self.grafico:
            if p is None:
                p = K / N if N > 0 else 0
            self.grafico.crear_grafico_hipergeometrica(
                valores_x, probabilidades, n, N, K, p, x_destacado
            )

    def crear_grafico_poisson(
        self, valores_x, probabilidades, lam, n, p, x_destacado=None
    ):
        """Crea el gráfico de distribución de Poisson"""
        if self.grafico:
            self.grafico.crear_grafico_poisson(
                valores_x, probabilidades, lam, n, p, x_destacado
            )

    def mostrar_comparacion(self, datos_binomial, datos_hipergeometrica, tolerancia):
        """
        Muestra los resultados de comparación entre distribuciones

        Args:
            datos_binomial (dict): Datos calculados de distribución binomial
            datos_hipergeometrica (dict): Datos calculados de distribución hipergeométrica
            tolerancia (float): Porcentaje de tolerancia
        """
        self.modo_comparacion = True
        self.datos_comparacion_binomial = datos_binomial
        self.datos_comparacion_hipergeometrica = datos_hipergeometrica

        if self.area_resultados:
            self.area_resultados.limpiar()
            self.area_resultados.scrollable_frame.grid_forget()

        if self.tabla_comparacion is None:
            if self.area_resultados:
                parent = self.area_resultados.frame
                self.tabla_comparacion = TablaComparacion(
                    parent, on_cambio_distribucion=self._actualizar_grafico_comparacion
                )
                self.tabla_comparacion.frame.grid(
                    row=0, column=0, sticky="nsew", padx=5, pady=5
                )
        else:
            self.tabla_comparacion.frame.grid(
                row=0, column=0, sticky="nsew", padx=5, pady=5
            )

        self.tabla_comparacion.mostrar(
            datos_binomial, datos_hipergeometrica, tolerancia
        )

        self._actualizar_grafico_comparacion("binomial")

    def _actualizar_grafico_comparacion(self, distribucion):
        """
        Actualiza el gráfico de comparación según la distribución seleccionada

        Args:
            distribucion (str): "binomial" o "hipergeometrica"
        """
        if not self.grafico:
            return

        if distribucion == "binomial" and self.datos_comparacion_binomial:
            datos = self.datos_comparacion_binomial
            self.grafico.crear_grafico_comparacion(
                datos["valores_x"],
                datos["probabilidades"],
                datos["probabilidades_acumuladas"],
                datos["n"],
                datos["p"],
                datos["N"],
                datos["es_infinita"],
                datos["valor_tolerancia"],
                es_hipergeometrica=False,
            )
        elif (
            distribucion == "hipergeometrica" and self.datos_comparacion_hipergeometrica
        ):
            datos = self.datos_comparacion_hipergeometrica
            self.grafico.crear_grafico_comparacion(
                datos["valores_x"],
                datos["probabilidades"],
                datos["probabilidades_acumuladas"],
                datos["n"],
                datos["p"],
                datos["N"],
                datos["es_infinita"],
                datos["valor_tolerancia"],
                es_hipergeometrica=True,
                K=datos["K"],
            )

    def mostrar_resultados_poisson_binomial(self, datos):
        """
        Muestra resultados de aproximación Binomial → Poisson

        Args:
            datos (dict): Diccionario con resultados del cálculo
        """
        # Limpiar área de resultados previa
        if self.area_resultados:
            self.area_resultados.limpiar()

        # Crear tabla comparativa
        if not self.tabla_poisson:
            self.tabla_poisson = TablaComparacionPoisson(
                self.content_frame, expand_callback=self.expandir_tabla_poisson_binomial
            )
            self.tabla_poisson.pack(fill="both", expand=True, padx=5, pady=5)

        # Mostrar tabla acotada
        self.tabla_poisson.mostrar_tabla_acotada(
            datos["valores_k"],
            datos["probs_binom"],
            datos["probs_poisson"],
            datos["k_ingresado"],
        )

        # Mostrar estadísticas
        if self.area_resultados:
            self.area_resultados.mostrar_estadisticas_poisson(datos)

    def mostrar_resultados_poisson_hipergeometrica(self, datos):
        """
        Muestra resultados de aproximación Hipergeométrica → Poisson

        Args:
            datos (dict): Diccionario con resultados del cálculo
        """
        # Limpiar área de resultados previa
        if self.area_resultados:
            self.area_resultados.limpiar()

        # Crear tabla comparativa
        if not self.tabla_poisson:
            self.tabla_poisson = TablaComparacionPoisson(
                self.content_frame,
                expand_callback=self.expandir_tabla_poisson_hipergeometrica,
            )
            self.tabla_poisson.pack(fill="both", expand=True, padx=5, pady=5)

        # Mostrar tabla acotada
        self.tabla_poisson.mostrar_tabla_acotada(
            datos["valores_k"],
            datos["probs_hiper"],
            datos["probs_poisson"],
            datos["k_ingresado"],
        )

        # Mostrar estadísticas
        if self.area_resultados:
            self.area_resultados.mostrar_estadisticas_poisson(datos)

    def expandir_tabla_poisson_binomial(self):
        """Expande tabla completa para aproximación Binomial → Poisson"""
        if self.tabla_poisson:
            self.tabla_poisson.mostrar_tabla_completa()

    def expandir_tabla_poisson_hipergeometrica(self):
        """Expande tabla completa para aproximación Hipergeométrica → Poisson"""
        if self.tabla_poisson:
            self.tabla_poisson.mostrar_tabla_completa()

    def crear_grafico_poisson_binomial(
        self, valores_k, probs_binom, probs_poisson, k_destacado, n, p, lam
    ):
        """
        Crea gráfica comparativa para Binomial → Poisson

        Args:
            valores_k (list): Valores de k
            probs_binom (list): Probabilidades binomiales
            probs_poisson (list): Probabilidades de Poisson
            k_destacado (int): Valor de k a destacar
            n (int): Número de ensayos
            p (float): Probabilidad
            lam (float): Parámetro λ
        """
        # Limpiar gráfica anterior
        if self.grafico:
            self.grafico.limpiar()

        # Crear gráfica nueva
        if not self.grafico:
            self.grafico = GraficoBinomial(self.content_frame)
            self.grafico.pack(fill="both", expand=True, padx=5, pady=5)

        titulo = f"Binomial (n={n}, p={p:.3f}) vs Poisson (λ={lam:.3f})"
        self.grafico.crear_barras_agrupadas(
            valores_k, probs_binom, probs_poisson, k_destacado, n, titulo
        )

    def crear_grafico_poisson_hipergeometrica(
        self, valores_k, probs_hiper, probs_poisson, k_destacado, N, K, n, lam
    ):
        """
        Crea gráfica comparativa para Hipergeométrica → Poisson

        Args:
            valores_k (list): Valores de k
            probs_hiper (list): Probabilidades hipergeométricas
            probs_poisson (list): Probabilidades de Poisson
            k_destacado (int): Valor de k a destacar
            N (int): Tamaño de población
            K (int): Elementos de interés
            n (int): Tamaño de muestra
            lam (float): Parámetro λ
        """
        # Limpiar gráfica anterior
        if self.grafico:
            self.grafico.limpiar()

        # Crear gráfica nueva
        if not self.grafico:
            self.grafico = GraficoBinomial(self.content_frame)
            self.grafico.pack(fill="both", expand=True, padx=5, pady=5)

        p = K / N if N > 0 else 0
        titulo = f"Hipergeométrica (N={N}, K={K}, n={n}) vs Poisson (λ={lam:.3f})"
        max_k = min(K, n)
        self.grafico.crear_barras_agrupadas(
            valores_k, probs_hiper, probs_poisson, k_destacado, max_k, titulo
        )
