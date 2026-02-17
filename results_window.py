"""
Ventana para mostrar los resultados del cálculo de probabilidades
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional, Dict, Any

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from probability_engine import ProbabilityEngine, ErrorCalculo, ParametrosInvalidosError
from base_window import BaseToplevelWindow


class ResultsWindow(BaseToplevelWindow):
    """
    Ventana para mostrar los resultados del cálculo de distribuciones.
    
    Muestra los resultados estadísticos en un panel izquierdo y una
    gráfica de la distribución en un panel derecho.
    
    Attributes:
        N: Tamaño de la población.
        K: Número de éxitos en la población.
        n: Tamaño de la muestra.
        x: Número de éxitos deseados.
        engine: Instancia de ProbabilityEngine para cálculos.
        resultados: Diccionario con todos los resultados calculados.
    """
    
    def __init__(
        self,
        master=None,
        N: int = None,
        K: int = None,
        n: int = None,
        x: int = None
    ):
        """
        Inicializa la ventana de resultados.
        
        Args:
            master: Ventana padre.
            N (int): Tamaño de la población.
            K (int): Número de éxitos en la población.
            n (int): Tamaño de la muestra.
            x (int): Número de éxitos deseados.
        """
        super().__init__(master)
        
        if hasattr(self, '_skip_init') and self._skip_init:
            return
        
        self.N = N
        self.K = K
        self.n = n
        self.x = x
        self.engine = ProbabilityEngine()
        self.resultados = None
        
        self._configurar_ventana()
        self._calcular_resultados()
        self._crear_widgets()
        
        self.centrar_ventana(1300, 750)
    
    def _configurar_ventana(self):
        """Configura las propiedades de la ventana."""
        self.title("Resultados del Análisis")
        self.geometry("1300x750")
        self.minsize(1100, 650)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
    
    def _calcular_resultados(self):
        """Ejecuta todos los cálculos usando ProbabilityEngine."""
        try:
            self.resultados = self.engine.calcular_resumen_completo(
                self.N, self.K, self.n, self.x
            )
            self.modelo = self.resultados['modelo']
            self.proporcion = self.n / self.N
        except (ErrorCalculo, ParametrosInvalidosError) as e:
            messagebox.showerror("Error de Cálculo", str(e))
            self.after(100, self.destroy)
    
    def _crear_widgets(self):
        """Crea todos los widgets de la ventana."""
        self._crear_panel_resultados()
        self._crear_panel_grafico()
        self._crear_panel_botones()
    
    def _crear_panel_resultados(self):
        """Crea el panel izquierdo con los resultados."""
        frame_resultados = ctk.CTkFrame(self)
        frame_resultados.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame_resultados.grid_columnconfigure(0, weight=1)
        frame_resultados.grid_rowconfigure(0, weight=0)
        frame_resultados.grid_rowconfigure(1, weight=1)
        
        titulo = ctk.CTkLabel(
            frame_resultados,
            text="RESULTADOS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f6aa5", "#1f6aa5")
        )
        titulo.grid(row=0, column=0, pady=(15, 10), sticky="ew")
        
        frame_contenido = ctk.CTkScrollableFrame(
            frame_resultados,
            fg_color="transparent"
        )
        frame_contenido.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        frame_contenido.grid_columnconfigure(0, weight=1)
        
        self._crear_seccion_modelo(frame_contenido)
        self._crear_seccion_probabilidad(frame_contenido)
        self._crear_seccion_estadisticas(frame_contenido)
        self._crear_seccion_forma(frame_contenido)
    
    def _crear_seccion_modelo(self, parent):
        """Crea la sección del modelo utilizado."""
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="MODELO DE DISTRIBUCIÓN",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        modelo = self.resultados['modelo']
        color = "#9b59b6" if modelo == "Hipergeométrica" else "#3b8ed0"
        
        lbl_modelo = ctk.CTkLabel(
            frame,
            text=f"Distribución {modelo}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=color,
            anchor="w"
        )
        lbl_modelo.pack(fill="x", padx=10, pady=2)
        
        porcentaje = self.proporcion * 100
        if porcentaje >= 20:
            justificacion = f"Justificación: n({self.n}) ≥ 20% de N({self.N}) ({porcentaje:.1f}%)"
        else:
            justificacion = f"Justificación: n({self.n}) < 20% de N({self.N}) ({porcentaje:.1f}%)"
        
        lbl_justificacion = ctk.CTkLabel(
            frame,
            text=justificacion,
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        lbl_justificacion.pack(fill="x", padx=10, pady=(0, 10))
    
    def _crear_seccion_probabilidad(self, parent):
        """Crea la sección de probabilidad calculada."""
        frame = ctk.CTkFrame(parent)
        frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="PROBABILIDAD CALCULADA",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        prob = self.resultados['probabilidad_x']
        porcentaje = prob * 100
        
        lbl_prob = ctk.CTkLabel(
            frame,
            text=f"P(X = {self.x}) = {prob:.6f}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2ecc71",
            anchor="w"
        )
        lbl_prob.pack(fill="x", padx=10, pady=2)
        
        lbl_porc = ctk.CTkLabel(
            frame,
            text=f"Equivalente: {porcentaje:.4f}%",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        lbl_porc.pack(fill="x", padx=10, pady=(0, 10))
    
    def _crear_seccion_estadisticas(self, parent):
        """Crea la sección de estadísticas descriptivas."""
        frame = ctk.CTkFrame(parent)
        frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="ESTADÍSTICAS DESCRIPTIVAS",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        stats = [
            ("Media (μ)", f"{self.resultados['media']:.6f}"),
            ("Desviación estándar (σ)", f"{self.resultados['desviacion']:.6f}"),
            ("Mediana", f"{self.resultados['mediana']:.1f}"),
        ]
        
        for label, valor in stats:
            frame_stat = ctk.CTkFrame(frame, fg_color="transparent")
            frame_stat.pack(fill="x", padx=10, pady=2)
            
            lbl = ctk.CTkLabel(
                frame_stat,
                text=f"{label}:",
                font=ctk.CTkFont(size=11),
                width=160,
                anchor="w"
            )
            lbl.pack(side="left")
            
            val = ctk.CTkLabel(
                frame_stat,
                text=valor,
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w"
            )
            val.pack(side="left", padx=5)
        
        lbl_espacio = ctk.CTkLabel(frame, text="")
        lbl_espacio.pack(pady=(5, 0))
    
    def _crear_seccion_forma(self, parent):
        """Crea la sección de forma de la distribución."""
        frame = ctk.CTkFrame(parent)
        frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="FORMA DE LA DISTRIBUCIÓN",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        frame_sesgo = ctk.CTkFrame(frame, fg_color="transparent")
        frame_sesgo.pack(fill="x", padx=10, pady=2)
        
        lbl_sesgo_label = ctk.CTkLabel(
            frame_sesgo,
            text="Sesgo:",
            font=ctk.CTkFont(size=11),
            width=60,
            anchor="w"
        )
        lbl_sesgo_label.pack(side="left")
        
        sesgo = self.resultados['sesgo']
        color_sesgo = "#e74c3c" if "Negativo" in sesgo else "#2ecc71" if "Positivo" in sesgo else "gray"
        
        lbl_sesgo_val = ctk.CTkLabel(
            frame_sesgo,
            text=sesgo,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=color_sesgo,
            anchor="w"
        )
        lbl_sesgo_val.pack(side="left", padx=5)
        
        frame_curtosis = ctk.CTkFrame(frame, fg_color="transparent")
        frame_curtosis.pack(fill="x", padx=10, pady=2)
        
        lbl_curt_label = ctk.CTkLabel(
            frame_curtosis,
            text="Curtosis:",
            font=ctk.CTkFont(size=11),
            width=60,
            anchor="w"
        )
        lbl_curt_label.pack(side="left")
        
        curt_valor = self.resultados['curtosis_valor']
        curt_tipo = self.resultados['curtosis_tipo']
        
        lbl_curt_val = ctk.CTkLabel(
            frame_curtosis,
            text=f"{curt_valor:.4f}",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        lbl_curt_val.pack(side="left", padx=5)
        
        color_curt = "#e74c3c" if curt_tipo == "Leptocúrtica" else "#3498db" if curt_tipo == "Platicúrtica" else "gray"
        
        lbl_curt_tipo = ctk.CTkLabel(
            frame_curtosis,
            text=f"({curt_tipo})",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=color_curt,
            anchor="w"
        )
        lbl_curt_tipo.pack(side="left", padx=5)
        
        lbl_espacio = ctk.CTkLabel(frame, text="")
        lbl_espacio.pack(pady=(5, 0))
    
    def _crear_panel_grafico(self):
        """Crea el panel derecho con la gráfica."""
        frame_grafico = ctk.CTkFrame(self)
        frame_grafico.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        frame_grafico.grid_columnconfigure(0, weight=1)
        frame_grafico.grid_rowconfigure(0, weight=1)
        
        self._crear_grafico(frame_grafico)
    
    def _crear_grafico(self, parent):
        """Crea la gráfica de la distribución."""
        probs = self.resultados['probabilidades_rango']
        
        valores_x = list(probs.keys())
        valores_prob = list(probs.values())
        max_prob = max(valores_prob) if valores_prob else 1
        
        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        colores = []
        for xi in valores_x:
            if xi == self.x:
                colores.append('#e74c3c')
            else:
                colores.append('#3b8ed0')
        
        bars = ax.bar(
            valores_x,
            valores_prob,
            color=colores,
            alpha=0.8,
            edgecolor='white',
            linewidth=0.5
        )
        
        if len(valores_x) > 1:
            x_suave = np.linspace(min(valores_x) - 0.5, max(valores_x) + 0.5, 300)
            y_suave = np.interp(x_suave, valores_x, valores_prob)
            ax.plot(
                x_suave,
                y_suave,
                color='#f39c12',
                linewidth=2.5,
                alpha=0.9,
                label='Curva de distribución'
            )
        
        media = self.resultados['media']
        desviacion = self.resultados['desviacion']
        
        if desviacion > 0:
            x_normal = np.linspace(
                max(0, media - 4*desviacion),
                media + 4*desviacion,
                200
            )
            y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * \
                       np.exp(-0.5 * ((x_normal - media) / desviacion) ** 2)
            
            if max(y_normal) > 0:
                y_normal = y_normal * (max_prob / max(y_normal))
            
            ax.plot(
                x_normal,
                y_normal,
                color='#9b59b6',
                linewidth=2,
                linestyle='--',
                alpha=0.8,
                label='Curva Normal (Curtosis ref.)'
            )
        
        for i, (xi, prob) in enumerate(zip(valores_x, valores_prob)):
            if xi == self.x:
                ax.text(
                    xi,
                    prob + max_prob * 0.05,
                    f'P(X={xi})={prob:.4f}',
                    ha='center',
                    va='bottom',
                    color='#e74c3c',
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#2b2b2b', edgecolor='#e74c3c')
                )
            elif prob > max_prob * 0.05:
                ax.text(
                    xi,
                    prob + max_prob * 0.02,
                    f'{prob:.3f}',
                    ha='center',
                    va='bottom',
                    color='white',
                    fontsize=8,
                    fontweight='bold'
                )
        
        text_color = '#ffffff'
        grid_color = '#444444'
        
        ax.set_xlabel(
            f'Número de éxitos (x) - Rango: 0 a {self.x}',
            fontsize=11,
            color=text_color,
            fontweight='bold'
        )
        ax.set_ylabel(
            'Probabilidad P(X=x)',
            fontsize=11,
            color=text_color,
            fontweight='bold'
        )
        
        curtosis_tipo = self.resultados['curtosis_tipo']
        prob_x = self.resultados['probabilidad_x']
        titulo_modelo = self.modelo
        ax.set_title(
            f'Distribución {titulo_modelo} — N={self.N}, K={self.K}, n={self.n}, x={self.x}\n'
            f'P(X={self.x}) = {prob_x:.6f} | Curtosis: {curtosis_tipo}',
            fontsize=10,
            color=text_color,
            fontweight='bold',
            pad=10
        )
        
        legend = ax.legend(
            loc='upper right',
            facecolor='#3b3b3b',
            edgecolor='#555555',
            fontsize=9
        )
        for text in legend.get_texts():
            text.set_color(text_color)
        
        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines['bottom'].set_color(grid_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(grid_color)
        
        ax.grid(True, alpha=0.3, linestyle='--', color=grid_color, axis='y')
        ax.set_axisbelow(True)
        
        ax.axvline(
            x=media,
            color='#2ecc71',
            linestyle=':',
            linewidth=2,
            alpha=0.7
        )
        ax.text(
            media,
            max_prob * 0.85,
            f'μ={media:.2f}',
            ha='center',
            va='bottom',
            color='#2ecc71',
            fontsize=10,
            fontweight='bold'
        )
        
        if len(valores_x) > 0:
            ax.set_xlim(min(valores_x) - 0.5, max(valores_x) + 0.5)
        
        ax.set_xticks(valores_x)
        
        plt.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(self.figura, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def _crear_panel_botones(self):
        """Crea el panel inferior con los botones."""
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        btn_exportar = ctk.CTkButton(
            frame_botones,
            text="Exportar gráfica como PNG",
            command=self._exportar_grafica,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=38,
            width=200,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        btn_exportar.pack(side="right", padx=5)
        
        btn_cerrar = ctk.CTkButton(
            frame_botones,
            text="Cerrar",
            command=self._cerrar_ventana,
            font=ctk.CTkFont(size=12),
            height=38,
            width=100,
            fg_color="gray",
            hover_color="darkgray"
        )
        btn_cerrar.pack(side="right", padx=5)
    
    def _exportar_grafica(self):
        """Exporta la gráfica como archivo PNG."""
        try:
            from tkinter import filedialog
            
            nombre_archivo = filedialog.asksaveasfilename(
                title="Guardar gráfica",
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("Todos", "*.*")],
                initialfile=f"distribucion_{self.modelo.lower()}_N{self.N}_K{self.K}_n{self.n}.png"
            )
            
            if nombre_archivo:
                self.figura.savefig(
                    nombre_archivo,
                    dpi=150,
                    bbox_inches='tight',
                    facecolor=self.figura.get_facecolor()
                )
                messagebox.showinfo(
                    "Exportación exitosa",
                    f"Gráfica guardada en:\n{nombre_archivo}"
                )
        except Exception as e:
            messagebox.showerror(
                "Error de exportación",
                f"No se pudo guardar la gráfica:\n{str(e)}"
            )
    
    def _cerrar_ventana(self):
        """Cierra la ventana desde el botón."""
        self._al_cerrar()
    
    def _al_cerrar(self):
        """Maneja el cierre de la ventana."""
        super()._limpiar_recursos()
        super()._al_cerrar()
    
    def obtener_resultados(self) -> Optional[Dict[str, Any]]:
        """
        Retorna los resultados calculados.
        
        Returns:
            Dict con todos los resultados del cálculo.
        """
        return self.resultados
