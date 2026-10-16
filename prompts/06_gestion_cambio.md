# Revisión acotada — Semana 09: gestión del cambio

Actúa como revisor del RRHH. Lee AGENTS.md, README.md, specs/c07_gestion_cambio.json, configuracion/solicitudes_semana09.json y docs/semanas/semana09/.

1. Comprueba las tres solicitudes, formato, matriz e impacto; distingue implementación y propuesta.
2. Revisa solo CAM-S09-001: Generar v5 dispone ComandoReporte tras la llamada síncrona. Preparar entrega la propiedad al llamador.
3. Coteja evidencia: rojo v4 4/6 con dos fallos esperados; verde v5 6/6 y regresión 16/16; verifica fuentes y artefactos por hashes.
4. Examina riesgos: SelectCommand retenido, objDA público, consumidores no recuperados y límites de adquisición/Dispose/concurrencia.
5. Verifica conservación del legado, fuentes/evidencias anteriores, exclusiones y DOCX intacto.
6. Comprueba Issue #10, PR #13 y commit de integración; #11/#12 deben seguir propuestas.
7. Revisa presentación y guion: ejemplos concretos, sin métricas no medidas ni afirmaciones de producción.

No implementes 002/003, no modifiques originales ni abras SQL o ejecutes binarios recibidos. No ejecutes herramientas históricas que sobrescriben sus evidencias. Reproduce únicamente con compilar_v5.py y verificar_v5.py en el entorno documentado. No publiques nuevos cambios fuera de una tarea autorizada.
