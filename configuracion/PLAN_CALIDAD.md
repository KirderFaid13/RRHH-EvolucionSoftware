# Plan inicial de calidad de configuración

**Ámbito:** preparación C06/S08 del RRHH académico. Objetivo: entregar componentes identificables, cambios explicados y comprobaciones reproducibles con sus límites.

| Criterio | Control concreto | Evidencia de aceptación |
| --- | --- | --- |
| Procedencia | Distinguir original, recuperación parcial, antecedente, caso activo y propuesta. | Rutas e informes existentes; elementos e inventario C05. |
| Conservación | Mantener `src/`, `legado/`, antecedentes y evidencia previa sin cambios en C06. | Auditoría contra los 531 archivos de la base y contrato de alcance. |
| Trazabilidad | Vincular consigna, contrato, cambio, archivos, explicación y comprobación. | PDF semana 08 → C06-S08 → CAM-S08-001 → informe/planes → evidencia C06. |
| Coordinación | Anunciar alcance/rutas y revisar antes de integrar. | Registro de cambio y posterior revisión de KirderFaid13; revisión aún pendiente en preparación. |
| Reproducibilidad | Declarar comandos, dependencias y resultados sin ejecutar binarios recibidos ni SQL. | Auditor, verificador y repetición aislada de v4 con metadatos y códigos de salida. |
| Información permitida | Excluir claves, configuraciones restauradas, datos reales y compilados generados. | Comprobación de exclusiones y revisión de la diferencia; no publicar contenido privado. |
| Exactitud documental | Explicar qué, dónde, por qué, validación y límites; separar ejecutado de propuesto. | Informe, planes, registro y guion coherentes con los archivos de evidencia. |
| Calidad de exposición | Ocho diapositivas legibles, estructura lógica y guion breve; participación acordada por el equipo. | Renders revisados y registro de presentación. No se inventan nombres ni distribución de participación. |

## Revisión de la preparación

1. Leer el contrato y `CAM-S08-001`.
2. Revisar archivos base modificados y altas contra el alcance autorizado.
3. Comprobar integridad de la referencia y capacidad del auditor para detectar fallos con muestras temporales.
4. Consultar resultados de las pruebas aisladas y separar las validaciones futuras de SQL, interfaz, rendimiento y seguridad.
5. Revisar coherencia y legibilidad del informe, planes, presentación y guion.
6. KirderFaid13 registra su decisión. La autorización de preparación no se interpreta como aprobación de revisión ni publicación.

Después de una incorporación autorizada se verificará que el árbol integrado corresponda a lo revisado, que `main` tenga la nueva etapa y que no se hayan incluido archivos privados. Esta preparación no configura CI o protección de ramas ni acredita una auditoría de producción.

Los defectos se registran en el cambio con archivo, evidencia y corrección requerida. Tras una corrección se repiten solo las comprobaciones afectadas. No se altera una evidencia previa para aparentar un resultado nuevo.

Referencia de criterios académicos: [Semana08_EVO_TG.pdf](../referencias/semanas/semana08/Semana08_EVO_TG.pdf), página 17. El plan ofrece controles del equipo; no promete una calificación ni reemplaza la evaluación del docente.
