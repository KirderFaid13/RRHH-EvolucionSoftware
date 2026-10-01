# Propuesta v3 anterior, conservada como antecedente

Se preservan 18 archivos de `RRHH_Evolucion/archivo/preorganizacion/versiones/v3.0_Semana05_OCP/`: 17 C# y el README recibido, renombrado [README_recibido.md.txt](README_recibido.md.txt). El [inventario](../../../evidencia/semanas/semana05/antecedentes.json) registra procedencia, tamaño y SHA-256; la [verificación](../../../evidencia/semanas/semana05/verificacion_v3.json) confirma los 18 hashes. Los archivos recibidos permanecen sin editar.

Su compilación diagnóstica separada termina sin errores ni advertencias con Roslyn SDK 10.0.103 y referencias instaladas Framework4. Compilar no acredita equivalencia con el legado ni funcionamiento SQL; estas fuentes no participan en la biblioteca activa y no se ejecutan.

La comparación identifica diferencias de contrato:

- `ReporteOficina.Generar(params object[])` devuelve `DataTable`, permite omitir el argumento usando `0` y llama `spRRHH_Report_Oficina` con `@idOficina`. En v1, la variante por código devuelve `object` con `DataSet`, llama `spRRHH_Report_Oficina_Unico` con `@idarea` explícitamente `Int` y utiliza el nombre del procedimiento en `Fill`.
- La variante real por sigla, `spRRHH_Report_Oficina/@sigla VarChar`, no está representada en ese reporte. `DatabaseHelper` crea otra conexión en lugar de conservar la conexión/adaptador compartidos de la fachada.
- Los reportes de cumpleaños, cargos y profesión omiten los argumentos observados en v1: `@mes`, `@idCargo` y `@profesion`, respectivamente. Sus llamadas no acreditan preservación de los contratos.

Los comentarios y métricas del README recibido son afirmaciones históricas; no respaldan riesgo de regresión «nulo» ni equivalencia completa. Las interfaces y el registro de importadores muestran una idea de extensión, pero su presencia no valida los contratos del sistema real. C04 no incorpora esos importadores, modelos ni reportes.

La [v3 activa](../README.md) delimita dos reportes de oficina y demuestra la extensión por sigla mediante un ensamblado externo y un consumidor sin modificaciones. [Informe del caso](../../../docs/semanas/semana05/01_ocp.md).
