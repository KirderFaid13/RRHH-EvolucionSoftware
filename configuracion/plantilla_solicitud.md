# Formato simple de solicitud de cambio

Usar un registro por cambio y su Issue real. La solicitud describe una necesidad; abrirla no significa que ya esté aprobada o implementada. Completar los campos con información comprobada y marcar los desconocidos como pendientes.

- **ID:** CAM-S09-NNN.
- **Título:** acción concreta y componente afectado.
- **Fecha real y solicitante/origen:** quién lo pide o dónde se identificó; no inventar un usuario de negocio.
- **Problema o necesidad:** comportamiento observado o hallazgo estático, con fuente y límites.
- **Tipo:** correctivo, adaptativo, perfectivo o preventivo; justificar la elección.
- **Cambio solicitado y motivo:** qué se propone y qué beneficio se espera.
- **Alcance:** componentes afectados, dependencias y exclusiones.
- **Impacto y riesgos:** compatibilidad, consecuencias de fallo y datos/sistemas afectados; indicar lo que falta conocer.
- **Prioridad propuesta:** orden relativo y motivo; distinguir de una prioridad aprobada.
- **Criterios de aceptación:** resultados observables para decidir si el cambio cumple.
- **Verificación prevista:** casos, entorno, evidencia esperada y límites; no anotar PASS antes de ejecutar.
- **Decisión y responsable:** pendiente, seleccionada, aplazada o rechazada; fundamento, fecha y autoridad real.
- **Plan y reversión:** rama/base, pasos, responsables, condiciones y manera de volver a la referencia anterior.
- **Estado y trazabilidad:** ID, Issue, fuente, evidencia, commit/PR cuando existan y fecha de cierre.

## Reglas de uso

1. Registrar antes de implementar y actualizar el estado con evidencia.
2. Mantener una solicitud por necesidad; relacionar las dependencias sin mezclar mejoras no aprobadas.
3. No copiar credenciales, datos reales o configuraciones restauradas en la Issue.
4. Usar `null` o «pendiente» para un commit/PR todavía inexistente; no fabricar enlaces.
5. Una prueba aislada no acredita SQL, producción ni una revisión independiente.
6. Conservar solicitudes aplazadas o rechazadas con su motivo y sus fechas reales.

[Solicitudes de semana 09](solicitudes_semana09.json) · [Detalle legible](../docs/semanas/semana09/02_solicitudes.md) · [Matriz](../docs/semanas/semana09/03_matriz_impacto.md) · [Flujo](../docs/semanas/semana09/04_flujo_y_reversion.md).
