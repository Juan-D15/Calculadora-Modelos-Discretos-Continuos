"""
Componente de tabla para comparación de distribuciones
Muestra resultados con toggle entre Binomial e Hipergeométrica
"""

import customtkinter as ctk


class TablaComparacion:
    """Tabla con toggle para mostrar resultados de ambas distribuciones"""

    def __init__(self, frame_contenedor, on_cambio_distribucion=None):
        """
        Inicializa la tabla de comparación

        Args:
            frame_contenedor: Frame donde se mostrará la tabla
            on_cambio_distribucion: Callback que se llama cuando cambia la distribución
        """
        self.frame_contenedor = frame_contenedor
        self.on_cambio_distribucion = on_cambio_distribucion
        self.frame = ctk.CTkFrame(frame_contenedor, fg_color="transparent")
        self.datos_binomial = None
        self.datos_hipergeometrica = None
        self.tolerancia = None
        self.distribucion_actual = "binomial"

        self.toggle = None
        self.tabla = None
        self.mensaje_label = None
        self.info_label = None

        self.crear_componentes()

    def crear_componentes(self):
        """Crea los componentes de la tabla"""
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.toggle = ctk.CTkSegmentedButton(
            header_frame,
            values=["Binomial", "Hipergeométrica"],
            command=self._cambiar_distribucion,
            selected_color="#3b8ed0",
            selected_hover_color="#3672a9",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.toggle.set("Binomial")
        self.toggle.pack(side="left", padx=5)

        self.info_label = ctk.CTkLabel(
            header_frame, text="", font=ctk.CTkFont(size=11), text_color="gray"
        )
        self.info_label.pack(side="right", padx=10)

        table_container = ctk.CTkFrame(self.frame)
        table_container.grid(row=1, column=0, sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_columnconfigure(1, weight=2)
        table_container.grid_columnconfigure(2, weight=2)

        header_x = ctk.CTkLabel(
            table_container,
            text="X",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3b8ed0",
            corner_radius=5,
            height=30,
        )
        header_x.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)

        header_px = ctk.CTkLabel(
            table_container,
            text="P(X)",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3b8ed0",
            corner_radius=5,
            height=30,
        )
        header_px.grid(row=0, column=1, sticky="ew", padx=2, pady=5)

        header_acum = ctk.CTkLabel(
            table_container,
            text="P(X ≤ x)",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3b8ed0",
            corner_radius=5,
            height=30,
        )
        header_acum.grid(row=0, column=2, sticky="ew", padx=(2, 5), pady=5)

        self.tabla = ctk.CTkScrollableFrame(table_container, fg_color="transparent")
        self.tabla.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.tabla.grid_columnconfigure(0, weight=1)
        self.tabla.grid_columnconfigure(1, weight=2)
        self.tabla.grid_columnconfigure(2, weight=2)

        self.mensaje_label = ctk.CTkLabel(
            self.frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2ecc71",
            wraplength=400,
        )
        self.mensaje_label.grid(row=2, column=0, pady=10)

    def _cambiar_distribucion(self, valor):
        """Cambia la distribución mostrada"""
        self.distribucion_actual = (
            "binomial" if valor == "Binomial" else "hipergeometrica"
        )
        self._actualizar_tabla()
        if self.on_cambio_distribucion:
            self.on_cambio_distribucion(self.distribucion_actual)

    def mostrar(self, datos_binomial, datos_hipergeometrica, tolerancia):
        """
        Muestra los datos de ambas distribuciones

        Args:
            datos_binomial (dict): Datos de distribución binomial
            datos_hipergeometrica (dict): Datos de distribución hipergeométrica
            tolerancia (float): Porcentaje de tolerancia para buscar valor
        """
        self.datos_binomial = datos_binomial
        self.datos_hipergeometrica = datos_hipergeometrica
        self.tolerancia = tolerancia

        self._actualizar_info()
        self._actualizar_tabla()

    def _actualizar_info(self):
        """Actualiza la información de la distribución actual"""
        if self.distribucion_actual == "binomial" and self.datos_binomial:
            d = self.datos_binomial
            n, p, N = d["n"], d["p"], d["N"]
            pob = f"N={N}" if N else "Pob. Infinita"
            self.info_label.configure(
                text=f"n={n}, p={p:.4f}, {pob} | μ={d['media']:.2f}, σ={d['desviacion']:.4f}"
            )
        elif self.datos_hipergeometrica:
            d = self.datos_hipergeometrica
            self.info_label.configure(
                text=f"N={d['N']}, K={d['K']}, n={d['n']} | μ={d['media']:.2f}, σ={d['desviacion']:.4f}"
            )

    def _actualizar_tabla(self):
        """Actualiza la tabla con los datos de la distribución actual"""
        if self.distribucion_actual == "binomial":
            datos = self.datos_binomial
            color_normal = "#3b8ed0"
        else:
            datos = self.datos_hipergeometrica
            color_normal = "#9b59b6"

        if not datos:
            return

        for widget in self.tabla.winfo_children():
            widget.destroy()

        valores_x = datos.get("valores_x", [])
        probabilidades = datos.get("probabilidades", [])
        probabilidades_acumuladas = datos.get("probabilidades_acumuladas", [])
        valor_tolerancia = datos.get("valor_tolerancia", None)

        row_destacado = None

        for i, x in enumerate(valores_x):
            prob = probabilidades[i] if i < len(probabilidades) else 0
            prob_acum = (
                probabilidades_acumuladas[i]
                if i < len(probabilidades_acumuladas)
                else 0
            )

            es_destacado = valor_tolerancia is not None and x == valor_tolerancia

            if es_destacado:
                fg_color = "#e74c3c"
                text_color = "white"
            else:
                fg_color = "transparent"
                text_color = ("gray10", "gray90")

            row_frame = ctk.CTkFrame(self.tabla, fg_color=fg_color, corner_radius=5)
            row_frame.grid(row=i, column=0, columnspan=3, sticky="ew", pady=1)
            row_frame.grid_columnconfigure(0, weight=1)
            row_frame.grid_columnconfigure(1, weight=2)
            row_frame.grid_columnconfigure(2, weight=2)

            if es_destacado:
                row_destacado = row_frame

            label_x = ctk.CTkLabel(
                row_frame,
                text=str(x),
                font=ctk.CTkFont(size=12, weight="bold" if es_destacado else "normal"),
                text_color=text_color,
            )
            label_x.grid(row=0, column=0, padx=5, pady=3)

            label_px = ctk.CTkLabel(
                row_frame,
                text=f"{prob:.6f}",
                font=ctk.CTkFont(size=11, weight="bold" if es_destacado else "normal"),
                text_color=text_color,
            )
            label_px.grid(row=0, column=1, padx=5, pady=3)

            label_acum = ctk.CTkLabel(
                row_frame,
                text=f"{prob_acum:.6f} ({prob_acum * 100:.2f}%)",
                font=ctk.CTkFont(size=11, weight="bold" if es_destacado else "normal"),
                text_color=text_color,
            )
            label_acum.grid(row=0, column=2, padx=5, pady=3)

        if valor_tolerancia is not None:
            idx = (
                valores_x.index(valor_tolerancia)
                if valor_tolerancia in valores_x
                else None
            )
            if idx is not None and idx < len(probabilidades_acumuladas):
                prob_acum_tolerancia = probabilidades_acumuladas[idx] * 100
                self.mensaje_label.configure(
                    text=f"Para tolerancia {self.tolerancia}%, el valor más cercano es X = {valor_tolerancia} "
                    f"con P(X ≤ {valor_tolerancia}) = {prob_acum_tolerancia:.2f}%"
                )
                if row_destacado is not None:
                    self.tabla.after(
                        200, lambda r=row_destacado: self._scroll_to_widget(r)
                    )
        else:
            self.mensaje_label.configure(text="")

    def _scroll_to_widget(self, widget):
        """Hace scroll para mostrar el widget destacado"""
        try:
            self.tabla.update_idletasks()
            widget.update_idletasks()

            canvas = self.tabla._parent_frame

            widget_y = widget.winfo_y()
            canvas_height = canvas.winfo_height()

            children = self.tabla.winfo_children()
            if children:
                total_height = children[-1].winfo_y() + children[-1].winfo_height() + 10
            else:
                total_height = canvas_height

            if total_height > canvas_height:
                scroll_region = total_height - canvas_height
                if scroll_region > 0:
                    target_y = max(0, widget_y - 30)
                    scroll_fraction = target_y / scroll_region
                    scroll_fraction = max(0, min(1, scroll_fraction))
                    canvas.yview_moveto(scroll_fraction)
        except Exception:
            pass

    def limpiar(self):
        """Limpia la tabla"""
        self.datos_binomial = None
        self.datos_hipergeometrica = None
        self.tolerancia = None

        try:
            if self.tabla is not None and self.tabla.winfo_exists():
                for widget in self.tabla.winfo_children():
                    widget.destroy()
        except Exception:
            pass

        try:
            if self.mensaje_label is not None and self.mensaje_label.winfo_exists():
                self.mensaje_label.configure(text="")
            if self.info_label is not None and self.info_label.winfo_exists():
                self.info_label.configure(text="")
        except Exception:
            pass
