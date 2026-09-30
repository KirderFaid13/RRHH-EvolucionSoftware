# Especificaciones por etapa

Esta carpeta contiene contratos vinculados con una etapa del [roadmap](../.context/ROADMAP.md). [C02: ingeniería inversa](c02_ingenieria_inversa.json) delimita la recuperación estática y las comprobaciones de v1. Los contratos se definen en cada etapa y no presuponen un esquema SQL validado.

[C03: SRP/DRY](c03_srp_dry.json) delimita tres consultas reales y su ejecución compartida, con firmas/contratos conservados y pruebas sin SQL. C04/v3 se definirá cuando el equipo indique avanzar.

Antes de intervenir un caso, su especificación deberá indicar:

- El objetivo y el tema académico al que corresponde.
- La versión y los archivos de partida.
- Las evidencias que justifican el caso.
- El cambio permitido y los límites de su alcance.
- El comportamiento que se debe conservar.
- Los resultados esperados y las comprobaciones necesarias.
- Las incógnitas que impiden afirmar una validación completa.

Los contratos pueden usar Markdown o JSON según resulte más claro. No deben presuponer interfaces web, endpoints, roles o tablas que todavía no se hayan recuperado del sistema.
