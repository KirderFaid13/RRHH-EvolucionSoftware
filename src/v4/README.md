# v4: IoC en la ejecución de reportes

Semana 07, contrato C05. La dependencia seleccionada es `GeneradorReportes` hacia `EjecutorReportesSql`: v3 crea el ejecutor dentro del constructor; v4 recibe un `IEjecutorReportes` y deja la creación SQL a `ComposicionReportes`. La fachada sigue usando sus referencias actuales `ObjCnn` y `objDA`.

| Archivo en `caso_ioc/` | Función |
| --- | --- |
| [GeneradorReportes.cs](caso_ioc/GeneradorReportes.cs) | Recibe el ejecutor por constructor; conserva `Preparar` y `Generar`. |
| [IEjecutorReportes.cs](caso_ioc/IEjecutorReportes.cs) | Contrato `DataSet Ejecutar(ComandoReporte reporte)`. |
| [EjecutorReportesSql.cs](caso_ioc/EjecutorReportesSql.cs) | Implementación SQL; conserva constructor y cuerpo de ejecución de v3. |
| [ComposicionReportes.cs](caso_ioc/ComposicionReportes.cs) | Crea el ejecutor SQL fuera del generador y lo entrega por constructor. |
| [RRHHClass.cs](caso_ioc/RRHHClass.cs) | Fachada acumulativa; cambia únicamente los dos cuerpos del caso de oficina para usar composición. |

Se reutilizan sin copiar cuatro fuentes de `src/v3/caso_reportes/`: `IDefinicionReporte`, `ReporteOficina`, `ReporteOficinaPorSigla` y `ComandoReporte`. También se conservan los dos helpers de empleados de `src/v2/caso_empleados/`. El [borrador recibido](antecedentes/README.md) queda separado y no participa en la biblioteca o pruebas activas.

## Reproducir las comprobaciones

Desde la raíz del repositorio, con Python, SDK .NET 10.0.103 y referencias Framework v4.0.30319 instaladas, clave privada local y legado ya restaurado:

```powershell
python herramientas/compilar_v4.py
python herramientas/verificar_v4.py
```

La biblioteca diagnóstica x86 combina 22 fuentes: 11 de v1 sin su fachada, dos helpers de empleados v2, las cuatro fuentes v3 reutilizadas y los cinco C# de `caso_ioc/`. El harness compila 10 fuentes: ocho componentes escritos para reportes, [PruebasIoC.cs](pruebas/PruebasIoC.cs) y las llamadas generadas desde los contratos v1 en `ContratosRecuperados.cs`. La fachada y los ensamblados recibidos no se ejecutan. Los artefactos diagnósticos y el archivo generado quedan en `.local/c05/`, ignorada por Git.

La [ejecución registrada](../../evidencia/semanas/semana07/README.md) muestra ambas compilaciones sin errores ni advertencias y 16 escenarios aprobados con salida 0: once contratos mediante `Generar` con sustituto y cinco comprobaciones de sustitución, preparación, errores y composición sin abrir SQL. La verificación registra `ok: true`, ocho antecedentes conservados y etapas anteriores intactas. Los datos devueltos en pruebas son sintéticos.

El constructor público de `GeneradorReportes` cambia a `(SqlConnection, IEjecutorReportes)`. Las firmas originales de la fachada se conservan. El punto desacoplado es la ejecución mediante una clase propia: conexión y comandos `SqlClient` permanecen concretos. Se conserva la ruta SQL normal, sin incorporar contenedor, `using`, `finally`, validaciones o cambios de reglas. SQL, `Fill`, UI, despliegue, framework original y equivalencia completa permanecen sin ejecución comprobada.

La entrega C05 se incorpora desde la rama `semana-07-ioc` mediante PR hacia `main` y squash, conservando un único commit de esta etapa en la línea principal. [Contrato](../../specs/c05_ioc.json), [informe antes/después](../../docs/semanas/semana07/01_ioc.md), [guion de exposición](../../docs/semanas/semana07/02_guion_exposicion.md), [presentación local](../../docs/semanas/semana07/Semana07_IoC_RRHH.pptx) y [prompt de revisión](../../prompts/04_ioc.md).
