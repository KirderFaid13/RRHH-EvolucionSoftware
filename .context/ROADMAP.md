# Roadmap del RRHH original a sus mejoras

Este roadmap establece el orden de incorporación al repositorio. C01 conserva el original, C02 recupera una base parcial verificable, C03 refactoriza tres consultas mediante SRP/DRY y C04 crea un punto de extensión para reportes. La publicación se confirma con el resultado de Git, no por la existencia de este archivo.

| Etapa | Objetivo | Estado de esta revisión | Evidencia de cierre |
| --- | --- | --- | --- |
| C01 | Incorporar RRHH original y estructura organizada. | Publicado en e1ead41; contenido preservado. | Inventarios y comprobaciones en evidencia/baseline/. |
| C02 | Ingeniería inversa y v1. | Publicado en 9e18ca4; recuperación parcial y compilación diagnóstica. | Evidencia/ingenieria_inversa/: informe, metadatos, hashes y contratos. Equivalencia funcional y esquema SQL pendientes. |
| C03 | v2: única responsabilidad y DRY. | Publicado en a5849d9; tres consultas extraídas, ejecución común centralizada y 11 escenarios aprobados sin SQL. | docs/semanas/semana04/ y evidencia/semanas/semana04/: contratos, diff, compilación, pruebas y conservación del resto. Integración real pendiente. |
| C04 | v3: abierto/cerrado. | Contenido de esta revisión: dos definiciones de reporte, biblioteca acumulativa de 20 fuentes compilada, núcleo conservado al añadir variante externa y 11 escenarios aprobados. | docs/semanas/semana05/ y evidencia/semanas/semana05/: contratos, diff, hashes del núcleo, compilación separada y preparación de comandos. Fill/SQL e integración real pendientes. |
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

El [contrato C03](../specs/c03_srp_dry.json) delimita tres consultas reales y el [contrato C04](../specs/c04_ocp.json) delimita las definiciones extensibles de dos reportes. La interfaz de reporte permite variar su contrato; el generador sigue creando un ejecutor SQL concreto. La entrega IoC de semana 07 permanece pendiente de indicación.
