# C04: reproducir y revisar el caso OCP de oficina

Este prompt revisa la implementación actual del cuarto commit; no solicita regenerar v3 ni avanzar a semana 07. [Contrato C04](../specs/c04_ocp.json) e [informe](../docs/semanas/semana05/01_ocp.md).

```text
Actúa como responsable de revisión del caso C04 del sistema RRHH.

Lee AGENTS.md, README.md, .context/ROADMAP.md, el contexto funcional
y del curso, specs/c04_ocp.json, src/v3/README.md y las evidencias de
evidencia/semanas/semana05/. Revisa los siete C# de
src/v3/caso_reportes/ y los dos helpers reutilizados desde v2.

Objetivo:
Reproducir y contrastar la implementación OCP existente, separando
conservación de fuentes, compilación, preparación de comandos y lo
que permanece sin ejecución SQL. No reemplazarla por otra propuesta.

Trabajo:
1. Contrasta contratos_v1.json con la fuente y sus hashes. Confirma
   object Generar_Report_oficina(int CodOficina): DataSet,
   spRRHH_Report_Oficina_Unico/@idarea Int y tabla homónima; y
   object Generar_Report_oficina_Dep(string Sigla): DataSet,
   spRRHH_Report_Oficina/@sigla VarChar y tabla homónima.
2. Revisa el diff v2/v3 y confirma que solo cambian los dos cuerpos;
   firmas, resto de fachada y helpers v2 se conservan. No edites
   v1/v2, legado ni antecedentes recibidos para hacer pasar pruebas.
3. Comprueba que GeneradorReportes usa IDefinicionReporte sin
   seleccionar clases concretas. Explica que una nueva definición
   y su composición cambian, mientras el consumidor se mantiene.
4. Con clave local, legado restaurado, Python, SDK 10.0.103 y
   referencias Framework instaladas, ejecuta desde la raíz:
   python herramientas/compilar_v3.py
   python herramientas/verificar_v3.py
   No conectes SQL, restaures bases ni ejecutes binarios recibidos.
5. Contrasta los resultados actuales: biblioteca acumulativa de
   20 fuentes; núcleo de cinco con ReporteOficina; PorSigla como
   DLL externa de una fuente; harness de una fuente y 11 escenarios.
   Confirma hashes de DLL y fuentes del núcleo intactos, sin
   recompilarlo para la extensión, y 18 antecedentes preservados.
   La compilación aparte de 17 C# recibidos no acredita sus contratos.
6. Revisa qué prueba el harness: Preparar, SP/tipo de comando,
   parámetro/tipo/dirección/tamaño/valor, conexión cerrada, adaptador
   sin modificación y nombre de tabla. No ejecuta Generar/Fill,
   RRHHClass ni GRLL. Si falla, informa el fallo real y su alcance;
   no reutilices una evidencia anterior como resultado actual.

Límites:
- No inventes SP, columnas, roles, reglas, resultados ni equivalencia.
- No introduzcas defaults, normalizaciones, DBNull, validaciones o
  cambios de ciclo de conexión como parte de esta revisión OCP.
- DataSet/Fill/apertura/cierre se contrastan por fuente y compilación,
  no por SQL. Preparar ocurre antes de Open; no se acredita
  equivalencia de todos los fallos, UI, despliegue o framework original.
- Mantén claves, configuraciones reales y diagnósticos en .local/;
  no muestres ni incorpores secretos a documentación o Git.
- No cambies new EjecutorReportesSql por abstracción/inyección:
  IoC, semana 07 y sus diapositivas siguen pendientes de autorización.
- No regeneres código, amplíes reportes/importadores ni publiques
  commits en esta reproducción sin una instrucción expresa del equipo.

Entrega:
Explica qué cambió, dónde, por qué y qué aporta OCP; cita evidencia
actual, indica fallos o límites pendientes y detén el trabajo en C04.
```
