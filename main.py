"""
Aplicación de Calculadora de Distribución Binomial

Punto de entrada principal de la aplicación.
"""
import customtkinter as ctk
from ventana_principal import VentanaPrincipal


def configurar_tema():
    """Configura el tema visual de la aplicación"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


def main():
    """Función principal que inicia la aplicación"""
    # Configurar tema
    configurar_tema()
    
    # Crear ventana principal
    root = ctk.CTk()
    app = VentanaPrincipal(root)
    
    # Iniciar loop de eventos
    root.mainloop()


if __name__ == "__main__":
    main()