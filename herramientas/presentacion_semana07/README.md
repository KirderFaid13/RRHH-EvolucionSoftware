# Reproducción de la presentación de semana 07

`generar_presentacion.mjs` usa `@oai/artifact-tool` del runtime local de Codex. No instala dependencias ni modifica el runtime. `contenido_verificado.json` contiene el texto y las notas contrastados manualmente con el código v3/v4, la consigna de semana 07 y los JSON de evidencia. El script exige compilación correcta y 16 escenarios aprobados, incluidos 11 contratos, sin abrir SQL.

Desde la raíz del repositorio, configure las rutas del runtime disponible. Estas fueron las rutas de esta sesión:

```powershell
$presentationRuntime = 'C:\Users\KirderFaid\.cache\codex-runtimes\codex-primary-runtime\dependencies'
$env:RUNTIME_NODE_MODULES = Join-Path $presentationRuntime 'node\node_modules'
$env:RUNTIME_PYTHON = Join-Path $presentationRuntime 'python\python.exe'
$env:SKILL_DIR = 'C:\Users\KirderFaid\.codex\plugins\cache\openai-primary-runtime\presentations\26.904.11930\skills\presentations'
& (Join-Path $presentationRuntime 'node\bin\node.exe') .\herramientas\presentacion_semana07\generar_presentacion.mjs . .\evidencia\semanas\semana07\compilacion_y_pruebas.json .\.local\c05\presentacion\salida\Reproduccion.pptx
```

Los argumentos son directorio del repositorio, evidencia y destino PPTX. Sin el segundo argumento, la evidencia se resuelve desde el repositorio a `evidencia/semanas/semana07/compilacion_y_pruebas.json`. El destino por defecto es `docs/semanas/semana07/Semana07_IoC_RRHH.pptx`. Use un nombre de salida nuevo: el finalizador no sobrescribe archivos existentes.

La validación y los renders individuales quedan en `.local/c05/presentacion/`. La revisión visual utilizó PNG generados al importar el PPTX final con ArtifactTool. No se abrió la aplicación PowerPoint ni LibreOffice. No se abrieron imágenes o presentaciones PowerPoint originales como fuente o plantilla. Texto, código, diagrama y notas del archivo final conservan objetos nativos editables.
