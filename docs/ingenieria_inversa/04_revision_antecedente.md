# Revisión del antecedente académico v1

El trabajo previo llamado `v1.0_Original` incluía dos archivos VB reconstruidos a partir de indicios y una descripción que afirmaba fidelidad al sistema. La ingeniería inversa de esta etapa permite corregir esa descripción: el antecedente simplifica clases, firmas, consultas e interfaz. **La base v1 incorporada en C02 es la fuente recuperada de `ClassRRHH.dll`; el antecedente se conserva por separado y no forma parte de su compilación.**

## Qué se conserva y qué cambia

Se incorporan los dos VB y el README anterior en [src/v1/antecedentes/](../../src/v1/antecedentes/). Sus bytes permanecen iguales al material recibido; sus hashes quedan en [auditoria_antecedente.json](../../evidencia/ingenieria_inversa/auditoria_antecedente.json). El README anterior se llama `README_recibido.md.txt` y la guía vigente explica su condición. Esto permite revisar el trabajo del grupo sin convertir una afirmación anterior en un resultado verificado.

La recuperación de la DLL se mantiene en [src/v1/recuperado/](../../src/v1/recuperado/). El código C# allí representa la descompilación de un assembly; no demuestra la recuperación de los archivos VB originales utilizados en 2008 ni de todo el diseñador de Windows Forms.

## Comparación con evidencia

| Hallazgo | Antecedente recibido | Código o metadatos contrastados | Consecuencia para la documentación |
| --- | --- | --- | --- |
| A01. Clases y estado | Clase `ClassRRHH` con responsabilidades agrupadas; propiedades de código y año como `String`; sin `FamiliaresClass`. | [RRHHClass.cs](../../src/v1/recuperado/ClassRRHH/RRHHClass.cs), [AsistenciaAccess.cs](../../src/v1/recuperado/ClassRRHH/AsistenciaAccess.cs), [FamiliaresClass.cs](../../src/v1/recuperado/ClassRRHH/FamiliaresClass.cs) y [FichaSocialClass.cs](../../src/v1/recuperado/ClassRRHH/FichaSocialClass.cs). `CodigoEmpleado` y `Anio` son `int`. | Diferenciar el nombre del assembly y namespace de sus clases; conservar tipos y responsabilidades al delimitar cambios. |
| A02. Importadores | Cuatro `Sub Access2Sql*()` sin parámetros en `ClassRRHH`, líneas 206, 232, 256 y 280. | `AsistenciaAccess` implementa los cuatro métodos como `bool`, con fechas inicial/final y `int forzar`. | La separación de las importaciones ya existía en la DLL; no atribuir esa extracción a una refactorización posterior del sistema original. |
| A03. Familiares de ficha | `FichaSocialClass` vacía, línea 405. | `FichaSocialClass.llenarFamiliares(int CodEmple)` ejecuta una consulta con `@idempleado`. | La reconstrucción omitía una operación existente; no declarar recuperación completa. |
| A04. Interfaz principal | `frmPrincipal`, sin diseñador completo ni proyecto de la aplicación. | Los metadatos del ejecutable identifican `RecursosHumanos.MainMDI`. | El formulario académico no es el formulario original recuperado; integración y experiencia real siguen pendientes. |
| A05. Trabajo en segundo plano | Eventos de importación esquemáticos que llaman directamente al importador. | Cinco tipos `FrmImportarAsistencia*` contienen métodos `BackgroundWorker1_DoWork` y `BackgroundWorker1_RunWorkerCompleted`. | No concluir un bloqueo general de interfaz a partir del ejemplo; el comportamiento necesita observación y revisión de cuerpos. |
| A06. Compilación del antecedente | Cabeceras `//` en líneas 1-15 y 1-7 de los VB y dependencias incompletas. | Inspección directa de los dos archivos, 408 y 117 líneas. | No incluirlos en la compilación de la biblioteca recuperada; no afirmar que son un proyecto ejecutable. |
| A07. Cuerpos y firmas incompletos | Parámetros omitidos en `Ingresa_Empleado`/`Actualiza_Empleado`, líneas 101/111; `Generar_Ficha` esquemático, línea 345; `CargarListas` vacío, línea 113 del formulario. | Los métodos de `RRHHClass` recuperados incluyen firmas y cuerpos inspeccionables. | Un nombre coincidente no demuestra parámetros, efectos ni equivalencia del flujo. |
| A08. Contratos de importación | Tabla `Marcaciones`, campos simplificados y `spRRHH_InsertarMarcacion`. | `AsistenciaAccess` consulta `Asis_Norm` y `Marcacion`; construye comandos `Exec SpRRHH_Asistencia_Import` y `Exec SpRRHH_Marcacion_Import`. | Registrar los contratos de llamada observados; confirmar después tipos, claves y procedimientos en Access/CMI. |
| A09. Afirmación de fidelidad | El README anterior describe arquitectura y lógica fieles al sistema. | Discrepancias A01-A08 y ausencia de pruebas de equivalencia del antecedente. | La guía vigente lo clasifica como reconstrucción académica parcial; conserva el texto anterior para trazabilidad. |

Los cuerpos descompilados aportan más información que una búsqueda de nombres o cadenas. Por ejemplo, permiten distinguir dónde vive un método, qué argumentos recibe y cómo construye comandos. Los nombres SQL recuperados describen **lo que el cliente intenta consultar o ejecutar**. No demuestran por sí solos el esquema físico instalado, la firma efectiva de un procedimiento, sus restricciones ni los datos que contiene.

## Relación con lo solicitado en el curso

Se inventariaron **ocho PDF, 119 páginas**, con ruta y SHA-256; entre ellos no hay una consigna independiente de semana 03. El [sílabo](../../referencias/curso/Silabo%20del%20curso.pdf), página 2, sitúa ingeniería inversa en esa semana. El [proyecto final](../../referencias/curso/Proyecto%20Final_Legado.pdf), página 6, pide analizar el legado y conservar el ejecutable como referencia de la nueva solución; la página 8 pide reconstruir funciones, flujos, actores, reglas visibles y limitaciones. La página 10 establece documentación, pruebas y demostración funcional para la evaluación final.

Esta revisión contribuye a comprender y documentar el sistema. La observación de los flujos reales, los permisos de cada actor, las reglas completas y la validación de Access/CMI permanecen pendientes. Las referencias del curso orientan esas tareas; no convierten los supuestos del antecedente en hechos comprobados.

## Cómo se comprobó y por qué mejora el trabajo

Se compararon SHA-256 de los tres antecedentes con sus copias públicas y se contrastó la arquitectura con metadatos cuyo hash coincide con los binarios locales. Las firmas y consultas indicadas se cotejaron con las cuatro clases descompiladas. Se revisaron las páginas pertinentes del sílabo y del proyecto final mediante extracción y visualización; los documentos originales no se modificaron.

La búsqueda de credenciales conocidas y asignaciones `Password`/`Pwd` no encontró coincidencias en el antecedente. El diagnóstico anterior contenía una credencial, por lo que sus bytes no se incorporan como documentación pública de esta etapa.

La mejora es de conocimiento y trazabilidad: evita diseñar cambios sobre una arquitectura atribuida erróneamente y facilita justificar un caso concreto con evidencia. **Todavía no cambia el comportamiento del ejecutable original ni acredita equivalencia funcional de la biblioteca recuperada.**
