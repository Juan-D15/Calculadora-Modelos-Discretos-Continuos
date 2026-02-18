"""
Módulo para carga y procesamiento de archivos de datos
Soporta archivos CSV y Excel (.xlsx)
"""
import os
import pandas as pd
from tkinter import filedialog
from typing import Dict, List, Optional


class ErrorCargaArchivo(Exception):
    """Excepción base para errores de carga de archivos"""
    pass


class ArchivoNoSeleccionadoError(ErrorCargaArchivo):
    """Excepción cuando el usuario cancela la selección de archivo"""
    pass


class ArchivoVacioError(ErrorCargaArchivo):
    """Excepción cuando el archivo no contiene datos"""
    pass


class ArchivoSinEncabezadosError(ErrorCargaArchivo):
    """Excepción cuando el archivo no tiene columnas con encabezados válidos"""
    pass


class FormatoNoSoportadoError(ErrorCargaArchivo):
    """Excepción cuando el formato de archivo no es soportado"""
    pass


class ColumnaNoEncontradaError(ErrorCargaArchivo):
    """Excepción cuando la columna solicitada no existe en el DataFrame"""
    pass


class FileLoader:
    """
    Clase para cargar y procesar archivos de datos (CSV y Excel).
    
    Permite cargar archivos mediante un diálogo de selección,
    obtener encabezados de columnas y calcular frecuencias de valores.
    """
    
    def __init__(self):
        """Inicializa el FileLoader."""
        self.ultima_ruta: Optional[str] = None
        self._extensiones_validas = ('.xlsx', '.xls', '.csv')
    
    def cargar_archivo(self, titulo: str = "Seleccionar archivo de datos") -> pd.DataFrame:
        """
        Abre un diálogo para seleccionar y cargar un archivo de datos.
        
        Soporta archivos Excel (.xlsx, .xls) y CSV (.csv).
        """
        tipos_archivo = [
            ("Archivos Excel", "*.xlsx *.xls"),
            ("Archivos CSV", "*.csv"),
            ("Todos los archivos soportados", "*.xlsx *.xls *.csv")
        ]
        
        ruta_archivo = filedialog.askopenfilename(
            title=titulo,
            filetypes=tipos_archivo
        )
        
        if not ruta_archivo:
            raise ArchivoNoSeleccionadoError(
                "No se seleccionó ningún archivo. "
                "Por favor, seleccione un archivo .xlsx o .csv."
            )
        
        ruta_lower = ruta_archivo.lower()
        if not ruta_lower.endswith(self._extensiones_validas):
            raise FormatoNoSoportadoError(
                f"El formato de archivo no es soportado.\n"
                f"Formatos aceptados: {', '.join(self._extensiones_validas)}\n"
                f"Archivo seleccionado: {ruta_archivo}"
            )
        
        try:
            if ruta_lower.endswith('.csv'):
                df = pd.read_csv(ruta_archivo, encoding='utf-8')
            elif ruta_lower.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(ruta_archivo)
            else:
                raise FormatoNoSoportadoError(
                    f"Formato no soportado: {ruta_archivo}"
                )
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(ruta_archivo, encoding='latin-1')
            except Exception as e:
                raise ErrorCargaArchivo(
                    f"Error de codificación al leer el archivo:\n{str(e)}\n\n"
                    "Intente guardar el archivo con codificación UTF-8."
                )
        except pd.errors.EmptyDataError:
            raise ArchivoVacioError(
                "El archivo está vacío o no contiene datos legibles.\n"
                "Por favor, verifique que el archivo tenga contenido."
            )
        except Exception as e:
            raise ErrorCargaArchivo(
                f"Error al leer el archivo:\n{str(e)}\n\n"
                "Verifique que el archivo no esté corrupto o en uso."
            )
        
        if df.empty:
            raise ArchivoVacioError(
                "El archivo no contiene filas de datos.\n"
                "Por favor, verifique que el archivo tenga registros."
            )
        
        if len(df.columns) == 0:
            raise ArchivoSinEncabezadosError(
                "El archivo no tiene columnas con encabezados.\n"
                "Por favor, verifique que la primera fila contenga los nombres de las columnas."
            )
        
        columnas_sin_nombre = [col for col in df.columns if str(col).startswith('Unnamed')]
        if len(columnas_sin_nombre) == len(df.columns):
            raise ArchivoSinEncabezadosError(
                "El archivo no tiene encabezados válidos.\n"
                "Todas las columnas están sin nombre.\n"
                "Por favor, asegúrese de que la primera fila contenga los nombres de las columnas."
            )
        
        self.ultima_ruta = ruta_archivo
        return df
    
    def obtener_nombre_archivo(self) -> str:
        """Obtiene solo el nombre del archivo de la última ruta cargada."""
        if self.ultima_ruta:
            return os.path.basename(self.ultima_ruta)
        return ""
    
    def obtener_encabezados(self, df: pd.DataFrame) -> List[str]:
        """
        Obtiene la lista de encabezados (nombres de columnas) de un DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Se esperaba un DataFrame de pandas, pero se recibió: {type(df).__name__}"
            )
        
        if len(df.columns) == 0:
            raise ArchivoSinEncabezadosError(
                "El DataFrame no tiene columnas definidas."
            )
        
        return df.columns.tolist()
    
    def obtener_frecuencias(self, df: pd.DataFrame, columna: str) -> Dict[str, int]:
        """
        Calcula las frecuencias de valores únicos en una columna específica.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Se esperaba un DataFrame de pandas, pero se recibió: {type(df).__name__}"
            )
        
        if columna not in df.columns:
            columnas_disponibles = ', '.join(df.columns.tolist())
            raise ColumnaNoEncontradaError(
                f"La columna '{columna}' no existe en el archivo.\n"
                f"Columnas disponibles: {columnas_disponibles}"
            )
        
        conteo = df[columna].value_counts()
        frecuencias = conteo.to_dict()
        
        frecuencias_str = {}
        for clave, valor in frecuencias.items():
            clave_str = str(clave) if pd.notna(clave) else "NaN (valor nulo)"
            frecuencias_str[clave_str] = int(valor)
        
        return frecuencias_str
    
    def obtener_resumen_datos(self, df: pd.DataFrame) -> Dict:
        """
        Genera un resumen general de los datos cargados.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Se esperaba un DataFrame de pandas, pero se recibió: {type(df).__name__}"
            )
        
        return {
            'filas': len(df),
            'columnas': len(df.columns),
            'encabezados': self.obtener_encabezados(df),
            'ultima_ruta': self.ultima_ruta
        }
