# Presentación de semana 09

El generador construye una presentación editable sobre gestión del cambio a partir de `contenido_verificado.json`. La entrega reúne el bloque teórico y el caso práctico del RRHH, con notas para exponer y fuentes por diapositiva. El contenido JSON es la autoridad: el generador organiza sus textos, tablas y código sin inventar resultados ni estados de publicación.

La presentación original del compañero es una fuente de cobertura temática. El rediseño se entrega en una copia nueva, sin modificar ese PPTX ni el informe DOCX original.

## Requisitos

- Runtime de presentaciones suministrado con `@oai/artifact-tool`, sin instalar paquetes alternativos.
- Node.js y Python del entorno de trabajo.
- Fuentes Arial y Consolas disponibles.
- `contenido_verificado.json` junto al generador y la ilustración `assets/portada_conceptual.png`.

La ilustración conceptual fue generada con IA para esta portada. Aparece una sola vez. El texto, las notas, las tablas y la comparación de código permanecen editables; las tablas de evidencia conservan objetos nativos de PowerPoint.

## Ejecución

Establecer las rutas del runtime instalado y ejecutar desde la raíz del repositorio:

```powershell
$env:RUNTIME_NODE_MODULES = 'RUTA_ABSOLUTA/node_modules'
$env:RUNTIME_PYTHON = 'RUTA_ABSOLUTA/python.exe'
$env:SKILL_DIR = 'RUTA_ABSOLUTA/skills/presentations'
node herramientas/presentacion_semana09/generar_presentacion.mjs . .local/c07/presentacion/salidas/reproduccion_01.pptx
```

El argumento opcional siguiente permite indicar otra copia de contenido JSON para un borrador privado. La salida debe conservarse dentro del proyecto y usar un nombre nuevo en cada revisión. El generador rechaza sobrescribir una presentación existente.

Para producir la entrega final, después de revisar el contenido y los borradores:

```powershell
node herramientas/presentacion_semana09/generar_presentacion.mjs . docs/semanas/semana09/Semana09_Gestion_Cambio_RRHH.pptx
```

La ruta final exige 26 diapositivas. Las comprobaciones del finalizador incluyen estructura del paquete, tamaño de página, geometría declarada, tablas nativas, política de fuentes e importación por Artifact Tool. En Windows, el guardado atómico del finalizador puede requerir ejecutar el proceso fuera del sandbox cuando este impida crear el enlace local.

## Resultados y límites

- PPTX en la ruta elegida, tamaño 1280 × 720.
- Borrador, recibo de validación, resumen de generación y render individual PNG en `.local/c07/presentacion/`, excluida de Git.
- Fuentes citadas en las notas de la diapositiva correspondiente.
- Cifras y estados tomados del contenido verificado por el equipo.

La validación automática no sustituye revisar visualmente cada diapositiva. El render no acredita apertura en PowerPoint ni pruebas funcionales del RRHH. Las propuestas, comprobaciones aisladas y resultados publicados deben distinguirse explícitamente en el contenido y las evidencias del caso práctico.

Los hashes documentales publicados se calculan sobre los bytes versionados por Git. `.gitattributes` normaliza Markdown y JSON a LF; una copia local con CRLF puede conservar el mismo texto y tener otro SHA-256. La evidencia de publicación distingue ambos casos y mantiene el hash anterior de preparación.
