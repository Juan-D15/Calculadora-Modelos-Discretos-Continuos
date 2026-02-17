"""
Módulo para crear y gestionar gráficos de distribuciones
Diseño mejorado con colores diferenciados para valores específicos
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraficoBinomial:
    """Clase para crear y gestionar gráficos de distribuciones"""
    
    def __init__(self, frame_contenedor):
        """
        Inicializa el gestor de gráficos
        
        Args:
            frame_contenedor: Frame de tkinter donde se mostrará el gráfico
        """
        self.frame = frame_contenedor
        self.canvas = None
        self.figura = None
    
    def limpiar(self):
        """Limpia el gráfico actual y cierra la figura de matplotlib"""
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        if self.figura is not None:
            try:
                plt.close(self.figura)
            except Exception:
                pass
            self.figura = None
        
        self.canvas = None
    
    def crear_grafico(self, valores_x, probabilidades, n, p, N=None, es_infinita=True, x_destacado=None):
        """
        Crea y muestra el gráfico de barras de la distribución binomial
        con diseño mejorado y colores diferenciados
        
        Args:
            valores_x (list): Valores del eje X
            probabilidades (list): Probabilidades correspondientes
            n (int): Tamaño de muestra
            p (float): Probabilidad de éxito
            N (int, optional): Tamaño de población
            es_infinita (bool): Indica si la población es infinita
            x_destacado (int, optional): Valor X específico a resaltar
        """
        from utils import calcular_media, calcular_desviacion_estandar, calcular_curtosis
        
        self.limpiar()
        
        media = calcular_media(n, p)
        desviacion = calcular_desviacion_estandar(n, p, N)
        curtosis, _ = calcular_curtosis(n, p, N)
        max_prob = max(probabilidades) if probabilidades else 1
        
        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        text_color = '#ffffff'
        grid_color = '#444444'
        bar_color_normal = '#3b8ed0'
        bar_color_destacado = '#e74c3c'
        curve_color = '#f39c12'
        normal_color = '#9b59b6'
        
        colores = []
        for x in valores_x:
            if x_destacado is not None and x == x_destacado:
                colores.append(bar_color_destacado)
            else:
                colores.append(bar_color_normal)
        
        bar_width = 0.7 if n <= 20 else 0.6 if n <= 50 else 0.5
        
        bars = ax.bar(
            valores_x,
            probabilidades,
            color=colores,
            alpha=0.8,
            edgecolor='white',
            linewidth=0.5,
            width=bar_width,
            label='Distribución Binomial'
        )
        
        if len(valores_x) > 1:
            x_suave = np.linspace(min(valores_x) - 0.5, max(valores_x) + 0.5, 300)
            y_suave = np.interp(x_suave, valores_x, probabilidades)
            ax.plot(
                x_suave,
                y_suave,
                color=curve_color,
                linewidth=2.5,
                alpha=0.9,
                label='Curva de distribución'
            )
        
        if desviacion > 0:
            x_normal = np.linspace(max(0, media - 4*desviacion), media + 4*desviacion, 200)
            y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * \
                       np.exp(-0.5 * ((x_normal - media) / desviacion) ** 2)
            if max(y_normal) > 0:
                y_normal = y_normal * (max_prob / max(y_normal))
            ax.plot(
                x_normal,
                y_normal,
                color=normal_color,
                linewidth=2,
                linestyle='--',
                alpha=0.8,
                label='Curva Normal (referencia)'
            )
        
        for i, (x, prob) in enumerate(zip(valores_x, probabilidades)):
            if x_destacado is not None and x == x_destacado:
                ax.text(
                    x,
                    prob + max_prob * 0.05,
                    f'P(X={x})={prob:.4f}',
                    ha='center',
                    va='bottom',
                    color='#e74c3c',
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#2b2b2b', edgecolor='#e74c3c')
                )
            elif prob > max_prob * 0.05:
                ax.text(
                    x,
                    prob + max_prob * 0.02,
                    f'{prob:.3f}',
                    ha='center',
                    va='bottom',
                    color='white',
                    fontsize=8,
                    fontweight='bold'
                )
        
        ax.set_xlabel(
            'Número de éxitos (X)',
            fontsize=11,
            color=text_color,
            fontweight='bold'
        )
        ax.set_ylabel(
            'Probabilidad P(X)',
            fontsize=11,
            color=text_color,
            fontweight='bold'
        )
        
        poblacion_texto = "Población Infinita" if es_infinita else f"Población Finita (N={N})"
        ax.set_title(
            f'Distribución Binomial (n={n}, p={p:.4f})\n{poblacion_texto}',
            fontsize=11,
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
        
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
    
    def crear_grafico_hipergeometrica(self, valores_x, probabilidades, n, N, K, p, x_destacado=None):
        """
        Crea y muestra el gráfico de barras de la distribución hipergeométrica
        con diseño mejorado y colores diferenciados
        
        Args:
            valores_x (list): Valores del eje X
            probabilidades (list): Probabilidades correspondientes
            n (int): Tamaño de muestra
            N (int): Tamaño de población
            K (int): Éxitos en población
            p (float): Probabilidad implícita (K/N)
            x_destacado (int, optional): Valor X específico a resaltar
        """
        from utils.calculos import (
            calcular_media_hipergeometrica,
            calcular_desviacion_hipergeometrica,
            calcular_curtosis_hipergeometrica
        )
        
        self.limpiar()
        
        media = calcular_media_hipergeometrica(n, N, K)
        desviacion = calcular_desviacion_hipergeometrica(n, N, K)
        curtosis, _ = calcular_curtosis_hipergeometrica(n, N, K)
        max_prob = max(probabilidades) if probabilidades else 1
        
        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        text_color = '#ffffff'
        grid_color = '#444444'
        bar_color_normal = '#9b59b6'
        bar_color_destacado = '#e74c3c'
        curve_color = '#f39c12'
        normal_color = '#3498db'
        
        colores = []
        for x in valores_x:
            if x_destacado is not None and x == x_destacado:
                colores.append(bar_color_destacado)
            else:
                colores.append(bar_color_normal)
        
        bar_width = 0.7 if len(valores_x) <= 20 else 0.6
        
        bars = ax.bar(
            valores_x,
            probabilidades,
            color=colores,
            alpha=0.8,
            edgecolor='white',
            linewidth=0.5,
            width=bar_width,
            label='Distribución Hipergeométrica'
        )
        
        if len(valores_x) > 1:
            x_suave = np.linspace(min(valores_x) - 0.5, max(valores_x) + 0.5, 300)
            y_suave = np.interp(x_suave, valores_x, probabilidades)
            ax.plot(
                x_suave,
                y_suave,
                color=curve_color,
                linewidth=2.5,
                alpha=0.9,
                label='Curva de distribución'
            )
        
        if desviacion > 0:
            x_normal = np.linspace(max(0, media - 4*desviacion), media + 4*desviacion, 200)
            y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * \
                       np.exp(-0.5 * ((x_normal - media) / desviacion) ** 2)
            if max(y_normal) > 0:
                y_normal = y_normal * (max_prob / max(y_normal))
            ax.plot(
                x_normal,
                y_normal,
                color=normal_color,
                linewidth=2,
                linestyle='--',
                alpha=0.8,
                label='Curva Normal (referencia)'
            )
        
        for i, (x, prob) in enumerate(zip(valores_x, probabilidades)):
            if x_destacado is not None and x == x_destacado:
                ax.text(
                    x,
                    prob + max_prob * 0.05,
                    f'P(X={x})={prob:.4f}',
                    ha='center',
                    va='bottom',
                    color='#e74c3c',
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#2b2b2b', edgecolor='#e74c3c')
                )
            elif prob > max_prob * 0.05:
                ax.text(
                    x,
                    prob + max_prob * 0.02,
                    f'{prob:.3f}',
                    ha='center',
                    va='bottom',
                    color='white',
                    fontsize=8,
                    fontweight='bold'
                )
        
        ax.set_xlabel(
            'Número de éxitos en la muestra (X)',
            fontsize=11,
            color=text_color,
            fontweight='bold'
        )
        ax.set_ylabel(
            'Probabilidad P(X)',
            fontsize=11,
            color=text_color,
            fontweight='bold'
        )
        
        ax.set_title(
            f'Distribución Hipergeométrica (N={N}, K={K}, n={n})\np={p:.4f}',
            fontsize=11,
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
            max_prob * 0.85 if max_prob > 0 else 0.1,
            f'μ={media:.2f}',
            ha='center',
            va='bottom',
            color='#2ecc71',
            fontsize=10,
            fontweight='bold'
        )
        
        max_x = min(n, K)
        ax.set_xlim(-0.5, max_x + 0.5)
        ax.set_xticks(valores_x)
        
        plt.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
