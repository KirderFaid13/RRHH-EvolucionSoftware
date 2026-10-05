# Presentación de semana 08

`generar_presentacion.mjs` construye una presentación local editable de ocho diapositivas con el runtime `@oai/artifact-tool`. Requiere la habilidad de presentaciones y sus dependencias disponibles; no instala paquetes ni modifica el runtime. El PowerPoint local se construye independientemente de Canva.

## Contenido y evidencia

`contenido_verificado.json` contiene los títulos, el inventario resumido y las notas con sus fuentes. La consigna práctica está en las páginas 14 a 16 de `referencias/semanas/semana08/Semana08_EVO_TG.pdf`.

Antes de construir, el script exige `auditoria_configuracion.json` y `verificacion_configuracion.json`: 531 archivos C05 comprobados, cero fallos, 14 escenarios del auditor aprobados y 16 escenarios v4 sin conexión SQL. Los escenarios incluyen el rechazo de un CSV incompleto, sin hash ni esquema, y la comparación de sus seis columnas con el JSON. No declara funcionamiento completo del RRHH ni una publicación C06.

La tabla de la diapositiva 3 es nativa. Todos los textos y las notas permanecen editables. Las pruebas de la tabla pertenecen a subdirectorios dentro de `src/`. El informe amplía las diez categorías de configuración enumeradas por el docente e identifica también el material del curso.

## Reproducción

Resolver primero el runtime disponible de Codex. Definir `SKILL_DIR`, `RUNTIME_NODE_MODULES` y `RUNTIME_PYTHON` mediante sus rutas absolutas. Usar el ejecutable Node de ese runtime, sin instalar dependencias sustitutas. Estas fueron las rutas verificadas de esta sesión; en otra máquina deben ajustarse al runtime instalado:

```powershell
$presentationRuntime = 'C:\Users\KirderFaid\.cache\codex-runtimes\codex-primary-runtime\dependencies'
$runtimeNode = Join-Path $presentationRuntime 'node\bin\node.exe'
$env:RUNTIME_NODE_MODULES = Join-Path $presentationRuntime 'node\node_modules'
$env:RUNTIME_PYTHON = Join-Path $presentationRuntime 'python\python.exe'
$env:SKILL_DIR = 'C:\Users\KirderFaid\.codex\plugins\cache\openai-primary-runtime\presentations\26.904.11930\skills\presentations'
```

Antes de una nueva operación de autoría, seguir el marcador y las instrucciones de la habilidad de presentaciones. Ejecutar desde la raíz del repositorio:

```powershell
& $runtimeNode .\herramientas\presentacion_semana08\generar_presentacion.mjs . .\.local\c06\reproducciones\Reproduccion_S08.pptx
```

El finalizador no sobrescribe una salida existente. Para otra reproducción, usar un nombre nuevo. Las reproducciones privadas escriben su recibo de presentación local y conservan la evidencia pública del PPTX entregado. Una revisión del destino público requiere comprobar de nuevo imágenes, hechos y hashes antes de reemplazarlo.

La salida debe estar separada de `.local/c06/presentacion/`, donde se guardan los recibos técnicos. El finalizador impide mezclar el directorio de entrega con esos recibos.

Los borradores, los renderizados individuales y el recibo técnico quedan en `.local/c06/presentacion/`, fuera de Git. Los resultados compartibles son el PowerPoint, `vista_previa.png` y `evidencia/semanas/semana08/presentacion.json`.

La revisión individual de los ocho renderizados complementa las comprobaciones automáticas de estructura, fuentes, geometría e importación. No equivale a abrir el archivo en PowerPoint.
