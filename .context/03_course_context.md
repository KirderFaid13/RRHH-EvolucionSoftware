# Contexto del curso y secuencia del repositorio

## Proyecto académico

Curso: **Evolución y Configuración de Software**. El equipo debe aplicar ingeniería inversa, refactorización y evolución a un sistema de Recursos Humanos identificado como un sistema del año 2008.

La fuente de este documento es el temario y la consigna compartidos por el equipo. Las consignas adicionales, las rúbricas y los resultados técnicos deberán incorporarse con sus propias evidencias.

El trabajo avanza semanalmente: cada entrega debe explicar la mejora correspondiente al tema de la semana, conservar el comportamiento que ya se haya comprobado y mostrar cómo se verificó el cambio.

## Temario de las 16 semanas

| Semana | Tema comunicado por el equipo |
| --- | --- |
| 01 | Presentación del sílabo, introducción al curso y avances de la inteligencia artificial en mantenimiento y configuración de software. |
| 02 | Mantenimiento del software. |
| 03 | Ingeniería inversa. |
| 04 | Refactorización, principio de única responsabilidad y DRY. |
| 05 | Refactorización y principio abierto/cerrado. |
| 06 | Evaluación T1. |
| 07 | Refactorización y principio de inversión de control. |
| 08 | Introducción a la gestión de la configuración. |
| 09 | Gestión del cambio. |
| 10 | Evaluación T2. |
| 11 | Taller de gestión de cambios. |
| 12 | Gestión de versiones. |
| 13 | Evaluación T3. |
| 14 | Taller de gestión de versiones. |
| 15 | Herramientas de proceso de ingeniería de software. |
| 16 | Evaluación final. |

La unidad I busca desarrollar mantenimiento preventivo mediante refactorización y principios SOLID. La unidad II busca desarrollar el proyecto y su plan de mantenimiento, controles de cambio y control de versiones.

## Situación comunicada por el equipo

El equipo se encuentra en la semana 07. Indica que sus últimos avances corresponden a la semana 05 y que en la evaluación T1 de la semana 06 no realizó una entrega. Este repositorio se organiza comenzando por el sistema original para que un lector pueda seguir cada incorporación en orden.

En C02 se incorporó la recuperación parcial de ClassRRHH.dll. C03, publicado en a5849d9, refactoriza tres consultas de empleados con SRP/DRY. C04, publicado en 7bd215a, aplica OCP a dos reportes. C05/S07 aplica IoC sobre GeneradorReportes→ejecutor, con composición externa, compilación y 16 escenarios con sustitutos. El equipo revisó la preparación y autorizó su incorporación como quinto commit por PR desde semana-07-ioc y squash en main. Sílabo página 2 y guía final páginas 6, 8 y 10 respaldan los requisitos finales; [revisión documental](../docs/ingenieria_inversa/04_revision_antecedente.md). Guías de semana 05 y 07, páginas 8-12, sustentan cada caso; [informe OCP](../docs/semanas/semana05/01_ocp.md) e [informe IoC](../docs/semanas/semana07/01_ioc.md).

## Cuatro commits iniciales acordados

| Orden | Contenido esperado | Alcance |
| --- | --- | --- |
| 1 | RRHH original y estructura organizada | Conservar la base disponible y explicar cómo se trabajará. |
| 2 | Ingeniería inversa y v1 | Recuperar conocimiento del sistema y documentar la procedencia y los límites del código recuperado. |
| 3 | v2: SRP y DRY | Mostrar una separación de responsabilidades y una reducción de duplicación justificadas. |
| 4 | v3: OCP | Mostrar el caso elegido y cómo admite la extensión que se haya comprobado. |

Después de cada commit se debe detener el trabajo y explicar qué se incorporó, dónde, por qué y qué aporta. Se continúa con el siguiente únicamente cuando el equipo lo solicite. Los commits se crearán con la fecha real del trabajo; esta secuencia no pretende fabricar un historial de entregas antiguas.

Cada etapa debe describir su estado real: propuesta, recuperación parcial, compilación comprobada o ejecución comprobada. No se debe presentar una mejora como validada si solo existe una descripción o un fragmento de código.

Durante la preparación de C05 el responsable aclaró que convirtió el repositorio a público por decisión propia. La comprobación previa de GitHub confirmó visibilidad pública y cuatro commits, con `7bd215a` como último. Esta preferencia reemplaza la indicación inicial de usar un repositorio privado; no cambia las exclusiones de claves, configuraciones restauradas y datos locales. Esa comprobación se conserva como evidencia histórica anterior a la incorporación de semana 07.

## Consigna conocida para la semana 07

Después de los cuatro commits iniciales, el equipo autorizó preparar semana 07 antes del quinto commit. Se eligió **GeneradorReportes → EjecutorReportesSql**, dependencia concreta creada dentro del generador, y se mejora mediante interfaz e inyección por constructor con composición manual.

La consigna admite casos como una clase que crea otra mediante `new`, un controlador o servicio que depende de una clase concreta, una implementación fija que dificulta las pruebas o un cambio de implementación que obliga a modificar varias clases.

La exposición debe concentrarse en esa mejora, con documentación ordenada y diapositivas breves y precisas. No corresponde convertirla en una presentación general del progreso del proyecto.

Consulta el [roadmap](ROADMAP.md) para el estado de las etapas.
