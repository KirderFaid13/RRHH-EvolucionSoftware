# Roadmap del RRHH original a sus mejoras

Este roadmap establece el orden de incorporación al repositorio. C01 conserva el original, C02 recupera una base parcial verificable y C03 refactoriza tres consultas mediante SRP/DRY. La publicación se confirma con el resultado de Git, no por la existencia de este archivo.

| Etapa | Objetivo | Estado de esta revisión | Evidencia de cierre |
| --- | --- | --- | --- |
| C01 | Incorporar RRHH original y estructura organizada. | Publicado en e1ead41; contenido preservado. | Inventarios y comprobaciones en evidencia/baseline/. |
| C02 | Ingeniería inversa y v1. | Publicado en 9e18ca4; recuperación parcial y compilación diagnóstica. | Evidencia/ingenieria_inversa/: informe, metadatos, hashes y contratos. Equivalencia funcional y esquema SQL pendientes. |
| C03 | v2: única responsabilidad y DRY. | Contenido de esta revisión: tres consultas extraídas, ejecución común centralizada, biblioteca compilada y 11 escenarios aprobados sin abrir SQL. | docs/semanas/semana04/ y evidencia/semanas/semana04/: contratos, diff, compilación, pruebas y conservación del resto. Integración real pendiente. |
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

El [contrato C03](../specs/c03_srp_dry.json) delimita la mejora de tres consultas reales. C04/v3 permanece pendiente de indicación y de su contrato; no se incorporó OCP ni la entrega IoC de semana 07.
