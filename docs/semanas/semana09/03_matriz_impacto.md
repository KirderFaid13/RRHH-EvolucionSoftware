# Matriz de cambios e impacto

**Base:** `6c13e74482563cc158c4329852753f7f1eb2effd`, v4 diagnóstica. **Fecha del registro:** 15 de octubre de 2026. Esta matriz evalúa las tres solicitudes exigidas por la consigna. Las prioridades son propuestas relativas a la práctica; no se inventan estimaciones de horas ni niveles de servicio.

| Solicitud / Issue | Tipo | Problema y cambio | Prioridad propuesta | Componentes y dependencias | Riesgo principal | Verificación prevista | Decisión de preparación |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CAM-S09-001 · [#10](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/10) | Correctivo | El comando creado por `Generar` no se libera explícitamente; envolverlo en `using`. | Alta en esta práctica | Nuevo generador v5; `ComandoReporte` v3; contrato síncrono `IEjecutorReportes` v4. | Liberar antes de que el ejecutor termine o afectar el resultado/error. | Espía de ciclo de vida, éxito, excepción, resultado y propiedad de `Preparar`; repetir los 16 escenarios previos. | Implementada y verificada localmente: 6/6 y regresión 16/16; PR/integración pendientes. |
| CAM-S09-002 · [#11](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/11) | Preventivo | Faltan guardas explícitas de argumentos; proponer fallo temprano documentado. | Media | Constructor, `Preparar`, fachada/composición y consumidores. | Cambiar el tipo o momento de las excepciones esperadas por consumidores. | Entradas nulas por parámetro, ausencia de llamada al ejecutor y regresión de entradas válidas. | Propuesta pendiente; no implementada. |
| CAM-S09-003 · [#12](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/12) | Perfectivo | Sin opción contractual de espera del reporte; proponer `CommandTimeout` configurable. | Baja | Contrato de configuración y definiciones/preparación de comandos; decidir dónde reside la política. | Límites inadecuados o configuración incompatible. | Predeterminado compatible, valor explícito y entradas inválidas; integración posterior para timeout real. | Propuesta pendiente; no implementada. |

## Impacto evaluado por solicitud

**CAM-S09-001:** el impacto de código queda acotado a `Generar` en una fuente nueva de v5. La secuencia preparar → ejecutar se conserva y se añade la liberación al salir. Depende de que el ejecutor síncrono termine de usar el comando antes de regresar. Deben comprobarse también el camino de error y la identidad del `DataSet`. El contrato de `Preparar`, las definiciones SQL y los componentes v1–v4 permanecen como referencia. No cambia esquema ni datos; no se ha medido una mejora de memoria o rendimiento del programa completo.

**CAM-S09-002:** el impacto es de contrato público, aunque el cambio de código pueda ser pequeño. Introducir `ArgumentNullException` puede anticipar una falla que antes ocurría en otro punto. Antes de aprobar se deben decidir los parámetros cubiertos y actualizar documentación y pruebas. No corresponde incluirla silenciosamente dentro de la corrección 001.

**CAM-S09-003:** el impacto afecta configuración y expectativas del consumidor. Se debe preservar el comportamiento predeterminado y distinguir un límite de espera de una optimización. La decisión necesita una política explícita para valores admitidos y una ruta de integración controlada; las pruebas de comando por sí solas no demuestran que un reporte real termine a tiempo.

## Qué se conserva y qué se verifica aparte

La revisión de conservación debe comparar los blobs de los archivos históricos contra la base, además de los hashes originales DOCX/PPTX/PDF. Compilar, aprobar pruebas aisladas y conservar bytes son comprobaciones distintas. SQL/CMI, interfaz, seguridad, rendimiento y equivalencia completa siguen sin comprobarse.

Esta matriz no sustituye el detalle de los [criterios de cada solicitud](02_solicitudes.md). La [evidencia S09](../../../evidencia/semanas/semana09/compilacion_y_pruebas.json) confirma los resultados locales de 001: v4 con 4/6 y dos fallos esperados, v5 con 6/6 y regresión con 16/16; todos los harness compilaron. 002 y 003 no tienen implementación ni pruebas ejecutadas. La publicación efectiva se consulta por separado en GitHub. El [registro JSON](../../../configuracion/solicitudes_semana09.json) permite relacionar solicitud, Issue, fuentes, decisión y futura integración.
