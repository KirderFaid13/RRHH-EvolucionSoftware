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

El avance documentado llega a la semana 09. En la revisión inicial indicó que sus últimos avances correspondían a la semana 05 y que en la evaluación T1 de semana 06 no realizó una entrega. El repositorio conserva el sistema original y sus mejoras incorporadas en orden, incluyendo la entrega IoC de semana 07 publicada en el quinto commit.

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

## Consigna y preparación de semana 08

El usuario proporcionó [Semana08_EVO_TG.pdf](../referencias/semanas/semana08/Semana08_EVO_TG.pdf). La práctica de páginas 14–16 pide justificar GCS, identificar elementos, organizar el repositorio y proponer controles iniciales de versiones, cambios y pruebas. La rúbrica de página 17 evalúa organización, dominio del tema, calidad visual y participación. Los textos IoC/OCP de páginas 4 y 18 no cambian el alcance de esa práctica.

C06 se prepara desde `6d82f9f` (531 archivos versionados) en `semana-08-gcs`. Se añade control de configuración y un auditor repetible; el código v4 permanece intacto. El usuario confirmó «Yo revisaré e integraré los cambios»: se registra a KirderFaid13 como responsable. Después de recibir la preparación, indicó «realiza el 6to commit entonces» el 5 de octubre de 2026. Esta autorización habilita su incorporación con la dinámica anterior de rama, PR y squash, sin atribuir una revisión formal que no está registrada. [Informe](../docs/semanas/semana08/01_gestion_configuracion.md), [contrato](../specs/c06_gestion_configuracion.json) y [registro CAM-S08-001](../configuracion/cambios.json). La publicación real se comprueba mediante el historial y el estado del PR.

## Semana 09: gestión del cambio

La consigna de páginas 14–15 pide tres solicitudes RRHH, formato simple, matriz, impacto por cambio y flujo; página 7 pide código funcional. Se registraron CAM-S09-001/#10 (liberación de comando), CAM-S09-002/#11 (guardas nulas) y CAM-S09-003/#12 (tiempo de espera) antes de implementar la primera.

El usuario autorizó teoría, código, documentos, Issues y publicación, confirmó 20–30 minutos de exposición y pidió conservar el DOCX de su compañero. C07 selecciona una corrección mínima de Generar en v5 con using; 002/003 continúan propuestas. Biblioteca: 22 fuentes; rojo v4 4/6 con dos fallos esperados, verde v5 6/6 y regresión 16/16, sin SQL. Las fuentes y evidencias anteriores se conservan.

Base: 6c13e74, seis entregas académicas y un commit documental. Rama semana-09-gestion-cambios; PR #13 para integrar C07 por squash. C07 es la séptima entrega académica y el octavo commit de main; el resultado publicado se comprueba en GitHub. La revisión automática no acredita revisión formal humana. Riesgo pendiente: SelectCommand conserva el comando dispuesto y pueden existir consumidores en UI/binarios no recuperados.

Fuentes: [consigna](../referencias/semanas/semana09/Semana09_EVO_TG.pdf), [contrato C07](../specs/c07_gestion_cambio.json), [informe](../docs/semanas/semana09/01_gestion_cambio.md) e [Issue #10](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/10).
