"""
Clase base para ventanas secundarias de la aplicación.
Proporciona funcionalidad común: centrado, instancia única y limpieza de recursos.
"""
import customtkinter as ctk
import matplotlib.pyplot as plt
from typing import Optional, Dict, Type


_instancias: Dict[Type, 'BaseToplevelWindow'] = {}


class BaseToplevelWindow(ctk.CTkToplevel):
    """
    Clase base para ventanas secundarias (CTkToplevel).
    
    Proporciona:
    - Centrado automático en pantalla
    - Control de instancia única por tipo de ventana
    - Apertura como ventana modal (adelante de la principal)
    - Limpieza de recursos matplotlib al cerrar
    
    Cada subclase tiene su propio control de instancia única.
    """
    
    def __init__(self, master=None, **kwargs):
        """
        Inicializa la ventana base.
        
        Args:
            master: Ventana padre.
            **kwargs: Argumentos adicionales para CTkToplevel.
        """
        clase = type(self)
        
        if clase in _instancias:
            try:
                if _instancias[clase].winfo_exists():
                    _instancias[clase].focus_force()
                    _instancias[clase].lift()
                    self._skip_init = True
                    return
                else:
                    del _instancias[clase]
            except Exception:
                del _instancias[clase]
        
        self._skip_init = False
        
        super().__init__(master, **kwargs)
        _instancias[clase] = self
        
        self.figura = None
        self.canvas = None
        self._master = master
        
        if master is not None:
            try:
                self.transient(master)
            except Exception:
                pass
        
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)
    
    def _al_cerrar(self):
        """Maneja el evento de cierre de la ventana."""
        self._limpiar_recursos()
        self._liberar_instancia()
        self.destroy()
    
    def _limpiar_recursos(self):
        """Limpia los recursos de matplotlib si existen."""
        if self.canvas is not None:
            try:
                self.canvas.get_tk_widget().destroy()
            except Exception:
                pass
            self.canvas = None
        
        if self.figura is not None:
            try:
                plt.close(self.figura)
            except Exception:
                pass
            self.figura = None
    
    def _liberar_instancia(self):
        """Libera la referencia a la instancia activa."""
        clase = type(self)
        if clase in _instancias and _instancias[clase] is self:
            del _instancias[clase]
    
    def centrar_ventana(self, ancho: int, alto: int):
        """
        Centra la ventana en la pantalla y la coloca adelante.
        
        Args:
            ancho (int): Ancho de la ventana.
            alto (int): Alto de la ventana.
        """
        self.update_idletasks()
        
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        
        x = (ancho_pantalla - ancho) // 2
        y = (alto_pantalla - alto) // 2
        
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        self.attributes('-topmost', True)
        self.lift()
        self.focus_force()
        self.after(100, lambda: self.attributes('-topmost', False))
    
    @classmethod
    def hay_instancia_activa(cls) -> bool:
        """
        Verifica si hay una instancia activa de esta clase de ventana.
        
        Returns:
            bool: True si hay una instancia activa de esta clase específica.
        """
        if cls not in _instancias:
            return False
        
        try:
            return _instancias[cls].winfo_exists()
        except Exception:
            if cls in _instancias:
                del _instancias[cls]
            return False
    
    @classmethod
    def obtener_instancia(cls) -> Optional['BaseToplevelWindow']:
        """
        Obtiene la instancia activa de esta clase de ventana.
        
        Returns:
            BaseToplevelWindow o None si no hay instancia activa de esta clase.
        """
        if cls in _instancias:
            return _instancias[cls]
        return None
    
    @classmethod
    def cerrar_todas(cls):
        """Cierra todas las ventanas secundarias."""
        global _instancias
        for instancia in list(_instancias.values()):
            try:
                if instancia.winfo_exists():
                    instancia._al_cerrar()
            except Exception:
                pass
        _instancias = {}
