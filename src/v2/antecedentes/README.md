# Propuesta v2 anterior, conservada como antecedente

Se preservan ocho archivos recibidos: siete C# y el README anterior, renombrado `README_recibido.md.txt`. Sus bytes se cotejan con [antecedentes.json](../../../evidencia/semanas/semana04/antecedentes.json).

Esta propuesta separaba modelos, repositorios, un helper y un importador. Su compilación original falla con ocho `CS0246`: falta `using System` en modelos que utilizan `DateTime` y `TimeSpan`. Estos archivos permanecen sin editar para documentar el estado recibido.

La comparación con v1 recuperada identifica cambios de contrato: reemplaza la consulta textual de empleados por un procedimiento; buscar por código cambia `int/@codigo` por `string/@CodigoEmpleado` y otro procedimiento; simplifica inserción y actualización de área; el importador supone `Marcaciones` y columnas que no corresponden a las consultas recuperadas.

Sus comentarios y métricas son afirmaciones históricas, no conclusiones de esta entrega. No se sostiene que los cuatro importadores fueran idénticos ni que estuvieran en una única clase original. No compilar estos archivos junto con el caso activo.

La v2 verificable del tercer commit está en [caso_empleados](../README.md). Conserva tres contratos reales y delimita el alcance de SRP/DRY. [Auditoría y decisión](../../../docs/semanas/semana04/01_srp_dry.md).
