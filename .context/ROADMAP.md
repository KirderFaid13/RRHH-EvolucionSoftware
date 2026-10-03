# Roadmap del RRHH original a sus mejoras

Este roadmap establece el orden de incorporación al repositorio. C01 conserva el original, C02 recupera una base parcial verificable, C03 refactoriza tres consultas mediante SRP/DRY y C04 crea un punto de extensión para reportes. La publicación se confirma con el resultado de Git, no por la existencia de este archivo.

| Etapa | Objetivo | Estado de esta revisión | Evidencia de cierre |
| --- | --- | --- | --- |
| C01 | Incorporar RRHH original y estructura organizada. | Publicado en e1ead41; contenido preservado. | Inventarios y comprobaciones en evidencia/baseline/. |
| C02 | Ingeniería inversa y v1. | Publicado en 9e18ca4; recuperación parcial y compilación diagnóstica. | Evidencia/ingenieria_inversa/: informe, metadatos, hashes y contratos. Equivalencia funcional y esquema SQL pendientes. |
| C03 | v2: única responsabilidad y DRY. | Publicado en a5849d9; tres consultas extraídas, ejecución común centralizada y 11 escenarios aprobados sin SQL. | docs/semanas/semana04/ y evidencia/semanas/semana04/: contratos, diff, compilación, pruebas y conservación del resto. Integración real pendiente. |
| C04 | v3: abierto/cerrado. | Publicado en 7bd215a; dos definiciones, biblioteca acumulativa compilada y 11 escenarios de preparación aprobados sin recompilar núcleo al añadir variante. | docs/semanas/semana05/ y evidencia/semanas/semana05/: contratos, diff y hashes. Fill/SQL e integración real pendientes. |
| C05/S07 | Mejora puntual mediante inversión de control. | Entrega v4 implementada y comprobada: 22 fuentes compiladas, 16 escenarios con sustitutos. Incorporación autorizada por PR desde semana-07-ioc y squash como quinto commit de main. | docs/semanas/semana07/ y evidencia/semanas/semana07/: dependencia antes/después, composición manual, pruebas de Generar y exposición centrada en IoC. El resultado de publicación se verifica en Git; SQL real pendiente. |
| S08-S16 | Gestión de configuración, cambios, versiones y cierre del curso. | Pendiente de las consignas de cada semana. | Entregables definidos por el docente y registros verificables del trabajo. |

## Forma de avanzar

1. Leer el [README del repositorio](../README.md), el [contexto funcional](01_business_rules.md), el [diccionario de datos](02_data_dictionary.json) y el [contexto del curso](03_course_context.md).
2. Seleccionar únicamente la etapa autorizada por el equipo.
3. Definir su alcance y sus comprobaciones antes de modificar el código.
4. Mantener la entrega original separada del código recuperado y del código modificado.
5. Documentar qué cambió, dónde, por qué y cómo se verificó. Señalar los puntos pendientes.
6. Preparar un commit descriptivo de esa etapa y verificar el resultado de su publicación.
7. Detenerse después del commit y esperar la indicación para la etapa siguiente.

El [contrato C03](../specs/c03_srp_dry.json) delimita tres consultas reales y el [contrato C04](../specs/c04_ocp.json) delimita las definiciones extensibles de dos reportes. El [contrato C05/S07](../specs/c05_ioc.json) desacopla al generador de la ejecución: recibe interfaz y la composición externa crea SQL. Después de revisar la preparación, el equipo autorizó crear y subir el quinto commit, abrir PR e integrarlo en main mediante squash. Se detiene el avance después de explicar esta etapa.
