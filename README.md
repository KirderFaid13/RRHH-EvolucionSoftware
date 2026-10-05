# RRHH — Evolución y Configuración de Software

Proyecto académico para estudiar, refactorizar y evolucionar el sistema de Recursos Humanos recibido por el grupo, identificado como un sistema de 2008. Curso: **Evolución y Configuración de Software, UPN, 2026-2**.

Repositorio [RRHH-EvolucionSoftware](https://github.com/KirderFaid13/RRHH-EvolucionSoftware) público por decisión del responsable, confirmada durante esta preparación. Las claves, configuraciones restauradas y datos locales siguen excluidos de Git.

**Entrega C06: semana 08, gestión de la configuración.** Se añade el inventario de los 531 archivos de C05, un catálogo de elementos, reglas de versiones y cambios, planes de pruebas y calidad y un auditor funcional. El responsable autorizó incorporar esta entrega como sexto commit desde `semana-08-gcs` hacia `main`, mediante solicitud de cambios y squash. [Detalle de incorporación](docs/semanas/semana08/03_preparacion_sexto_commit.md), [informe](docs/semanas/semana08/01_gestion_configuracion.md) y [resultado real en el historial de GitHub](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/commits/main/).

Las diapositivas y evidencias fechadas durante la preparación conservan ese momento anterior al commit. El registro `CAM-S08-001` añade la autorización posterior. El estado del PR y el historial Git acreditan la publicación; las pruebas automáticas no acreditan una revisión humana formal.

La base software sigue siendo **v4 diagnóstica**, publicada como quinto commit `6d82f9f` mediante [PR #1](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/pull/1). Sus 22 fuentes y 16 escenarios con sustitutos vuelven a comprobarse sin abrir SQL. Resultados reales de CMI, interfaz y equivalencia completa siguen pendientes.

## Lectura inicial

La entrega actual se recorre desde el [plan de configuración](configuracion/PLAN_CONFIGURACION.md), el [inventario completo C05](configuracion/inventario_c05.csv), el [registro de cambios](configuracion/cambios.json), las [diapositivas semana 08](docs/semanas/semana08/Semana08_GCS_RRHH.pptx) y el [guion de exposición](docs/semanas/semana08/02_guion_exposicion.md). Los informes anteriores conservan su estado histórico:

1. [Semana 07: IoC, antes/después y pruebas](docs/semanas/semana07/01_ioc.md), [código v4](src/v4/README.md) y [evidencias](evidencia/semanas/semana07/README.md).
2. [Cuarto commit: OCP](docs/semanas/semana05/01_ocp.md), [código v3](src/v3/README.md) y [evidencias semana 05](evidencia/semanas/semana05/README.md).
3. [Tercer commit: SRP/DRY](docs/semanas/semana04/01_srp_dry.md), [código v2](src/v2/README.md) y [evidencias semana 04](evidencia/semanas/semana04/README.md).
4. [Ingeniería inversa y v1](docs/ingenieria_inversa/01_informe.md), [fuentes v1](src/v1/README.md) y [baseline original](docs/organizacion/01_baseline.md).
5. [Cómo localizar y restaurar el RRHH original](legado/README.md).
6. [Contexto del curso](.context/03_course_context.md), [reglas funcionales pendientes](.context/01_business_rules.md) y [diccionario de datos](.context/02_data_dictionary.json).
7. [Roadmap](.context/ROADMAP.md), [orden de commits y ramas](docs/organizacion/git_y_github.md) e [inventario del baseline](evidencia/baseline/README.md).

La entrega de semana 07 incluye [diapositivas editables](docs/semanas/semana07/Semana07_IoC_RRHH.pptx), [guion breve](docs/semanas/semana07/02_guion_exposicion.md) y [detalle del quinto commit y su incorporación](docs/semanas/semana07/03_preparacion_quinto_commit.md).

## Estructura del repositorio

```text
.
├── .context/                    Memoria del proyecto, desconocidos y roadmap
├── specs/                       Contratos de las siguientes tareas
├── configuracion/               Elementos, inventario, cambios y planes iniciales
├── src/                         Código recuperado y mejoras posteriores
├── legado/
│   └── RRHH/                    Archivos originales y originales cifrados
├── datos/
│   └── respaldos/               Guía para el respaldo conservado localmente
├── referencias/                 Documentos del curso y bibliografía
├── docs/
│   ├── organizacion/            Decisiones, baseline y uso de Git
│   ├── ingenieria_inversa/      Informe, arquitectura y procedencia de v1
│   └── semanas/                 Destino de las mejoras semanales
├── evidencia/
│   ├── baseline/                Inventarios SHA-256 y verificaciones
│   ├── ingenieria_inversa/      Metadatos, contratos y comprobaciones de v1
│   └── semanas/                 Destino de las comprobaciones semanales
├── prompts/                     Instrucciones para tareas delimitadas
├── herramientas/                Restauración y comprobación de integridad
├── .env.example                 Plantilla vacía para desarrollos posteriores
├── .gitattributes               Conservación de bytes del paquete original
└── .gitignore                   Exclusión de claves, datos y archivos locales
```

Git registra archivos; los directorios pendientes contienen un README que explica su función.

## Qué significa «original» aquí

El paquete recibido contiene **348 archivos, 519.216.065 bytes**. Su inventario identifica todos mediante ruta, tamaño y SHA-256:

- **335 archivos** están almacenados sin cambios de contenido.
- **12 archivos** conservan sus bytes originales cifrados con AES-256-GCM: seis configuraciones, tres copias de `RecursosHumanos.exe` y tres de `GRLL.dll`, que contienen credenciales.
- **1 archivo**, `CMI_Backup_QA.bak`, permanece fuera de Git: pesa 199.401.472 bytes y su contenido no ha sido revisado. Su hash queda registrado.
- Se añaden **6 configuraciones de ejemplo** sin conexiones reales y **8 PDF** de referencia.

La clave se conserva en `.local/clave_legado.key`, ignorada por Git. Al clonar, se debe obtener del responsable por un medio privado. No se puede restaurar la parte cifrada únicamente con el repositorio. Los originales completos también permanecen en el workspace local del responsable.

El cifrado protege el almacenamiento: al restaurar se recuperan exactamente los archivos recibidos, incluidas sus configuraciones originales. Esas credenciales siguen formando parte del programa restaurado; esta etapa no modifica su manejo interno.

## Comprobaciones

Desde la raíz del repositorio:

```powershell
python -m pip install -r .\herramientas\requirements.txt
python .\herramientas\verificar_baseline.py
```

Sin la clave, el verificador comprueba los archivos almacenados y las referencias. Con la clave local también autentica y descifra en memoria los 12 archivos para comparar su contenido con el hash original. [Detalles de la evidencia](evidencia/baseline/README.md).

Para recuperar una copia del programa fuera de los archivos versionados:

```powershell
python .\herramientas\restaurar_legado.py
```

El destino predeterminado es `.local/RRHH/`. El respaldo SQL se obtiene por separado; no lo descarga este comando. Ninguna de estas herramientas ejecuta la aplicación ni restaura una base de datos.

La integridad de archivos **no acredita funcionamiento**. Todavía no se ha probado instalación, conexión a CMI, ejecución del programa ni equivalencia de código recuperado.

## Secuencia acordada

| Commit | Contenido | Estado de esta revisión |
| --- | --- | --- |
| 1 | RRHH original protegido y estructura organizada. | Conservado; publicado en `e1ead41`. |
| 2 | Ingeniería inversa y base v1 con procedencia documentada. | Publicado en `9e18ca4`; recuperación parcial, compilación diagnóstica comprobada. |
| 3 | v2: refactorización mediante SRP y DRY. | Publicado en `a5849d9`; tres consultas refactorizadas y 11 escenarios aprobados. |
| 4 | v3: mejora mediante abierto/cerrado, OCP. | Publicado en `7bd215a`; biblioteca de 20 fuentes compilada y extensión externa aceptada sin recompilar el núcleo. |
| 5 | v4: semana 07, inversión de control. | Entrega C05 validada: 22 fuentes compiladas y 16 escenarios aprobados con sustitutos. Incorporación por PR desde `semana-07-ioc` con squash. |
| 6 | Semana 08: gestión de la configuración. | Inventario, auditor, planes y exposición comprobados. Incorporación autorizada desde `semana-08-gcs` mediante PR y squash; resultado consultable en GitHub. |

Se avanza y se explica **un commit por vez**, esperando la indicación del equipo antes del siguiente. C06 corresponde a la sexta entrega autorizada. Los archivos y análisis de etapas anteriores se conservan. El [historial de GitHub](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/commits/main/) y las solicitudes de cambios registran la publicación real. Después de incorporar y explicar semana 08 se detiene el avance.

Para repetir la comprobación de v1, después de restaurar el legado y disponer de la clave local:

```powershell
python .\herramientas\compilar_v1.py
```

La compilación incluye 12 fuentes recuperadas, no los VB del antecedente académico. `MySettings.cs` se almacena cifrada por sus valores codificados; once C# quedan visibles. [Procedimiento y límites](docs/ingenieria_inversa/03_procedencia_v1.md).

Para repetir la comprobación de v2, después de restaurar el legado:

```powershell
python herramientas/compilar_v2.py
python herramientas/verificar_v2.py
```

Se compila la combinación de v1 con el caso v2 y se prueban comandos del código nuevo sin abrir SQL. La propuesta v2 previa se preserva como antecedente; no participa en la biblioteca activa. [Qué cambió y por qué](docs/semanas/semana04/01_srp_dry.md).

Para repetir la comprobación de v3:

```powershell
python herramientas/compilar_v3.py
python herramientas/verificar_v3.py
```

v3 reutiliza las fuentes v1 y los dos helpers de empleados de v2, sustituye la fachada por su variante v3 y añade el caso de reportes. Se demuestra la preparación de una extensión contra el núcleo ya compilado; no se ejecuta `Fill`, SQL ni la aplicación recibida. La propuesta v3 anterior se conserva como antecedente. [Qué cambió y por qué](docs/semanas/semana05/01_ocp.md).

Para repetir el procedimiento histórico de v4 (genera evidencia de semana 07):

```powershell
python herramientas/compilar_v4.py
python herramientas/verificar_v4.py
```

v4 conserva cuatro fuentes de reportes v3 y dos helpers v2, sustituye fachada/generador/ejecutor y añade interfaz/composición. `Generar` se ejecuta con sustitutos, devuelve un `DataSet` sintético y permite comprobar llamadas y errores; el ejecutor SQL real no se ejecuta. [Informe](docs/semanas/semana07/01_ioc.md) y [prompt de revisión](prompts/04_ioc.md).

Para comprobar la preparación de semana 08 conservando la evidencia anterior:

```powershell
python herramientas/auditar_configuracion.py
python herramientas/verificar_configuracion.py
```

El primer comando audita C05 y el alcance autorizado. El segundo prueba el auditor con muestras temporales, comprueba JSON/CSV y recompila/repite v4 con salidas nuevas en `.local/c06/`. Auditor: Python 3.12 o posterior y Git con `check-attr --source`; compilación v4: entorno Windows, SDK/referencias y fuentes privadas descritos en el [plan de pruebas](configuracion/PLAN_PRUEBAS.md). En AppContainer, SqlClient puede necesitar permiso adicional para inicializar contadores locales. [Resultados y límites](evidencia/semanas/semana08/README.md).
