# v2: SRP y DRY en consultas de empleados

Tercer commit, semana 04. La mejora parte de tres métodos reales de la v1 recuperada: `ObtenerEmpleados`, `BuscarEmpleado_Codigo` y `spRRHH_ListarTrabajadores`. Sus firmas públicas se mantienen en `RRHHClass`.

- `caso_empleados/RRHHClass.cs`: misma fachada de v1, con los tres métodos delegados. El resto del código se conserva.
- `caso_empleados/EmpleadoConsultas.cs`: define las tres consultas y sus parámetros. Cambia cuando se modifica ese contrato de consulta.
- `caso_empleados/EjecutorConsultasSql.cs`: reúne construcción de comandos y ejecución ADO.NET compartida. Cambia cuando se modifica esa mecánica.
- [antecedentes](antecedentes/README.md): propuesta v2 anterior intacta; no participa en la compilación activa.

El código usa clases concretas. No se incorporan interfaces, contenedores ni la entrega OCP/IoC. Se pasan las referencias ADO.NET existentes para conservar su uso; la selección de clases permanece fija. La refactorización es parcial: otros métodos de `RRHHClass` siguen gestionando consultas directamente.

## Compilar y comprobar

Con Python, SDK .NET 10.0.103, referencias Framework instaladas y la clave local del primer commit:

```powershell
python herramientas/restaurar_legado.py
python herramientas/compilar_v2.py
python herramientas/verificar_v2.py
```

La herramienta restaura v1 en privado, usa sus once fuentes no sustituidas y añade los tres C# del caso: 14 fuentes en una biblioteca x86. Ejecuta un harness del código nuevo que construye comandos y los compara con contratos extraídos de v1; no abre conexiones. Los antecedentes se compilan aparte para registrar sus defectos, sin corregirlos ni ejecutarlos.

No hay un ejecutable nuevo ni se reemplaza la DLL de `legado/`. La compilación utiliza referencias Framework4 y no verifica el framework original, UI, despliegue, resultados SQL ni equivalencia funcional completa. [Informe antes/después](../../docs/semanas/semana04/01_srp_dry.md) y [evidencias](../../evidencia/semanas/semana04/README.md).
