"""
Widget para mostrar tabla comparativa de aproximación de Poisson
"""

import customtkinter as ctk


class TablaComparacionPoisson(ctk.CTkFrame):
    """Widget para mostrar tabla comparativa acotada"""

    def __init__(self, master, expand_callback=None):
        """
        Inicializa widget de tabla comparativa

        Args:
            master: Widget padre
            expand_callback: Función callback al expandir tabla
        """
        super().__init__(master, fg_color="transparent")
        self.expand_callback = expand_callback
        self.datos_completos = None  # Guardar datos completos para expansión
        self.k_destacado = None
        self.es_expandido = False

        self.frame_contenido = ctk.CTkFrame(self)
        self.frame_contenido.pack(fill="both", expand=True)

        self.scrollframe = ctk.CTkScrollableFrame(self.frame_contenido)
        self.scrollframe.pack(fill="both", expand=True, padx=5, pady=5)

        self.header_frame = None
        self.filas = []

        self.btn_expandir = ctk.CTkButton(
            self, text="Ver tabla completa", command=self.expandir_tabla
        )

    def mostrar_tabla_acotada(self, valores_k, probs_binom, probs_poisson, k_destacado):
        """
        Muestra máximo 20 filas centradas en k_destacado

        Args:
            valores_k (list): Lista de valores de k
            probs_binom (list): Lista de probabilidades binomiales
            probs_poisson (list): Lista de probabilidades de Poisson
            k_destacado (int): Valor de k a destacar
        """
        self.datos_completos = (valores_k, probs_binom, probs_poisson)
        self.k_destacado = k_destacado
        self.es_expandido = False

        # Encontrar centro
        if k_destacado is None or k_destacado not in valores_k:
            k_centro = len(valores_k) // 2
        else:
            k_centro = valores_k.index(k_destacado)

        # Calcular rango acotado (máximo 20 filas)
        inicio = max(0, k_centro - 10)
        fin = min(len(valores_k), k_centro + 10)

        self._render_filas(
            valores_k[inicio:fin], probs_binom[inicio:fin], probs_poisson[inicio:fin]
        )

        # Mostrar botón de expansión
        self.btn_expandir.pack(pady=10)

    def mostrar_tabla_completa(self):
        """Muestra todas las filas"""
        if not self.datos_completos:
            return

        valores_k, probs_binom, probs_poisson = self.datos_completos
        self.es_expandido = True

        self._render_filas(valores_k, probs_binom, probs_poisson)

        # Ocultar botón de expansión
        self.btn_expandir.pack_forget()

    def _render_filas(self, valores_k, probs_binom, probs_poisson):
        """
        Renderiza las filas de la tabla

        Args:
            valores_k (list): Valores de k a mostrar
            probs_binom (list): Probabilidades binomiales
            probs_poisson (list): Probabilidades de Poisson
        """
        self.limpiar()

        # Header
        self.header_frame = ctk.CTkFrame(self.scrollframe, fg_color="#2b2b2b")
        self.header_frame.pack(fill="x", pady=(0, 2))

        for col in ["k", "P(X=k) Original", "P(X=k) Poisson"]:
            ctk.CTkLabel(
                self.header_frame,
                text=col,
                font=("Arial", 11, "bold"),
                text_color=("gray10", "gray90"),
            ).pack(side="left", padx=15, pady=5)

        # Filas
        for k, prob_orig, prob_pois in zip(valores_k, probs_binom, probs_poisson):
            es_destacado = k == self.k_destacado
            bg_color = "#3b8ed0" if es_destacado else "transparent"
            text_color = "white" if es_destacado else ("gray10", "gray90")

            fila = ctk.CTkFrame(self.scrollframe, fg_color=bg_color)
            fila.pack(fill="x", pady=1)

            ctk.CTkLabel(fila, text=str(k), width=40, text_color=text_color).pack(
                side="left", padx=15
            )

            ctk.CTkLabel(
                fila, text=f"{prob_orig:.6f}", width=120, text_color=text_color
            ).pack(side="left", padx=15)

            ctk.CTkLabel(
                fila, text=f"{prob_pois:.6f}", width=120, text_color=text_color
            ).pack(side="left", padx=15)

            self.filas.append(fila)

    def limpiar(self):
        """Limpia todas las filas de la tabla"""
        if self.header_frame:
            self.header_frame.destroy()
            self.header_frame = None

        for fila in self.filas:
            fila.destroy()

        self.filas.clear()

    def expandir_tabla(self):
        """Callback para expandir a tabla completa"""
        if self.expand_callback:
            self.expand_callback()
        else:
            self.mostrar_tabla_completa()
