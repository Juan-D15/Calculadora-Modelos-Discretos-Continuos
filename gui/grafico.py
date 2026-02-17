"""
Módulo para crear y gestionar gráficos de la distribución binomial
Gráfico mejorado para visualizar la curtosis
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraficoBinomial:
    """Clase para crear y gestionar el gráfico de distribución binomial"""
    
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
        # Destruir widgets
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Cerrar figura de matplotlib si existe
        if self.figura is not None:
            try:
                plt.close(self.figura)
            except Exception:
                pass
            self.figura = None
        
        self.canvas = None
    
    def crear_grafico(self, valores_x, probabilidades, n, p, N=None, es_infinita=True):
        """
        Crea y muestra el gráfico de barras de la distribución binomial
        con curva suave para visualizar la curtosis
        
        Args:
            valores_x (list): Valores del eje X
            probabilidades (list): Probabilidades correspondientes
            n (int): Tamaño de muestra
            p (float): Probabilidad de éxito
            N (int, optional): Tamaño de población
            es_infinita (bool): Indica si la población es infinita
        """
        from utils import calcular_media, calcular_desviacion_estandar, calcular_curtosis
        
        # Limpiar gráfico anterior
        self.limpiar()
        
        # Calcular estadísticas
        media = calcular_media(n, p)
        desviacion = calcular_desviacion_estandar(n, p, N)
        curtosis, _ = calcular_curtosis(n, p, N)
        max_prob = max(probabilidades)
        
        # Crear figura con mejor tamaño y márgenes (más grande)
        self.figura, ax = plt.subplots(figsize=(14, 9))
        self.figura.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        # Configurar colores
        text_color = '#ffffff'
        grid_color = '#444444'
        bar_color = '#3b8ed0'
        bar_edge = '#ffffff'
        curve_color = '#ff6b6b'
        normal_color = '#ffd93d'
        
        # Crear gráfico de barras para TODOS los valores de X
        # Ajustar el ancho de las barras según la cantidad de valores
        if n <= 20:
            bar_width = 0.7
        elif n <= 50:
            bar_width = 0.6
        else:
            bar_width = 0.5
        
        bars = ax.bar(
            valores_x,
            probabilidades,
            color=bar_color,
            alpha=0.7,
            edgecolor=bar_edge,
            linewidth=1.0,
            width=bar_width,
            label='Distribución Binomial'
        )
        
        # Crear curva suave para la distribución binomial (completa)
        x_suave = np.linspace(min(valores_x) - 0.5, max(valores_x) + 0.5, 300)
        y_suave = np.interp(x_suave, valores_x, probabilidades)
        ax.plot(
            x_suave,
            y_suave,
            color=curve_color,
            linewidth=3,
            alpha=0.9,
            label='Curva Ajustada'
        )
        
        # Crear curva de distribución normal para comparación (curva mesocúrtica)
        x_normal = np.linspace(media - 4*desviacion, media + 4*desviacion, 200)
        y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * \
                   np.exp(-0.5 * ((x_normal - media) / desviacion) ** 2)
        # Ajustar escala de la normal para comparar con binomial
        y_normal = y_normal * (max(probabilidades) / max(y_normal))
        ax.plot(
            x_normal,
            y_normal,
            color=normal_color,
            linewidth=2,
            linestyle='--',
            alpha=0.7,
            label='Normal (Mesocúrtica)'
        )
        
        # Añadir valores encima de las barras (solo para probabilidades significativas)
        for x, prob in zip(valores_x, probabilidades):
            if prob > max_prob * 0.1:
                text_y = prob + (max_prob * 0.015)
                
                if prob >= 0.01:
                    text_str = f'{prob:.3f}'
                elif prob >= 0.001:
                    text_str = f'{prob:.4f}'
                elif prob >= 0.0001:
                    text_str = f'{prob:.5f}'
                else:
                    text_str = f'{prob:.6f}'
                
                ax.text(
                    x,
                    text_y,
                    text_str,
                    ha='center',
                    va='bottom',
                    color=text_color,
                    fontsize=7 if n > 40 else 8,
                    fontweight='bold'
                )
        
        # Configurar ejes
        ax.set_xlabel(
            'Número de éxitos (X)',
            fontsize=12,
            color=text_color,
            fontweight='bold'
        )
        ax.set_ylabel(
            'Probabilidad P(X)',
            fontsize=12,
            color=text_color,
            fontweight='bold'
        )
        
        # Título con información de curtosis
        poblacion_texto = "Población Infinita" if es_infinita else f"Población Finita (N={N})"
        curtosis_interpretacion = "Mesocúrtica" if abs(curtosis) <= 0.1 else \
                                  "Leptocúrtica (Elevada)" if curtosis > 0.1 else \
                                  "Platicúrtica (Aplanada)"
        
        ax.set_title(
            f'Distribución Binomial (n={n}, p={p:.4f})\n{poblacion_texto} | Curtosis: {curtosis:.4f} ({curtosis_interpretacion})',
            fontsize=10,
            color=text_color,
            fontweight='bold',
            pad=15
        )
        
        # Añadir leyenda
        legend = ax.legend(
            loc='upper right',
            facecolor='#3b3b3b',
            edgecolor='#555555',
            fontsize=10
        )
        for text in legend.get_texts():
            text.set_color(text_color)
        
        # Configurar grid
        ax.grid(True, alpha=0.3, linestyle='--', color=grid_color, axis='y')
        ax.set_axisbelow(True)
        
        # Personalizar colores de los ejes y ticks
        ax.tick_params(
            colors=text_color,
            labelsize=10,
            width=1
        )
        ax.spines['bottom'].set_color(grid_color)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(grid_color)
        ax.spines['left'].set_linewidth(1.5)
        
        # Configurar límites del eje X
        ax.set_xlim(-0.5, n + 0.5)
        
        # Configurar ticks del eje X: mostrar TODOS los valores
        ax.set_xticks(valores_x)
        
        # Añadir líneas guía para media
        ax.axvline(
            x=media,
            color='#00ff00',
            linestyle=':',
            linewidth=2,
            alpha=0.6,
            label=f'Media = {media:.2f}'
        )
        ax.text(
            media,
            max_prob * 0.95,
            f'μ = {media:.2f}',
            ha='center',
            va='bottom',
            color='#00ff00',
            fontsize=10,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#3b3b3b', edgecolor='#00ff00', alpha=0.8)
        )
        
        # Ajustar layout con márgenes óptimos
        plt.tight_layout(pad=2.0)
        
        # Integrar en tkinter
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
    
    def crear_grafico_hipergeometrica(self, valores_x, probabilidades, n, N, K, p):
        """
        Crea y muestra el gráfico de barras de la distribución hipergeométrica
        
        Args:
            valores_x (list): Valores del eje X
            probabilidades (list): Probabilidades correspondientes
            n (int): Tamaño de muestra
            N (int): Tamaño de población
            K (int): Éxitos en población
            p (float): Probabilidad implícita (K/N)
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
        max_prob = max(probabilidades) if probabilidades else 0
        
        self.figura, ax = plt.subplots(figsize=(14, 9))
        self.figura.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        text_color = '#ffffff'
        grid_color = '#444444'
        bar_color = '#9b59b6'
        bar_edge = '#ffffff'
        curve_color = '#e74c3c'
        normal_color = '#ffd93d'
        
        bar_width = 0.7 if len(valores_x) <= 20 else 0.6
        
        bars = ax.bar(
            valores_x,
            probabilidades,
            color=bar_color,
            alpha=0.7,
            edgecolor=bar_edge,
            linewidth=1.0,
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
                linewidth=3,
                alpha=0.9,
                label='Curva Ajustada'
            )
        
        if desviacion > 0:
            x_normal = np.linspace(media - 4*desviacion, media + 4*desviacion, 200)
            y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * \
                       np.exp(-0.5 * ((x_normal - media) / desviacion) ** 2)
            y_normal = y_normal * (max(probabilidades) / max(y_normal)) if max(y_normal) > 0 else y_normal
            ax.plot(
                x_normal,
                y_normal,
                color=normal_color,
                linewidth=2,
                linestyle='--',
                alpha=0.7,
                label='Normal (Referencia)'
            )
        
        for x, prob in zip(valores_x, probabilidades):
            if prob > max_prob * 0.1:
                text_y = prob + (max_prob * 0.015)
                if prob >= 0.01:
                    text_str = f'{prob:.3f}'
                elif prob >= 0.001:
                    text_str = f'{prob:.4f}'
                else:
                    text_str = f'{prob:.5f}'
                ax.text(
                    x,
                    text_y,
                    text_str,
                    ha='center',
                    va='bottom',
                    color=text_color,
                    fontsize=8,
                    fontweight='bold'
                )
        
        ax.set_xlabel(
            'Número de éxitos en la muestra (X)',
            fontsize=12,
            color=text_color,
            fontweight='bold'
        )
        ax.set_ylabel(
            'Probabilidad P(X)',
            fontsize=12,
            color=text_color,
            fontweight='bold'
        )
        
        curtosis_interpretacion = "Mesocúrtica" if abs(curtosis) <= 0.1 else \
                                  "Leptocúrtica" if curtosis > 0.1 else "Platicúrtica"
        
        ax.set_title(
            f'Distribución Hipergeométrica (N={N}, K={K}, n={n})\n'
            f'p={p:.4f} | Curtosis: {curtosis:.4f} ({curtosis_interpretacion})',
            fontsize=10,
            color=text_color,
            fontweight='bold',
            pad=15
        )
        
        legend = ax.legend(
            loc='upper right',
            facecolor='#3b3b3b',
            edgecolor='#555555',
            fontsize=10
        )
        for text in legend.get_texts():
            text.set_color(text_color)
        
        ax.grid(True, alpha=0.3, linestyle='--', color=grid_color, axis='y')
        ax.set_axisbelow(True)
        
        ax.tick_params(colors=text_color, labelsize=10, width=1)
        ax.spines['bottom'].set_color(grid_color)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(grid_color)
        ax.spines['left'].set_linewidth(1.5)
        
        max_x = min(n, K)
        ax.set_xlim(-0.5, max_x + 0.5)
        ax.set_xticks(valores_x)
        
        ax.axvline(
            x=media,
            color='#00ff00',
            linestyle=':',
            linewidth=2,
            alpha=0.6
        )
        ax.text(
            media,
            max_prob * 0.95 if max_prob > 0 else 0.1,
            f'μ = {media:.2f}',
            ha='center',
            va='bottom',
            color='#00ff00',
            fontsize=10,
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#3b3b3b', edgecolor='#00ff00', alpha=0.8)
        )
        
        plt.tight_layout(pad=2.0)
        
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
