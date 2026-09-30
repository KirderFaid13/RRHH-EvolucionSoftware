# Evidencias C03 — v2 SRP/DRY

- [Contratos de v1](contratos_v1.json): fuente, SHA-256, firmas, comandos y parámetros extraídos.
- [Diferencias de la fachada](antes_despues.diff): comparación v1/v2 con finales de línea normalizados para mostrar únicamente los tres cuerpos modificados.
- [Compilación y pruebas](compilacion_y_pruebas.json): biblioteca activa, diagnóstico separado del antecedente y once escenarios sin abrir SQL.
- [Verificación de v2](verificacion_v2.json): alcance de los cambios, hashes y conservación de etapas anteriores.
- [Antecedentes](antecedentes.json): ocho archivos recibidos preservados.

Desde la raíz: `python herramientas/compilar_v2.py` y `python herramientas/verificar_v2.py`. La herramienta necesita clave local, legado restaurado, SDK10.0.103 y referencias Framework de Windows.

Los logs, respuesta del compilador, fuente del harness y DLL/EXE de diagnóstico quedan en `.local/c03/`, ignorada por Git. El harness se genera desde los contratos recuperados y ejecuta código nuevo de construcción de comandos, manteniendo la conexión cerrada. No se ejecutan ensamblados recibidos ni consultas contra CMI.

La fuente `RRHHClass.cs` de v2 sustituye una de las doce fuentes de v1 durante la compilación; se añaden dos helpers. No se duplica ni modifica el settings cifrado. Los hashes de las DLL diagnósticas no significan equivalencia binaria con el legado.
