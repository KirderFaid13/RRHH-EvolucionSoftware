# Evidencia de semana 09 — C07

La base es `6c13e74`. El código nuevo de CAM-S09-001 está en src/v5; las versiones y evidencias anteriores se conservan.

- [Compilación y pruebas](compilacion_y_pruebas.json): biblioteca de 22 fuentes; compilaciones sin errores ni advertencias. Contra v4: 4/6, dos fallos de Dispose esperados, salida 1. Contra v5: 6/6, salida 0. Regresión IoC: 16/16, salida 0.
- [Procedencia del código](procedencia_codigo.json): hashes de fuentes, harness, referencias de compilación y herramienta.
- [Verificación](verificacion_v5.json): cambio mínimo, 516 blobs históricos protegidos y exclusiones privadas. Compara archivos de trabajo; el índice final se comprueba por separado.
- [Procedencia documental](procedencia_documental.json): originales PDF/DOCX/PPTX y portada conceptual. El DOCX no se edita.
- [Presentación](presentacion.json): contenido, notas, renderizados y hash de la entrega final.

Reproducción: primero `python herramientas/compilar_v5.py`, después `python herramientas/verificar_v5.py`. Requiere el entorno descrito en [v5](../../../src/v5/README.md). La inicialización de contadores SqlClient puede necesitar ejecución fuera de AppContainer; no equivale a abrir una conexión.

Disposed observa la invocación de Dispose, no memoria ni handles. No se ejecutaron SQL, Fill, fachada real ni binarios recibidos. El adaptador conserva una referencia al comando dispuesto; consumidores no recuperados, fallos de adquisición/Dispose y concurrencia quedan fuera de estas pruebas. No se acredita equivalencia completa ni revisión humana formal.

La evidencia registra el momento de preparación. La publicación y el cierre se comprueban en [Issue #10](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/10) y [PR #13](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/pull/13). Las [#11](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/11) y [#12](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/issues/12) continúan propuestas.
