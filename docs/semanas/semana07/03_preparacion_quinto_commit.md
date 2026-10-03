# Quinto commit: semana 07, v4 IoC

Esta entrega parte de `7bd215a` en la rama `semana-07-ioc`. Los cuatro commits anteriores conservan sus contenidos. Después de revisar código, pruebas y presentaciones, el equipo autorizó crear el quinto commit, subir la rama, abrir una solicitud de cambios e integrarla en `main` mediante squash. El historial de Git y la solicitud de cambios registran los identificadores reales y el resultado de publicación.

## Qué cambia, dónde y por qué

En v3, `GeneradorReportes` guardaba un `EjecutorReportesSql` concreto y lo creaba en su constructor. Por ello, llamar a `Generar` obligaba a usar esa ejecución SQL. La consigna de semana 07 pide identificar y mejorar una dependencia directa mediante inversión de control.

El caso activo está en `src/v4/caso_ioc/`:

- `IEjecutorReportes.cs` define el contrato de ejecución: recibir un `ComandoReporte` y devolver un `DataSet`.
- `GeneradorReportes.cs` guarda esa interfaz y recibe el ejecutor por constructor. `Preparar` y `Generar` conservan sus cuerpos.
- `EjecutorReportesSql.cs` implementa la interfaz conservando su constructor y el cuerpo de ejecución anterior.
- `ComposicionReportes.cs` crea el ejecutor SQL y lo entrega al generador, con la misma conexión y el adaptador actuales.
- `RRHHClass.cs` adapta únicamente los dos cuerpos públicos de reportes para utilizar esa composición. Sus firmas y el resto de su código se conservan.

La mejora permite escoger la implementación fuera del generador y usar un sustituto para probar su flujo completo sin SQL. Aplica inyección de dependencias por constructor y composición manual; el caso no necesita un contenedor.

El constructor público del generador cambia deliberadamente de `(SqlConnection, SqlDataAdapter)` a `(SqlConnection, IEjecutorReportes)`. Los puntos de creación del caso se adaptaron. No se presenta esta biblioteca como sustitución binaria de la DLL original.

## Qué se comprobó

La biblioteca acumulativa de 22 fuentes y el harness de 10 compilan con salida 0, sin errores ni advertencias. Se aprobaron 16 escenarios:

- Once entradas de caracterización recuperadas de v1 pasan por `Generar` con un sustituto. Conservan procedimiento, tabla y propiedades de parámetros; comprueban una llamada y la identidad del `DataSet` devuelto.
- Cinco escenarios comprueban ejecutores distintos en dos instancias del generador, preparación sin ejecución, propagación del error del sustituto, composición SQL sin abrir conexión y fallo de preparación sin llamar al ejecutor.

El verificador comprueba los cambios mínimos, las fuentes compiladas y los hashes de ocho antecedentes. Las versiones previas y el legado se preservan. El borrador v4 recibido queda separado en `src/v4/antecedentes/` y no participa en la compilación activa.

Continúan pendientes la ejecución real contra CMI, la interfaz y la equivalencia funcional completa. `SqlConnection` y `SqlCommand` siguen presentes; el ejecutor SQL conserva su gestión manual de conexión y su comportamiento ante fallos. Los datos de las pruebas son sintéticos.

## Documentación que acompaña el cambio

El [informe](01_ioc.md) explica el antes/después y sus límites. Las [evidencias](../../../evidencia/semanas/semana07/README.md) conservan procedencia, hashes, comparación y resultados. El [contrato C05](../../../specs/c05_ioc.json) delimita el trabajo y el [prompt](../../../prompts/04_ioc.md) permite continuar su revisión. El contexto y los índices del repositorio reflejan esta etapa.

La exposición presenta exclusivamente el caso IoC: [PowerPoint editable de seis diapositivas](Semana07_IoC_RRHH.pptx), [vista previa](vista_previa.png) y [guion de 4:45](02_guion_exposicion.md). La presentación local es un entregable completo; cualquier diseño en Canva se registra por separado y no se atribuye a un exportado de Canva.

Canva creó también un diseño de seis diapositivas. Se corrigieron seis nombres y fragmentos de código, se mostró el borrador al responsable y se guardaron con su aprobación explícita; la consulta posterior comprobó esas correcciones. La diapositiva «Antes» quedó como imagen y no es editable como texto; su exactitud no se verifica mediante la API de texto. Canva no generó notas. El PPTX local conserva código, diagrama y seis notas editables, con revisión visual de sus seis renders. El [registro de presentación](../../../evidencia/semanas/semana07/presentacion.json) distingue ambos entregables y sus estados. Los enlaces de acceso y vistas previas de Canva permanecen fuera del repositorio público.

## Mensaje del commit

```text
refactor(rrhh): aplicar IoC a la ejecución de reportes en semana 07

GeneradorReportes creaba EjecutorReportesSql y fijaba su ejecución.
Introducir IEjecutorReportes e inyectarlo por constructor permite elegir
el ejecutor fuera del generador y probar Generar completo con sustitutos.

Añadir ComposicionReportes y adaptar los dos cuerpos de reportes de la
fachada. Conservar sus firmas, el resto del código y el constructor/cuerpo
SQL; reutilizar las definiciones y comandos OCP de v3 y los helpers v2.
Documentar el cambio intencional del constructor público del generador.

Compilar 22 fuentes de biblioteca y 10 del harness sin errores ni avisos.
Aprobar 16 escenarios sin abrir SQL: once entradas de caracterización y
cinco casos de sustitución, preparación, composición y propagación de fallos.
Conservar los ocho antecedentes v4 por hash fuera de la compilación activa.

Añadir informe, contratos, evidencias, prompt, presentación editable y guion.
Actualizar contexto e índices para explicar qué cambia, por qué y su alcance.
Mantener legado y C01-C04 intactos; excluir claves y artefactos locales.

La integración CMI, la interfaz y la equivalencia completa quedan pendientes.
El caso sigue utilizando SqlClient y conserva la política SQL anterior.
```

## Incorporación y criterio de cierre

La incorporación autorizada sigue este orden: comprobar fuentes y exclusiones; crear un commit con el mensaje anterior; subir `semana-07-ioc`; abrir un PR descriptivo hacia `main`; revisar su diferencia y el estado de comprobaciones; integrar mediante squash utilizando el mismo título y cuerpo descriptivo.

El cierre exige verificar que `main` contiene cinco commits, que los cuatro anteriores no cambiaron, que el árbol integrado coincide con la entrega revisada y que no se publicaron claves, configuraciones restauradas ni archivos locales. Después se explica esta etapa y se espera la siguiente indicación del equipo. La rama semanal se conserva para consultar el PR y su revisión.

[preparacion.json](../../../evidencia/semanas/semana07/preparacion.json) y los indicadores de preparación en [presentacion.json](../../../evidencia/semanas/semana07/presentacion.json) son comprobaciones históricas anteriores al commit: sus cuatro commits y campos de publicación pendientes describen ese momento. El resultado actual de publicación se consulta en [GitHub](https://github.com/KirderFaid13/RRHH-EvolucionSoftware/commits/main/) y en el PR. No se crean commits adicionales únicamente para insertar en el propio contenido el hash que Git calculará después.
