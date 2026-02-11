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
        
        self.crear_campos()
    
    def crear_campos(self):
        """Crea todos los campos de entrada"""
        # Primera fila: n y p
        row1 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row1.pack(fill="x", pady=4)
        
        # n - tamaño de muestra
        ctk.CTkLabel(
            row1,
            text="Tamaño de muestra (n):",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)
        
        self.n_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 10")
        self.n_entry.pack(side="left", padx=8)
        
        # p - probabilidad de éxito
        ctk.CTkLabel(
            row1,
            text="Probabilidad de éxito (p):",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)
        
        self.p_entry = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 0.5")
        self.p_entry.pack(side="left", padx=8)

        # N - tamaño de población
        ctk.CTkLabel(
            row1,
            text="Población (N):",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)

        self.n_entry_poblacion = ctk.CTkEntry(row1, width=120, placeholder_text="Ej: 100")
        self.n_entry_poblacion.pack(side="left", padx=8)

        # Segunda fila: valores de X
        row2 = ctk.CTkFrame(self.frame, fg_color="transparent")
        row2.pack(fill="x", pady=4)
        
        ctk.CTkLabel(
            row2,
            text="Valores de X (separados por coma):",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=8)
        
        self.x_entry = ctk.CTkEntry(
            row2,
            width=380,
            placeholder_text="Ej: 0,1,2,3,4,5 o 'todos' para todos los valores"
        )
        self.x_entry.pack(side="left", padx=8)
    
    def obtener_valores(self):
        """
        Obtiene los valores de todos los campos
        
        Returns:
            dict: Diccionario con los valores de entrada
        """
        n_pob = self.n_entry_poblacion.get().strip()
        return {
            'n': self.n_entry.get().strip(),
            'p': self.p_entry.get().strip(),
            'n_poblacion': n_pob if n_pob else None,
            'x': self.x_entry.get().strip()
        }
    
    def limpiar(self):
        """Limpia todos los campos de entrada"""
        self.n_entry.delete(0, "end")
        self.p_entry.delete(0, "end")
        self.n_entry_poblacion.delete(0, "end")
        self.x_entry.delete(0, "end")
