# Semana 09: gestionar un cambio antes de incorporarlo

**Entrega C07 · Gestión del cambio · Registro de preparación: 15 de octubre de 2026.** La base es `6c13e74482563cc158c4329852753f7f1eb2effd`: siete commits en Git que representan seis entregas académicas y una actualización documental. C07 será la séptima entrega académica; si se integra con un único squash, será el octavo commit de `main`.

## Qué pide la práctica y cómo la aplicamos

La consigna docente de páginas 14–15 pide identificar al menos tres solicitudes relacionadas con el sistema, elaborar un formato, presentar una matriz, analizar el impacto por solicitud y proponer un flujo. Página 7 solicita ejemplos con código funcional. El PDF no exige implementar las tres propuestas. Sus referencias a semana 8, IoC y OCP corresponden a restos de plantilla; el tema y la práctica de semana 9 son gestión del cambio.

Registramos tres solicitudes reales antes de implementar: [CAM-S09-001 / Issue #10](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/10), [CAM-S09-002 / Issue #11](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/11) y [CAM-S09-003 / Issue #12](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/12). Seleccionamos una corrección acotada y dejamos las otras dos como propuestas. La selección deriva de la autorización general del responsable para realizar esta práctica y publicarla; no representa una votación de un CAB ni una aprobación formal por otra persona.

Los entregables se recorren en este orden:

1. [Formato simple](../../../configuracion/plantilla_solicitud.md) y [registro JSON](../../../configuracion/solicitudes_semana09.json).
2. [Tres solicitudes y sus criterios](02_solicitudes.md).
3. [Matriz e impacto](03_matriz_impacto.md).
4. [Flujo, decisiones y reversión](04_flujo_y_reversion.md).
5. [Contrato C07](../../../specs/c07_gestion_cambio.json), que define el alcance previo al código.

El informe DOCX teórico del compañero permanece sin modificaciones. Esta documentación complementa ese informe mediante un caso práctico trazable.

## El cambio seleccionado

En v4, `GeneradorReportes.Generar` prepara un `ComandoReporte` y lo entrega al ejecutor. La clase `ComandoReporte` implementa `IDisposable`, pero el generador no llama a `Dispose` sobre el recurso que creó. Es un hallazgo del código: todavía no acredita una fuga de memoria medida en el sistema desplegado.

Antes, en `src/v4/caso_ioc/GeneradorReportes.cs`:

```csharp
public DataSet Generar(IDefinicionReporte reporte)
{
    return _sql.Ejecutar(Preparar(reporte));
}
```

El cambio C07 se implementa por separado en `src/v5/caso_cambio/GeneradorReportes.cs`:

```csharp
public DataSet Generar(IDefinicionReporte reporte)
{
    using (var comando = Preparar(reporte))
    {
        return _sql.Ejecutar(comando);
    }
}
```

La ejecución es síncrona: el comando permanece disponible durante `Ejecutar` y se libera al salir del bloque, tanto si devuelve un resultado como si el ejecutor lanza una excepción. El `DataSet` devuelto conserva su identidad y debe seguir utilizable. `Preparar` mantiene su contrato: entrega el comando al llamador, que asume su liberación. Este cambio no libera la conexión ni modifica su apertura o cierre.

Hay un riesgo de integración concreto: `EjecutorReportesSql` deja `SqlDataAdapter.SelectCommand` apuntando al comando que v5 dispone al terminar. La fachada v4 expone `objDA` públicamente, por lo que no podemos descartar consumidores en la interfaz o en binarios todavía no recuperados que intenten reutilizar esa referencia. Los métodos visibles reasignan `SelectCommand` antes de `Fill`, pero esta revisión estática no demuestra compatibilidad con SQL ni con la interfaz real. El contrato comprobado presupone ejecución síncrona y ausencia de reutilización posterior del comando por sus consumidores; esa condición requiere revisión al integrar el sistema completo.

Los seis escenarios no cubren fallos durante la adquisición/preparación del comando ni una excepción lanzada por el propio `Dispose`. Si `Dispose` lanzara una excepción, podría impedir devolver el resultado u ocultar una excepción anterior; la conservación comprobada se refiere a los caminos concretos del ejecutor ensayados. v5 continúa siendo una corrección diagnóstica; no reemplaza una versión de producción validada.

Se mantiene v4 como antecedente verificable. La biblioteca diagnóstica v5 reutiliza la fachada, la composición, la interfaz y el ejecutor de v4, las definiciones y el comando de v3 y las fuentes anteriores indicadas en la compilación. No se reemplazan binarios originales ni se modifican `src/v1` a `src/v4`.

## Por qué mejora el proyecto

La mejora de código hace explícita la responsabilidad sobre un recurso creado por el generador y evita dejar su liberación al recolector de basura. La mejora de proceso conecta necesidad, evaluación, decisión, implementación y comprobación. Conservar dos solicitudes abiertas muestra que registrar una idea no obliga a implementarla inmediatamente.

GitHub materializa el seguimiento: Issue para la solicitud, rama `semana-09-gestion-cambios` para aislar el trabajo y Pull Request para presentar el diff y la evidencia antes de integrarlo. La autorización del responsable no acredita una revisión independiente. Tampoco se configura en esta entrega integración continua ni protección de ramas.

## Cómo se comprobó y qué falta

La verificación comparó el generador anterior con v5 mediante un ejecutor espía. La misma suite de seis escenarios comprueba disponibilidad del comando durante la llamada, liberación tras éxito y error, identidad del resultado, propagación de la misma excepción y propiedad del llamador al usar `Preparar`.

- **Antes, v4:** 4 de 6 escenarios aprobados; fallan exactamente los dos de liberación, después de éxito y después de excepción. La salida 1 es el resultado esperado para reproducir el hallazgo.
- **Después, v5:** 6 de 6 escenarios aprobados y salida 0.
- **Regresión:** los 16 escenarios previos de IoC se repitieron sobre v5 y aprobaron, con salida 0.
- **Compilación:** biblioteca diagnóstica de 22 fuentes; harness de ciclo de vida de nueve fuentes por versión y harness de regresión de diez. Sin errores ni advertencias en esas compilaciones.

Esta secuencia de antes/después acredita que el cambio hace pasar los dos criterios de liberación que antes fallaban. No mide una fuga de memoria, una carga productiva ni una mejora de rendimiento. La salida roja tampoco indica que v4 no compile: su harness compiló correctamente antes de ejecutar los escenarios.

Los harness usan datos sintéticos y ejecutores sustitutos: no abren una conexión, no ejecutan `Fill` ni la fachada o binarios originales. Para inicializar contadores de `SqlClient` de Windows fue necesario ejecutar los harness fuera de AppContainer; este requisito del entorno no equivale a una conexión SQL.

Desde la raíz del repositorio se utilizan las herramientas nuevas:

```powershell
python herramientas/compilar_v5.py
python herramientas/verificar_v5.py
```

Los resultados efectivos están en [compilación y pruebas](../../../evidencia/semanas/semana09/compilacion_y_pruebas.json), [verificación de alcance](../../../evidencia/semanas/semana09/verificacion_v5.json) y [procedencia del código](../../../evidencia/semanas/semana09/procedencia_codigo.json). Los compilados y otros artefactos privados quedan en `.local/c07/`. La verificación de alcance registró 516 blobs históricos protegidos conservados, ningún cambio en ese conjunto, ausencia de cambios adicionales en el generador y exclusiones locales comprobadas. Su revisión del árbol de trabajo no certifica el índice futuro de Git ni el estado de publicación.

No se ejecutan los binarios recibidos, no se restaura el respaldo y no se abre SQL. La comprobación aislada no demuestra funcionamiento de la interfaz, integración con CMI, equivalencia completa, seguridad ni rendimiento del RRHH. Las guardas nulas y `CommandTimeout` siguen fuera de la implementación seleccionada.


## Trazabilidad de la consigna

- **S09-P01:** las tres solicitudes están descritas en `02_solicitudes.md` y tienen Issues reales.
- **S09-P02:** el formato y el registro JSON explican cada solicitud; `03_matriz_impacto.md` relaciona alcance, riesgo y verificaciones.
- **S09-P03:** `04_flujo_y_reversion.md` desarrolla las ocho etapas, decisiones y marcha atrás.
- **S09-D01:** el generador v5, los seis escenarios de ciclo de vida y la regresión proporcionan un ejemplo funcional de alcance explícito, sin SQL.

## Publicación y cierre

El usuario autorizó publicar el trabajo con Issues y su PR. C07 se prepara desde la base indicada y se propone integrar mediante squash para conservar una sola entrega académica en la línea principal. La Issue #10 se cerrará al integrar y comprobar la corrección; #11 y #12 permanecerán abiertas. El número de PR y el hash final se verifican en GitHub después de su creación, sin inventar enlaces ni incluir un hash autorreferente en el propio commit.
