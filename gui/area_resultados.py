"""
Módulo para el área de visualización de resultados
Mejorado con mejor formato y scroll
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
        self.text_widget = None
        self.scrollbar = None
        
        self.crear_area()
    
    def crear_area(self):
        """Crea el área de texto para mostrar resultados"""
        # Frame contenedor con scrollbar
        container = ctk.CTkFrame(self.frame)
        container.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Crear scrollbar vertical
        self.scrollbar = ctk.CTkScrollbar(container, width=18)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 2))
        
        # Crear textbox con dimensiones fijas
        self.text_widget = ctk.CTkTextbox(
            container,
            width=650,
            height=600,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="none",
            padx=15,
            pady=15,
            scrollbar_button_color="#3b8ed0",
            scrollbar_button_hover_color="#3672a9",
            corner_radius=8
        )
        self.text_widget.pack(side="left", fill="both", expand=True, padx=(2, 0))
        
        # Conectar scrollbar al textbox
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.text_widget.yview)
        
        # Configurar estado de solo lectura
        self.text_widget.configure(state="disabled")
    
    def mostrar_texto(self, texto):
        """
        Muestra texto en el área de resultados
        
        Args:
            texto (str): Texto a mostrar
        """
        # Habilitar para editar
        self.text_widget.configure(state="normal")
        
        # Limpiar contenido anterior
        self.text_widget.delete("1.0", "end")
        
        # Insertar nuevo texto
        self.text_widget.insert("1.0", texto)
        
        # Deshabilitar edición
        self.text_widget.configure(state="disabled")
        
        # Scroll al inicio
        self.text_widget.see("1.0")
    
    def limpiar(self):
        """Limpia el área de resultados"""
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.configure(state="disabled")
