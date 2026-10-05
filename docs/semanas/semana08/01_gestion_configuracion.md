# Semana 08: gestión de la configuración del RRHH

**Preparación C06 — 5 de octubre de 2026.** Se aplica gestión de la configuración del software (GCS) al repositorio existente del RRHH. Se identifican sus componentes, se fija una base verificable, se acuerdan reglas de versiones y cambios y se documentan pruebas iniciales. La versión de código más reciente continúa siendo **v4, diagnóstica**. Esta entrega se preparó en `semana-08-gcs`; posteriormente el responsable indicó realizar el sexto commit. El [detalle de incorporación](03_preparacion_sexto_commit.md) y GitHub registran la autorización y el resultado.

## Consigna y alcance

La [guía de semana 08](../../../referencias/semanas/semana08/Semana08_EVO_TG.pdf), páginas 14–16, pide justificar la GCS, elaborar una tabla de elementos de configuración, proponer la organización del repositorio, definir controles básicos de versiones y cambios e indicar pruebas iniciales. Las páginas 9–13 dan el fundamento teórico. La rúbrica de la página 17 evalúa organización, dominio, calidad visual y participación; no fija cantidad de diapositivas ni duración.

Las páginas 4 y 18 conservan textos de IoC/OCP. Esta entrega sigue el desarrollo práctico de GCS de las páginas 14–16. No se deduce de esos textos una nueva refactorización del negocio. El ejemplo funcional de esta semana es un **auditor de configuración**, que compara archivos y alcance contra una base conocida.

El [contrato C06](../../../specs/c06_gestion_configuracion.json) delimita la preparación. No se modifica `src/`, `legado/`, antecedentes ni evidencias de etapas anteriores; tampoco se ejecutan binarios recibidos ni se conecta o restaura SQL.

## 1. Por qué este proyecto necesita GCS

El proyecto combina originales recibidos, originales cifrados, código recuperado parcialmente, propuestas anteriores, casos activos v1–v4, documentos del curso y evidencias. **GCS permite identificar qué integra una versión, registrar sus cambios y comprobar su estado**, de modo que el mantenimiento se apoye en una base reconocible. Esta aplicación sigue las actividades de identificación, control de cambios, informes de estado y auditoría descritas en [SWEBOK, capítulo 8](https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf).

Sin ese control, podrían confundirse una propuesta y una implementación activa, compilarse fuentes de distintas versiones, sobrescribirse un original o exponerse una configuración restaurada. También podría presentarse una prueba antigua como evidencia de archivos modificados. Son **riesgos del proyecto**, no incidentes cuya ocurrencia se haya demostrado.

El equipo mejora su coordinación al acordar alcance y rutas antes de editar, consultar un inventario común y entregar cada cambio con su explicación y comprobaciones. Un nuevo integrante puede identificar la base, localizar la versión estudiada y saber qué sigue sin validar. La GCS contribuye a la mantenibilidad y la evolución porque conserva ese vínculo entre componente, decisión, versión y evidencia; por sí sola no demuestra que el sistema funcione.

## 2. Actividades aplicadas

| Actividad | Aplicación al RRHH | Registro concreto |
| --- | --- | --- |
| Identificación | Distinguir componentes por tipo, ubicación, procedencia y estado. | [Elementos de configuración](../../../configuracion/elementos.json) e [inventario C05](../../../configuracion/inventario_c05.json). |
| Control de versiones | Utilizar Git y ramas por semana sobre una base conocida. | C05: `6d82f9fa6aa608a0d7d71c14fb2fc661e9d21fa2`; trabajo C06: `semana-08-gcs`. |
| Control de cambios | Registrar qué se cambia, por qué, dónde y cómo se comprobará; revisar antes de integrar. | [CAM-S08-001](../../../configuracion/cambios.json) y [plan de configuración](../../../configuracion/PLAN_CONFIGURACION.md). |
| Informe de estado | Separar base publicada, preparación local, pruebas ejecutadas y validaciones pendientes. | [Auditoría de esta preparación](../../../evidencia/semanas/semana08/auditoria_configuracion.json) y este informe. |
| Auditoría | Comparar hashes de la base y detectar archivos ausentes, alterados o fuera de alcance. | [Auditor funcional](../../../herramientas/auditar_configuracion.py) y [verificador](../../../herramientas/verificar_configuracion.py). |

Un elemento de configuración puede ser un archivo o un conjunto que se controla como unidad. La tabla siguiente usa agregados para facilitar su lectura; el inventario individual cubre los **531 archivos versionados en C05**. El compromiso de referencia y los hashes permiten reconocer esa base; los nuevos entregables C06 se identifican por separado, sin atribuirles pertenencia histórica a C05. [SWEBOK: temas de gestión de configuración](https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics).

## 3. Tabla de elementos que se ponen bajo control

| Tipo | Elemento y ubicación | Estado y regla de control |
| --- | --- | --- |
| Código fuente | `src/v1/recuperado/`, `src/v2/caso_empleados/`, `src/v3/caso_reportes/`, `src/v4/caso_ioc/`; propuestas en `antecedentes/`. | Recuperación parcial y casos académicos activos. Git conserva cada versión y su procedencia; C06 no cambia estos archivos. |
| Archivos de datos | `.context/02_data_dictionary.json`; metadatos e inventarios en `evidencia/` y `configuracion/`. Respaldo SQL conservado fuera de Git, orientado por `datos/respaldos/`. | Se versionan diccionario y metadatos sin datos reales. El esquema completo sigue desconocido; el `.bak` no se restaura. |
| Archivos compilados | Binarios recibidos en `legado/RRHH/`, incluidos originales cifrados; nuevos resultados de compilación en `.local/`. | Los recibidos se preservan como referencia y no se ejecutan. Los compilados generados permanecen locales; se versionan sus metadatos y resultados de comprobación. |
| Scripts | `herramientas/compilar_v*.py`, `verificar_v*.py`, `auditar_configuracion.py`, `verificar_configuracion.py` y generador de presentación. | Scripts propios versionados. Cada procedimiento declara entradas, salida y límites; no se incorporan sus directorios temporales. |
| Requerimientos | `docs/organizacion/01_baseline.md`, contratos C02–C06 en `specs/` y `.context/03_course_context.md`. | Alcance de cada etapa y criterios de aceptación. No se inventan reglas funcionales ni requisitos SQL. |
| Diseño | `.context/01_business_rules.md`, informes y comparaciones antes/después de las semanas 04, 05 y 07. | Diseño observado, decisiones y dudas identificadas. Se enlaza cada propuesta con el caso y la evidencia que la sustenta. |
| Arquitectura | `docs/ingenieria_inversa/02_arquitectura.md` y descripción de composición en `docs/semanas/semana07/01_ioc.md`. | Arquitectura recuperada parcialmente y caso IoC documentado. La interfaz completa y la integración real están pendientes. |
| Planes de prueba | [PLAN_PRUEBAS.md](../../../configuracion/PLAN_PRUEBAS.md) y criterios de `specs/`. | Plan inicial C06 versionado; separa comprobaciones disponibles de pruebas propuestas para un entorno autorizado. |
| Procedimientos de prueba | Harness `src/v4/pruebas/PruebasIoC.cs`, verificadores de `herramientas/` y evidencia semanal. | Procedimientos repetibles con entradas sintéticas y resultados registrados; no equivalen a pruebas de toda la aplicación. |
| Planes de calidad | [PLAN_CALIDAD.md](../../../configuracion/PLAN_CALIDAD.md) y reglas del [plan de configuración](../../../configuracion/PLAN_CONFIGURACION.md). | Plan inicial de trazabilidad, conservación, revisión y comprobación. Revisión del responsable e integración de C06 pendientes. |
| Documentación del curso | `referencias/curso/`, `referencias/semanas/`, informes, guion y presentación en `docs/`. | Se conserva la consigna exacta y se controla la documentación de cada etapa. La presentación C06 describe GCS; no declara resultados de SQL o interfaz. |

Las rutas e identificadores formales están en `configuracion/elementos.json`. **Estar bajo control no implica publicar todo:** la clave, configuraciones restauradas, datos reales, respaldo y compilados locales tienen política de almacenamiento privado. Solo se incluye su documentación o metadatos permitidos.

## 4. Organización inicial del repositorio

La propuesta aprovecha la organización existente y añade `configuracion/` para los controles comunes. No se duplica ni se traslada el legado para preparar esta semana.

```text
.context/                 Contexto, desconocidos y roadmap
specs/                    Contratos y aceptación por etapa
src/v1/ ... src/v4/        Código recuperado y casos activos
legado/RRHH/              Referencia recibida conservada
datos/respaldos/           Guía de datos mantenidos fuera de Git
referencias/              Consignas y bibliografía
docs/                     Explicaciones, decisiones y exposición semanal
evidencia/                Procedencia, hashes y resultados de comprobación
configuracion/            Inventario, elementos, cambios y planes iniciales
herramientas/             Scripts de compilación, verificación y presentación
prompts/                  Órdenes de trabajo delimitadas por contrato
.local/                   Material privado y resultados generados; ignorado
```

`src/` muestra lo estudiado o implementado; `docs/` explica decisiones; `evidencia/` conserva lo comprobado. Los `antecedentes/` permanecen separados del caso activo. Así se evita confundir organización de archivos con equivalencia funcional entre versiones.

## 5. Control básico de versiones

Se usa **Git** para registrar cambios y **GitHub** para alojar el [repositorio RRHH-EvolucionSoftware](https://github.com/KirderFaid13/RRHH-EvolucionSoftware), actualmente público por decisión del responsable. Git permite recuperar estados y comparar cambios de archivos; GitHub añade colaboración mediante ramas y solicitudes de cambios. [Git: control de versiones](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control), [GitHub: solicitudes de cambios](https://docs.github.com/en/pull-requests/get-started/about-pull-requests).

Se versionan fuentes permitidas, originales protegidos, contratos, contexto, scripts, documentación, planes, metadatos y evidencias sin secretos. Las exclusiones de `.gitignore` siguen aplicándose a `.local/`, claves, respaldos y compilados generados.

La base publicada de esta semana es C05: `6d82f9f`, árbol `a6b85aad0d6ab119297cd4ffd37c8ef5421a383e`. Sus 531 archivos se congelan como referencia del auditor. Los cinco commits publicados permiten ubicar original, ingeniería inversa, SRP/DRY, OCP e IoC; esta lista demuestra trazabilidad, sin convertir la exposición en un repaso de mejoras pasadas.

Reglas iniciales del equipo:

1. `main` contiene entregas integradas. Cada semana se prepara en una rama, esta vez `semana-08-gcs`.
2. Antes de editar, el autor comunica al responsable el alcance y las rutas. Se acuerda quién trabajará en archivos compartidos.
3. Se revisan `git status` y la diferencia; se agregan únicamente los archivos de la etapa, sin forzar material ignorado.
4. Cada commit explica problema, cambio, motivo, validación y límites. La integración semanal puede usar squash para conservar un commit por entrega.
5. Se abre una solicitud de cambios hacia `main`, se revisa y se integra cuando el responsable lo autorice. No se atribuyen controles de CI ni protección de ramas que no se hayan configurado.
6. Después de integrar, se explica el resultado y se espera la siguiente indicación. No se fabrican fechas ni avances históricos.

## 6. Control básico de cambios

El cambio de esta semana se registra como **CAM-S08-001** en `configuracion/cambios.json`. La solicitud inicial autorizó preparar GCS y las diapositivas. La indicación posterior «realiza el 6to commit entonces» autoriza su incorporación; el registro no atribuye una revisión formal de GitHub.

**KirderFaid13 revisará e integrará los cambios**, según su confirmación. El autor coordina rutas antes de editar, explica su diferencia y aporta evidencia; el responsable verifica alcance, documentación y comprobaciones antes de la integración. Si el responsable también es autor, solicitar una lectura a otro integrante puede mejorar la revisión, pero no se presenta como un rol ya asignado ni una obligación acordada.

El registro conserva ID, fecha, origen, motivo, alcance, riesgos, validaciones, estado de revisión y estado de integración. Los archivos de esta preparación se identifican en el contrato; los cambios no permitidos se reportan. Las instrucciones iniciales y los commits previos se documentan como antecedentes reales, sin atribuirles aprobaciones inexistentes.

Secuencia: **registrar → coordinar alcance → preparar → comprobar → revisar → autorizar incorporación → integrar → verificar publicación**. Registrar y revisar cambios reduce el riesgo de sobrescribir trabajo o introducir una diferencia sin explicación. Git guarda el contenido; el registro del cambio guarda su motivo y decisión.

## 7. Pruebas iniciales vinculadas al proyecto

**Caja negra, blanca y gris describen cuánto se conoce del interior de lo probado.** Funcionalidad, rendimiento y seguridad describen qué objetivo se evalúa. No son categorías intercambiables. El [plan de pruebas](../../../configuracion/PLAN_PRUEBAS.md) aplica esta distinción al RRHH.

| Comprobación | Alcance real o propuesto | Evidencia y límite |
| --- | --- | --- |
| Auditoría de configuración | Comparar los 531 archivos de C05, cambios permitidos y archivos nuevos de C06; comprobar exclusiones. | `auditoria_configuracion.json` registra el estado observado de esta preparación. Un hash correcto demuestra integridad, no funcionamiento. |
| Pruebas del auditor | Casos temporales que detectan archivo alterado o ausente, ruta inválida, inventario alterado y alta fuera de alcance. | Resultados del verificador C06. Se usan muestras aisladas; no se altera el legado para provocar errores. |
| Compilación y pruebas aisladas de v4 | Se repitió la compilación de la biblioteca de 22 fuentes y del harness de 10 fuentes. Aprobaron los 16 escenarios con sustitutos y datos sintéticos. | La repetición C06 se registra por separado. No ejecuta el ejecutor SQL real, la interfaz ni CMI. |
| Funcionalidad integrada, caja negra | Propuesta: en entorno autorizado, comprobar entradas y salidas de consultas y reportes desde la aplicación. | Pendiente de entorno, datos de prueba y resultados esperados acordados. No se inventan pantallas, roles ni esquema. |
| Integración, caja gris | Propuesta: observar aplicación y conexión con conocimiento de contratos recuperados. | SQL, procedimientos y salidas reales siguen pendientes de verificación. |
| Rendimiento | Propuesta: medir una operación acordada con volumen sintético y entorno controlado. | No hay medición ni umbral aceptado; se definirán antes de ejecutar. |
| Seguridad | Comprobación disponible: exclusiones de secretos y datos locales. Propuesta: validar autenticación y permisos reales cuando se conozcan. | La exclusión Git no certifica seguridad completa ni autorización de la aplicación. |

Los comandos de demostración se ejecutan desde la raíz de `RRHH_GitHub`:

```powershell
python herramientas/auditar_configuracion.py
python herramientas/verificar_configuracion.py
```

El verificador C06 también repite la compilación y las 16 pruebas de v4, conservando los resultados nuevos exclusivamente en `evidencia/semanas/semana08/`. Esta compilación depende del legado restaurado y de herramientas locales ya documentadas. Estos comandos no autorizan ejecutar la aplicación recibida ni restaurar SQL. Los procedimientos antiguos de v4 se consultan como antecedente; no se usan para reescribir la evidencia C05.

En esta preparación aprobaron **14 pruebas aisladas del auditor**, la coincidencia de las seis columnas del inventario JSON/CSV y **16 escenarios v4**. La auditoría compara el contenido de los archivos de trabajo; no acredita los bytes preparados en el índice Git ni los de un futuro commit. Antes de incorporar la etapa se revisarán también `git diff --cached`, las exclusiones del índice y el árbol integrado. En AppContainer, Windows bloqueó la inicialización de contadores de SqlClient; la repetición autorizada fuera de ese entorno aprobó sin abrir SQL.

## Qué mejora y cómo revisar esta entrega

La mejora concreta es **poder reconocer y comprobar la configuración de trabajo antes de integrar un cambio**. Se pasa de una organización documentada por etapas a un inventario congelado con control de alcance, registro de cambio, responsable y planes iniciales. El auditor aporta el ejemplo funcional solicitado: detecta diferencias que requieren explicación.

Para revisar, leer `CAM-S08-001`, comparar la diferencia con el contrato, consultar el inventario y el resultado de auditoría y comprobar la presentación y el guion. El [detalle del sexto commit](03_preparacion_sexto_commit.md) contiene el mensaje propuesto y el criterio de cierre. Los resultados iniciales conservan el momento de preparación. La decisión posterior del responsable autoriza C06 y su publicación se comprueba en el historial y el PR.

La organización, la integridad y la compilación son comprobaciones distintas. Continúan pendientes el funcionamiento completo, la base CMI, interfaz, rendimiento, autenticación y equivalencia con el sistema original.
