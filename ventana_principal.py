"""
Ventana principal de la aplicación de distribución binomial
Diseño mejorado y centrado
"""

import customtkinter as ctk
from tkinter import messagebox

from gui.dashboard import Dashboard
from utils import (
    calcular_probabilidades,
    calcular_media,
    calcular_desviacion_estandar,
    validar_parametros,
    validar_valores_x,
    parsear_valores_x,
    es_poblacion_infinita,
    calcular_factor_correccion,
    calcular_sesgo,
    calcular_curtosis,
    calcular_probabilidades_acumuladas,
    buscar_valor_tolerancia,
    validar_parametros_comparacion,
    validar_tolerancia,
    validar_condiciones_poisson,
    parsear_valores_x_poisson,
    calcular_probabilidades_poisson,
    calcular_desviacion_poisson,
    calcular_sesgo_poisson,
    calcular_curtosis_poisson,
    validar_valores_x_poisson,
)
from utils.calculos import (
    cumple_condicion_hipergeometrica,
    calcular_media_hipergeometrica,
    calcular_desviacion_hipergeometrica,
    calcular_sesgo_hipergeometrica,
    calcular_curtosis_hipergeometrica,
    calcular_probabilidades_hipergeometrica,
    calcular_probabilidades_acumuladas_hipergeometrica,
    calcular_mediana_hipergeometrica,
    determinar_tipo_sesgo,
)
from utils.validaciones import (
    validar_parametros_hipergeometrica,
    validar_valores_x_hipergeometrica,
    parsear_valores_x_hipergeometrica,
    normalizar_probabilidad,
)
from utils.formato import generar_mensaje_usar_binomial
from data_viewer import DataViewerWindow


class VentanaPrincipal:
    """Clase principal de la aplicación"""

    def __init__(self, root):
        """
        Inicializa la ventana principal

        Args:
            root: Ventana raíz de CTk
        """
        self.root = root
        self.dashboard = None
        self.configurar_ventana()
        self.crear_interfaz()

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def configurar_ventana(self):
        """Configura las propiedades de la ventana principal"""
        self.root.title("Calculadora de Distribuciones")
        self.root.geometry("1300x850")
        self.root.minsize(1200, 750)

    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.crear_titulo()

        self.dashboard = Dashboard(self.main_frame, self)

    def crear_titulo(self):
        """Crea el título de la aplicación"""
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(5, 8))

        title = ctk.CTkLabel(
            title_frame,
            text="MODELOS DISCRETOS Y CONTINUOS",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=("#1f6aa5", "#1f6aa5"),
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            title_frame, text="", font=ctk.CTkFont(size=11), text_color="gray"
        )
        subtitle.pack(pady=3)

    def cerrar_aplicacion(self):
        """
        Maneja el cierre de la aplicación limpiando recursos
        """
        try:
            if self.dashboard:
                if self.dashboard.grafico:
                    self.dashboard.grafico.limpiar()

            import matplotlib.pyplot as plt

            plt.close("all")

        except Exception:
            pass
        finally:
            self.root.destroy()

    def calcular_desde_dashboard(self):
        """Procesa los datos y realiza los cálculos desde el dashboard"""
        try:
            valores = self.dashboard.obtener_campos()

            if not valores:
                return

            # Check if Poisson approximation is activated
            if (
                hasattr(self.dashboard.campos, "chk_poisson")
                and self.dashboard.campos.chk_poisson.get()
            ):
                self.calcular_poisson_binomial()
                return

            n = int(valores["n"])
            p_str = valores.get("p", "").strip()
            n_poblacion_val = valores.get("n_poblacion", None)
            K_val = valores.get("K", None)

            if (
                n_poblacion_val is None
                or n_poblacion_val == ""
                or n_poblacion_val == "0"
            ):
                N = None
            else:
                N = int(n_poblacion_val)

            es_comparacion = valores.get("comparacion", False)
            tolerancia_val = valores.get("tolerancia", None)

            if es_comparacion:
                valido_tol, tolerancia, msg_tol = validar_tolerancia(tolerancia_val)
                if not valido_tol:
                    messagebox.showerror("Error de Validación", msg_tol)
                    return

                if N is None or N <= 0:
                    messagebox.showerror(
                        "Error de Validación",
                        "Para comparación, el tamaño de población (N) es obligatorio",
                    )
                    return

                K_manual = None
                if K_val is not None and K_val != "":
                    try:
                        K_manual = int(K_val)
                        if K_manual <= 0:
                            messagebox.showerror(
                                "Error de Validación",
                                "K debe ser mayor a 0",
                            )
                            return
                        if K_manual > N:
                            messagebox.showerror(
                                "Error de Validación",
                                f"K ({K_manual}) no puede ser mayor que N ({N})",
                            )
                            return
                    except ValueError:
                        messagebox.showerror(
                            "Error de Validación",
                            "K debe ser un número entero válido",
                        )
                        return

                p = None
                if p_str:
                    valido, p, error = normalizar_probabilidad(p_str)
                    if not valido:
                        messagebox.showerror("Error de Validación", error)
                        return

                if K_manual is not None:
                    p_desde_K = K_manual / N
                    if p is not None and abs(p - p_desde_K) > 0.001:
                        response = messagebox.askyesno(
                            "Conflicto de Probabilidad",
                            f"Existe un conflicto entre los valores:\n\n"
                            f"• p ingresado manualmente: {p:.4f}\n"
                            f"• p calculado desde K: K/N = {K_manual}/{N} = {p_desde_K:.4f}\n\n"
                            f"¿Desea usar p = {p_desde_K:.4f} (calculado desde K)?\n\n"
                            f"• SÍ: Usar p = {p_desde_K:.4f} (K = {K_manual})\n"
                            f"• NO: Usar p = {p:.4f} (K = {round(p * N)})",
                        )
                        if response:
                            p = p_desde_K
                        else:
                            K_manual = round(p * N)
                    else:
                        p = p_desde_K
                elif p is None:
                    messagebox.showerror(
                        "Error de Validación",
                        "Debe ingresar al menos p (probabilidad) o K (éxitos en población)",
                    )
                    return

                valido, mensaje = validar_parametros_comparacion(
                    n, p, N, tolerancia, K_manual
                )
                if not valido:
                    messagebox.showerror("Error de Validación", mensaje)
                    return

                valores_x = parsear_valores_x(valores["x"], n)
                valido, mensaje = validar_valores_x(valores_x, n)
                if not valido:
                    messagebox.showerror("Error de Validación", mensaje)
                    return

                self.calcular_comparacion(n, p, N, valores_x, tolerancia, K_manual)
                return

            if not p_str:
                messagebox.showerror(
                    "Error de Validación",
                    "La probabilidad (p) es obligatoria",
                )
                return
            valido, p, error = normalizar_probabilidad(p_str)
            if not valido:
                messagebox.showerror("Error de Validación", error)
                return

            valido, mensaje = validar_parametros(n, p, N)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return

            valores_x = parsear_valores_x(valores["x"], n)

            valido, mensaje = validar_valores_x(valores_x, n)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return

            es_infinita = es_poblacion_infinita(n, N)

            factor_correccion = None
            if not es_infinita and N is not None:
                factor_correccion = calcular_factor_correccion(n, N)

            probabilidades = calcular_probabilidades(valores_x, n, p)
            media = calcular_media(n, p)
            desviacion = calcular_desviacion_estandar(n, p, N)

            sesgo, interpretacion_sesgo = calcular_sesgo(n, p, N)
            curtosis, interpretacion_curtosis = calcular_curtosis(n, p, N)

            datos_resultados = {
                "n": n,
                "p": p,
                "N": N,
                "valores_x": valores_x,
                "probabilidades": probabilidades,
                "media": media,
                "desviacion": desviacion,
                "factor_correccion": factor_correccion,
                "sesgo": sesgo,
                "interpretacion_sesgo": interpretacion_sesgo,
                "curtosis": curtosis,
                "interpretacion_curtosis": interpretacion_curtosis,
            }

            if self.dashboard.modo_comparacion:
                self.dashboard.limpiar_comparacion()

            self.dashboard.mostrar_resultados_binomial(datos_resultados)

            x_destacado = valores_x[0] if len(valores_x) == 1 else None
            self.dashboard.crear_grafico(
                valores_x, probabilidades, n, p, N, es_infinita, x_destacado
            )

        except ValueError as e:
            messagebox.showerror(
                "Error de Entrada",
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}",
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al procesar los datos:\n\n{str(e)}",
            )

    def calcular_hipergeometrica(self):
        """Procesa los datos y realiza los cálculos de distribución hipergeométrica"""
        try:
            valores = self.dashboard.obtener_campos_hipergeometrica()

            if not valores:
                return

            N = int(valores["N"])
            K = int(valores["K"])
            n = int(valores["n"])

            valido, mensaje = validar_parametros_hipergeometrica(n, N, K)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return

            cumple, porcentaje = cumple_condicion_hipergeometrica(n, N)

            if not cumple:
                mensaje = generar_mensaje_usar_binomial(n, N, K, porcentaje)
                datos_advertencia = {
                    "n": n,
                    "N": N,
                    "K": K,
                    "cumple_condicion": False,
                    "porcentaje_muestra": porcentaje,
                }
                self.dashboard.mostrar_resultados_hipergeometrica(datos_advertencia)
                return

            valores_x = parsear_valores_x_hipergeometrica(valores["x"], n, K)

            valido, mensaje = validar_valores_x_hipergeometrica(valores_x, n, K)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return

            probabilidades = calcular_probabilidades_hipergeometrica(valores_x, n, N, K)
            media = calcular_media_hipergeometrica(n, N, K)
            desviacion = calcular_desviacion_hipergeometrica(n, N, K)
            mediana = calcular_mediana_hipergeometrica(n, N, K)

            sesgo, interpretacion_sesgo, tipo_sesgo_formula = (
                calcular_sesgo_hipergeometrica(n, N, K)
            )
            tipo_sesgo_media_mediana = determinar_tipo_sesgo(media, mediana)
            curtosis, interpretacion_curtosis = calcular_curtosis_hipergeometrica(
                n, N, K
            )

            datos_resultados = {
                "n": n,
                "N": N,
                "K": K,
                "valores_x": valores_x,
                "probabilidades": probabilidades,
                "media": media,
                "desviacion": desviacion,
                "mediana": mediana,
                "sesgo": sesgo,
                "interpretacion_sesgo": interpretacion_sesgo,
                "curtosis": curtosis,
                "interpretacion_curtosis": interpretacion_curtosis,
                "cumple_condicion": cumple,
                "porcentaje_muestra": porcentaje,
            }

            self.dashboard.mostrar_resultados_hipergeometrica(datos_resultados)

            p = K / N if N > 0 else 0
            x_destacado = valores_x[0] if len(valores_x) == 1 else None
            self.dashboard.crear_grafico_hipergeometrica(
                valores_x, probabilidades, n, N, K, p, x_destacado
            )

        except ValueError as e:
            messagebox.showerror(
                "Error de Entrada",
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}",
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al procesar los datos:\n\n{str(e)}",
            )

    def calcular_poisson(self):
        """Procesa los datos y realiza los cálculos de distribución de Poisson"""
        try:
            valores = self.dashboard.obtener_campos_poisson()

            if not valores:
                return

            n_str = valores.get("n", "").strip()
            p_str = valores.get("p", "").strip()
            x_str = valores.get("x", "").strip()

            if not n_str:
                messagebox.showerror(
                    "Error de Validación",
                    "El número de ensayos (n) es obligatorio",
                )
                return

            if not p_str:
                messagebox.showerror(
                    "Error de Validación",
                    "La probabilidad (p) es obligatoria",
                )
                return

            n = int(n_str)

            if n <= 0:
                messagebox.showerror(
                    "Error de Validación",
                    "El número de ensayos (n) debe ser mayor a 0",
                )
                return

            valido, p, error = normalizar_probabilidad(p_str)
            if not valido:
                messagebox.showerror("Error de Validación", error)
                return

            valido, mensaje, lam = validar_condiciones_poisson(n, p)
            if not valido:
                messagebox.showerror(
                    "Condiciones No Cumplidas",
                    mensaje,
                )
                return

            valores_x = parsear_valores_x_poisson(x_str, lam, n)

            valido, mensaje = validar_valores_x_poisson(valores_x, n)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return

            probabilidades = calcular_probabilidades_poisson(valores_x, lam)
            media = lam
            desviacion = calcular_desviacion_poisson(lam)
            sesgo, interpretacion_sesgo = calcular_sesgo_poisson(lam)
            curtosis, interpretacion_curtosis = calcular_curtosis_poisson(lam)

            datos_resultados = {
                "n": n,
                "p": p,
                "lambda": lam,
                "valores_x": valores_x,
                "probabilidades": probabilidades,
                "media": media,
                "desviacion": desviacion,
                "sesgo": sesgo,
                "interpretacion_sesgo": interpretacion_sesgo,
                "curtosis": curtosis,
                "interpretacion_curtosis": interpretacion_curtosis,
            }

            self.dashboard.mostrar_resultados_poisson(datos_resultados)

            x_destacado = valores_x[0] if len(valores_x) == 1 else None
            self.dashboard.crear_grafico_poisson(
                valores_x, probabilidades, lam, n, p, x_destacado
            )

        except ValueError as e:
            messagebox.showerror(
                "Error de Entrada",
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}",
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al procesar los datos:\n\n{str(e)}",
            )

    def abrir_analisis_archivo(self):
        """Abre la ventana de análisis desde archivo."""
        DataViewerWindow(master=self.root)

    def calcular_comparacion(self, n, p, N, valores_x, tolerancia, K_manual=None):
        """
        Calcula y compara distribuciones Binomial e Hipergeométrica

        Args:
            n (int): Tamaño de muestra
            p (float): Probabilidad de éxito
            N (int): Tamaño de población
            valores_x (list): Valores de X a calcular
            tolerancia (float): Porcentaje de tolerancia
            K_manual (int, optional): Valor de K ingresado manualmente
        """
        try:
            for x in valores_x:
                if x > n:
                    messagebox.showerror(
                        "Error de Validación",
                        f"El valor X = {x} no puede ser mayor que el tamaño de la muestra (n = {n}).\n\n"
                        f"Los valores de X deben estar entre 0 y {n}.",
                    )
                    return
                if x < 0:
                    messagebox.showerror(
                        "Error de Validación",
                        f"El valor X = {x} no puede ser negativo.",
                    )
                    return

            if K_manual is not None:
                K = K_manual
            else:
                K = round(p * N)

            if K <= 0:
                messagebox.showerror(
                    "Error de Cálculo",
                    f"K calculado (K = p × N = {p} × {N} = {K}) debe ser mayor a 0",
                )
                return

            if K > N:
                messagebox.showerror(
                    "Error de Cálculo",
                    f"K calculado (K = p × N = {p} × {N} = {K}) no puede ser mayor que N = {N}",
                )
                return

            cumple_20, porcentaje_muestra = cumple_condicion_hipergeometrica(n, N)

            advertencia_20 = None
            if not cumple_20:
                advertencia_20 = (
                    f"Advertencia: La muestra ({n}) representa {porcentaje_muestra:.1f}% de la población.\n"
                    f"Se recomienda usar solo distribución Binomial (muestra < 20% de población).\n\n"
                    f"El cálculo de Hipergeométrica continuará pero puede no ser apropiado."
                )

            es_infinita = es_poblacion_infinita(n, N)

            probabilidades_bin = calcular_probabilidades(valores_x, n, p)
            probabilidades_acum_bin = calcular_probabilidades_acumuladas(
                valores_x, n, p
            )
            media_bin = calcular_media(n, p)
            desviacion_bin = calcular_desviacion_estandar(n, p, N)

            valores_x_hiper = [x for x in valores_x if x <= min(n, K)]
            probabilidades_hiper = calcular_probabilidades_hipergeometrica(
                valores_x_hiper, n, N, K
            )
            probabilidades_acum_hiper = (
                calcular_probabilidades_acumuladas_hipergeometrica(
                    valores_x_hiper, n, N, K
                )
            )
            media_hiper = calcular_media_hipergeometrica(n, N, K)
            desviacion_hiper = calcular_desviacion_hipergeometrica(n, N, K)

            valor_tolerancia_bin = buscar_valor_tolerancia(
                valores_x, probabilidades_acum_bin, tolerancia
            )
            valor_tolerancia_hiper = buscar_valor_tolerancia(
                valores_x_hiper, probabilidades_acum_hiper, tolerancia
            )

            datos_binomial = {
                "n": n,
                "p": p,
                "N": N,
                "valores_x": valores_x,
                "probabilidades": probabilidades_bin,
                "probabilidades_acumuladas": probabilidades_acum_bin,
                "media": media_bin,
                "desviacion": desviacion_bin,
                "es_infinita": es_infinita,
                "valor_tolerancia": valor_tolerancia_bin,
            }

            datos_hipergeometrica = {
                "n": n,
                "N": N,
                "K": K,
                "p": p,
                "valores_x": valores_x_hiper,
                "probabilidades": probabilidades_hiper,
                "probabilidades_acumuladas": probabilidades_acum_hiper,
                "media": media_hiper,
                "desviacion": desviacion_hiper,
                "valor_tolerancia": valor_tolerancia_hiper,
                "es_infinita": False,
            }

            if advertencia_20:
                messagebox.showwarning("Advertencia de Muestra", advertencia_20)

            self.dashboard.mostrar_comparacion(
                datos_binomial, datos_hipergeometrica, tolerancia
            )

        except ValueError as e:
            messagebox.showerror(
                "Error de Entrada",
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}",
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al procesar la comparación:\n\n{str(e)}",
            )

    def calcular_poisson_binomial(self):
        """
        Calcula aproximación Binomial → Poisson cuando el checkbox está activado

        Valida parámetros, calcula probabilidades para ambas distribuciones,
        y muestra resultados comparativos en el dashboard.
        """
        try:
            from utils import AproximacionPoissonBinomial

            valores = self.dashboard.obtener_campos()

            if not valores:
                return

            n = int(valores["n"])
            p = float(valores["p"])
            x_str = valores.get("x", "").strip()

            # Parsear k ingresado
            k_ingresado = int(x_str) if x_str else None

            # Validar parámetros básicos
            if n <= 0:
                messagebox.showerror(
                    "Error de Validación", "El número de ensayos (n) debe ser mayor a 0"
                )
                return

            if not (0 < p < 1):
                messagebox.showerror(
                    "Error de Validación", "La probabilidad (p) debe estar entre 0 y 1"
                )
                return

            if k_ingresado is not None and (k_ingresado < 0 or k_ingresado > n):
                messagebox.showerror(
                    "Error de Validación", f"El valor k debe estar entre 0 y {n}"
                )
                return

            # Validar condiciones de aproximación
            cumple, advertencia = AproximacionPoissonBinomial.validar_condiciones(n, p)

            if not cumple:
                messagebox.showwarning("Advertencia de Aproximación", advertencia)

            # Calcular probabilidades para rango completo
            valores_k, probs_binom, probs_poisson = (
                AproximacionPoissonBinomial.calcular_probabilidades_rango(n, p)
            )

            # Calcular estadísticas
            lam = AproximacionPoissonBinomial.calcular_lambda(n, p)
            media, varianza, desviacion = (
                AproximacionPoissonBinomial.calcular_estadisticas(n, p)
            )

            # Datos para resultados
            datos_resultados = {
                "n": n,
                "p": p,
                "lambda": lam,
                "k_ingresado": k_ingresado,
                "valores_k": valores_k,
                "probs_binom": probs_binom,
                "probs_poisson": probs_poisson,
                "media": media,
                "varianza": varianza,
                "desviacion": desviacion,
                "advertencia": advertencia if not cumple else None,
            }

            # Mostrar resultados en dashboard
            self.dashboard.mostrar_resultados_poisson_binomial(datos_resultados)

            # Crear gráfica comparativa
            self.dashboard.crear_grafico_poisson_binomial(
                valores_k, probs_binom, probs_poisson, k_ingresado, n, p, lam
            )

        except ValueError as e:
            messagebox.showerror(
                "Error de Entrada",
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}",
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al calcular la aproximación:\n\n{str(e)}",
            )

    def calcular_poisson_hipergeometrica(self):
        """
        Calcula aproximación Hipergeométrica → Poisson cuando el checkbox está activado

        Valida parámetros, calcula probabilidades para ambas distribuciones,
        y muestra resultados comparativos en el dashboard.
        """
        try:
            from utils import AproximacionPoissonHiper

            valores = self.dashboard.obtener_campos_hipergeometrica()

            if not valores:
                return

            N = int(valores["N"])
            K = int(valores["K"])
            n = int(valores["n"])
            x_str = valores.get("x", "").strip()

            # Validar parámetros básicos
            if N <= 0:
                messagebox.showerror(
                    "Error de Validación",
                    "El tamaño de población (N) debe ser mayor a 0",
                )
                return

            if K <= 0 or K > N:
                messagebox.showerror(
                    "Error de Validación", f"K debe estar entre 1 y N ({N})"
                )
                return

            if n <= 0 or n > N:
                messagebox.showerror(
                    "Error de Validación", f"n debe estar entre 1 y N ({N})"
                )
                return

            k_ingresado = int(x_str) if x_str else None

            if k_ingresado is not None:
                if k_ingresado < 0 or k_ingresado > min(K, n):
                    messagebox.showerror(
                        "Error de Validación",
                        f"k debe estar entre 0 y min(K, n) = {min(K, n)}",
                    )
                    return

            # Validar condiciones de aproximación
            cumple, advertencia = AproximacionPoissonHiper.validar_condiciones(N, n)

            if not cumple:
                messagebox.showwarning("Advertencia de Aproximación", advertencia)

            # Calcular probabilidades para rango completo
            valores_k, probs_hiper, probs_poisson = (
                AproximacionPoissonHiper.calcular_probabilidades_rango(n, N, K)
            )

            # Calcular estadísticas
            lam = AproximacionPoissonHiper.calcular_lambda(N, K, n)
            media, varianza, desviacion = (
                AproximacionPoissonHiper.calcular_estadisticas(n, N, K)
            )

            # Datos para resultados
            datos_resultados = {
                "N": N,
                "K": K,
                "n": n,
                "lambda": lam,
                "k_ingresado": k_ingresado,
                "valores_k": valores_k,
                "probs_hiper": probs_hiper,
                "probs_poisson": probs_poisson,
                "media": media,
                "varianza": varianza,
                "desviacion": desviacion,
                "advertencia": advertencia if not cumple else None,
            }

            # Mostrar resultados en dashboard
            self.dashboard.mostrar_resultados_poisson_hipergeometrica(datos_resultados)

            # Crear gráfica comparativa
            self.dashboard.crear_grafico_poisson_hipergeometrica(
                valores_k, probs_hiper, probs_poisson, k_ingresado, N, K, n, lam
            )

        except ValueError as e:
            messagebox.showerror(
                "Error de Entrada",
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}",
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al calcular la aproximación:\n\n{str(e)}",
            )
