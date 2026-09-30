# Roadmap del RRHH original a sus mejoras

Este roadmap establece el orden de incorporación al repositorio. La primera etapa prepara la base; las demás permanecen pendientes hasta que se realice y documente su trabajo. La publicación se confirma con el resultado de Git, no por la existencia de este archivo.

| Etapa | Objetivo | Estado en el primer commit | Evidencia de cierre |
| --- | --- | --- | --- |
| C01 | Incorporar RRHH original y estructura organizada. | Contenido de esta revisión: baseline preservado y verificado. | Inventario de lo incorporado y excluido y comprobaciones de integridad en evidencia/baseline/. La publicación se confirma mediante Git. |
| C02 | Ingeniería inversa y v1. | Pendiente; requiere indicación del equipo para continuar. | Procedencia del código, hallazgos sustentados, arquitectura recuperada, limitaciones y comprobaciones efectuadas. |
| C03 | v2: única responsabilidad y DRY. | Pendiente; depende de una base identificada en C02. | Caso antes/después, responsabilidades separadas, duplicación tratada y verificación del alcance. |
| C04 | v3: abierto/cerrado. | Pendiente; depende del caso y la base seleccionados. | Punto de extensión, implementación del caso, explicación de lo conservado y verificaciones reales. |
| S07 | Mejora puntual mediante inversión de control. | Pendiente; fuera de los cuatro commits iniciales. | Dependencia directa identificada, mejora por abstracción e inyección, prueba pertinente y exposición breve. |
| S08-S16 | Gestión de configuración, cambios, versiones y cierre del curso. | Pendiente de las consignas de cada semana. | Entregables definidos por el docente y registros verificables del trabajo. |

## Forma de avanzar

1. Leer el [README del repositorio](../README.md), el [contexto funcional](01_business_rules.md), el [diccionario de datos](02_data_dictionary.json) y el [contexto del curso](03_course_context.md).
2. Seleccionar únicamente la etapa autorizada por el equipo.
3. Definir su alcance y sus comprobaciones antes de modificar el código.
4. Mantener la entrega original separada del código recuperado y del código modificado.
5. Documentar qué cambió, dónde, por qué y cómo se verificó. Señalar los puntos pendientes.
6. Preparar un commit descriptivo de esa etapa y verificar el resultado de su publicación.
7. Detenerse después del commit y esperar la indicación para la etapa siguiente.

El [prompt de ingeniería inversa](../prompts/01_ingenieria_inversa.md) queda preparado para C02. Tener ese prompt disponible no significa que el análisis ni la v1 ya estén realizados.
