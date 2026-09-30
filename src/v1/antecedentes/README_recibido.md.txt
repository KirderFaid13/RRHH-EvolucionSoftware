# v1.0 - Sistema Original (Línea Base)

## Descripción
Reconstrucción del código fuente original del sistema RRHH mediante ingeniería inversa de los binarios compilados (RecursosHumanos.exe, ClassRRHH.dll, GRLL.dll, Seguridad.dll).

## Archivos
- `src/ClassRRHH_Original.vb` — Clase principal de acceso a datos (reconstruida). Contiene todos los métodos del sistema en una sola clase.
- `src/frmPrincipal_Original.vb` — Formulario principal (reconstruido). Muestra cómo los event handlers contienen lógica de negocio.

## Problemas Identificados
Los comentarios en el código marcan las violaciones a SRP, DRY y OCP detectadas.

## Nota
Estos archivos son reconstrucciones basadas en el análisis de strings, metadatos XML y estructura de los binarios compilados. Representan la arquitectura y lógica del sistema original de forma fiel.
