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
    calcular_curtosis
)
from utils.calculos import (
    cumple_condicion_hipergeometrica,
    calcular_media_hipergeometrica,
    calcular_desviacion_hipergeometrica,
    calcular_sesgo_hipergeometrica,
    calcular_curtosis_hipergeometrica,
    calcular_probabilidades_hipergeometrica,
    calcular_mediana_hipergeometrica,
    determinar_tipo_sesgo
)
from utils.validaciones import (
    validar_parametros_hipergeometrica,
    validar_valores_x_hipergeometrica,
    parsear_valores_x_hipergeometrica
)
from utils.formato import (
    generar_mensaje_usar_binomial
)
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
            text_color=("#1f6aa5", "#1f6aa5")
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
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
            plt.close('all')
            
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
            
            n = int(valores['n'])
            p = float(valores['p'])
            n_poblacion_val = valores.get('n_poblacion', None)
            
            if n_poblacion_val is None or n_poblacion_val == '' or n_poblacion_val == '0':
                N = None
            else:
                N = int(n_poblacion_val)
            
            valido, mensaje = validar_parametros(n, p, N)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return
            
            valores_x = parsear_valores_x(valores['x'], n)
            
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
                'n': n,
                'p': p,
                'N': N,
                'valores_x': valores_x,
                'probabilidades': probabilidades,
                'media': media,
                'desviacion': desviacion,
                'factor_correccion': factor_correccion,
                'sesgo': sesgo,
                'interpretacion_sesgo': interpretacion_sesgo,
                'curtosis': curtosis,
                'interpretacion_curtosis': interpretacion_curtosis
            }
            
            self.dashboard.mostrar_resultados_binomial(datos_resultados)
            
            x_destacado = valores_x[0] if len(valores_x) == 1 else None
            self.dashboard.crear_grafico(
                valores_x, probabilidades, n, p, N, es_infinita, x_destacado
            )
            
        except ValueError as e:
            messagebox.showerror(
                "Error de Entrada",
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al procesar los datos:\n\n{str(e)}"
            )
    
    def calcular_hipergeometrica(self):
        """Procesa los datos y realiza los cálculos de distribución hipergeométrica"""
        try:
            valores = self.dashboard.obtener_campos_hipergeometrica()
            
            if not valores:
                return
            
            N = int(valores['N'])
            K = int(valores['K'])
            n = int(valores['n'])
            
            valido, mensaje = validar_parametros_hipergeometrica(n, N, K)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return
            
            cumple, porcentaje = cumple_condicion_hipergeometrica(n, N)
            
            if not cumple:
                mensaje = generar_mensaje_usar_binomial(n, N, K, porcentaje)
                datos_advertencia = {
                    'n': n,
                    'N': N,
                    'K': K,
                    'cumple_condicion': False,
                    'porcentaje_muestra': porcentaje
                }
                self.dashboard.mostrar_resultados_hipergeometrica(datos_advertencia)
                return
            
            valores_x = parsear_valores_x_hipergeometrica(valores['x'], n, K)
            
            valido, mensaje = validar_valores_x_hipergeometrica(valores_x, n, K)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return
            
            probabilidades = calcular_probabilidades_hipergeometrica(valores_x, n, N, K)
            media = calcular_media_hipergeometrica(n, N, K)
            desviacion = calcular_desviacion_hipergeometrica(n, N, K)
            mediana = calcular_mediana_hipergeometrica(n, N, K)
            
            sesgo, interpretacion_sesgo, tipo_sesgo_formula = calcular_sesgo_hipergeometrica(n, N, K)
            tipo_sesgo_media_mediana = determinar_tipo_sesgo(media, mediana)
            curtosis, interpretacion_curtosis = calcular_curtosis_hipergeometrica(n, N, K)
            
            datos_resultados = {
                'n': n,
                'N': N,
                'K': K,
                'valores_x': valores_x,
                'probabilidades': probabilidades,
                'media': media,
                'desviacion': desviacion,
                'mediana': mediana,
                'sesgo': sesgo,
                'interpretacion_sesgo': interpretacion_sesgo,
                'curtosis': curtosis,
                'interpretacion_curtosis': interpretacion_curtosis,
                'cumple_condicion': cumple,
                'porcentaje_muestra': porcentaje
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
                f"Por favor ingrese valores numéricos válidos.\n\nDetalle: {str(e)}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Ocurrió un error al procesar los datos:\n\n{str(e)}"
            )
    
    def abrir_analisis_archivo(self):
        """Abre la ventana de análisis desde archivo."""
        DataViewerWindow(master=self.root)
