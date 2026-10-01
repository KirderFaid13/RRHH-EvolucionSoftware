# v3: OCP en definiciones de reportes de oficina

Cuarto commit, semana 05. La fachada parte de v2 y sustituye únicamente los cuerpos de `Generar_Report_oficina(int)` y `Generar_Report_oficina_Dep(string)`. Conserva sus firmas `object`, con `DataSet` en la ruta de ejecución, y los contratos observados en v1. La variante por sigla ya existía: se incorpora como segunda definición al consumidor OCP, sin añadir una funcionalidad empresarial nueva.

| Archivo en `caso_reportes/` | Función |
| --- | --- |
| `RRHHClass.cs` | Fachada acumulativa con las dos delegaciones del caso C04. |
| `IDefinicionReporte.cs` | Punto de extensión: nombre de tabla y construcción del comando. |
| `ReporteOficina.cs` | `spRRHH_Report_Oficina_Unico`, `@idarea` de tipo `Int`. |
| `ReporteOficinaPorSigla.cs` | Extensión real: `spRRHH_Report_Oficina`, `@sigla` de tipo `VarChar`. |
| `GeneradorReportes.cs` | Prepara o ejecuta cualquier definición de la interfaz sin seleccionar clases concretas. |
| `ComandoReporte.cs` | Mantiene juntos el comando y el nombre suministrado a `Fill`. |
| `EjecutorReportesSql.cs` | Mecánica concreta de `DataSet`, apertura/cierre y adaptador compartido. |

Los dos helpers de empleados se reutilizan desde `src/v2/caso_empleados/`, sin copiarlos ni cambiar v2. La [propuesta recibida](antecedentes/README.md) se preserva separadamente; no participa en la biblioteca activa.

## Reproducir las comprobaciones

Desde la raíz del repositorio, con Python, SDK .NET 10.0.103, referencias Framework instaladas, clave local y legado ya restaurado:

```powershell
python herramientas/compilar_v3.py
python herramientas/verificar_v3.py
```

La herramienta restaura las fuentes v1 en privado y compila una biblioteca x86 de 20 fuentes: 11 de v1 sin su fachada, dos helpers de v2 y los siete C# de v3. Compila los antecedentes aparte, sin ejecutarlos. Después compila un núcleo de cinco fuentes, la definición por sigla como DLL externa y un harness que prepara comandos con ambas implementaciones.

La ejecución registrada aprueba 11 escenarios y verifica que la DLL y las fuentes del núcleo permanecen intactas sin recompilarlo al incorporar la extensión. Solo se ejecuta preparación de comandos nuevos, con conexión cerrada; `Generar`, `Fill`, la fachada y los ensamblados recibidos no se ejecutan. Los artefactos diagnósticos quedan en `.local/c04/`, ignorada por Git.

El consumidor es estable frente a esta variante; agregar la definición y seleccionarla en la composición requiere cambios. `new EjecutorReportesSql` mantiene una dependencia concreta para la futura etapa IoC. No se despliega ni reemplaza la DLL del legado, ni se acredita SQL, UI, framework original o equivalencia completa. [Contrato](../../specs/c04_ocp.json), [informe antes/después](../../docs/semanas/semana05/01_ocp.md) y [evidencias](../../evidencia/semanas/semana05/README.md).
