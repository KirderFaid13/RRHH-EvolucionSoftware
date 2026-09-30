# Antecedente académico recibido

Estos archivos conservan el trabajo anterior del grupo para poder auditar su procedencia. **Son una reconstrucción parcial y esquemática; no son el código original recuperado del ejecutable ni una aplicación equivalente.** En esta etapa, la v1 de referencia corresponde a la [recuperación real de ClassRRHH.dll](../recuperado/), obtenida mediante descompilación.

## Contenido y procedencia

| Archivo conservado | Procedencia local anterior | SHA-256 |
| --- | --- | --- |
| [ClassRRHH_Original.vb](ClassRRHH_Original.vb) | `versiones/v1.0_Original/src/ClassRRHH_Original.vb` | `3257c4262e5f7164f1442b474a9b3bd96b65f377a31c229d0eada0e4acc10e4e` |
| [frmPrincipal_Original.vb](frmPrincipal_Original.vb) | `versiones/v1.0_Original/src/frmPrincipal_Original.vb` | `e8965ef46380592c4ea261225865212fd6d7ace4fc14baf33ab588b829134f0b` |
| [README recibido](README_recibido.md.txt) | `versiones/v1.0_Original/README.md` | `929256a459bfefe92b020fbf7dbe10e1defa101af9cb52cc6e10aac2735b0226` |

Los tres archivos mantienen los bytes recibidos. Solo cambia el nombre del README histórico, terminado en `.md.txt`, para distinguirlo de esta guía vigente. Los dos VB suman **525 líneas físicas: 408 y 117**, incluidos comentarios y líneas vacías. La búsqueda de las credenciales conocidas del paquete y de asignaciones `Password`/`Pwd` no encontró coincidencias en este antecedente.

## Diferencias comprobadas

1. El assembly real tiene `RRHHClass`, `AsistenciaAccess`, `FamiliaresClass` y `FichaSocialClass`. El antecedente concentra responsabilidades en una clase denominada `ClassRRHH` y omite `FamiliaresClass`. En el código recuperado, `CodigoEmpleado` y `Anio` son enteros; el antecedente los representa como cadenas.
2. Los cuatro `Access2Sql*` pertenecen a `AsistenciaAccess` y devuelven `bool`, con fechas inicial/final y el parámetro `forzar`. El antecedente los coloca en `ClassRRHH` como procedimientos sin argumentos.
3. La `FichaSocialClass` recuperada implementa `llenarFamiliares(int CodEmple)`; la del antecedente está vacía.
4. El tipo principal observado en el ejecutable es `RecursosHumanos.MainMDI`. El antecedente utiliza `frmPrincipal` y carece del diseñador y de las dependencias necesarias para reconstruir la interfaz.
5. Los metadatos del ejecutable contienen métodos `BackgroundWorker` en cinco formularios de importación. El ejemplo síncrono del antecedente no demuestra que todas las importaciones originales bloqueen la interfaz.
6. Los dos VB comienzan con comentarios `//`, incompatibles con VB, y no vienen acompañados por un proyecto ni un diseñador completo. **No incorporarlos a la compilación de la biblioteca recuperada ni compilarlos en lote como si fueran parte de ella.**
7. El antecedente deja incompletos parámetros de `Ingresa_Empleado`/`Actualiza_Empleado`, las consultas de `Generar_Ficha` y la carga inicial `CargarListas`. Los cuerpos recuperados permiten examinar información que esos fragmentos omiten.
8. El antecedente propone `Marcaciones`, campos simplificados y `spRRHH_InsertarMarcacion`. La importación recuperada utiliza consultas a `Asis_Norm`/`Marcacion` y construye llamadas a `SpRRHH_Asistencia_Import`/`SpRRHH_Marcacion_Import`. Son contratos observados en código, sujetos a comprobar en las bases reales.
9. El README histórico afirma fidelidad de arquitectura y lógica. Las discrepancias anteriores impiden sostener esa afirmación; conservar el texto sirve para explicar la corrección y su procedencia.

Contrastar con las clases recuperadas: [RRHHClass](../recuperado/ClassRRHH/RRHHClass.cs), [AsistenciaAccess](../recuperado/ClassRRHH/AsistenciaAccess.cs), [FamiliaresClass](../recuperado/ClassRRHH/FamiliaresClass.cs) y [FichaSocialClass](../recuperado/ClassRRHH/FichaSocialClass.cs). La [revisión documentada](../../../docs/ingenieria_inversa/04_revision_antecedente.md) y su [evidencia JSON](../../../evidencia/ingenieria_inversa/auditoria_antecedente.json) explican los límites y las comprobaciones.

## Uso permitido dentro del proyecto

Sirve como antecedente para estudiar decisiones anteriores y corregir explicaciones. Los próximos cambios se deben justificar contra una base identificada, indicando expresamente si se parte del código recuperado o del ejemplo académico. Conservarlo no acredita compilación, integración con el formulario real, conexión a CMI ni equivalencia funcional con RRHH.
