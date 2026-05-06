# Diseño: tasas observadas M/M/1 desde Super24

## Contexto

La sección Simulador Super24 carga escenarios desde PostgreSQL mediante `Super24DBConnector` y permite calcular distribuciones con esos datos. Para la opción `M/M/1`, la implementación actual en `ventana_principal.py` usa directamente `lambda_h` y `mu_h` del escenario seleccionado.

El objetivo es que `M/M/1` modele lo observado en la simulación, no solo los parámetros teóricos configurados. Para eso se deben derivar `lambda` y `mu` desde las métricas reales guardadas por Super24: `w`, `wq`, `lq`, `rho` y `servidores_c`.

## Alcance

Se modificará únicamente el flujo de cálculo `M/M/1` de la sección Super24. Las distribuciones Binomial, Hipergeométrica y Poisson seguirán usando el flujo actual basado en ventas importadas.

No se cambiará la consulta SQL porque `db_connector.py` ya trae los campos necesarios: `lambda_h`, `mu_h`, `servidores_c`, `rho`, `wq`, `w` y `lq`.

## Arquitectura

La lógica se agregará en `ventana_principal.py`, cerca de `_calcular_super24_mm1`, mediante un helper privado. Esta opción mantiene el cambio mínimo y evita mezclar lógica de interpretación de Super24 dentro de `MM1Queue` o del conector de base de datos.

Unidad propuesta:

```python
def _derivar_tasas_super24_mm1(self, escenario) -> tuple[float, float]:
    """Deriva lambda y mu observadas desde metricas Super24."""
```

El helper recibirá el diccionario del escenario y devolverá `(lambda_real, mu_real)` en clientes por hora.

## Flujo De Datos

1. `_calcular_super24_mm1` obtiene el escenario seleccionado desde el dashboard.
2. En lugar de leer `lambda_h` y `mu_h` como tasas finales, llama a `_derivar_tasas_super24_mm1(escenario)`.
3. El helper convierte los campos del escenario a valores numéricos seguros.
4. Calcula la tasa de servicio observada con `mu_real = 60 / (w - wq)` si `w - wq > 0`.
5. Si el tiempo neto de servicio no es válido, usa `mu_h` como respaldo.
6. Calcula la tasa de llegada observada con `lambda_real = rho * servidores_c * mu_real`.
7. Si `lambda_real <= 0` y `wq > 0`, usa Ley de Little para cola: `lambda_real = (lq / wq) * 60`.
8. Si el resultado sigue sin ser positivo, usa `lambda_h` como respaldo final.
9. `_calcular_super24_mm1` construye `MM1Queue(lambda_real, mu_real, n_solicitado)` y conserva el flujo actual de resultados y graficas.

## Servidores Multiples

Si `servidores_c` es mayor que 1, se usará la fórmula exacta indicada:

```text
lambda_real = rho * servidores_c * mu_real
```

La calculadora seguirá usando el modelo `M/M/1`. Si la tasa total observada produce `lambda_real >= mu_real`, `MM1Queue` levantará el error de sistema inestable existente. Esto es intencional: no se ajustará la llegada a una tasa por servidor y no se ocultará la incompatibilidad con `M/M/1`.

## Manejo De Errores

El helper evitará divisiones por cero y valores ausentes usando respaldos en este orden:

Para `mu_real`:

1. `60 / (w - wq)` cuando `w - wq > 0`.
2. `mu_h` cuando el tiempo de servicio no sea positivo.

Para `lambda_real`:

1. `rho * servidores_c * mu_real` cuando produzca un valor positivo.
2. `(lq / wq) * 60` cuando `wq > 0` y la fórmula principal no produzca valor positivo.
3. `lambda_h` como respaldo final.

Si luego de los respaldos `lambda_real` o `mu_real` no cumplen las validaciones de `MM1Queue`, se mantendrá el comportamiento actual: se mostrará un error de validación o entrada desde el flujo existente de `calcular_super24`.

## Pruebas

Se agregarán pruebas unitarias enfocadas en la derivación de tasas observadas:

1. Caso principal: con `w=12`, `wq=2`, `rho=0.5`, `servidores_c=2`, debe calcular `mu_real=6` y `lambda_real=6`.
2. Respaldo de `mu`: si `w - wq <= 0`, debe usar `mu_h`.
3. Respaldo de `lambda` por Ley de Little: si `rho=0`, `lq=3` y `wq=15`, debe calcular `lambda_real=12`.
4. Respaldo final de `lambda`: si la fórmula principal y Ley de Little no aplican, debe usar `lambda_h`.

Las pruebas pueden instanciar `VentanaPrincipal` sin ejecutar `__init__` mediante `VentanaPrincipal.__new__(VentanaPrincipal)` para probar el helper sin abrir la interfaz grafica.

## Criterios De Aceptacion

La opción `M/M/1` del Simulador Super24 debe usar tasas observadas derivadas desde las métricas reales de la simulación.

Los campos teóricos `lambda_h` y `mu_h` solo deben actuar como respaldos cuando las métricas observadas no permiten calcular tasas válidas.

La fórmula para múltiples servidores debe usar `rho * servidores_c * mu_real`, aunque el modelo `M/M/1` pueda rechazar el resultado por inestabilidad.

El flujo visual de resultados y graficas no debe cambiar, salvo que los valores mostrados de `lambda` y `mu` ahora correspondan a las tasas derivadas.
