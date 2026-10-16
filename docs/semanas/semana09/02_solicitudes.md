# Tres solicitudes vinculadas al RRHH

Registro inicial: **15 de octubre de 2026**. Las prioridades siguientes son propuestas de trabajo para esta práctica, no niveles de servicio acordados con un cliente. Los identificadores `CAM-S09-*` son del registro del proyecto; `#10`, `#11` y `#12` son números reales de GitHub. El estado vigente de incorporación se verifica en cada Issue y su PR.

## CAM-S09-001 · Liberar el comando creado por Generar

- **Seguimiento:** [Issue #10](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/10).
- **Tipo y prioridad:** correctivo; alta dentro de esta práctica.
- **Origen comprobado:** al revisar `src/v4/caso_ioc/GeneradorReportes.cs`, `Generar` crea un `ComandoReporte` desechable sin liberarlo explícitamente. No se reporta un incidente observado en producción.
- **Cambio solicitado:** incorporar en v5 un bloque `using` sobre el comando que crea `Generar`, conservándolo disponible mientras se ejecuta el reporte.
- **Motivo:** definir la propiedad y el fin de vida del recurso sin alterar SQL, parámetros o resultados.
- **Estado de preparación:** implementada y verificada localmente; 6/6 escenarios de ciclo de vida y 16/16 de regresión aprobados. La integración mediante PR sigue pendiente en este registro.
- **Responsabilidades:** implementación asistida por el agente; KirderFaid13 es el responsable declarado para revisar e integrar. No se atribuye aprobación formal a terceros.

Criterios de aceptación:

1. El comando sigue disponible mientras `IEjecutorReportes.Ejecutar` lo utiliza.
2. Se llama a `Dispose` al terminar con éxito.
3. También se libera si el ejecutor lanza una excepción.
4. Se devuelve el mismo `DataSet`, todavía utilizable.
5. La excepción original se propaga sin sustituirla por otra.
6. `Preparar` no ejecuta ni libera el comando: conserva la propiedad del llamador.
7. Los 16 escenarios previos de IoC se repiten sobre v5 sin abrir SQL.

**Alcance y exclusiones:** solo cambia el generador de v5; se reutilizan los componentes existentes. No se libera la conexión ni se garantiza su cierre ante un error de `Fill`. Tampoco se añaden guardas nulas, valores nuevos, cambios de esquema o pruebas productivas. La [evidencia efectiva](../../../evidencia/semanas/semana09/compilacion_y_pruebas.json) distingue v4 con 4/6 y dos fallos esperados de liberación, v5 con 6/6 y regresión con 16/16. No se interpreta el rojo esperado como una falla de compilación o una fuga medida.

**Riesgo pendiente de integración:** el adaptador SQL conserva `SelectCommand` referenciando el comando ya dispuesto. Como `objDA` es público en la fachada v4, pueden existir consumidores no recuperados que necesiten esa referencia. Los métodos visibles vuelven a asignarla antes de `Fill`, sin que se haya ejecutado la ruta SQL o la interfaz. Debe comprobarse que los consumidores terminen su uso síncrono y no reutilicen después ese comando antes de adoptar v5 en el sistema completo. Fallos de adquisición y del propio `Dispose` quedan fuera de los seis escenarios. La aceptación local no acredita un reemplazo productivo.

## CAM-S09-002 · Validar argumentos nulos

- **Seguimiento:** [Issue #11](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/11).
- **Tipo y prioridad:** preventivo; media propuesta.
- **Origen comprobado:** el constructor del generador asigna directamente sus dependencias y `Preparar` utiliza la definición sin validaciones de entrada explícitas.
- **Cambio solicitado:** evaluar guardas `ArgumentNullException` para dependencias y definición, con nombres de parámetros y comportamiento documentados.
- **Motivo:** detectar contratos inválidos al entrar al componente y facilitar su diagnóstico.
- **Estado:** propuesta pendiente; **no implementada en C07**. Requiere una decisión específica antes de pasar a implementación.

Criterios propuestos: una dependencia inválida debe provocar el error temprano acordado; una definición nula no debe activar el ejecutor; las entradas válidas deben conservar sus resultados. Las pruebas deben fijar el tipo de excepción y el parámetro afectado, además de repetir los casos válidos.

**Impacto:** cambia intencionalmente el tipo o momento de los errores para entradas inválidas. Un consumidor podría depender del comportamiento anterior, por lo que deben evaluarse constructor, fachada, composición y pruebas antes de aprobarla. No se afirma que existan llamadas nulas en la operación real.

## CAM-S09-003 · Configurar el tiempo de espera del reporte

- **Seguimiento:** [Issue #12](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/12).
- **Tipo y prioridad:** perfectivo; baja propuesta.
- **Origen comprobado:** las definiciones preparan `SqlCommand` sin una opción de tiempo de espera definida por el contrato del reporte.
- **Cambio solicitado:** evaluar una configuración explícita de `CommandTimeout`, conservando el valor predeterminado actual cuando el consumidor no aporte una opción.
- **Motivo:** permitir ajustar el comportamiento del reporte de forma explícita sin editar repetidamente el núcleo.
- **Estado:** propuesta pendiente; **no implementada en C07**. La política de valores admitidos debe definirse antes de aprobarla.

Criterios propuestos: conservar el valor predeterminado compatible; aplicar una opción explícita al comando; documentar límites, tratamiento de valores inválidos y responsabilidades del consumidor. Las primeras pruebas pueden inspeccionar comandos preparados sin SQL. Comprobar el comportamiento de un tiempo de espera real requeriría después un entorno controlado de integración.

**Impacto:** afecta contrato/configuración y preparación de comandos. Un valor inadecuado puede interrumpir reportes válidos o prolongar una espera. Debe evaluarse si la opción pertenece a la definición o a una política de composición. No se presume un cambio del servidor ni se promete mayor rendimiento: cambiar el límite de espera no acelera una consulta.
