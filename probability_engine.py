"""
Motor de cálculo de probabilidades para distribuciones binomial e hipergeométrica.
Sin dependencias de UI - solo lógica de negocio.
"""
import math
from typing import Dict, Tuple, Optional


class ErrorCalculo(Exception):
    """Excepción base para errores de cálculo."""
    pass


class ParametrosInvalidosError(ErrorCalculo):
    """Excepción cuando los parámetros son inválidos."""
    pass


class ProbabilityEngine:
    """
    Motor de cálculo de probabilidades para distribuciones estadísticas.
    
    Soporta distribución Binomial e Hipergeométrica con todos los cálculos
    estadísticos relacionados: media, desviación, mediana, sesgo y curtosis.
    
    Example:
        >>> engine = ProbabilityEngine()
        >>> modelo = engine.seleccionar_modelo(25, 100)  # 25% >= 20%
        >>> modelo
        'Hipergeométrica'
        >>> prob = engine.calcular_probabilidad(100, 30, 25, 5, modelo)
    """
    
    UMBRAL_HIPERGEOMETRICA = 0.20
    
    def seleccionar_modelo(self, n: int, N: int) -> str:
        """
        Determina qué modelo de distribución usar basado en el tamaño de muestra.
        
        Si la muestra representa el 20% o más de la población, se usa
        distribución Hipergeométrica. De lo contrario, se recomienda Binomial.
        
        Args:
            n (int): Tamaño de la muestra.
            N (int): Tamaño de la población.
        
        Returns:
            str: "Hipergeométrica" si n/N >= 0.20, sino "Binomial".
        
        Raises:
            ParametrosInvalidosError: Si n o N son inválidos.
        
        Example:
            >>> engine = ProbabilityEngine()
            >>> engine.seleccionar_modelo(20, 100)
            'Hipergeométrica'
            >>> engine.seleccionar_modelo(10, 100)
            'Binomial'
        """
        try:
            if N is None or N <= 0:
                raise ParametrosInvalidosError(
                    "El tamaño de población (N) debe ser mayor a 0."
                )
            
            if n is None or n <= 0:
                raise ParametrosInvalidosError(
                    "El tamaño de muestra (n) debe ser mayor a 0."
                )
            
            if n > N:
                raise ParametrosInvalidosError(
                    f"El tamaño de muestra (n={n}) no puede ser mayor que la población (N={N})."
                )
            
            proporcion = n / N
            
            if proporcion >= self.UMBRAL_HIPERGEOMETRICA:
                return "Hipergeométrica"
            else:
                return "Binomial"
                
        except TypeError as e:
            raise ParametrosInvalidosError(
                f"Los parámetros deben ser números enteros. Error: {str(e)}"
            )
    
    def _combinatoria(self, n: int, k: int) -> int:
        """
        Calcula la combinatoria C(n, k) = n! / (k! * (n-k)!).
        
        Args:
            n (int): Total de elementos.
            k (int): Elementos a seleccionar.
        
        Returns:
            int: Número de combinaciones posibles.
        """
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        return math.comb(n, k)
    
    def calcular_probabilidad(
        self, 
        N: int, 
        K: int, 
        n: int, 
        x: int, 
        modelo: str
    ) -> float:
        """
        Calcula la probabilidad P(X=x) según el modelo especificado.
        
        Fórmulas:
        - Hipergeométrica: P(X=x) = C(K,x) * C(N-K, n-x) / C(N, n)
        - Binomial: p = K/N, P(X=x) = C(n,x) * p^x * (1-p)^(n-x)
        
        Args:
            N (int): Tamaño de la población.
            K (int): Número de éxitos en la población.
            n (int): Tamaño de la muestra.
            x (int): Número de éxitos deseados.
            modelo (str): "Hipergeométrica" o "Binomial".
        
        Returns:
            float: Probabilidad P(X=x).
        
        Raises:
            ParametrosInvalidosError: Si los parámetros son inválidos.
            ErrorCalculo: Si ocurre un error durante el cálculo.
        
        Example:
            >>> engine = ProbabilityEngine()
            >>> engine.calcular_probabilidad(25, 6, 4, 2, "Hipergeométrica")
            0.20276679841897233
        """
        try:
            self._validar_parametros_basicos(N, K, n, x)
            
            if modelo == "Hipergeométrica":
                return self._probabilidad_hipergeometrica(N, K, n, x)
            elif modelo == "Binomial":
                return self._probabilidad_binomial(N, K, n, x)
            else:
                raise ParametrosInvalidosError(
                    f"Modelo no reconocido: {modelo}. "
                    "Use 'Hipergeométrica' o 'Binomial'."
                )
                
        except ParametrosInvalidosError:
            raise
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular la probabilidad: {str(e)}"
            )
    
    def _validar_parametros_basicos(self, N: int, K: int, n: int, x: int):
        """Valida los parámetros básicos para cualquier cálculo."""
        if N is None or N <= 0:
            raise ParametrosInvalidosError("N debe ser mayor a 0.")
        if K is None or K < 0:
            raise ParametrosInvalidosError("K no puede ser negativo.")
        if K > N:
            raise ParametrosInvalidosError(f"K ({K}) no puede ser mayor que N ({N}).")
        if n is None or n <= 0:
            raise ParametrosInvalidosError("n debe ser mayor a 0.")
        if n > N:
            raise ParametrosInvalidosError(f"n ({n}) no puede ser mayor que N ({N}).")
        if x is None or x < 0:
            raise ParametrosInvalidosError("x no puede ser negativo.")
        if x > K:
            raise ParametrosInvalidosError(f"x ({x}) no puede ser mayor que K ({K}).")
        if x > n:
            raise ParametrosInvalidosError(f"x ({x}) no puede ser mayor que n ({n}).")
    
    def _probabilidad_hipergeometrica(self, N: int, K: int, n: int, x: int) -> float:
        """Calcula P(X=x) para distribución hipergeométrica."""
        numerador = self._combinatoria(K, x) * self._combinatoria(N - K, n - x)
        denominador = self._combinatoria(N, n)
        
        if denominador == 0:
            return 0.0
        
        return numerador / denominador
    
    def _probabilidad_binomial(self, N: int, K: int, n: int, x: int) -> float:
        """Calcula P(X=x) para distribución binomial."""
        p = K / N
        q = 1 - p
        
        comb = self._combinatoria(n, x)
        prob = comb * (p ** x) * (q ** (n - x))
        
        return prob
    
    def calcular_probabilidades_rango_x(
        self, 
        N: int, 
        K: int, 
        n: int, 
        x_max: int,
        modelo: str
    ) -> Dict[int, float]:
        """
        Calcula las probabilidades desde 0 hasta x_max.
        
        Genera un diccionario con P(X=x) para x desde 0 hasta x_max.
        
        Args:
            N (int): Tamaño de la población.
            K (int): Número de éxitos en la población.
            n (int): Tamaño de la muestra.
            x_max (int): Valor máximo de x para calcular probabilidades.
            modelo (str): "Hipergeométrica" o "Binomial".
        
        Returns:
            Dict[int, float]: Diccionario {x: P(X=x)} para x en range(0, x_max+1).
        """
        try:
            self._validar_parametros_basicos(N, K, n, 0)
            
            probabilidades = {}
            limite = min(x_max, n, K) if modelo == "Hipergeométrica" else min(x_max, n)
            
            for x in range(0, limite + 1):
                probabilidades[x] = self.calcular_probabilidad(N, K, n, x, modelo)
            
            return probabilidades
            
        except (ParametrosInvalidosError, ErrorCalculo):
            raise
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular las probabilidades: {str(e)}"
            )
    
    def calcular_todas_probabilidades(
        self, 
        N: int, 
        K: int, 
        n: int, 
        modelo: str
    ) -> Dict[int, float]:
        """
        Calcula las probabilidades para todos los valores posibles de x.
        
        Genera un diccionario con P(X=x) para x desde 0 hasta n.
        
        Args:
            N (int): Tamaño de la población.
            K (int): Número de éxitos en la población.
            n (int): Tamaño de la muestra.
            modelo (str): "Hipergeométrica" o "Binomial".
        
        Returns:
            Dict[int, float]: Diccionario {x: P(X=x)} para x en range(0, n+1).
        
        Raises:
            ParametrosInvalidosError: Si los parámetros son inválidos.
            ErrorCalculo: Si ocurre un error durante el cálculo.
        
        Example:
            >>> engine = ProbabilityEngine()
            >>> probs = engine.calcular_todas_probabilidades(25, 6, 4, "Hipergeométrica")
            >>> probs[2]
            0.20276679841897233
        """
        try:
            self._validar_parametros_basicos(N, K, n, 0)
            
            probabilidades = {}
            max_x = min(n, K) if modelo == "Hipergeométrica" else n
            
            for x in range(0, max_x + 1):
                probabilidades[x] = self.calcular_probabilidad(N, K, n, x, modelo)
            
            for x in range(max_x + 1, n + 1):
                probabilidades[x] = 0.0
            
            return probabilidades
            
        except (ParametrosInvalidosError, ErrorCalculo):
            raise
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular todas las probabilidades: {str(e)}"
            )
    
    def calcular_media(
        self, 
        n: int, 
        K: int, 
        N: int, 
        modelo: str
    ) -> float:
        """
        Calcula la media (esperanza) de la distribución.
        
        Fórmulas:
        - Binomial: μ = n * p = n * (K/N)
        - Hipergeométrica: μ = n * K / N
        
        Args:
            n (int): Tamaño de la muestra.
            K (int): Número de éxitos en la población.
            N (int): Tamaño de la población.
            modelo (str): "Hipergeométrica" o "Binomial".
        
        Returns:
            float: Media de la distribución.
        
        Raises:
            ParametrosInvalidosError: Si los parámetros son inválidos.
            ErrorCalculo: Si ocurre un error durante el cálculo.
        
        Example:
            >>> engine = ProbabilityEngine()
            >>> engine.calcular_media(4, 6, 25, "Hipergeométrica")
            0.96
        """
        try:
            if N is None or N <= 0:
                raise ParametrosInvalidosError("N debe ser mayor a 0.")
            if n is None or n <= 0:
                raise ParametrosInvalidosError("n debe ser mayor a 0.")
            
            p = K / N
            media = n * p
            
            return media
            
        except ParametrosInvalidosError:
            raise
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular la media: {str(e)}"
            )
    
    def calcular_desviacion(
        self, 
        n: int, 
        K: int, 
        N: int, 
        modelo: str
    ) -> float:
        """
        Calcula la desviación estándar de la distribución.
        
        Fórmulas:
        - Binomial: σ = sqrt(n * p * (1-p)) donde p = K/N
        - Hipergeométrica: σ = sqrt(n * (K/N) * ((N-K)/N) * ((N-n)/(N-1)))
        
        Args:
            n (int): Tamaño de la muestra.
            K (int): Número de éxitos en la población.
            N (int): Tamaño de la población.
            modelo (str): "Hipergeométrica" o "Binomial".
        
        Returns:
            float: Desviación estándar.
        
        Raises:
            ParametrosInvalidosError: Si los parámetros son inválidos.
            ErrorCalculo: Si ocurre un error durante el cálculo.
        
        Example:
            >>> engine = ProbabilityEngine()
            >>> engine.calcular_desviacion(4, 6, 25, "Hipergeométrica")
            0.7989993742175272
        """
        try:
            if N is None or N <= 0:
                raise ParametrosInvalidosError("N debe ser mayor a 0.")
            if n is None or n <= 0:
                raise ParametrosInvalidosError("n debe ser mayor a 0.")
            
            p = K / N
            q = (N - K) / N
            
            if modelo == "Hipergeométrica":
                if N <= 1:
                    return 0.0
                fpc = (N - n) / (N - 1)
                varianza = n * p * q * fpc
            else:
                varianza = n * p * q
            
            return math.sqrt(varianza)
            
        except ParametrosInvalidosError:
            raise
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular la desviación estándar: {str(e)}"
            )
    
    def calcular_mediana(self, probs: Dict[int, float]) -> float:
        """
        Calcula la mediana de la distribución acumulada.
        
        La mediana es el valor donde la probabilidad acumulada alcanza
        o supera 0.5 por primera vez.
        
        Args:
            probs (Dict[int, float]): Diccionario {x: P(X=x)} con las probabilidades.
        
        Returns:
            float: Mediana de la distribución.
        
        Raises:
            ParametrosInvalidosError: Si el diccionario está vacío.
            ErrorCalculo: Si ocurre un error durante el cálculo.
        
        Example:
            >>> engine = ProbabilityEngine()
            >>> probs = {0: 0.3, 1: 0.4, 2: 0.2, 3: 0.1}
            >>> engine.calcular_mediana(probs)
            1
        """
        try:
            if not probs:
                raise ParametrosInvalidosError(
                    "El diccionario de probabilidades no puede estar vacío."
                )
            
            valores_ordenados = sorted(probs.keys())
            
            prob_acumulada = 0.0
            for x in valores_ordenados:
                prob_acumulada += probs[x]
                if prob_acumulada >= 0.5:
                    return float(x)
            
            return float(valores_ordenados[-1])
            
        except ParametrosInvalidosError:
            raise
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular la mediana: {str(e)}"
            )
    
    def calcular_sesgo(self, media: float, mediana: float) -> str:
        """
        Determina el tipo de sesgo comparando la media y la mediana.
        
        Criterios:
        - Sesgo negativo: media < mediana
        - Sesgo nulo: media = mediana
        - Sesgo positivo: media > mediana
        
        Args:
            media (float): Valor de la media.
            mediana (float): Valor de la mediana.
        
        Returns:
            str: Descripción del tipo de sesgo.
        
        Example:
            >>> engine = ProbabilityEngine()
            >>> engine.calcular_sesgo(0.96, 1)
            'Negativo (media < mediana)'
        """
        try:
            tolerancia = 0.001
            diferencia = media - mediana
            
            if abs(diferencia) < tolerancia:
                return "Nulo (media = mediana)"
            elif diferencia < 0:
                return "Negativo (media < mediana)"
            else:
                return "Positivo (media > mediana)"
                
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular el sesgo: {str(e)}"
            )
    
    def calcular_curtosis(
        self, 
        N: int, 
        K: int, 
        n: int
    ) -> Tuple[float, str]:
        """
        Calcula la curtosis de la distribución hipergeométrica.
        
        La curtosis indica la forma de la distribución:
        - Leptocúrtica (>0): Curva más puntiaguda que la normal
        - Mesocúrtica (~0): Similar a la normal
        - Platicúrtica (<0): Curva más aplanada que la normal
        
        Args:
            N (int): Tamaño de la población.
            K (int): Número de éxitos en la población.
            n (int): Tamaño de la muestra.
        
        Returns:
            Tuple[float, str]: (valor_curtosis, tipo_curtosis)
            donde tipo_curtosis es "Leptocúrtica", "Mesocúrtica" o "Platicúrtica".
        
        Raises:
            ParametrosInvalidosError: Si los parámetros son inválidos.
            ErrorCalculo: Si ocurre un error durante el cálculo.
        
        Example:
            >>> engine = ProbabilityEngine()
            >>> engine.calcular_curtosis(25, 6, 4)
            (38.50867542517721, 'Leptocúrtica')
        """
        try:
            if N is None or N <= 3:
                raise ParametrosInvalidosError("N debe ser mayor a 3 para calcular curtosis.")
            if K is None or K <= 0:
                raise ParametrosInvalidosError("K debe ser mayor a 0.")
            if n is None or n <= 0:
                raise ParametrosInvalidosError("n debe ser mayor a 0.")
            if K > N:
                raise ParametrosInvalidosError(f"K ({K}) no puede ser mayor que N ({N}).")
            if n > N:
                raise ParametrosInvalidosError(f"n ({n}) no puede ser mayor que N ({N}).")
            
            p = K / N
            q = 1 - p
            
            if N - n <= 0 or N - K <= 0:
                return 0.0, "Mesocúrtica"
            
            varianza = n * p * q * (N - n) / (N - 1)
            
            if varianza == 0:
                return 0.0, "Mesocúrtica"
            
            try:
                numerador = (N - 1) * (N * (N + 1) - 6 * N * (N - n) * p * q + 
                                      6 * n * (N - n) * (N - 2) * (N - 3) * p * p * q * q)
                denominador = n * (N - n) * (N - 2) * (N - 3) * p * q * varianza
                
                if denominador == 0:
                    return 0.0, "Mesocúrtica"
                
                curtosis = numerador / denominador - 3
                
            except (ZeroDivisionError, OverflowError):
                return 0.0, "Mesocúrtica"
            
            if curtosis > 0.1:
                tipo = "Leptocúrtica"
            elif curtosis < -0.1:
                tipo = "Platicúrtica"
            else:
                tipo = "Mesocúrtica"
            
            return curtosis, tipo
            
        except ParametrosInvalidosError:
            raise
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular la curtosis: {str(e)}"
            )
    
    def calcular_resumen_completo(
        self, 
        N: int, 
        K: int, 
        n: int, 
        x: int
    ) -> Dict:
        """
        Calcula un resumen completo con todas las estadísticas.
        
        Args:
            N (int): Tamaño de la población.
            K (int): Número de éxitos en la población.
            n (int): Tamaño de la muestra.
            x (int): Número de éxitos deseados (calcula probabilidades de 0 a x).
        
        Returns:
            Dict: Diccionario con todos los cálculos:
                - modelo: str
                - probabilidad_x: float
                - probabilidades_rango: dict (de 0 a x)
                - media: float
                - desviacion: float
                - mediana: float
                - sesgo: str
                - curtosis_valor: float
                - curtosis_tipo: str
        """
        try:
            modelo = self.seleccionar_modelo(n, N)
            
            probs_rango = self.calcular_probabilidades_rango_x(N, K, n, x, modelo)
            
            probs_completas = self.calcular_todas_probabilidades(N, K, n, modelo)
            
            media = self.calcular_media(n, K, N, modelo)
            desviacion = self.calcular_desviacion(n, K, N, modelo)
            mediana = self.calcular_mediana(probs_completas)
            sesgo = self.calcular_sesgo(media, mediana)
            curtosis_valor, curtosis_tipo = self.calcular_curtosis(N, K, n)
            
            return {
                'modelo': modelo,
                'probabilidad_x': probs_rango.get(x, 0.0),
                'probabilidades_rango': probs_rango,
                'todas_probabilidades': probs_completas,
                'media': media,
                'desviacion': desviacion,
                'mediana': mediana,
                'sesgo': sesgo,
                'curtosis_valor': curtosis_valor,
                'curtosis_tipo': curtosis_tipo
            }
            
        except Exception as e:
            raise ErrorCalculo(
                f"Error al calcular el resumen completo: {str(e)}"
            )
