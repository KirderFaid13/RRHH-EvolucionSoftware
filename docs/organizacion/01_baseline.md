# Commit 1: RRHH original y estructura organizada

## Punto de partida

El material del proyecto estaba mezclado: distribución del programa, documentos del curso, propuestas de versiones y evidencias. Se necesita una referencia original identificable para explicar posteriormente qué se recuperó, qué se modificó y por qué.

Este primer commit incorpora únicamente el paquete recibido de RRHH, su inventario, los documentos de referencia y la estructura de trabajo. Los análisis y versiones anteriores se conservan localmente para su incorporación y validación en los siguientes commits.

## Cambios y motivos

| Ubicación | Qué se incorpora | Para qué sirve |
| --- | --- | --- |
| `legado/RRHH/` | Paquete recibido, manteniendo estructura y contenido; 12 originales almacenados cifrados. | Conservar una referencia contra la que comparar el código recuperado y las mejoras. |
| `.context/` | Contexto del curso, información funcional pendiente, diccionario inicial vacío y roadmap. | Dar contexto común y evitar inventar reglas, roles o un esquema SQL. |
| `specs/` | Guía para definir tareas y criterios de aceptación. | Delimitar cada mejora antes de implementarla. |
| `src/` | Destino para fuentes recuperadas y mejoras; todavía sin implementación. | Distinguir el programa recibido del trabajo nuevo. |
| `referencias/` | Ocho PDF, ordenados por curso, semana y bibliografía. | Localizar las consignas y fuentes de consulta. |
| `docs/` | Guías de organización y Git; destinos para ingeniería inversa y semanas. | Explicar decisiones con una ruta de lectura para el equipo y revisores. |
| `evidencia/baseline/` | Inventarios con tamaño y SHA-256; registro de comprobaciones. | Comprobar que la copia conserva los originales y dejar explícitas las exclusiones. |
| `prompts/` | Instrucción delimitada para el siguiente paso de ingeniería inversa. | Mantener continuidad del trabajo sin anticipar las mejoras. |
| `herramientas/` | Verificación y restauración de originales cifrados. | Repetir las comprobaciones y recuperar los archivos sin modificarlos. |
| `.gitignore` y `.gitattributes` | Exclusiones locales y reglas para conservar bytes del legado. | Evitar versionar claves/datos y alteraciones por conversión de finales de línea. |

## Tratamiento del material sensible

La inspección necesaria para preparar el almacenamiento identificó credenciales en seis configuraciones y seis binarios. Excluir solo los archivos `.config` habría dejado contraseñas en los ejecutables y DLL. Se cifran los 12 archivos completos con AES-256-GCM; la clave de 32 bytes queda en `.local/`, fuera de Git. Cada archivo utiliza un nonce de 12 bytes y su ruta original como dato autenticado.

El cifrado no edita el programa ni su configuración. Descifrar y comparar el SHA-256 permite comprobar la conservación exacta del original. Las configuraciones de ejemplo son archivos nuevos y están identificadas como tales.

El BAK de 199.401.472 bytes queda fuera del repositorio. Su contenido no fue revisado y GitHub bloquea archivos de más de 100 MiB en Git normal. Su ruta, tamaño y hash permanecen en el inventario. [Documentación oficial del límite](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

## Qué mejora este paso

Mejora la organización y la trazabilidad del proyecto: el equipo puede localizar la referencia original, conocer las decisiones de almacenamiento y verificar su integridad antes de comparar una nueva versión. Cada cambio posterior tendrá una etapa y una evidencia identificables.

Todavía no cambia el funcionamiento, rendimiento, diseño interno ni mantenibilidad del código del RRHH. Tampoco representa la ingeniería inversa académica del segundo commit, la recuperación de fuentes o una refactorización.

## Comprobaciones y límites

Las comprobaciones de aceptación son: inventario de 348 originales; igualdad de los 335 archivos directos; autenticación y coincidencia de los 12 cifrados; identificación del BAK local; integridad de ocho PDF; JSON válido; enlaces internos resolubles; exclusión de la clave y de configuraciones originales en Git.

Los resultados se registran en [evidencia del baseline](../../evidencia/baseline/README.md). Se diferencia una comprobación de archivos de una prueba del programa: no se ejecutó RRHH, no se restauró CMI y no se comprobó equivalencia funcional.

## Siguiente paso, cuando el equipo lo indique

El segundo commit documentará la ingeniería inversa y definirá una v1 con procedencia y límites verificables. Consultar el [roadmap](../../.context/ROADMAP.md) y el [prompt preparado](../../prompts/01_ingenieria_inversa.md). La indicación del equipo se espera después de publicar y explicar este primer commit.
