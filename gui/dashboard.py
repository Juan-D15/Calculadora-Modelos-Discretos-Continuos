"""
Módulo del Dashboard de la aplicación
Permite navegar entre diferentes distribuciones estadísticas
Diseño mejorado y centrado
"""
import customtkinter as ctk
from gui.campos_entrada import CamposEntrada, CamposEntradaHipergeometrica
from gui.area_resultados import AreaResultados
from gui.grafico import GraficoBinomial


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
        self.area_resultados = None
        self.grafico = None
        
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
        self.sidebar = ctk.CTkFrame(
            self.dashboard_frame,
            width=180,
            corner_radius=10
        )
        self.sidebar.pack(side="left", fill="y", padx=8, pady=8)
        self.sidebar.pack_propagate(False)
        
        titulo = ctk.CTkLabel(
            self.sidebar,
            text="DISTRIBUCIONES",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("gray10", "gray90")
        )
        titulo.pack(pady=(15, 15))
        
        self.btn_binomial = self.crear_boton_sidebar(
            "Binomial",
            "binomial",
            True
        )
        
        self.btn_hipergeometrica = self.crear_boton_sidebar(
            "Hipergeométrica",
            "hipergeometrica",
            False
        )
        
        separador = ctk.CTkFrame(self.sidebar, height=2, fg_color="gray50")
        separador.pack(fill="x", padx=10, pady=15)
        
        titulo_analisis = ctk.CTkLabel(
            self.sidebar,
            text="ANÁLISIS",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("gray10", "gray90")
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
            command=self.abrir_analisis_archivo
        )
        self.btn_analisis_archivo.pack(fill="x", padx=8, pady=4)
    
    def abrir_analisis_archivo(self):
        """Abre la ventana de análisis desde archivo"""
        if self.ventana_principal:
            self.ventana_principal.abrir_analisis_archivo()
    
    def crear_boton_sidebar(self, texto, distribucion, es_activo):
        """
        Crea un botón de navegación en el sidebar
        
        Args:
            texto: Texto del botón
            distribucion: Nombre de la distribución
            es_activo: Si es la distribución activa
        """
        color = "#3b8ed0" if es_activo else "transparent"
        hover_color = "#3672a9" if es_activo else ("gray70", "gray30")
        
        btn = ctk.CTkButton(
            self.sidebar,
            text=texto,
            font=ctk.CTkFont(size=12),
            fg_color=color,
            hover_color=hover_color,
            text_color=("white", "gray10") if es_activo else ("gray10", "gray90"),
            anchor="w",
            height=38,
            corner_radius=8,
            command=lambda: self.cargar_distribucion(distribucion)
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
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
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
    
    def actualizar_botones_sidebar(self, distribucion_activo):
        """Actualiza el estado visual de los botones del sidebar"""
        botones = {
            "binomial": self.btn_binomial,
            "hipergeometrica": self.btn_hipergeometrica,
        }
        
        for dist, btn in botones.items():
            es_activo = dist == distribucion_activo
            btn.configure(
                fg_color="#3b8ed0" if es_activo else "transparent",
                hover_color="#3672a9" if es_activo else ("gray70", "gray30"),
                text_color=("white", "gray10") if es_activo else ("gray10", "gray90")
            )
    
    def crear_interfaz_binomial(self):
        """Crea la interfaz para distribución binomial"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN BINOMIAL",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(pady=(12, 8))
        
        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
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
            corner_radius=8
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
            corner_radius=8
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
            text="DISTRIBUCIÓN POISSON",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(pady=(12, 8))
        
        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Modela el número de eventos en un intervalo de tiempo o espacio",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        descripcion.pack(pady=(0, 12))
        
        info = ctk.CTkLabel(
            self.content_frame,
            text="🚧 Próximamente disponible",
            font=ctk.CTkFont(size=15),
            text_color="#3b8ed0"
        )
        info.pack(pady=50)
    
    def crear_interfaz_normal(self):
        """Crea la interfaz para distribución Normal"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN NORMAL",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(pady=(12, 8))
        
        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Distribución continua más importante en estadística",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        descripcion.pack(pady=(0, 12))
        
        info = ctk.CTkLabel(
            self.content_frame,
            text="🚧 Próximamente disponible",
            font=ctk.CTkFont(size=15),
            text_color="#3b8ed0"
        )
        info.pack(pady=50)
    
    def crear_interfaz_geometrica(self):
        """Crea la interfaz para distribución Geométrica"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN GEOMÉTRICA",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(pady=(12, 8))
        
        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Modela el número de ensayos hasta el primer éxito",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        descripcion.pack(pady=(0, 12))
        
        info = ctk.CTkLabel(
            self.content_frame,
            text="🚧 Próximamente disponible",
            font=ctk.CTkFont(size=15),
            text_color="#3b8ed0"
        )
        info.pack(pady=50)
    
    def crear_interfaz_hipergeometrica(self):
        """Crea la interfaz para distribución Hipergeométrica"""
        titulo = ctk.CTkLabel(
            self.content_frame,
            text="DISTRIBUCIÓN HIPERGEOMÉTRICA",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        titulo.pack(pady=(12, 8))
        
        descripcion = ctk.CTkLabel(
            self.content_frame,
            text="Modela muestreo sin reemplazo de una población finita (muestra ≥ 20% de población)",
            font=ctk.CTkFont(size=11),
            text_color="gray"
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
            corner_radius=8
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
            corner_radius=8
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
        if self.grafico:
            self.grafico.limpiar()
    
    def limpiar_hipergeometrica(self):
        """Limpia campos y resultados de hipergeométrica"""
        if self.campos_hipergeometrica:
            self.campos_hipergeometrica.limpiar()
        if self.area_resultados:
            self.area_resultados.limpiar()
        if self.grafico:
            self.grafico.limpiar()
    
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
    
    def crear_grafico(self, valores_x, probabilidades, n, p, N=None, es_infinita=True, x_destacado=None):
        """Crea el gráfico de distribución binomial"""
        if self.grafico:
            self.grafico.crear_grafico(valores_x, probabilidades, n, p, N, es_infinita, x_destacado)
    
    def crear_grafico_hipergeometrica(self, valores_x, probabilidades, n, N, K, p=None, x_destacado=None):
        """Crea el gráfico de distribución hipergeométrica"""
        if self.grafico:
            if p is None:
                p = K / N if N > 0 else 0
            self.grafico.crear_grafico_hipergeometrica(valores_x, probabilidades, n, N, K, p, x_destacado)
