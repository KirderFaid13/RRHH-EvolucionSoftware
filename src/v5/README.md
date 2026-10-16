# v5: cambio correctivo de la semana 09

La solicitud [CAM-S09-001 / Issue #10](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/10), definida en el [contrato C07](../../specs/c07_gestion_cambio.json), corrige la falta de liberación explícita del comando creado por `Generar`. El recurso es `ComandoReporte` y su `SqlCommand`; no se ha medido una fuga en producción ni modificado el cierre de conexiones.

La única implementación nueva es [GeneradorReportes.cs](caso_cambio/GeneradorReportes.cs). Frente a v4, solo el cuerpo de `Generar` añade `using`: se libera el comando cuando termina el ejecutor síncrono, tanto si devuelve el `DataSet` como si lanza una excepción. Se conserva el resultado y la excepción por identidad. `Preparar` no ejecuta ni libera; quien solicita un comando preparado conserva la responsabilidad de disponerlo.

El ejecutor recibe el comando prestado durante `Ejecutar`. No debe conservarlo para usarlo después de retornar. El `DataSet` devuelto permanece bajo responsabilidad del llamador. No se añaden guardas de argumentos ni configuración de tiempo de espera: las Issues #11 y #12 son propuestas pendientes.

## Fuentes seleccionadas para compilar

La biblioteca diagnóstica x86 mantiene 22 fuentes: once de v1 restauradas de forma privada sin su fachada; dos helpers de empleados v2; cuatro fuentes v3 (`ComandoReporte`, `IDefinicionReporte`, `ReporteOficina`, `ReporteOficinaPorSigla`); cuatro fuentes v4 (`RRHHClass`, `IEjecutorReportes`, `ComposicionReportes`, `EjecutorReportesSql`); y el generador v5. Se selecciona un solo `GeneradorReportes` y una sola fachada. No se modifica ninguna fuente v1–v4.

La composición y fachada v4 se compilan contra el generador v5. Sus firmas, consultas, parámetros, nombres de tablas y código permanecen iguales. La biblioteca se compila con referencias recibidas verificadas, pero no se ejecutan la fachada, los binarios originales ni el ejecutor SQL.

## Reproducir

Desde la raíz del repositorio, en Windows con Python 3.12 o posterior, Git, SDK .NET `10.0.103`, referencias Framework `v4.0.30319` y las dependencias privadas verificadas ya disponibles:

```powershell
python herramientas/compilar_v5.py
python herramientas/verificar_v5.py
```

Un clon limpio no contiene las dependencias privadas: se requieren las fuentes recuperadas en `.local/v1_src/` y `GRLL.dll` en `.local/RRHH/GRLL.dll`, restauradas previamente mediante los procedimientos autorizados de [restaurar_v1.py](../../herramientas/restaurar_v1.py) y [restaurar_legado.py](../../herramientas/restaurar_legado.py), con la clave conservada fuera de Git. El compilador comprueba sus hashes; no lee la clave ni restaura automáticamente el legado. Las herramientas de restauración usan la dependencia Python `cryptography` del entorno de recuperación.

El contrato diagnóstico `ContratosRecuperados.cs` se regenera siempre en `.local/c07/` a partir del JSON público de contratos y la procedencia S07. Se exige que produzca exactamente el SHA-256 histórico registrado; no se necesita `.local/c05/` ni ejecutar verificadores antiguos. Los compilados, el contrato generado y los logs quedan en `.local/c07/`, fuera de Git; únicamente se publica evidencia nueva en `evidencia/semanas/semana09/`.

La [suite de ciclo de vida](pruebas/PruebasCicloVida.cs) se compila dos veces sin SQL: v4 reproduce los dos fallos de liberación (cuatro de seis casos aprobados, salida 1 esperada) y v5 debe aprobar los seis. Un ejecutor espía observa el evento `SqlCommand.Disposed` antes de la limpieza propia del harness. Además se repiten los dieciséis escenarios IoC S07 contra el generador nuevo, con el harness anterior intacto. El harness de ciclo de vida selecciona nueve fuentes; el de regresión diez.

Las [evidencias S09](../../evidencia/semanas/semana09/compilacion_y_pruebas.json) y su [verificación](../../evidencia/semanas/semana09/verificacion_v5.json) distinguen compilación, reproducción del defecto, prueba de la corrección y preservación histórica. No certifican SQL/CMI, interfaz, rendimiento, datos reales, autenticación o equivalencia completa con el RRHH original.

## Riesgo de integración y límites

El ejecutor conserva `SqlDataAdapter.SelectCommand` apuntando al comando que v5 dispone. La fachada expone `objDA` públicamente: aunque los consumidores visibles reasignan el comando antes de `Fill`, no se descarta su reutilización desde UI/binarios no recuperados. Este riesgo debe revisarse antes de sustituir componentes en el sistema real. No se añade aquí limpieza del adaptador, porque sería otro cambio observable.

El evento `Disposed` acredita la invocación de `Dispose`, no una reducción medida de memoria o handles. La suite no cubre adquisición fallida del comando, errores del propio `Dispose`, concurrencia ni usos posteriores. `verificar_v5.py` coteja evidencia y hashes; para repetir la ejecución se utiliza primero `compilar_v5.py`.
