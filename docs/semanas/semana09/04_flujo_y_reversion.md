# Flujo de gestión y reversión del cambio

El flujo aplica ocho etapas al alcance diagnóstico del RRHH. KirderFaid13 es el responsable declarado de revisar e integrar. El agente realiza análisis, implementación y comprobaciones bajo la autorización del usuario. Esas acciones no acreditan un CAB ni una revisión independiente. No existe una regla automática de CI configurada por esta entrega.

## Ocho etapas y sus salidas

1. **Solicitar.** Registrar ID, necesidad, origen verificable, tipo y criterios en el formato y abrir su Issue. Salida: solicitudes CAM-S09-001, 002 y 003, vinculadas a #10, #11 y #12.
2. **Analizar.** Revisar código y contrato, identificar causas y alternativas. En 001 se observa un recurso `IDisposable` creado sin liberación explícita; no se inventa un incidente productivo.
3. **Evaluar impacto.** Identificar componentes afectados, riesgos, dependencias, compatibilidad, pruebas y reversión. Registrar en la matriz; las prioridades son propuestas.
4. **Decidir.** Aceptar, rechazar o aplazar con motivo y responsable. El usuario autorizó la práctica completa y la publicación; bajo ese alcance se selecciona 001. Las propuestas 002 y 003 siguen pendientes. Rechazar o aplazar no equivale a implementar.
5. **Planificar.** Fijar base `6c13e74`, rama `semana-09-gestion-cambios`, fuente v5, criterios y salidas privadas. No añadir cambios nulos/timeout al alcance de 001. No estimar horas sin trabajo de estimación.
6. **Implementar.** Se añadió el generador v5 con `using`, conservando v1–v4. Asociar el commit y el PR a #10 cuando existan. El diff debe permitir distinguir código, pruebas, documentación y presentación.
7. **Verificar.** El resultado local fue v4 con 4/6 y dos fallos esperados de liberación, v5 con 6/6 y regresión con 16/16, con salidas nuevas S09 y sin SQL. La verificación de alcance comprobó 516 blobs históricos protegidos, ausencia de cambios adicionales en el generador y exclusiones. Es una comprobación del árbol de trabajo, no del índice futuro de Git. Un PASS automático no representa una aprobación humana.
8. **Registrar y cerrar.** Publicar un PR descriptivo con evidencia y límites, integrar mediante squash y verificar commit, árbol y estado final. Cerrar #10 tras la incorporación comprobada; mantener #11 y #12 abiertas. Actualizar enlaces públicos y detener el trabajo hasta la siguiente indicación.

## Estados y decisiones

El recorrido normal es `registrada → analizada → seleccionada → implementada_localmente → verificada → incorporada → cerrada`. La transición a verificada necesita resultados efectivos; 001 ya alcanzó esa etapa local con la evidencia S09. La transición a incorporada requiere comprobar GitHub y sigue pendiente en este registro.

Desde análisis/decisión pueden aparecer estas salidas:

- **Pendiente:** todavía no se ha decidido si implementar. Es el estado de 002 y 003.
- **Aplazada:** se decidió diferir con motivo y condición de reanudación; no se atribuye este acuerdo a las propuestas actuales sin una decisión expresa.
- **Rechazada:** se descarta con una razón registrada; no se elimina su historial.
- **Requiere ajustes:** vuelve a análisis o implementación si falla un criterio. No se cierra como completada.

Las fechas son las reales del trabajo, comenzando el 15 de octubre de 2026. No se reconstruyen aprobaciones semanales ficticias. El registro JSON conserva el momento de preparación; el historial de la Issue y el PR acredita las decisiones posteriores.

## Reversión prevista para CAM-S09-001

Esta práctica cambia código diagnóstico, sin migraciones ni escrituras SQL. La reversión se limita al generador y a su selección en la compilación; no requiere restaurar la base de datos. La referencia anterior está conservada en `src/v4/caso_ioc/GeneradorReportes.cs` y en la base C07.

**Disparadores:** un resultado deja de ser utilizable, cambia una excepción, se libera el comando antes de terminar la ejecución o aparece una regresión que no puede corregirse dentro del alcance. Una falla del entorno de compilación debe diagnosticarse antes de atribuirla al cambio.

Procedimiento propuesto:

1. Registrar el motivo en #10 o abrir una solicitud correctiva vinculada si C07 ya está cerrada; conservar la evidencia del fallo.
2. Crear una rama de reparación desde el estado publicado. Preparar un parche acotado que restaure el cuerpo anterior de `Generar`, tomando v4 como referencia, y documentar que vuelve la ausencia de liberación explícita.
3. Mantener disponibles las fuentes, las solicitudes y la evidencia de C07. No revertir toda la entrega por defecto, porque también incluye documentación y propuestas independientes.
4. Compilar y repetir los escenarios de comportamiento en salidas privadas/nuevas. El criterio de liberación dejaría de cumplirse en la reversión; ese resultado debe registrarse como una limitación aceptada de la marcha atrás, no ocultarse como PASS.
5. Presentar el parche y la evidencia mediante un nuevo PR para revisión e integración del responsable. Comprobar el estado publicado y actualizar el registro.

No se ejecuta `git revert` sobre `main` para demostrar este plan. Una simulación, si se realiza, debe ocurrir con archivos/parches privados en `.local/c07/`, conservando el árbol de trabajo y la evidencia histórica. Hasta que exista su resultado no se declara una reversión probada. El plan no cubre recuperación productiva, CMI ni datos.
