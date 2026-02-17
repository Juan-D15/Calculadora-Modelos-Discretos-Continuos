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
    generar_texto_resultados,
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
    generar_texto_resultados_hipergeometrica,
    generar_mensaje_usar_binomial
)


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
        
        # Configurar manejador de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    
    def configurar_ventana(self):
        """Configura las propiedades de la ventana principal"""
        self.root.title("Calculadora de Distribuciones")
        self.root.geometry("1300x850")
        self.root.minsize(1200, 750)
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título principal
        self.crear_titulo()
        
        # Crear dashboard
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
            # Limpiar dashboard si existe
            if self.dashboard:
                if self.dashboard.grafico:
                    self.dashboard.grafico.limpiar()
            
            # Cerrar todas las figuras de matplotlib
            import matplotlib.pyplot as plt
            plt.close('all')
            
        except Exception:
            # Ignorar errores durante la limpieza
            pass
        finally:
            # Destruir la ventana principal
            self.root.destroy()
    
    def calcular_desde_dashboard(self):
        """Procesa los datos y realiza los cálculos desde el dashboard"""
        try:
            # Obtener valores de entrada
            valores = self.dashboard.obtener_campos()
            
            if not valores:
                return
            
            # Convertir a tipos apropiados
            n = int(valores['n'])
            p = float(valores['p'])
            n_poblacion_val = valores.get('n_poblacion', None)
            
            # Si N está vacío, es None o es 0, se trata como población infinita (None)
            if n_poblacion_val is None or n_poblacion_val == '' or n_poblacion_val == '0':
                N = None
            else:
                N = int(n_poblacion_val)
            
            # Validar parámetros
            valido, mensaje = validar_parametros(n, p, N)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return
            
            # Parsear valores de X
            valores_x = parsear_valores_x(valores['x'], n)
            
            # Validar valores de X
            valido, mensaje = validar_valores_x(valores_x, n)
            if not valido:
                messagebox.showerror("Error de Validación", mensaje)
                return
            
            # Verificar tipo de población
            es_infinita = es_poblacion_infinita(n, N)
            
            # Calcular factor de corrección si es población finita
            factor_correccion = None
            if not es_infinita and N is not None:
                factor_correccion = calcular_factor_correccion(n, N)
            
            # Realizar cálculos
            probabilidades = calcular_probabilidades(valores_x, n, p)
            media = calcular_media(n, p)
            desviacion = calcular_desviacion_estandar(n, p, N)
            
            # Calcular sesgo y curtosis
            sesgo, interpretacion_sesgo = calcular_sesgo(n, p, N)
            curtosis, interpretacion_curtosis = calcular_curtosis(n, p, N)
            
            # Generar y mostrar resultados
            texto_resultados = generar_texto_resultados(
                n, p,
                valores_x, probabilidades,
                media, desviacion,
                N, factor_correccion, sesgo, interpretacion_sesgo,
                curtosis, interpretacion_curtosis
            )
            
            self.dashboard.mostrar_resultados(texto_resultados)
            
            # Crear gráfico
            self.dashboard.crear_grafico(valores_x, probabilidades, n, p, N, es_infinita)
            
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
                self.dashboard.mostrar_resultados(mensaje)
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
            
            texto_resultados = generar_texto_resultados_hipergeometrica(
                n, N, K, valores_x, probabilidades,
                media, desviacion,
                sesgo, interpretacion_sesgo, tipo_sesgo_media_mediana,
                curtosis, interpretacion_curtosis,
                mediana, cumple, porcentaje
            )
            
            self.dashboard.mostrar_resultados(texto_resultados)
            self.dashboard.crear_grafico_hipergeometrica(valores_x, probabilidades, n, N, K)
            
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
