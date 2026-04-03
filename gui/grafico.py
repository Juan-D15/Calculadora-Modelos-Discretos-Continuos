"""
Módulo para crear y gestionar gráficos de distribuciones
Diseño mejorado con colores diferenciados para valores específicos
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import math
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
        self.toggle_frame = None
        self.toggle_grafica = None
        self.modo_comparacion = False
        self.datos_actuales = None

    def limpiar(self):
        """Limpia el gráfico actual y cierra la figura de matplotlib"""
        try:
            if self.frame is not None and self.frame.winfo_exists():
                for widget in self.frame.winfo_children():
                    widget.destroy()
        except Exception:
            pass

        if self.figura is not None:
            try:
                plt.close(self.figura)
            except Exception:
                pass
            self.figura = None

        self.canvas = None
        self.toggle_frame = None
        self.toggle_grafica = None
        self.datos_actuales = None

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
        from utils import (
            calcular_media,
            calcular_desviacion_estandar,
            calcular_curtosis,
        )

        self.limpiar()

        media = calcular_media(n, p)
        desviacion = calcular_desviacion_estandar(n, p, N)
        curtosis, _ = calcular_curtosis(n, p, N)
        max_prob = max(probabilidades) if probabilidades else 1

        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")

        text_color = "#ffffff"
        grid_color = "#444444"
        bar_color_normal = "#3b8ed0"
        bar_color_destacado = "#e74c3c"
        curve_color = "#f39c12"
        normal_color = "#9b59b6"

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
            edgecolor="white",
            linewidth=0.5,
            width=bar_width,
            label="Distribución Binomial",
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
                label="Curva de distribución",
            )

        if desviacion > 0:
            x_normal = np.linspace(
                max(0, media - 4 * desviacion), media + 4 * desviacion, 200
            )
            y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * np.exp(
                -0.5 * ((x_normal - media) / desviacion) ** 2
            )
            if max(y_normal) > 0:
                y_normal = y_normal * (max_prob / max(y_normal))
            ax.plot(
                x_normal,
                y_normal,
                color=normal_color,
                linewidth=2,
                linestyle="--",
                alpha=0.8,
                label="Curva Normal (referencia)",
            )

        for i, (x, prob) in enumerate(zip(valores_x, probabilidades)):
            if x_destacado is not None and x == x_destacado:
                ax.text(
                    x,
                    prob + max_prob * 0.05,
                    f"P(X={x})={prob:.4f}",
                    ha="center",
                    va="bottom",
                    color="#e74c3c",
                    fontsize=10,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor="#2b2b2b",
                        edgecolor="#e74c3c",
                    ),
                )
            elif prob > max_prob * 0.05:
                ax.text(
                    x,
                    prob + max_prob * 0.02,
                    f"{prob:.3f}",
                    ha="center",
                    va="bottom",
                    color="white",
                    fontsize=8,
                    fontweight="bold",
                )

        ax.set_xlabel(
            "Número de éxitos (X)", fontsize=11, color=text_color, fontweight="bold"
        )
        ax.set_ylabel(
            "Probabilidad P(X)", fontsize=11, color=text_color, fontweight="bold"
        )

        poblacion_texto = (
            "Población Infinita" if es_infinita else f"Población Finita (N={N})"
        )
        ax.set_title(
            f"Distribución Binomial (n={n}, p={p:.4f})\n{poblacion_texto}",
            fontsize=11,
            color=text_color,
            fontweight="bold",
            pad=10,
        )

        legend = ax.legend(
            loc="upper right", facecolor="#3b3b3b", edgecolor="#555555", fontsize=9
        )
        for text in legend.get_texts():
            text.set_color(text_color)

        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines["bottom"].set_color(grid_color)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(grid_color)

        ax.grid(True, alpha=0.3, linestyle="--", color=grid_color, axis="y")
        ax.set_axisbelow(True)

        ax.axvline(x=media, color="#2ecc71", linestyle=":", linewidth=2, alpha=0.7)
        ax.text(
            media,
            max_prob * 0.85,
            f"μ={media:.2f}",
            ha="center",
            va="bottom",
            color="#2ecc71",
            fontsize=10,
            fontweight="bold",
        )

        if len(valores_x) > 0:
            ax.set_xlim(min(valores_x) - 0.5, max(valores_x) + 0.5)

        ax.set_xticks(valores_x)

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def crear_grafico_hipergeometrica(
        self, valores_x, probabilidades, n, N, K, p, x_destacado=None
    ):
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
            calcular_curtosis_hipergeometrica,
        )

        self.limpiar()

        media = calcular_media_hipergeometrica(n, N, K)
        desviacion = calcular_desviacion_hipergeometrica(n, N, K)
        curtosis, _ = calcular_curtosis_hipergeometrica(n, N, K)
        max_prob = max(probabilidades) if probabilidades else 1

        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")

        text_color = "#ffffff"
        grid_color = "#444444"
        bar_color_normal = "#9b59b6"
        bar_color_destacado = "#e74c3c"
        curve_color = "#f39c12"
        normal_color = "#3498db"

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
            edgecolor="white",
            linewidth=0.5,
            width=bar_width,
            label="Distribución Hipergeométrica",
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
                label="Curva de distribución",
            )

        if desviacion > 0:
            x_normal = np.linspace(
                max(0, media - 4 * desviacion), media + 4 * desviacion, 200
            )
            y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * np.exp(
                -0.5 * ((x_normal - media) / desviacion) ** 2
            )
            if max(y_normal) > 0:
                y_normal = y_normal * (max_prob / max(y_normal))
            ax.plot(
                x_normal,
                y_normal,
                color=normal_color,
                linewidth=2,
                linestyle="--",
                alpha=0.8,
                label="Curva Normal (referencia)",
            )

        for i, (x, prob) in enumerate(zip(valores_x, probabilidades)):
            if x_destacado is not None and x == x_destacado:
                ax.text(
                    x,
                    prob + max_prob * 0.05,
                    f"P(X={x})={prob:.4f}",
                    ha="center",
                    va="bottom",
                    color="#e74c3c",
                    fontsize=10,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor="#2b2b2b",
                        edgecolor="#e74c3c",
                    ),
                )
            elif prob > max_prob * 0.05:
                ax.text(
                    x,
                    prob + max_prob * 0.02,
                    f"{prob:.3f}",
                    ha="center",
                    va="bottom",
                    color="white",
                    fontsize=8,
                    fontweight="bold",
                )

        ax.set_xlabel(
            "Número de éxitos en la muestra (X)",
            fontsize=11,
            color=text_color,
            fontweight="bold",
        )
        ax.set_ylabel(
            "Probabilidad P(X)", fontsize=11, color=text_color, fontweight="bold"
        )

        ax.set_title(
            f"Distribución Hipergeométrica (N={N}, K={K}, n={n})\np={p:.4f}",
            fontsize=11,
            color=text_color,
            fontweight="bold",
            pad=10,
        )

        legend = ax.legend(
            loc="upper right", facecolor="#3b3b3b", edgecolor="#555555", fontsize=9
        )
        for text in legend.get_texts():
            text.set_color(text_color)

        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines["bottom"].set_color(grid_color)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(grid_color)

        ax.grid(True, alpha=0.3, linestyle="--", color=grid_color, axis="y")
        ax.set_axisbelow(True)

        ax.axvline(x=media, color="#2ecc71", linestyle=":", linewidth=2, alpha=0.7)
        ax.text(
            media,
            max_prob * 0.85 if max_prob > 0 else 0.1,
            f"μ={media:.2f}",
            ha="center",
            va="bottom",
            color="#2ecc71",
            fontsize=10,
            fontweight="bold",
        )

        max_x = min(n, K)
        ax.set_xlim(-0.5, max_x + 0.5)
        ax.set_xticks(valores_x)

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def crear_grafico_poisson(
        self,
        valores_x: list[int],
        probabilidades: list[float],
        lam: float,
        n: int,
        p: float,
        x_destacado: int = None,
    ):
        """
        Crea y muestra el gráfico de barras de la distribución de Poisson

        Args:
            valores_x (list): Valores del eje X
            probabilidades (list): Probabilidades correspondientes
            lam (float): Parámetro λ (media)
            n (int): Número de ensayos original
            p (float): Probabilidad de éxito original
            x_destacado (int, optional): Valor X específico a resaltar
        """
        self.limpiar()

        desviacion = math.sqrt(lam)
        max_prob = max(probabilidades) if probabilidades else 1

        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")

        text_color = "#ffffff"
        grid_color = "#444444"
        bar_color_normal = "#27ae60"
        bar_color_destacado = "#e74c3c"
        curve_color = "#f39c12"
        normal_color = "#3498db"

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
            edgecolor="white",
            linewidth=0.5,
            width=bar_width,
            label="Distribución de Poisson",
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
                label="Curva de distribución",
            )

        if desviacion > 0:
            x_normal = np.linspace(
                max(0, lam - 4 * desviacion), lam + 4 * desviacion, 200
            )
            y_normal = (1 / (desviacion * np.sqrt(2 * np.pi))) * np.exp(
                -0.5 * ((x_normal - lam) / desviacion) ** 2
            )
            if max(y_normal) > 0:
                y_normal = y_normal * (max_prob / max(y_normal))
            ax.plot(
                x_normal,
                y_normal,
                color=normal_color,
                linewidth=2,
                linestyle="--",
                alpha=0.8,
                label="Curva Normal (referencia)",
            )

        for i, (x, prob) in enumerate(zip(valores_x, probabilidades)):
            if x_destacado is not None and x == x_destacado:
                ax.text(
                    x,
                    prob + max_prob * 0.05,
                    f"P(X={x})={prob:.4f}",
                    ha="center",
                    va="bottom",
                    color="#e74c3c",
                    fontsize=10,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor="#2b2b2b",
                        edgecolor="#e74c3c",
                    ),
                )
            elif prob > max_prob * 0.05:
                ax.text(
                    x,
                    prob + max_prob * 0.02,
                    f"{prob:.3f}",
                    ha="center",
                    va="bottom",
                    color="white",
                    fontsize=8,
                    fontweight="bold",
                )

        ax.set_xlabel(
            "Número de eventos (X)", fontsize=11, color=text_color, fontweight="bold"
        )
        ax.set_ylabel(
            "Probabilidad P(X)", fontsize=11, color=text_color, fontweight="bold"
        )

        ax.set_title(
            f"Distribución de Poisson (λ={lam:.2f})\n"
            f"Aproximación de Binomial (n={n}, p={p:.4f})",
            fontsize=11,
            color=text_color,
            fontweight="bold",
            pad=10,
        )

        legend = ax.legend(
            loc="upper right", facecolor="#3b3b3b", edgecolor="#555555", fontsize=9
        )
        for text in legend.get_texts():
            text.set_color(text_color)

        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines["bottom"].set_color(grid_color)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(grid_color)

        ax.grid(True, alpha=0.3, linestyle="--", color=grid_color, axis="y")
        ax.set_axisbelow(True)

        ax.axvline(x=lam, color="#2ecc71", linestyle=":", linewidth=2, alpha=0.7)
        ax.text(
            lam,
            max_prob * 0.85,
            f"λ={lam:.2f}",
            ha="center",
            va="bottom",
            color="#2ecc71",
            fontsize=10,
            fontweight="bold",
        )

        if len(valores_x) > 0:
            ax.set_xlim(min(valores_x) - 0.5, max(valores_x) + 0.5)

        ax.set_xticks(valores_x)

        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def crear_grafico_comparacion(
        self,
        valores_x,
        probabilidades,
        probabilidades_acumuladas,
        n,
        p,
        N=None,
        es_infinita=True,
        x_destacado=None,
        es_hipergeometrica=False,
        K=None,
    ):
        """
        Crea gráfico con toggle para alternar entre P(x) y P acumulada

        Args:
            valores_x (list): Valores del eje X
            probabilidades (list): Probabilidades P(x)
            probabilidades_acumuladas (list): Probabilidades acumuladas
            n (int): Tamaño de muestra
            p (float): Probabilidad de éxito
            N (int, optional): Tamaño de población
            es_infinita (bool): Indica si la población es infinita
            x_destacado (int, optional): Valor X específico a resaltar
            es_hipergeometrica (bool): Si es distribución hipergeométrica
            K (int, optional): Éxitos en población (para hipergeométrica)
        """
        self.limpiar()
        self.modo_comparacion = True
        self.datos_actuales = {
            "valores_x": valores_x,
            "probabilidades": probabilidades,
            "probabilidades_acumuladas": probabilidades_acumuladas,
            "n": n,
            "p": p,
            "N": N,
            "es_infinita": es_infinita,
            "x_destacado": x_destacado,
            "es_hipergeometrica": es_hipergeometrica,
            "K": K,
        }

        self.toggle_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.toggle_frame.pack(fill="x", pady=5)

        self.toggle_grafica = ctk.CTkSegmentedButton(
            self.toggle_frame,
            values=["P(x)", "P Acumulada"],
            command=self._cambiar_tipo_grafica,
            selected_color="#3b8ed0",
            selected_hover_color="#3672a9",
        )
        self.toggle_grafica.set("P(x)")
        self.toggle_grafica.pack(pady=5)

        self._crear_grafico_px()

    def _cambiar_tipo_grafica(self, valor):
        """Cambia entre gráfica P(x) y P acumulada"""
        if self.datos_actuales is None:
            return

        if valor == "P(x)":
            self._crear_grafico_px()
        else:
            self._crear_grafico_acumulada()

    def _crear_grafico_px(self):
        """Crea la gráfica de probabilidad P(x)"""
        d = self.datos_actuales

        if d["es_hipergeometrica"]:
            self._crear_grafico_barras(
                d["valores_x"],
                d["probabilidades"],
                d["n"],
                d["p"],
                d["N"],
                d["es_infinita"],
                d["x_destacado"],
                es_hipergeometrica=True,
                K=d["K"],
            )
        else:
            self._crear_grafico_barras(
                d["valores_x"],
                d["probabilidades"],
                d["n"],
                d["p"],
                d["N"],
                d["es_infinita"],
                d["x_destacado"],
            )

    def _crear_grafico_acumulada(self):
        """Crea la gráfica de probabilidad acumulada"""
        d = self.datos_actuales

        if self.figura is not None:
            try:
                plt.close(self.figura)
            except Exception:
                pass

        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")

        text_color = "#ffffff"
        grid_color = "#444444"
        line_color = "#9b59b6" if d["es_hipergeometrica"] else "#3b8ed0"
        highlight_color = "#e74c3c"

        if d["x_destacado"] is not None and d["x_destacado"] in d["valores_x"]:
            idx = d["valores_x"].index(d["x_destacado"])
            for i, (x, prob_acum) in enumerate(
                zip(d["valores_x"], d["probabilidades_acumuladas"])
            ):
                color = highlight_color if i == idx else line_color
                marker = "o" if i == idx else "o"
                size = 12 if i == idx else 6
                ax.scatter(x, prob_acum, color=color, s=size**2, zorder=5)

            ax.plot(
                d["valores_x"],
                d["probabilidades_acumuladas"],
                color=line_color,
                linewidth=2,
                alpha=0.7,
                zorder=3,
            )

            prob_destacada = d["probabilidades_acumuladas"][idx]
            ax.axhline(
                y=prob_destacada, color=highlight_color, linestyle="--", alpha=0.5
            )
            ax.text(
                d["valores_x"][-1] * 0.02,
                prob_destacada + 0.02,
                f"P(X≤{d['x_destacado']})={prob_destacada:.4f}",
                color=highlight_color,
                fontsize=10,
                fontweight="bold",
            )
        else:
            ax.plot(
                d["valores_x"],
                d["probabilidades_acumuladas"],
                color=line_color,
                linewidth=2.5,
                marker="o",
                markersize=5,
            )

        if d["es_hipergeometrica"]:
            titulo = f"Probabilidad Acumulada - Hipergeométrica (N={d['N']}, K={d['K']}, n={d['n']})"
        else:
            pob_texto = (
                "Población Infinita"
                if d["es_infinita"]
                else f"Población Finita (N={d['N']})"
            )
            titulo = f"Probabilidad Acumulada - Binomial (n={d['n']}, p={d['p']:.4f})\n{pob_texto}"

        ax.set_xlabel(
            "Número de éxitos (X)", fontsize=11, color=text_color, fontweight="bold"
        )
        ax.set_ylabel("P(X ≤ x)", fontsize=11, color=text_color, fontweight="bold")
        ax.set_title(titulo, fontsize=11, color=text_color, fontweight="bold", pad=10)

        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines["bottom"].set_color(grid_color)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(grid_color)
        ax.grid(True, alpha=0.3, linestyle="--", color=grid_color)

        ax.set_xlim(min(d["valores_x"]) - 0.5, max(d["valores_x"]) + 0.5)
        ax.set_ylim(0, 1.05)
        ax.set_xticks(d["valores_x"])

        plt.tight_layout()

        try:
            if self.frame is not None and self.frame.winfo_exists():
                for widget in self.frame.winfo_children():
                    if widget != self.toggle_frame:
                        widget.destroy()
        except Exception:
            pass

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=5, pady=5, before=self.toggle_frame
        )

    def _crear_grafico_barras(
        self,
        valores_x,
        probabilidades,
        n,
        p,
        N=None,
        es_infinita=True,
        x_destacado=None,
        es_hipergeometrica=False,
        K=None,
    ):
        """Crea gráfico de barras reutilizable"""
        if es_hipergeometrica:
            from utils.calculos import (
                calcular_media_hipergeometrica,
                calcular_desviacion_hipergeometrica,
            )

            media = calcular_media_hipergeometrica(n, N, K)
            desviacion = calcular_desviacion_hipergeometrica(n, N, K)
        else:
            from utils import calcular_media, calcular_desviacion_estandar

            media = calcular_media(n, p)
            desviacion = calcular_desviacion_estandar(n, p, N)

        max_prob = max(probabilidades) if probabilidades else 1

        if self.figura is not None:
            try:
                plt.close(self.figura)
            except Exception:
                pass

        self.figura, ax = plt.subplots(figsize=(10, 7))
        self.figura.patch.set_facecolor("#2b2b2b")
        ax.set_facecolor("#2b2b2b")

        text_color = "#ffffff"
        grid_color = "#444444"
        bar_color_normal = "#9b59b6" if es_hipergeometrica else "#3b8ed0"
        bar_color_destacado = "#e74c3c"

        colores = []
        for x in valores_x:
            if x_destacado is not None and x == x_destacado:
                colores.append(bar_color_destacado)
            else:
                colores.append(bar_color_normal)

        bar_width = 0.7 if len(valores_x) <= 20 else 0.6

        ax.bar(
            valores_x,
            probabilidades,
            color=colores,
            alpha=0.8,
            edgecolor="white",
            linewidth=0.5,
            width=bar_width,
        )

        for i, (x, prob) in enumerate(zip(valores_x, probabilidades)):
            if x_destacado is not None and x == x_destacado:
                ax.text(
                    x,
                    prob + max_prob * 0.05,
                    f"P(X={x})={prob:.4f}",
                    ha="center",
                    va="bottom",
                    color="#e74c3c",
                    fontsize=10,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor="#2b2b2b",
                        edgecolor="#e74c3c",
                    ),
                )
            elif prob > max_prob * 0.05:
                ax.text(
                    x,
                    prob + max_prob * 0.02,
                    f"{prob:.3f}",
                    ha="center",
                    va="bottom",
                    color="white",
                    fontsize=8,
                    fontweight="bold",
                )

        if es_hipergeometrica:
            titulo = f"Distribución Hipergeométrica (N={N}, K={K}, n={n})"
        else:
            pob_texto = (
                "Población Infinita" if es_infinita else f"Población Finita (N={N})"
            )
            titulo = f"Distribución Binomial (n={n}, p={p:.4f})\n{pob_texto}"

        ax.set_xlabel(
            "Número de éxitos (X)", fontsize=11, color=text_color, fontweight="bold"
        )
        ax.set_ylabel(
            "Probabilidad P(X)", fontsize=11, color=text_color, fontweight="bold"
        )
        ax.set_title(titulo, fontsize=11, color=text_color, fontweight="bold", pad=10)

        ax.tick_params(colors=text_color, labelsize=10)
        ax.spines["bottom"].set_color(grid_color)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(grid_color)
        ax.grid(True, alpha=0.3, linestyle="--", color=grid_color, axis="y")

        ax.axvline(x=media, color="#2ecc71", linestyle=":", linewidth=2, alpha=0.7)
        ax.text(
            media,
            max_prob * 0.85,
            f"μ={media:.2f}",
            ha="center",
            va="bottom",
            color="#2ecc71",
            fontsize=10,
            fontweight="bold",
        )

        ax.set_xlim(min(valores_x) - 0.5, max(valores_x) + 0.5)
        ax.set_xticks(valores_x)

        plt.tight_layout()

        try:
            if self.frame is not None and self.frame.winfo_exists():
                for widget in self.frame.winfo_children():
                    if widget != self.toggle_frame:
                        widget.destroy()
        except Exception:
            pass

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=5, pady=5, before=self.toggle_frame
        )

    def crear_barras_agrupadas(
        self, valores_k, probs_orig, probs_poisson, k_destacado, n, titulo="Comparación"
    ):
        """
        Crea gráfica de barras agrupadas comparando dos distribuciones

        Args:
            valores_k (list): Valores de k
            probs_orig (list): Probabilidades de distribución original
            probs_poisson (list): Probabilidades de Poisson
            k_destacado (int): Valor de k a destacar
            n (int): Valor máximo de k
            titulo (str): Título de la gráfica
        """
        # Limpiar gráfica anterior
        self.limpiar()

        # Crear figura y ejes
        self.figura, self.ax = plt.subplots(figsize=(10, 6))

        # Configurar posiciones de barras
        x = np.array(valores_k)
        width = 0.35  # Ancho de cada barra

        # Crear barras agrupadas
        bars1 = self.ax.bar(
            x - width / 2,
            probs_orig,
            width,
            label="Original",
            color="#3b8ed0",
            alpha=0.8,
        )
        bars2 = self.ax.bar(
            x + width / 2,
            probs_poisson,
            width,
            label="Poisson",
            color="#ff6b6b",
            alpha=0.8,
        )

        # Destacar barra de k_ingresado
        if k_destacado is not None and k_destacado in valores_k:
            idx = valores_k.index(k_destacado)
            bars1[idx].set_alpha(1.0)
            bars1[idx].set_linewidth(2)
            bars1[idx].set_edgecolor("white")
            bars2[idx].set_alpha(1.0)
            bars2[idx].set_linewidth(2)
            bars2[idx].set_edgecolor("white")

        # Configurar ejes
        self.ax.set_xlabel("k", fontsize=12)
        self.ax.set_ylabel("P(X=k)", fontsize=12)
        self.ax.set_title(titulo, fontsize=14, fontweight="bold")
        self.ax.legend(fontsize=10)
        self.ax.grid(True, alpha=0.3, linestyle="--")

        # Configurar fondo
        self.ax.set_facecolor("#2b2b2b")
        self.figura.patch.set_facecolor("#2b2b2b")
        self.ax.tick_params(axis="x", colors="white")
        self.ax.tick_params(axis="y", colors="white")
        self.ax.xaxis.label.set_color("white")
        self.ax.yaxis.label.set_color("white")

        # Ajustar ticks si n es grande
        if n > 50:
            step = max(1, n // 20)
            self.ax.set_xticks(x[::step])

        # Crear canvas
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
