"""
Módulo para el área de visualización de resultados
Diseño mejorado con secciones visuales
"""
import customtkinter as ctk


class AreaResultados:
    """Clase para gestionar el área de visualización de resultados"""
    
    def __init__(self, frame_contenedor):
        """
        Inicializa el área de resultados
        
        Args:
            frame_contenedor: Frame contenedor principal
        """
        self.frame = frame_contenedor
        self.scrollable_frame = None
        self.resultados_data = None
        
        self.crear_area()
    
    def crear_area(self):
        """Crea el área con secciones organizadas"""
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="transparent"
        )
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
    
    def limpiar(self):
        """Limpia el área de resultados"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.resultados_data = None
    
    def mostrar_texto(self, texto):
        """
        Muestra texto simple (compatibilidad hacia atrás)
        
        Args:
            texto (str): Texto a mostrar
        """
        self.limpiar()
        
        textbox = ctk.CTkTextbox(
            self.scrollable_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="none",
            padx=15,
            pady=15
        )
        textbox.grid(row=0, column=0, sticky="nsew")
        textbox.insert("1.0", texto)
        textbox.configure(state="disabled")
    
    def mostrar_resultados_binomial(self, datos):
        """
        Muestra resultados de distribución binomial con diseño visual
        
        Args:
            datos (dict): Diccionario con los datos:
                - n: tamaño de muestra
                - p: probabilidad de éxito
                - valores_x: lista de valores X
                - probabilidades: lista de probabilidades
                - media: media
                - desviacion: desviación estándar
                - N: tamaño de población (opcional)
                - factor_correccion: factor FPC (opcional)
                - sesgo: valor del sesgo
                - interpretacion_sesgo: descripción del sesgo
                - curtosis: valor de curtosis
                - interpretacion_curtosis: descripción de curtosis
        """
        self.limpiar()
        self.resultados_data = datos
        
        row = 0
        
        titulo = ctk.CTkLabel(
            self.scrollable_frame,
            text="RESULTADOS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f6aa5", "#1f6aa5")
        )
        titulo.grid(row=row, column=0, pady=(10, 15), sticky="ew")
        row += 1
        
        row = self._crear_seccion_poblacion(row, datos)
        row = self._crear_seccion_parametros_binomial(row, datos)
        row = self._crear_seccion_probabilidades(row, datos)
        row = self._crear_seccion_estadisticas(row, datos)
        row = self._crear_seccion_forma(row, datos)
    
    def mostrar_resultados_hipergeometrica(self, datos):
        """
        Muestra resultados de distribución hipergeométrica con diseño visual
        
        Args:
            datos (dict): Diccionario con los datos
        """
        self.limpiar()
        self.resultados_data = datos
        
        row = 0
        
        titulo = ctk.CTkLabel(
            self.scrollable_frame,
            text="RESULTADOS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f6aa5", "#1f6aa5")
        )
        titulo.grid(row=row, column=0, pady=(10, 15), sticky="ew")
        row += 1
        
        row = self._crear_seccion_condicion(row, datos)
        row = self._crear_seccion_parametros_hipergeometrica(row, datos)
        row = self._crear_seccion_probabilidades(row, datos)
        row = self._crear_seccion_estadisticas(row, datos)
        row = self._crear_seccion_forma(row, datos)
    
    def _crear_seccion_poblacion(self, row, datos):
        """Crea la sección de tipo de población"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="TIPO DE POBLACIÓN",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        N = datos.get('N')
        n = datos.get('n')
        
        if N is None:
            tipo = "INFINITA"
            color = "#3498db"
            descripcion = "No se especificó población"
        elif n <= 0.05 * N:
            tipo = "INFINITA"
            color = "#3498db"
            porcentaje = (n / N) * 100
            descripcion = f"Muestra ≤ 5% de población ({porcentaje:.2f}%)"
        else:
            tipo = "FINITA"
            color = "#e67e22"
            porcentaje = (n / N) * 100
            descripcion = f"Muestra > 5% de población ({porcentaje:.2f}%)"
        
        frame_tipo = ctk.CTkFrame(frame, fg_color="transparent")
        frame_tipo.pack(fill="x", padx=10, pady=2)
        
        lbl_tipo = ctk.CTkLabel(
            frame_tipo,
            text=f"Distribución Binomial - Población {tipo}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3b8ed0",
            anchor="w"
        )
        lbl_tipo.pack(side="left")
        
        if N is not None:
            frame_n = ctk.CTkFrame(frame, fg_color="transparent")
            frame_n.pack(fill="x", padx=10, pady=2)
            
            lbl_n_label = ctk.CTkLabel(
                frame_n,
                text="Tamaño de población (N):",
                font=ctk.CTkFont(size=11),
                width=180,
                anchor="w"
            )
            lbl_n_label.pack(side="left")
            
            lbl_n_valor = ctk.CTkLabel(
                frame_n,
                text=str(N),
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w"
            )
            lbl_n_valor.pack(side="left", padx=5)
        
        lbl_desc = ctk.CTkLabel(
            frame,
            text=descripcion,
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        lbl_desc.pack(fill="x", padx=10, pady=(0, 10))
        
        return row + 1
    
    def _crear_seccion_condicion(self, row, datos):
        """Crea la sección de condición de aplicabilidad"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="CONDICIÓN DE APLICABILIDAD",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        cumple = datos.get('cumple_condicion', True)
        porcentaje = datos.get('porcentaje_muestra', 0)
        
        if cumple:
            color = "#2ecc71"
            texto_estado = f"VÁLIDO - Muestra representa {porcentaje:.2f}% (≥ 20%)"
        else:
            color = "#e74c3c"
            texto_estado = f"ADVERTENCIA - Muestra representa {porcentaje:.2f}% (< 20%)"
        
        lbl_estado = ctk.CTkLabel(
            frame,
            text=texto_estado,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color,
            anchor="w"
        )
        lbl_estado.pack(fill="x", padx=10, pady=2)
        
        modelo = "Hipergeométrica" if cumple else "Se recomienda Binomial"
        lbl_modelo = ctk.CTkLabel(
            frame,
            text=f"Modelo: {modelo}",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        lbl_modelo.pack(fill="x", padx=10, pady=(0, 10))
        
        return row + 1
    
    def _crear_seccion_parametros_binomial(self, row, datos):
        """Crea la sección de parámetros binomial"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="PARÁMETROS",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        params = [
            ("Tamaño de muestra (n):", str(datos.get('n', '--'))),
            ("Probabilidad de éxito (p):", f"{datos.get('p', 0):.6f}"),
            ("Probabilidad de fracaso (q):", f"{1 - datos.get('p', 0):.6f}"),
        ]
        
        for label, valor in params:
            frame_param = ctk.CTkFrame(frame, fg_color="transparent")
            frame_param.pack(fill="x", padx=10, pady=2)
            
            lbl = ctk.CTkLabel(
                frame_param,
                text=label,
                font=ctk.CTkFont(size=11),
                width=180,
                anchor="w"
            )
            lbl.pack(side="left")
            
            val = ctk.CTkLabel(
                frame_param,
                text=valor,
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w"
            )
            val.pack(side="left", padx=5)
        
        lbl_espacio = ctk.CTkLabel(frame, text="")
        lbl_espacio.pack(pady=(5, 0))
        
        return row + 1
    
    def _crear_seccion_parametros_hipergeometrica(self, row, datos):
        """Crea la sección de parámetros hipergeométrica"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="PARÁMETROS",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        N = datos.get('N', 0)
        K = datos.get('K', 0)
        n = datos.get('n', 0)
        p = K / N if N > 0 else 0
        
        params = [
            ("Población total (N):", str(N)),
            ("Éxitos en población (K):", str(K)),
            ("Tamaño de muestra (n):", str(n)),
            ("Probabilidad implícita (p):", f"{p:.6f}"),
        ]
        
        for label, valor in params:
            frame_param = ctk.CTkFrame(frame, fg_color="transparent")
            frame_param.pack(fill="x", padx=10, pady=2)
            
            lbl = ctk.CTkLabel(
                frame_param,
                text=label,
                font=ctk.CTkFont(size=11),
                width=180,
                anchor="w"
            )
            lbl.pack(side="left")
            
            val = ctk.CTkLabel(
                frame_param,
                text=valor,
                font=ctk.CTkFont(size=11, weight="bold"),
                anchor="w"
            )
            val.pack(side="left", padx=5)
        
        lbl_espacio = ctk.CTkLabel(frame, text="")
        lbl_espacio.pack(pady=(5, 0))
        
        return row + 1
    
    def _crear_seccion_probabilidades(self, row, datos):
        """Crea la sección de probabilidades calculadas"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="PROBABILIDADES CALCULADAS",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        valores_x = datos.get('valores_x', [])
        probabilidades = datos.get('probabilidades', [])
        
        if not valores_x or not probabilidades:
            lbl_no_data = ctk.CTkLabel(
                frame,
                text="Sin datos",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                anchor="w"
            )
            lbl_no_data.pack(fill="x", padx=10, pady=(0, 10))
            return row + 1
        
        max_prob = max(probabilidades) if probabilidades else 1
        
        for x, prob in zip(valores_x, probabilidades):
            frame_prob = ctk.CTkFrame(frame, fg_color="transparent")
            frame_prob.pack(fill="x", padx=10, pady=3)
            
            es_maximo = prob == max_prob and len(valores_x) > 1
            color_valor = "#2ecc71" if es_maximo else "#ffffff"
            
            lbl_x = ctk.CTkLabel(
                frame_prob,
                text=f"P(X={x})",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=70,
                anchor="w"
            )
            lbl_x.pack(side="left")
            
            lbl_prob = ctk.CTkLabel(
                frame_prob,
                text=f"{prob:.6f}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color_valor,
                width=100,
                anchor="w"
            )
            lbl_prob.pack(side="left", padx=5)
            
            porcentaje = prob * 100
            lbl_porc = ctk.CTkLabel(
                frame_prob,
                text=f"({porcentaje:.4f}%)",
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w"
            )
            lbl_porc.pack(side="left", padx=5)
        
        if probabilidades:
            frame_resumen = ctk.CTkFrame(frame, fg_color="transparent")
            frame_resumen.pack(fill="x", padx=10, pady=(10, 5))
            
            suma = sum(probabilidades)
            lbl_suma = ctk.CTkLabel(
                frame_resumen,
                text=f"Suma de probabilidades: {suma:.10f}",
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w"
            )
            lbl_suma.pack(side="left")
        
        lbl_espacio = ctk.CTkLabel(frame, text="")
        lbl_espacio.pack(pady=(5, 0))
        
        return row + 1
    
    def _crear_seccion_estadisticas(self, row, datos):
        """Crea la sección de estadísticas descriptivas"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="ESTADÍSTICAS DESCRIPTIVAS",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        media = datos.get('media', 0)
        desviacion = datos.get('desviacion', 0)
        varianza = desviacion ** 2 if desviacion else 0
        mediana = datos.get('mediana')
        
        stats = [
            ("Media (μ):", f"{media:.6f}"),
            ("Varianza (σ²):", f"{varianza:.6f}"),
            ("Desviación estándar (σ):", f"{desviacion:.6f}"),
        ]
        
        if media > 0:
            cv = (desviacion / media) * 100 if media != 0 else 0
            stats.append(("Coeficiente de variación:", f"{cv:.2f}%"))
        
        if mediana is not None:
            stats.append(("Mediana:", str(mediana)))
        
        for label, valor in stats:
            frame_stat = ctk.CTkFrame(frame, fg_color="transparent")
            frame_stat.pack(fill="x", padx=10, pady=2)
            
            lbl = ctk.CTkLabel(
                frame_stat,
                text=label,
                font=ctk.CTkFont(size=11),
                width=180,
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
        
        return row + 1
    
    def _crear_seccion_forma(self, row, datos):
        """Crea la sección de forma de la distribución"""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 10), padx=5)
        
        lbl_titulo = ctk.CTkLabel(
            frame,
            text="FORMA DE LA DISTRIBUCIÓN",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_titulo.pack(fill="x", padx=10, pady=(10, 5))
        
        sesgo = datos.get('sesgo')
        interpretacion_sesgo = datos.get('interpretacion_sesgo', '')
        
        if sesgo is not None:
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
            
            lbl_sesgo_val = ctk.CTkLabel(
                frame_sesgo,
                text=f"{sesgo:.4f}",
                font=ctk.CTkFont(size=11),
                anchor="w"
            )
            lbl_sesgo_val.pack(side="left", padx=5)
            
            color_sesgo = "#e74c3c" if "Negativo" in interpretacion_sesgo else "#2ecc71" if "Positivo" in interpretacion_sesgo else "gray"
            
            lbl_sesgo_tipo = ctk.CTkLabel(
                frame_sesgo,
                text=f"({interpretacion_sesgo})",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=color_sesgo,
                anchor="w"
            )
            lbl_sesgo_tipo.pack(side="left", padx=5)
        
        curtosis = datos.get('curtosis')
        interpretacion_curtosis = datos.get('interpretacion_curtosis', '')
        
        if curtosis is not None:
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
            
            lbl_curt_val = ctk.CTkLabel(
                frame_curtosis,
                text=f"{curtosis:.4f}",
                font=ctk.CTkFont(size=11),
                anchor="w"
            )
            lbl_curt_val.pack(side="left", padx=5)
            
            color_curt = "#e74c3c" if "Leptocúrtica" in interpretacion_curtosis else "#3498db" if "Platicúrtica" in interpretacion_curtosis else "gray"
            
            lbl_curt_tipo = ctk.CTkLabel(
                frame_curtosis,
                text=f"({interpretacion_curtosis})",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=color_curt,
                anchor="w"
            )
            lbl_curt_tipo.pack(side="left", padx=5)
        
        lbl_espacio = ctk.CTkLabel(frame, text="")
        lbl_espacio.pack(pady=(5, 0))
        
        return row + 1
