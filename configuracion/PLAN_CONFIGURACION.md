# Plan inicial de gestión de configuración

**Ámbito:** RRHH académico, preparación C06/S08 del 5 de octubre de 2026. Este plan aplica desde esta preparación; no afirma que todas sus reglas se siguieran antes.

## Base y componentes

La referencia congelada es C05, commit `6d82f9fa6aa608a0d7d71c14fb2fc661e9d21fa2`, árbol `a6b85aad0d6ab119297cd4ffd37c8ef5421a383e`, con 531 archivos versionados. El [inventario](inventario_c05.json) identifica archivos con ruta, tamaño, SHA-256 y objeto Git. Los [elementos](elementos.json) agrupan componentes por tipo, ubicación, procedencia, estado y política de almacenamiento.

La base no es una entrega de producción: v4 es diagnóstica y su funcionamiento completo está pendiente. C06 añade controles, documentación y herramientas; conserva el código y el material de etapas anteriores.

## Responsabilidades y coordinación

| Función | Responsabilidad |
| --- | --- |
| Autor del cambio | Registrar motivo y alcance, anunciar rutas, preparar cambios, documentación y comprobaciones. |
| KirderFaid13 | Revisar alcance, diferencia, resultados y límites; decidir e integrar. El usuario confirmó estas funciones. |
| Equipo | Consultar el registro, coordinar archivos compartidos y evitar ediciones simultáneas sin acuerdo. |

Los autores concretos de próximas tareas se registrarán cuando se asignen. Si KirderFaid13 también es autor, una lectura de otro integrante es recomendable; no se presume que exista un revisor adicional.

## Control de versiones

- Herramienta: Git. Alojamiento: [GitHub RRHH-EvolucionSoftware](https://github.com/KirderFaid13/RRHH-EvolucionSoftware), público por decisión del responsable.
- `main` conserva entregas integradas; una rama por semana delimita el trabajo. C06 usa `semana-08-gcs` desde C05.
- Se versionan archivos permitidos por el contrato y sin secretos. `.local/`, claves, configuraciones restauradas, respaldo SQL y compilados generados permanecen excluidos.
- Se revisan estado y diferencia antes de agregar archivos. No se fuerza la inclusión de material ignorado ni se reescriben commits publicados para simular entregas antiguas.
- Una solicitud de cambios describe problema, solución, motivo, pruebas y límites. La integración semanal puede usar squash, conservando un commit por etapa en `main`.
- No se presume protección de ramas ni CI. Su configuración sería una acción posterior acordada, con evidencia propia.

## Control de cambios

Los cambios relevantes se registran en [cambios.json](cambios.json) con ID, fecha real, origen, motivo, rutas, alcance, riesgos, validaciones, responsable de revisión y estado de integración.

1. Registrar la solicitud y su autorización de preparación.
2. Coordinar responsables y rutas antes de editar; resolver solapamientos con KirderFaid13.
3. Preparar exclusivamente el alcance aprobado por el contrato.
4. Adjuntar diferencia, informe, comprobaciones y límites.
5. KirderFaid13 revisa. Una preparación autorizada no implica una revisión aprobada.
6. Tras la indicación de incorporación, crear el commit descriptivo, subir la rama y abrir PR hacia `main`.
7. Integrar cuando el responsable lo autorice y verificar commit, árbol y archivos publicados.
8. Explicar el resultado y detenerse hasta la siguiente etapa.

`CAM-S08-001` registra la preparación inicial y la indicación posterior del responsable para incorporar C06. Commit, PR e integración se verifican en GitHub; esta autorización no fabrica revisiones históricas de C01–C05.

## Estado y auditoría

La auditoría compara el inventario congelado con los archivos de trabajo, separa cambios base permitidos de diferencias no autorizadas e identifica archivos nuevos dentro o fuera de C06. Rechaza rutas fuera del repositorio e inventarios alterados. Comprueba las exclusiones de Git sin mostrar contenidos privados.

```powershell
python herramientas/auditar_configuracion.py
python herramientas/verificar_configuracion.py
```

El [resultado de auditoría](../evidencia/semanas/semana08/auditoria_configuracion.json) describe el momento de preparación; no certifica una publicación posterior. Las pruebas usan muestras temporales, sin modificar originales reales. Después de cambios adicionales se repiten las comprobaciones afectadas.

La comparación de hashes cubre archivos de trabajo. Antes de crear el commit se revisarán `git diff --cached` y las exclusiones/conservación del índice con el procedimiento disponible de baseline. Un PASS local no certifica los blobs agregados ni el árbol de una publicación futura. El respaldo SQL real permanece fuera del repositorio activo en el workspace del responsable; las rutas BAK utilizadas por el auditor son muestras hipotéticas para comprobar reglas de exclusión.

La configuración preparada se acepta para revisión cuando no hay diferencias fuera de alcance, documentación y contratos son coherentes y las evidencias declaran su límite. El cierre de publicación necesita una comprobación independiente del commit y árbol integrados; no se inserta por anticipado un hash de C06.

## Conservación y recuperación

Los originales de `legado/RRHH/` y las etapas anteriores se conservan. Git permite consultar la versión publicada sin borrar o sobrescribir el trabajo local. Antes de recuperar un archivo, se revisa su diferencia y se conserva cualquier trabajo necesario; este plan no prescribe resets destructivos.

La clave del material cifrado se obtiene del responsable por un medio privado. La documentación de restauración no convierte la ejecución del programa ni la restauración SQL en acciones autorizadas para esta práctica. Inventario, integridad y pruebas aisladas tampoco demuestran equivalencia completa.

Fundamento: [SWEBOK, gestión de configuración](https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics), [Git: control de versiones](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control) y [GitHub: solicitudes de cambios](https://docs.github.com/en/pull-requests/get-started/about-pull-requests).
