# Calculadora de Distribuciones Estadísticas

Una aplicación de escritorio moderna y elegante para calcular y visualizar distribuciones de probabilidad discretas. Desarrollada en Python con una interfaz gráfica intuitiva.

## Características

### Distribuciones Soportadas

- **Distribución Binomial**: Para ensayos independientes con probabilidad constante
- **Distribución Hipergeométrica**: Para muestreo sin reemplazo
- **Modo Comparación**: Compara ambas distribuciones lado a lado

### Funcionalidades

- **Cálculo de probabilidades**: P(X=k), P(X≤k), P(X<k), P(X>k), P(X≥k)
- **Estadísticas descriptivas**: Media, desviación estándar, sesgo y curtosis
- **Visualización gráfica**: Gráficos interactivos de la distribución
- **Factor de corrección**: Aplicación automática para poblaciones finitas
- **Análisis desde archivo**: Carga datos desde archivos Excel/CSV
- **Exportación de resultados**: Guarda cálculos y gráficos

## Requisitos

- Python 3.9 o superior
- Windows / macOS / Linux

## Instalación

1. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Distribución Binomial

1. Selecciona "Binomial" en el menú lateral
2. Ingresa los parámetros:
   - **n**: Número de ensayos
   - **p**: Probabilidad de éxito (0 a 1)
   - **N**: Tamaño de población (opcional, para factor de corrección)
   - **x**: Valores a calcular (ej: `5` o `0,1,2,3`)
3. Presiona "Calcular"

### Distribución Hipergeométrica

1. Selecciona "Hipergeométrica" en el menú lateral
2. Ingresa los parámetros:
   - **N**: Tamaño de la población
   - **K**: Número de éxitos en la población
   - **n**: Tamaño de la muestra
   - **x**: Valores a calcular
3. Presiona "Calcular"

### Modo Comparación

1. Selecciona "Binomial" y activa el modo comparación
2. Ingresa los parámetros incluyendo N (población)
3. Define una tolerancia para análisis de riesgo
4. La aplicación mostrará ambas distribuciones en paralelo

## Estructura del Proyecto

```
DistribucionBinomial_python/
├── main.py                 # Punto de entrada
├── ventana_principal.py    # Ventana principal y lógica de cálculo
├── base_window.py          # Clase base para ventanas secundarias
├── data_viewer.py          # Visor de datos desde archivos
├── results_window.py       # Ventana de resultados detallados
├── parameter_window.py     # Configuración de parámetros
├── probability_engine.py   # Motor de cálculo de probabilidades
│
├── gui/
│   ├── dashboard.py        # Panel principal con navegación
│   ├── grafico.py          # Wrapper de gráficos Matplotlib
│   ├── campos_entrada.py   # Componentes de entrada de datos
│   ├── area_resultados.py  # Área de visualización de resultados
│   └── tabla_comparacion.py# Tabla de comparación de distribuciones
│
├── utils/
│   ├── calculos.py         # Funciones de cálculo estadístico
│   ├── validaciones.py     # Validación de parámetros
│   ├── formato.py          # Formateo de resultados
│   └── file_loader.py      # Carga de archivos externos
│
└── tests/
    └── test_calculos.py    # Pruebas unitarias
```

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interfaz gráfica moderna |
| [Matplotlib](https://matplotlib.org/) | Visualización de gráficos |
| [NumPy](https://numpy.org/) | Cálculos numéricos |
| [SciPy](https://scipy.org/) | Funciones estadísticas |
| [Pandas](https://pandas.pydata.org/) | Manejo de datos |
| [PyInstaller](https://pyinstaller.org/) | Empaquetado ejecutable |

## Fórmulas Utilizadas

### Distribución Binomial

```
P(X = k) = C(n,k) × p^k × (1-p)^(n-k)

Media (μ) = n × p
Varianza (σ²) = n × p × (1-p) × FC
```

### Distribución Hipergeométrica

```
P(X = k) = C(K,k) × C(N-K, n-k) / C(N,n)

Media (μ) = n × (K/N)
Varianza (σ²) = n × (K/N) × (1 - K/N) × ((N-n)/(N-1))
```

### Factor de Corrección

```
FC = (N - n) / (N - 1)  (para poblaciones finitas con n > 5% de N)
FC = 1                   (para poblaciones infinitas)
```

## Desarrollo

### Ejecutar Tests

```bash
pytest tests/
```

### Linting

```bash
ruff check .
ruff check --fix .  # Corrección automática
```

### Type Checking

```bash
mypy .
```

### Generar Ejecutable

```bash
pyinstaller --onefile --windowed main.py
```