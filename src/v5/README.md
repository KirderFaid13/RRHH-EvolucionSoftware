# v5: cambio correctivo de la semana 09

La solicitud [CAM-S09-001 / Issue #10](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/10), definida en el [contrato C07](../../specs/c07_gestion_cambio.json), corrige la falta de liberación explícita del comando creado por `Generar`. El recurso es `ComandoReporte` y su `SqlCommand`; no se ha medido una fuga en producción ni modificado el cierre de conexiones.

La única implementación nueva es [GeneradorReportes.cs](caso_cambio/GeneradorReportes.cs). Frente a v4, solo el cuerpo de `Generar` añade `using`: se libera el comando cuando termina el ejecutor síncrono, tanto si devuelve el `DataSet` como si lanza una excepción. Se conserva el resultado y la excepción por identidad. `Preparar` no ejecuta ni libera; quien solicita un comando preparado conserva la responsabilidad de disponerlo.

El ejecutor recibe el comando prestado durante `Ejecutar`. No debe conservarlo para usarlo después de retornar. El `DataSet` devuelto permanece bajo responsabilidad del llamador. No se añaden guardas de argumentos ni configuración de tiempo de espera: las Issues #11 y #12 son propuestas pendientes.

## Fuentes seleccionadas para compilar

La biblioteca diagnóstica x86 mantiene 22 fuentes: once de v1 restauradas de forma privada sin su fachada; dos helpers de empleados v2; cuatro fuentes v3 (`ComandoReporte`, `IDefinicionReporte`, `ReporteOficina`, `ReporteOficinaPorSigla`); cuatro fuentes v4 (`RRHHClass`, `IEjecutorReportes`, `ComposicionReportes`, `EjecutorReportesSql`); y el generador v5. Se selecciona un solo `GeneradorReportes` y una sola fachada. No se modifica ninguna fuente v1–v4.

La composición y fachada v4 se compilan contra el generador v5. Sus firmas, consultas, parámetros, nombres de tablas y código permanecen iguales. La biblioteca se compila con referencias recibidas verificadas, pero no se ejecutan la fachada, los binarios originales ni el ejecutor SQL.

## Reproducir

Desde la raíz del repositorio, en Windows con Python, Git, SDK .NET `10.0.103`, referencias Framework `v4.0.30319` y las dependencias privadas verificadas ya disponibles:

```powershell
python herramientas/compilar_v5.py
python herramientas/verificar_v5.py
```

El compilador comprueba las fuentes restauradas v1 contra sus hashes de recuperación y `GRLL.dll` contra el inventario original; no lee la clave ni restaura automáticamente el legado. Si faltan dependencias, indica el procedimiento privado previo. Los compilados, contratos copiados y logs quedan en `.local/c07/`, fuera de Git; únicamente se publica evidencia nueva en `evidencia/semanas/semana09/`.

La [suite de ciclo de vida](pruebas/PruebasCicloVida.cs) se compila dos veces sin SQL: v4 reproduce los dos fallos de liberación (cuatro de seis casos aprobados, salida 1 esperada) y v5 debe aprobar los seis. Un ejecutor espía observa el evento `SqlCommand.Disposed` antes de la limpieza propia del harness. Además se repiten los dieciséis escenarios IoC S07 contra el generador nuevo, con el harness anterior intacto. El harness de ciclo de vida selecciona nueve fuentes; el de regresión diez.

Las [evidencias S09](../../evidencia/semanas/semana09/compilacion_y_pruebas.json) y su [verificación](../../evidencia/semanas/semana09/verificacion_v5.json) distinguen compilación, reproducción del defecto, prueba de la corrección y preservación histórica. No certifican SQL/CMI, interfaz, rendimiento, datos reales, autenticación o equivalencia completa con el RRHH original.
