# Guion expositivo — Semana 09: gestión del cambio

Presentación de 26 páginas: 15 de teoría y 11 del caso RRHH. Duración orientativa de 25 min 20 s; ajustar el ritmo durante el ensayo. El tiempo no se obtiene solo de leer texto: incluye explicar los ejemplos, señalar el código y recorrer la evidencia.

## Cómo prepararlo

Primero entiende para cada página su idea y ejemplo. Después explícalos mirando solo el título. El guion es apoyo para hablar con tus palabras. Reparto sugerido: un integrante explica teoría y el otro el práctico; pueden intercambiar roles durante las preguntas.

El DOCX del compañero se conserva intacto. Las referencias y precisiones técnicas de esta exposición constan en las notas de la PPTX. Las pruebas son aisladas y usan datos sintéticos, sin SQL.

## 01. Gestión del cambio en software

**Idea:** Una modificación necesita motivo, alcance, decisión y evidencia.

**Ejemplo:** CAM-S09-001: gestionar la liberación de un comando de reporte.

**Qué explicar (50 s):**

Hoy explicaremos cómo gestionar una modificación de software y lo aplicaremos a nuestro RRHH. El proyecto parte de un sistema de 2008 y avanza mediante mejoras semanales. Esta semana seguimos una solicitud concreta: definir quién libera el comando que utiliza el generador de reportes. Veremos cómo reconocer el problema, evaluar su impacto y presentar una solución comprobable. También registraremos dos propuestas que todavía no implementamos. La diferencia importa: identificar una mejora no significa que ya esté terminada. La exposición relaciona conceptos con decisiones reales y termina mostrando dónde consultar el código, las pruebas y el seguimiento en GitHub.

## 02. Qué cambia y por qué lo controlamos

**Idea:** El análisis de dependencias permite delimitar una modificación.

**Ejemplo:** Corregir la propiedad del comando sin alterar conexiones, consultas ni resultados.

**Qué explicar (65 s):**

Un cambio puede modificar código, configuración, documentación o datos. Su tamaño aparente no determina todo su impacto. En nuestro caso, el generador prepara un comando, lo entrega a un ejecutor y devuelve un DataSet. Si queremos liberar ese comando, debemos conocer quién lo creó, quién lo utiliza y cuándo termina su uso. Cerrar además la conexión podría introducir otro comportamiento porque pertenece al llamador. Controlar el cambio significa delimitar esta responsabilidad y comprobar que conservamos el resultado y los errores esperados. Así protegemos la mantenibilidad sin prometer que una modificación pequeña elimina todos los riesgos del sistema completo.

## 03. Cambio correctivo

**Idea:** Corrige un defecto identificable mediante una comprobación.

**Ejemplo:** En Generar, delimitar ComandoReporte con using y preservar el DataSet devuelto.

**Qué explicar (50 s):**

El cambio correctivo responde a un defecto que podemos identificar. En el código v4, Generar obtiene un ComandoReporte y lo entrega al ejecutor sin delimitar su liberación. Esa clase implementa IDisposable, por lo que necesitamos una responsabilidad explícita sobre su ciclo de vida. La solicitud CAM-S09-001 propone que Generar lo libere al finalizar la ejecución síncrona, tanto si termina correctamente como si el ejecutor lanza una excepción. No afirmamos haber observado una fuga en producción. El defecto y su corrección se estudian en el código y mediante pruebas aisladas. En la parte práctica veremos la evidencia disponible y sus límites.

## 04. Cambio adaptativo

**Idea:** Responde a una modificación externa al sistema.

**Ejemplo:** Caso hipotético de adaptación a un proveedor, ajeno a las tres solicitudes implementadas o propuestas.

**Qué explicar (50 s):**

Un cambio adaptativo aparece porque cambia el entorno del software. Imaginemos que un proveedor anuncia el retiro de su API de autenticación v1. Aunque nuestra integración todavía funcione, debemos adaptar el cliente a v2 antes del retiro. Evaluaríamos el contrato de solicitudes, las respuestas y los errores, y comprobaríamos que los usuarios mantienen el acceso previsto. El motivo principal es la evolución de una dependencia externa. Este ejemplo es ilustrativo: no afirmamos que nuestro RRHH utilice esa API ni que esta semana hayamos cambiado su autenticación. Así distinguimos una categoría del mantenimiento de los cambios que realmente registramos en el proyecto.

## 05. Cambio perfectivo

**Idea:** Amplía una capacidad útil con criterios definidos.

**Ejemplo:** Configurar el tiempo de espera de un reporte sin atribuirle mejoras de rendimiento no medidas.

**Qué explicar (50 s):**

El cambio perfectivo mejora una capacidad según una necesidad. Nuestra propuesta CAM-S09-003 estudia permitir configurar CommandTimeout para un reporte, conservando un valor predeterminado compatible. Esto permitiría expresar una política de espera, pero no demuestra que una consulta sea más rápida. Antes de implementarlo debemos definir las unidades, los valores permitidos y el comportamiento ante entradas inválidas. También tendríamos que comprobar que la configuración llega al comando correcto. La Issue número doce conserva esta propuesta como pendiente. La clasificación describe su propósito principal. Una misma entrega puede combinar correcciones y mejoras, siempre que identifiquemos y justifiquemos cada alcance por separado.

## 06. Cambio preventivo

**Idea:** Reduce el riesgo de errores futuros mediante una mejora delimitada.

**Ejemplo:** Una dependencia nula produciría un error claro al construir el generador, según un contrato futuro.

**Qué explicar (50 s):**

El cambio preventivo busca reducir riesgos antes de que provoquen fallas difíciles de diagnosticar. CAM-S09-002 propone validar argumentos nulos al entrar al generador. Por ejemplo, una dependencia inválida podría rechazarse mediante ArgumentNullException en un punto claramente documentado. Debemos tener cuidado: adelantar un error o cambiar su tipo modifica el comportamiento y necesita un contrato, pruebas y decisión explícita. Esta propuesta permanece pendiente y no se incorpora dentro de la corrección del comando. Además, la inyección de dependencias ya existe desde semana siete. Esta semana no debemos atribuirnos otra vez esa refactorización al explicar una mejora preventiva diferente.

## 07. Las ocho etapas del cambio

**Idea:** Cada etapa responde una pregunta distinta y conserva evidencia.

**Ejemplo:** La solicitud de liberar el comando conserva su vínculo con implementación y comprobaciones.

**Qué explicar (65 s):**

El proceso ordena una necesidad hasta su cierre. La solicitud describe qué problema queremos resolver. El análisis considera causas y alternativas. El impacto identifica componentes afectados y riesgos. La decisión puede aprobar, posponer o rechazar con un motivo. Después planificamos responsables, criterios y contingencia. La implementación concreta la solución y la verificación contrasta sus resultados con lo acordado. Finalmente registramos e integramos la entrega, conservando sus evidencias. En RRHH seguimos ese recorrido con CAM-S09-001. Las otras dos solicitudes también tienen análisis y seguimiento, aunque permanezcan propuestas. No es necesario implementar todo lo registrado para demostrar que gestionamos correctamente su estado.

## 08. Análisis de impacto

**Idea:** El alcance incluye responsabilidades y efectos que deben conservarse.

**Ejemplo:** Liberar el comando al finalizar Generar, sin invalidar el DataSet ni apropiarse de recursos compartidos.

**Qué explicar (55 s):**

El análisis de impacto responde hasta dónde llega nuestra modificación. Generar prepara el comando para usarlo dentro de una ejecución síncrona, así que puede delimitar su vida. Preparar, en cambio, entrega el comando al llamador, que podría necesitarlo después. Liberarlo antes de devolverlo rompería ese contrato. También distinguimos el comando de la conexión y del adaptador, porque no debemos apropiarnos de recursos compartidos. Por eso comprobamos que el comando siga disponible durante Ejecutar y se libere después, mientras el DataSet devuelto conserva su identidad y utilidad. La excepción del ejecutor debe propagarse como antes. Estos límites guían la revisión técnica del cambio.

## 09. Roles y decisiones

**Idea:** Las funciones se distribuyen según el tamaño y riesgo del equipo.

**Ejemplo:** El responsable evalúa incorporar CAM-S09-001 y conservar 002 y 003 como propuestas.

**Qué explicar (50 s):**

Los roles aclaran responsabilidades, aunque un equipo pequeño puede reunir varias funciones en una persona. El solicitante explica la necesidad. El responsable decide prioridad y alcance. El desarrollador presenta la solución. La revisión técnica examina el código y QA contrasta los criterios de aceptación. El integrador incorpora la entrega. En nuestro proyecto, el responsable indicó que él revisa e integra los cambios. Esto no acredita una revisión de otra persona ni un comité formal. En organizaciones de mayor criticidad puede intervenir un comité de cambios. El control adecuado depende del contexto, y debemos representar lo que nuestro equipo realmente hace y registra.

## 10. Git y GitHub en el proceso

**Idea:** Las herramientas relacionan necesidad, propuesta y modificación concreta.

**Ejemplo:** Recorrer desde la Issue de la corrección hasta el diff, las pruebas y el commit que se integra.

**Qué explicar (50 s):**

Git conserva versiones y GitHub permite alojar el proyecto y organizar colaboración. La Issue explica el problema y su estado. La rama separa el trabajo mientras preparamos la solución. El commit registra cambios concretos y el Pull Request muestra el conjunto que proponemos integrar. Los enlaces permiten seguir esa relación sin depender de conversaciones externas. Un mensaje como fix puede comunicar que corregimos un defecto, pero su contenido debe explicar la modificación. El historial permite inspeccionar versiones y diferencias, aunque puede reescribirse bajo ciertas operaciones. Por eso evitamos llamarlo imposible de alterar o presentarlo como una garantía absoluta de autoría.

## 11. Solicitud y criterios de aceptación

**Idea:** Una petición evaluable especifica el resultado y sus límites.

**Ejemplo:** Verificar éxito y excepción, en lugar de aceptar únicamente que el código compila.

**Qué explicar (50 s):**

Una solicitud útil permite decidir cuándo el trabajo está terminado. En CAM-S09-001 describimos el problema y fijamos criterios observables. El comando debe existir mientras el ejecutor lo utiliza y liberarse después, tanto en éxito como ante excepción. El resultado debe conservarse y la excepción debe propagarse sin sustitución intencional. También delimitamos lo que no afirmaremos: las pruebas aisladas no demuestran la integración real con CMI. Estos criterios son más precisos que pedir simplemente mejorar los recursos. La plantilla de una Issue facilita reunir motivo, prioridad, impacto, decisión y evidencia. Después podemos revisar si el código y sus pruebas responden realmente a esa petición.

## 12. Revisión y pruebas

**Idea:** La evidencia debe comprobar el cambio y el comportamiento que se conserva.

**Ejemplo:** Comprobar el ciclo de vida del comando y repetir la regresión ya existente.

**Qué explicar (60 s):**

La revisión analiza si el cambio tiene un alcance coherente y si las pruebas observan lo que prometemos. Para este caso necesitamos examinar el ciclo de vida del comando, su disponibilidad durante la ejecución y su liberación al finalizar. Además, repetimos los escenarios de regresión del generador para comprobar comportamientos anteriores. El número final de casos y su resultado deben salir de la evidencia ejecutada, que mostraremos en el bloque práctico. Una compilación exitosa es una comprobación distinta de una prueba aprobada. Los sustitutos permiten aislar la lógica, pero no verifican procedimientos almacenados, datos reales ni el funcionamiento completo del programa original.

## 13. Artefactos y reglas de integración

**Idea:** Una política acordada necesita documentos y, cuando proceda, controles configurados.

**Ejemplo:** Documentar criterios en la solicitud y evidencias en el PR; comprobar por separado si existen checks obligatorios.

**Qué explicar (50 s):**

La gestión se apoya en artefactos sencillos. Una plantilla de Issue ayuda a explicar la necesidad y una de Pull Request reúne el alcance, las pruebas y los pendientes. El registro de cambios comunica qué contiene cada entrega. Las reglas de rama pueden exigir verificaciones o revisiones, pero solo si las configuramos y comprobamos. La integración continua puede ejecutar pruebas automáticamente cuando el proyecto dispone de ese flujo. No debemos confundir una recomendación con una configuración existente. En nuestro caso mostraremos los controles realmente publicados. Las versiones y los mensajes de commit también deben describir la evolución sin atribuir a semanas anteriores trabajo que realizamos ahora.

## 14. Plan de reversión

**Idea:** La contingencia depende del recurso y del entorno afectados.

**Ejemplo:** Si la corrección rompe una comprobación, detener la integración o revertir su commit según el estado real.

**Qué explicar (55 s):**

Planificar la reversión significa saber cómo actuar si la modificación falla. Antes de integrar podemos detener el cambio y corregirlo. Si ya se incorporó, git revert permite registrar un nuevo commit que deshace modificaciones de código. Esto no restaura automáticamente datos, migraciones ni un despliegue en producción. En nuestro caso no modificamos el esquema ni abrimos SQL para probar la corrección, así que debemos describir una contingencia ajustada a ese alcance. Las banderas de funcionalidad permiten activar gradualmente funciones cuando se han diseñado para ello. Son una técnica general, no una capacidad que afirmemos haber añadido al RRHH esta semana.

## 15. Aplicación a nuestro RRHH

**Idea:** El caso real debe permitir recorrer solicitud, decisión, código y evidencia.

**Ejemplo:** Issue #10 sigue la corrección; Issues #11 y #12 conservan propuestas diferenciadas.

**Qué explicar (45 s):**

Hasta aquí relacionamos la teoría con nuestro proyecto. Registramos tres necesidades y seleccionamos una corrección acotada para llevarla al código. Las otras dos permanecen propuestas, porque gestionar el cambio también implica decidir qué dejamos fuera de una entrega. Ahora mostraremos el estado anterior, la solución de v5 y las comprobaciones que efectivamente ejecutamos. Después recorreremos sus registros y enlaces de GitHub. El objetivo es que otra persona pueda entender por qué modificamos el generador y qué evidencia respalda esa decisión. Mantendremos claros los límites: una mejora diagnóstica y pruebas aisladas no equivalen a validar el RRHH completo contra su base de datos real.

## 16. Tres solicitudes, una intervención

**Idea:** Registrar propuestas permite decidir qué implementar y qué conservar pendiente.

**Ejemplo:** El alcance de esta entrega se limita a CAM-S09-001.

**Qué explicar (60 s):**

La práctica pide al menos tres solicitudes relacionadas con RRHH. Registramos las tres en GitHub antes de escribir la nueva implementación. La primera corrige la liberación del comando que crea el generador. La segunda propone validar argumentos nulos. La tercera propone configurar el tiempo de espera. Elegimos la primera porque encontramos una responsabilidad de recurso sin delimitar y podemos comprobar una solución pequeña sin acceder a CMI. Las otras dos continúan abiertas: haberlas identificado no significa que estén aprobadas ni terminadas. Esta distinción demuestra control del alcance. Cada solicitud tiene su motivo, impacto, prioridad propuesta y criterios, y puede seguirse desde la matriz hasta su Issue.

## 17. Matriz de impacto

**Idea:** El impacto se evalúa por cambio, no mediante una etiqueta general de riesgo.

**Ejemplo:** Cada solicitud conserva su propio criterio de aceptación.

**Qué explicar (65 s):**

La matriz compara las tres solicitudes usando los mismos criterios. En la primera cambia el final de vida del comando, con el riesgo de que alguien lo quiera reutilizar después. En la segunda cambiarían el tipo y el momento del error ante un argumento nulo, por lo que habría que revisar los consumidores. En la tercera cambiaría la configuración del comando y necesitaríamos definir límites y un valor predeterminado compatible. No asignamos horas o porcentajes de mejora sin medición. Las prioridades son propuestas para esta práctica. La matriz permite justificar la selección y evita que la corrección inicial se convierta informalmente en tres implementaciones distintas.

## 18. Solicitud CAM-S09-001

**Idea:** Un formato corto debe permitir decidir y verificar el cierre.

**Ejemplo:** Issue #10 concentra el contrato del cambio.

**Qué explicar (65 s):**

Esta es la solicitud que sí ejecutamos. Su origen es la revisión del generador v4, no un incidente reportado por un usuario de producción. El formato identifica el problema, la razón, el alcance y la evidencia que necesitamos. Definimos dos caminos obligatorios: ejecución con resultado y ejecución con excepción. También dejamos claro qué debemos conservar: el mismo DataSet, la misma excepción del ejecutor y la propiedad del recurso cuando alguien usa Preparar directamente. La autorización general del usuario nos permite realizar la práctica y publicarla. La selección técnica queda documentada sin inventar una aprobación de un comité o una revisión independiente que no ocurrió.

## 19. Antes y después de Generar

**Idea:** La modificación de código es pequeña porque el análisis delimitó su alcance.

**Ejemplo:** Un único GeneradorReportes nuevo en src/v5/.

**Qué explicar (90 s):**

El lado izquierdo muestra la ruta anterior: Preparar crea el contenedor del comando y el ejecutor lo utiliza. El método termina sin llamar explícitamente a Dispose sobre el contenedor. A la derecha delimitamos esa responsabilidad con using. El comando permanece disponible durante la llamada síncrona y se libera antes de salir del método, tanto al devolver el resultado como al propagarse un error del ejecutor. No copiamos ni reescribimos toda la aplicación. La biblioteca v5 selecciona este generador y reutiliza los componentes anteriores. Esta es la implementación visible del cambio; la explicación de gestión está en por qué lo solicitamos, qué riesgos evaluamos y cómo lo comprobamos.

## 20. Propiedad del comando

**Idea:** Liberar el comando no significa cerrar la conexión ni destruir el resultado.

**Ejemplo:** Generar libera lo que crea. Preparar entrega la propiedad a su llamador.

**Qué explicar (65 s):**

La pregunta importante es quién conserva la responsabilidad sobre cada recurso. Si llamamos Generar, el método crea el ComandoReporte para la ejecución y lo libera al terminar. Si llamamos Preparar directamente, recibimos el contenedor y debemos liberarlo nosotros. El DataSet devuelto es un objeto distinto: la prueba confirma que sigue siendo el mismo resultado y que podemos leer su tabla sintética. La conexión y el adaptador no pasan a ser propiedad del generador. Existe un límite relevante: el adaptador conserva SelectCommand apuntando al comando dispuesto. Por eso necesitamos revisar posibles consumidores externos antes de integrar esta biblioteca con la interfaz y CMI reales.

## 21. Primero, una prueba que falla

**Idea:** La reproducción conecta el hallazgo de código con una comprobación observable.

**Ejemplo:** La salida 1 del caso rojo confirma el resultado esperado de la reproducción.

**Qué explicar (65 s):**

No comenzamos mostrando solamente pruebas que pasan. Ejecutamos la suite nueva contra el generador anterior para comprobar que detecta precisamente la ausencia de liberación. Cuatro escenarios aprueban y dos fallan: Dispose después del éxito y después del error. La biblioteca y el harness sí compilan, por lo que este resultado no es un fallo de instalación. El ejecutor espía observa el evento Disposed del comando y devuelve datos sintéticos o lanza una excepción controlada. El harness limpia después de observar, para no confundir su propia limpieza con la del generador. Esto reproduce el comportamiento estudiado sin abrir una conexión ni medir una supuesta fuga en producción.

## 22. Corrección y regresión

**Idea:** El cambio debe resolver el defecto y conservar lo que ya estaba comprobado.

**Ejemplo:** Mismo DataSet, misma excepción y Preparar con propiedad del llamador.

**Qué explicar (65 s):**

Con el nuevo generador, la misma suite de ciclo de vida aprueba sus seis escenarios. Además repetimos los dieciséis escenarios de IoC anteriores contra v5. Así comprobamos tanto el objetivo nuevo como los contratos que ya conocíamos. Las pruebas observan que el comando está disponible dentro del ejecutor y que después recibe Dispose. También comprueban la identidad del resultado y de la excepción, y la responsabilidad del llamador al usar Preparar. La biblioteca diagnóstica compila veintidós fuentes reutilizadas y nuevas. Estos números describen escenarios concretos y compilación; no son un porcentaje de cobertura ni demuestran que el sistema completo funcione conectado al servidor.

## 23. Evidencia reproducible

**Idea:** La ejecución y la verificación de evidencia son pasos diferentes.

**Ejemplo:** Las evidencias de semanas anteriores se conservan.

**Qué explicar (60 s):**

Para reproducir el resultado se ejecuta primero compilar_v5.py y después verificar_v5.py. El primer comando compila la selección de fuentes y ejecuta los harness nuevos y de regresión. El segundo comprueba que los hashes, los artefactos y la evidencia corresponden al código actual; también verifica los archivos históricos protegidos y las exclusiones privadas. No usamos los main de las herramientas antiguas porque generarían resultados sobre sus carpetas históricas. Los compilados quedan en .local y los resultados permitidos en evidencia de semana nueve. El verificador conservó quinientos dieciséis blobs protegidos respecto de la base. El índice Git se revisa por separado antes de publicar.

## 24. El seguimiento queda en GitHub

**Idea:** Una solicitud debe permitir recorrer problema, cambio, evidencia e integración.

**Ejemplo:** El PR enlaza la solicitud y su commit de integración.

**Qué explicar (70 s):**

La trazabilidad se puede recorrer en GitHub. Partimos de la Issue diez, donde registramos la solicitud antes de implementar. En la rama semanal aislamos el código, las pruebas y la documentación. El Pull Request trece reúne el diff y explica los resultados y los riesgos. Al integrarlo mediante squash en main, la referencia Closes cierra la solicitud implementada. Las Issues once y doce permanecen abiertas porque no las ejecutamos. Los commits mantienen sus fechas reales. Main es la línea de integración del proyecto académico y no representa un despliegue productivo. El estado definitivo y el identificador del commit pueden comprobarse desde el propio PR.

## 25. Reversión prevista

**Idea:** Una contingencia necesita un procedimiento y límites explícitos.

**Ejemplo:** Esta corrección no contiene migraciones de base de datos.

**Qué explicar (55 s):**

El plan de reversión depende del estado real del cambio. Antes de integrar, una prueba fallida obliga a detenernos y revisar la propuesta. Después de integrar, una reversión debe identificar el commit correcto y crear una nueva revisión, conservando el historial. También requiere recompilar y comprobar el comportamiento restaurado; recuperar archivos por sí solo no verifica funcionamiento. En este caso no hay migraciones ni datos escritos, de modo que no existe una reversión de base asociada. Si otro cambio incluyera datos, necesitaría un procedimiento específico. Este es un plan previsto: no aplicamos una reversión sobre main para aparentar una recuperación que no necesitábamos.

## 26. Qué mejora y qué sigue pendiente

**Idea:** La calidad de la decisión también se demuestra explicando sus límites.

**Ejemplo:** La siguiente decisión se toma con evidencia, sin ampliar informalmente el alcance.

**Qué explicar (65 s):**

Concluimos mostrando el resultado y su alcance. Mejoramos una responsabilidad concreta sobre el comando y demostramos el cambio con pruebas antes y después, más regresión. También aplicamos el proceso de gestión: registramos tres solicitudes, analizamos su impacto, seleccionamos una y conservamos las demás como propuestas pendientes. La integración real con CMI y la interfaz no se ha probado. Tampoco medimos memoria, handles, rendimiento o seguridad. El adaptador y los consumidores no recuperados siguen siendo un punto de revisión. Si el docente pregunta por qué no implementamos las tres, la respuesta es que el enunciado pide identificarlas y evaluarlas, y el control del alcance permite demostrar correctamente una intervención seleccionada.

## Preguntas para defender el caso

1. **¿Por qué es correctivo?** Corrige una responsabilidad de liberación omitida en la ruta estudiada. No afirmamos haber medido una fuga productiva.
2. **¿Por qué tres solicitudes y una implementación?** La consigna pide identificar y evaluar al menos tres; seleccionamos una intervención demostrable y mantenemos las otras abiertas.
3. **¿Qué aporta using?** Delimita Dispose al salir del bloque, también ante el error del ejecutor que comprobamos.
4. **¿Se cierra la conexión?** La corrección dispone el comando, no asume la conexión ni cambia el código de apertura o cierre.
5. **¿Qué pasa con el DataSet?** La prueba confirma que es el mismo objeto devuelto y que su tabla sintética sigue siendo legible.
6. **¿Cuál es el riesgo del adaptador?** SelectCommand conserva una referencia al comando dispuesto. La fachada objDA pública y la interfaz no recuperada requieren revisión de integración.
7. **¿Por qué hay un rojo 4/6?** Las dos ausencias de Dispose son fallos intencionalmente esperados de la reproducción contra v4; el harness compila y ejecuta correctamente.
8. **¿Qué demuestra 6/6 y 16/16?** Seis casos propios de ciclo de vida y dieciséis regresiones concretas aprobadas. No son cobertura porcentual ni validación de todo RRHH.
9. **¿Se probó SQL o producción?** No. No se abrió SQL, no se ejecutó Fill ni la interfaz ni los binarios recibidos.
10. **¿Qué no cubren las pruebas?** Adquisición fallida, Dispose que lanza, concurrencia y reutilización posterior por otros consumidores.
11. **¿Quién aprobó?** El responsable autorizó realizar y publicar la práctica. La selección técnica está documentada; no inventamos CAB ni revisión formal de terceros.
12. **¿Qué hace cada herramienta?** compilar_v5 reproduce los harness; verificar_v5 comprueba evidencia, artefactos, hashes y conservación.

## Ensayo final

Explica sin leer: necesidad, impacto, cambio, evidencia y límites. Recorre Issue #10 y PR #13 para ubicar la implementación; identifica #11 y #12 como propuestas. No ejecutes SQL ni las herramientas antiguas durante la exposición. Si se demuestra en vivo, utiliza exclusivamente los comandos nuevos y el entorno ya documentado.
