# RRHH — Evolución y Configuración de Software

Proyecto académico para estudiar, refactorizar y evolucionar el sistema de Recursos Humanos recibido por el grupo, identificado como un sistema de 2008. Curso: **Evolución y Configuración de Software, UPN, 2026-2**.

**Etapa de esta revisión: ingeniería inversa y base v1.** Se recuperó código de `ClassRRHH.dll`, se identificaron clases y contratos de llamada y se compiló una biblioteca de diagnóstico. El programa original conserva su contenido; funcionamiento, esquema SQL y equivalencia siguen pendientes.

## Lectura inicial

1. [Segundo commit: qué recuperamos, dónde, por qué y límites](docs/ingenieria_inversa/01_informe.md).
2. [Código v1 y procedencia](src/v1/README.md), [arquitectura](docs/ingenieria_inversa/02_arquitectura.md) y [comprobaciones C02](evidencia/ingenieria_inversa/README.md).
3. [Primer commit: preservación y organización](docs/organizacion/01_baseline.md).
4. [Cómo localizar y restaurar el RRHH original](legado/README.md).
5. [Contexto del curso](.context/03_course_context.md), [reglas funcionales pendientes](.context/01_business_rules.md) y [diccionario de datos](.context/02_data_dictionary.json).
6. [Roadmap](.context/ROADMAP.md) y [orden de commits y ramas](docs/organizacion/git_y_github.md).
7. [Inventario y comprobaciones del baseline](evidencia/baseline/README.md).

## Estructura del repositorio

```text
.
├── .context/                    Memoria del proyecto, desconocidos y roadmap
├── specs/                       Contratos de las siguientes tareas
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
| 2 | Ingeniería inversa y base v1 con procedencia documentada. | Contenido de esta revisión: recuperación parcial, compilación diagnóstica comprobada. |
| 3 | v2: refactorización mediante SRP y DRY. | Pendiente. |
| 4 | v3: mejora mediante abierto/cerrado, OCP. | Pendiente. |

Se avanza y se explica **un commit por vez**, esperando la indicación del equipo antes del siguiente. La semana 07, IoC/v4, se trabajará después de esta secuencia. Las versiones y análisis anteriores se conservan localmente para revisarlos cuando corresponda.

Para repetir la comprobación de v1, después de restaurar el legado y disponer de la clave local:

```powershell
python .\herramientas\compilar_v1.py
```

La compilación incluye 12 fuentes recuperadas, no los VB del antecedente académico. `MySettings.cs` se almacena cifrada por sus valores codificados; once C# quedan visibles. [Procedimiento y límites](docs/ingenieria_inversa/03_procedencia_v1.md).
