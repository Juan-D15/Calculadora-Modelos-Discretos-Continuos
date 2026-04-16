"""
Módulo con los componentes de entrada de datos
Diseño mejorado y centrado
"""

import customtkinter as ctk


class CamposEntrada:
    """Clase para gestionar los campos de entrada de datos"""

    def __init__(self, frame_contenedor):
        """
        Inicializa los campos de entrada

        Args:
            frame_contenedor: Frame donde se colocarán los campos
        """
        self.frame = frame_contenedor
        self.n_entry = None
        self.p_entry = None
        self.n_entry_poblacion = None
        self.x_entry = None
        self.checkbox_comparacion = None
        self.tolerancia_entry = None
        self.frame_comparacion = None
        self.K_entry = None
        self.chk_poisson = None

        self.crear_campos()

    def crear_campos(self):
        """Crea todos los campos de entrada"""
        row1 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row1.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row1, text="Tamaño de muestra (n):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.n_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 10")
        self.n_entry.pack(side="left", padx=8)

        ctk.CTkLabel(
            row1, text="Probabilidad de éxito (p):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.p_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 0.5 o 50")
        self.p_entry.pack(side="left", padx=8)

        ctk.CTkLabel(row1, text="Población (N):", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=8
        )

        self.n_entry_poblacion = ctk.CTkEntry(
            row1, width=120, placeholder_text="Opcional (ej: 100)"
        )
        self.n_entry_poblacion.pack(side="left", padx=8)

        row2 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row2.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row2, text="Valores de X (separados por coma):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.x_entry = ctk.CTkEntry(
            row2,
            width=380,
            placeholder_text="Ej: 6 (rango 0-6), 0,1,2 o 'todos' (vacio=0 a n)",
        )
        self.x_entry.pack(side="left", padx=8)

        self.checkbox_comparacion = ctk.CTkCheckBox(
            row2,
            text="Comparar con Hipergeométrica",
            font=ctk.CTkFont(size=12),
            command=self._toggle_comparacion,
        )
        self.checkbox_comparacion.pack(side="left", padx=15)

        self.chk_poisson = ctk.CTkCheckBox(
            row2,
            text="Activar aproximación Poisson",
            font=ctk.CTkFont(size=12),
            command=self.on_poisson_toggle,
        )
        self.chk_poisson.pack(side="left", padx=10)

        self.frame_comparacion = ctk.CTkFrame(self.frame, fg_color="transparent")

        tolerancia_frame = ctk.CTkFrame(self.frame_comparacion, fg_color="transparent")
        tolerancia_frame.pack(fill="x", pady=4)

        ctk.CTkLabel(
            tolerancia_frame, text="Tolerancia (%):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.tolerancia_entry = ctk.CTkEntry(
            tolerancia_frame, width=100, placeholder_text="95"
        )
        self.tolerancia_entry.insert(0, "95")
        self.tolerancia_entry.pack(side="left", padx=8)

        ctk.CTkLabel(
            tolerancia_frame, text="Éxitos en población (K):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.K_entry = ctk.CTkEntry(
            tolerancia_frame, width=100, placeholder_text="Opcional"
        )
        self.K_entry.pack(side="left", padx=8)

        info_label = ctk.CTkLabel(
            tolerancia_frame,
            text="(Si K vacío: K = p × N)",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        info_label.pack(side="left", padx=8)

    def _toggle_comparacion(self):
        """Muestra u oculta los campos de comparación"""
        if self.checkbox_comparacion.get():
            self.frame_comparacion.pack(fill="x", pady=4)
        else:
            self.frame_comparacion.pack_forget()

    def on_poisson_toggle(self):
        """
        Callback cuando cambia el checkbox de aproximación Poisson
        Recalcula si hay datos válidos en el dashboard
        """
        if self.frame and hasattr(self.frame, "ventana_principal"):
            # Recalculará a través de ventana_principal
            pass

    def es_comparacion_activa(self):
        """
        Verifica si el modo comparación está activo

        Returns:
            bool: True si el checkbox está marcado
        """
        return self.checkbox_comparacion.get() if self.checkbox_comparacion else False

    def obtener_valores(self):
        """
        Obtiene los valores de todos los campos

        Returns:
            dict: Diccionario con los valores de entrada
        """
        n_pob = self.n_entry_poblacion.get().strip()
        tolerancia = (
            self.tolerancia_entry.get().strip()
            if self.es_comparacion_activa()
            else None
        )
        K_val = (
            self.K_entry.get().strip()
            if self.es_comparacion_activa() and self.K_entry
            else None
        )

        return {
            "n": self.n_entry.get().strip(),
            "p": self.p_entry.get().strip(),
            "n_poblacion": n_pob if n_pob else None,
            "x": self.x_entry.get().strip(),
            "comparacion": self.es_comparacion_activa(),
            "tolerancia": tolerancia,
            "K": K_val if K_val else None,
        }

    def limpiar(self):
        """Limpia todos los campos de entrada"""
        self.n_entry.delete(0, "end")
        self.p_entry.delete(0, "end")
        self.n_entry_poblacion.delete(0, "end")
        self.x_entry.delete(0, "end")
        self.tolerancia_entry.delete(0, "end")
        self.tolerancia_entry.insert(0, "95")
        if self.K_entry:
            self.K_entry.delete(0, "end")
        self.checkbox_comparacion.deselect()
        self.frame_comparacion.pack_forget()


class CamposEntradaHipergeometrica:
    """Clase para gestionar los campos de entrada de distribución hipergeométrica"""

    def __init__(self, frame_contenedor):
        """
        Inicializa los campos de entrada para hipergeométrica

        Args:
            frame_contenedor: Frame donde se colocarán los campos
        """
        self.frame = frame_contenedor
        self.N_entry = None
        self.K_entry = None
        self.n_entry = None
        self.x_entry = None
        self.chk_poisson = None

        self.crear_campos()

    def crear_campos(self):
        """Crea todos los campos de entrada para hipergeométrica"""
        row1 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row1.pack(fill="x", pady=4)

        ctk.CTkLabel(row1, text="Población total (N):", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=8
        )

        self.N_entry = ctk.CTkEntry(row1, width=100, placeholder_text="Ej: 100")
        self.N_entry.pack(side="left", padx=8)

        ctk.CTkLabel(
            row1, text="Éxitos en población (K):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.K_entry = ctk.CTkEntry(row1, width=100, placeholder_text="Ej: 30")
        self.K_entry.pack(side="left", padx=8)

        ctk.CTkLabel(row1, text="Tamaño muestra (n):", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=8
        )

        self.n_entry = ctk.CTkEntry(row1, width=100, placeholder_text="Ej: 20")
        self.n_entry.pack(side="left", padx=8)

        row2 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row2.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row2, text="Valores de X (separados por coma):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.x_entry = ctk.CTkEntry(
            row2,
            width=380,
            placeholder_text="Ej: 5 (rango 0-5), 0,1,2 o 'todos' (vacio=todos)",
        )
        self.x_entry.pack(side="left", padx=8)

        self.chk_poisson = ctk.CTkCheckBox(
            row2,
            text="Activar aproximación Poisson",
            font=ctk.CTkFont(size=12),
            command=self.on_poisson_toggle,
        )
        self.chk_poisson.pack(side="left", padx=10)

    def on_poisson_toggle(self):
        """
        Callback cuando cambia el checkbox de aproximación Poisson
        Recalcula si hay datos válidos en el dashboard
        """
        if self.frame and hasattr(self.frame, "ventana_principal"):
            # Recalculará a través de ventana_principal
            pass

    def obtener_valores(self):
        """
        Obtiene los valores de todos los campos

        Returns:
            dict: Diccionario con los valores de entrada
        """
        return {
            "N": self.N_entry.get().strip(),
            "K": self.K_entry.get().strip(),
            "n": self.n_entry.get().strip(),
            "x": self.x_entry.get().strip(),
        }

    def limpiar(self):
        """Limpia todos los campos de entrada"""
        self.N_entry.delete(0, "end")
        self.K_entry.delete(0, "end")
        self.n_entry.delete(0, "end")
        self.x_entry.delete(0, "end")


class CamposEntradaPoisson:
    """Clase para gestionar los campos de entrada de distribución Poisson"""

    def __init__(self, frame_contenedor):
        """
        Inicializa los campos de entrada para Poisson

        Args:
            frame_contenedor: Frame donde se colocarán los campos
        """
        self.frame = frame_contenedor
        self.n_entry = None
        self.p_entry = None
        self.x_entry = None

        self.crear_campos()

    def crear_campos(self):
        """Crea todos los campos de entrada para Poisson"""
        row1 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row1.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row1, text="Número de ensayos (n):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.n_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 100")
        self.n_entry.pack(side="left", padx=8)

        ctk.CTkLabel(
            row1, text="Probabilidad de éxito (p):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.p_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 0.05 o 5")
        self.p_entry.pack(side="left", padx=8)

        info_label = ctk.CTkLabel(
            row1,
            text="(acepta: 0.05 o 5 para 5%)",
            font=ctk.CTkFont(size=10),
            text_color="gray",
        )
        info_label.pack(side="left", padx=8)

        row2 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row2.pack(fill="x", pady=4)

        ctk.CTkLabel(
            row2, text="Valores de X (separados por coma):", font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.x_entry = ctk.CTkEntry(
            row2,
            width=380,
            placeholder_text="Ej: 0,1,2,3 o 'todos' (vacío=0 a n)",
        )
        self.x_entry.pack(side="left", padx=8)

        condiciones_label = ctk.CTkLabel(
            row2,
            text="Condiciones: p < 0.10 y λ < 10",
            font=ctk.CTkFont(size=10),
            text_color="#3b8ed0",
        )
        condiciones_label.pack(side="left", padx=15)

    def obtener_valores(self):
        """
        Obtiene los valores de todos los campos

        Returns:
            dict: Diccionario con los valores de entrada
        """
        return {
            "n": self.n_entry.get().strip(),
            "p": self.p_entry.get().strip(),
            "x": self.x_entry.get().strip(),
        }

    def limpiar(self):
        """Limpia todos los campos de entrada"""
        self.n_entry.delete(0, "end")
        self.p_entry.delete(0, "end")
        self.x_entry.delete(0, "end")


class CamposEntradaMM1:
    """Clase para gestionar los campos de entrada del modelo M/M/1"""

    def __init__(self, frame_contenedor):
        """
        Inicializa los campos de entrada para M/M/1

        Args:
            frame_contenedor: Frame donde se colocarán los campos
        """
        self.frame = frame_contenedor
        self.lam_entry = None
        self.mu_entry = None
        self.n_entry = None

        self.crear_campos()

    def crear_campos(self):
        """Crea todos los campos de entrada para M/M/1"""
        row1 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row1.pack(fill="x", pady=4)

        ctk.CTkLabel(row1, text="Tasa de llegada λ:", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=8
        )

        self.lam_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 4")
        self.lam_entry.pack(side="left", padx=8)

        ctk.CTkLabel(row1, text="Tasa de servicio μ:", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=8
        )

        self.mu_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 6")
        self.mu_entry.pack(side="left", padx=8)

        ctk.CTkLabel(row1, text="Clientes (n):", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=8
        )

        self.n_entry = ctk.CTkEntry(
            row1, width=100, placeholder_text="Opcional (ej: 3)"
        )
        self.n_entry.pack(side="left", padx=8)

        info_label = ctk.CTkLabel(
            row1,
            text="(λ debe ser < μ para sistema estable)",
            font=ctk.CTkFont(size=10),
            text_color="gray",
        )
        info_label.pack(side="left", padx=8)

    def obtener_valores(self):
        """
        Obtiene los valores de todos los campos

        Returns:
            dict: Diccionario con los valores de entrada
        """
        return {
            "lam": self.lam_entry.get().strip(),
            "mu": self.mu_entry.get().strip(),
            "n": self.n_entry.get().strip(),
        }

    def limpiar(self):
        """Limpia todos los campos de entrada"""
        self.lam_entry.delete(0, "end")
        self.mu_entry.delete(0, "end")
        self.n_entry.delete(0, "end")
