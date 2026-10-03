# C05: reproducir y revisar el caso IoC de reportes

Este prompt reproduce la revisión técnica de la entrega de semana 07 sobre C04; no solicita regenerar la mejora, activar borradores recibidos o publicar cambios por sí solo. La incorporación del quinto commit por PR y squash se documenta aparte y fue autorizada por el equipo. [Contrato C05](../specs/c05_ioc.json), [informe](../docs/semanas/semana07/01_ioc.md) y [evidencias](../evidencia/semanas/semana07/README.md).

```text
Actúa como responsable de revisión del caso C05 del sistema RRHH.

Lee AGENTS.md, README.md, .context/ROADMAP.md, el contexto funcional
y del curso, specs/c05_ioc.json, src/v4/README.md y las evidencias
de evidencia/semanas/semana07/. Revisa las cinco fuentes de
src/v4/caso_ioc/, las cuatro fuentes reutilizadas de v3 y los dos
helpers de empleados v2. Conserva la base C04 identificada en el contrato.

Objetivo:
Reproducir y contrastar la inversión de control de la ejecución de
reportes: el generador recibe IEjecutorReportes y la composición crea
SQL fuera de él. Distingue conservación, compilación y flujo ejecutado
con sustitutos de la integración SQL que permanece pendiente.

Trabajo:
1. Contrasta procedencia.json con v3 y sus hashes, y los contratos v1
   reutilizados: firmas object, procedimientos y tablas de oficina,
   @idarea Int y @sigla VarChar. No inventes contratos del servidor.
2. Revisa antes_despues.diff. Confirma solo dos cuerpos de fachada
   modificados, sus firmas y todo el resto conservados; Preparar y
   Generar iguales; constructor y Ejecutar SQL iguales; definiciones
   OCP, comandos y helpers empleados reutilizados sin cambios.
3. Comprueba que GeneradorReportes recibe IEjecutorReportes por su
   constructor y no crea ni selecciona EjecutorReportesSql.
   ComposicionReportes crea SQL y entrega el ejecutor y la conexión.
   Explica IoC, DI por constructor, interfaz y apoyo de DIP en ese
   punto concreto; la composición manual no requiere un contenedor.
4. Con clave local, legado restaurado, Python, SDK .NET 10.0.103 y
   referencias Framework v4.0.30319 instaladas, ejecuta desde la raíz:
   python herramientas/compilar_v4.py
   python herramientas/verificar_v4.py
   No abras SQL, restaures bases o ejecutes binarios recibidos.
5. Contrasta la salida real con los JSON recién generados. La
   referencia registrada es biblioteca de 22 fuentes, harness de 10,
   sin errores/advertencias, 16 escenarios y verificación ok: true.
   Confirma los conteos, hashes y estados del rerun, sin reutilizar
   una evidencia anterior como aprobación actual. La biblioteca
   reúne v1, helpers v2, cuatro fuentes v3 y cinco fuentes v4.
   El harness usa ocho componentes, PruebasIoC.cs y llamadas
   generadas desde contratos v1; solo ejecuta reportes y sustitutos.
6. Comprueba Generar completo con los once valores caracterizados
   en v1: comando, SP, parámetro/tipo/dirección/tamaño/valor,
   tabla, conexión cerrada, una llamada y DataSet por identidad.
   Revisa sustitución por ejecutores diferentes, Preparar sin
   ejecución, error del ejecutor propagado, composición SQL
   preparada sin abrir y fallo de preparación sin llamar al ejecutor.
7. Contrasta las ocho copias de antecedentes contra su manifiesto.
   Son un borrador incompleto, sin contenedor o composición
   implementados; permanecen fuera de compilación y ejecución.
8. Revisa informe y presentación: el antes/después debe corresponder
   al código actual y describir únicamente esta mejora IoC. La guía
   de semana 07, pp.8-11, establece la consigna; p.12 contiene la
   rúbrica. No reproduzcas las conclusiones OCP de su p.13 como IoC.

Límites:
- El constructor público del generador cambia a
  (SqlConnection, IEjecutorReportes); las firmas originales de la
  fachada se conservan. No prometas compatibilidad binaria del helper.
- SqlConnection y SqlCommand permanecen concretos. La mejora
  desacopla el ejecutor propio, sin probar independencia del motor SQL.
- Conserva gestión manual de conexión/comandos y política actual
  de fallos. No añadas using/finally, defaults, DBNull, validaciones,
  normalizaciones, reglas o nuevos reportes dentro de esta revisión.
- Los DataSet de prueba son sintéticos. No acreditan Fill, resultados
  CMI, esquema, permisos, UI, despliegue, framework original o
  equivalencia completa. La fachada y recibidos no se ejecutan.
- Conserva legado, v1/v2/v3 y antecedentes; no edites referencias
  anteriores para hacer pasar verificaciones. Protege secretos y
  artefactos privados en .local/, sin reproducir sus valores.
- No crees ni publiques el quinto commit en esta reproducción.
  Esa acción requiere la indicación posterior del equipo; no cambies
  la rama base publicada ni avances a otra etapa por inferencia.

Entrega:
Explica el problema, los archivos cambiados, la decisión de diseño,
los resultados actuales, fallos y límites. Deja la preparación C05
revisable y detén el trabajo sin publicar el quinto commit.
```
