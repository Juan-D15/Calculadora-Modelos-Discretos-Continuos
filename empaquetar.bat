@echo off
REM Script para empaquetar la Calculadora de Distribuciones con PyInstaller

echo ==========================================
echo Empaquetando Calculadora de Distribuciones
echo ==========================================
echo.

REM Limpiar archivos anteriores
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo Limpiando archivos anteriores... Listo.
echo.

REM Ejecutar PyInstaller
echo Creando ejecutable con PyInstaller...
.venv\Scripts\python -m PyInstaller ^
  --name "CalculadoraDistribuciones" ^
  --windowed ^
  --onefile ^
  --icon=NONE ^
  --hidden-import=customtkinter ^
  --hidden-import=matplotlib ^
  --hidden-import=numpy ^
  --hidden-import=PIL ^
  --hidden-import=matplotlib.backends.backend_tkagg ^
  main.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo ==========================================
    echo EXITO: Ejecutable creado correctamente!
    echo ==========================================
    echo.
    echo Ubicacion: dist\CalculadoraDistribuciones.exe
    echo Tamano:
    dir dist\CalculadoraDistribuciones.exe | find "CalculadoraDistribuciones.exe"
    echo.
    echo Para ejecutar el programa, haga doble clic en:
    echo dist\CalculadoraDistribuciones.exe
) else (
    echo ==========================================
    echo ERROR: Hubo un problema al crear el ejecutable
    echo ==========================================
    echo.
    echo Consulte el registro de errores en la carpeta build.
)

echo.
pause
