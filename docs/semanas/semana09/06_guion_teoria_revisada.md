# Guion revisado — Semana 09: gestión del cambio

Presentación de 26 páginas. Tiempo orientativo total: **25 min 20 s**; teoría **13 min 15 s** y caso práctico **12 min 05 s**. El tiempo incluye explicar los ejemplos y señalar los elementos de las diapositivas.

La teoría utiliza una plataforma hipotética de entradas para conciertos. Su regla central es conservar un solo titular y una única credencial vigente por entrada. Suponemos validación de acceso en línea. Es un ejemplo para comprender las decisiones de ingeniería; no describe una implementación ni resultados medidos.

Ensaya cada página con tres apoyos: qué significa el concepto, qué ocurre en el ejemplo y qué consecuencia tiene. Mira el título y explícalo con tus palabras. Las notas amplían la explicación; no es necesario recitarlas.

## 01. Gestión del cambio en software

**Tiempo:** 00:00–00:50 (50 s).

**Idea para recordar:** Una petición de negocio necesita decisiones y comprobaciones antes de llegar a los usuarios.

**Ejemplo concreto:** Una compradora quiere ceder su entrada a otra persona y conservar un único derecho de acceso.

**Cómo explicarlo:**

Imaginemos una plataforma que vende entradas digitales para conciertos. Cada entrada tiene un titular y un código QR que se valida al ingresar. Una compradora pide transferir su entrada a otra persona. Parece suficiente cambiar un nombre, pero debemos impedir que ambos códigos permitan entrar o que dos transferencias simultáneas creen dos titulares. Esta situación es hipotética y nos servirá para explicar los conceptos. Seguiremos la petición desde su origen hasta la publicación y el seguimiento. La pregunta central será qué debemos cambiar, qué condiciones debemos conservar y qué evidencia necesitamos antes de ofrecer la función a los usuarios.

## 02. Qué significa gestionar un cambio

**Tiempo:** 00:50–01:55 (65 s).

**Idea para recordar:** Gestionar una modificación implica evaluar, decidir, implementar y verificar con un registro trazable.

**Ejemplo concreto:** La transferencia debe cambiar quién puede ingresar, manteniendo una sola entrada válida.

**Cómo explicarlo:**

La gestión del cambio es el proceso que permite evaluar una modificación, decidir si conviene realizarla y comprobar su resultado. Puede afectar código, configuración, datos o documentación. En el ejemplo, necesitamos cambiar quién tiene derecho a ingresar y conservar una sola entrada válida. Supondremos que el lector consulta en línea el estado vigente. Por eso debemos considerar la pantalla, el servicio que procesa la transferencia y el control de acceso. Registrar estas relaciones permite conocer el motivo de una decisión y revisar después si se cumplió. La disciplina ayuda a reducir regresiones, cambios fuera de alcance y problemas de mantenimiento durante la evolución del producto.

## 03. Cambio correctivo

**Tiempo:** 01:55–02:45 (50 s).

**Idea para recordar:** Su propósito principal es corregir un comportamiento que incumple lo esperado.

**Ejemplo concreto:** Un QR consumido vuelve a aceptarse. La prueba debe reproducir ese segundo ingreso y confirmar su rechazo.

**Cómo explicarlo:**

Un cambio correctivo repara un defecto: existe un comportamiento que incumple una condición esperada. En nuestra plataforma hipotética, una entrada utilizada vuelve a ser aceptada por el lector. La condición acordada era que esa entrada permitiera un único ingreso. Primero reproducimos el problema y comprobamos qué causa el segundo acceso. Después corregimos el control correspondiente y repetimos el caso. También verificamos que una entrada válida todavía permita el primer ingreso, para detectar una posible regresión. El motivo principal de esta modificación es reparar el fallo identificado. El ejemplo ayuda a distinguir la causa del cambio de la herramienta o técnica elegida para resolverlo.

## 04. Cambio adaptativo

**Tiempo:** 02:45–03:35 (50 s).

**Idea para recordar:** Su propósito principal es conservar la utilidad del sistema frente a un cambio de su entorno.

**Ejemplo concreto:** El proveedor modifica su contrato de comunicación. La aplicación debe adaptarse para seguir procesando compras.

**Cómo explicarlo:**

Un cambio adaptativo responde a una modificación del entorno en el que funciona el software. Supongamos que el proveedor de pagos anuncia que retirará su API v1. Una API es el contrato de comunicación entre nuestra aplicación y ese servicio. Aunque las compras todavía funcionen, debemos adaptar la integración antes de que desaparezca la versión anterior. Revisamos los campos enviados, las respuestas y el tratamiento de errores. Después comprobamos que el comprador pueda completar o cancelar una operación según lo esperado. La necesidad nace del proveedor externo. Este ejemplo es hipotético y no presupone un servicio comercial concreto ni una fecha real de retiro.

## 05. Cambio perfectivo

**Tiempo:** 03:35–04:25 (50 s).

**Idea para recordar:** Su propósito principal es mejorar una capacidad o experiencia de uso.

**Ejemplo concreto:** La transferencia evita recomprar una entrada al cambiar de asistente, sin crear un derecho de acceso adicional.

**Cómo explicarlo:**

En la clasificación del curso, un cambio perfectivo mejora una capacidad del sistema o la experiencia del usuario. Nuestra plataforma ya permite comprar entradas, pero ahora se solicita transferir una a otra persona. La nueva capacidad debe respetar reglas claras: la entrada conserva un único titular y solamente el código vigente permite ingresar. Transferir no aumenta el aforo ni crea una compra adicional en este ejemplo. Esas condiciones delimitan el resultado esperado. El propósito principal es atender una necesidad adicional. Usamos las cuatro categorías del curso para explicar motivaciones; no estamos afirmando que sean la única clasificación posible de todo el mantenimiento de software.

## 06. Cambio preventivo

**Tiempo:** 04:25–05:15 (50 s).

**Idea para recordar:** Su propósito principal es reducir el riesgo de fallas futuras y facilitar el mantenimiento.

**Ejemplo concreto:** Una regla duplicada puede evolucionar de forma distinta en dos clientes. Una política común reduce ese riesgo.

**Cómo explicarlo:**

Un cambio preventivo reduce riesgos antes de que se manifiesten como fallas para el usuario. Imaginemos que la web y la aplicación móvil contienen copias de la misma regla de acceso. Hoy responden igual, pero una futura modificación podría actualizar una copia y olvidar la otra. Proponemos centralizar la política y comprobar que ambas vías conserven sus respuestas actuales. La finalidad es facilitar el mantenimiento y reducir esa posible divergencia. Debemos definir qué comportamiento se conserva y verificarlo con pruebas de regresión. Cambiar la organización del código requiere cuidado: llamar preventivo al trabajo no garantiza que automáticamente sea seguro o que mejore cualquier atributo del sistema.

## 07. Las ocho etapas del cambio

**Tiempo:** 05:15–06:20 (65 s).

**Idea para recordar:** Cada etapa responde una pregunta distinta y permite justificar la siguiente decisión.

**Ejemplo concreto:** La misma petición conserva su identidad mientras se analiza, decide, desarrolla y comprueba.

**Cómo explicarlo:**

La solicitud describe la necesidad. El análisis estudia el problema y sus alternativas. La evaluación de impacto identifica componentes afectados, riesgos y esfuerzo. Con esa información, la autoridad responsable aprueba, aplaza o rechaza el cambio. La planificación define cómo ejecutarlo y qué hacer si falla. La implementación realiza la modificación y la verificación contrasta su comportamiento con los criterios acordados. El registro enlaza la decisión, el cambio y sus pruebas. Tras verificar y registrar la aceptación de la entrega, se cierra la solicitud; el seguimiento operativo puede continuar. En la transferencia de entradas debemos recorrer estas preguntas, aunque el equipo use herramientas ligeras. No basta con abrir una tarea y programar: las decisiones intermedias justifican el alcance y las comprobaciones elegidas.

## 08. Solicitud y criterios de aceptación

**Tiempo:** 06:20–07:15 (55 s).

**Idea para recordar:** Una petición útil describe la necesidad y permite reconocer cuándo el resultado es aceptable.

**Ejemplo concreto:** Una solicitud evaluable fija lo que debe pasar y también las capacidades que no incluye la entrega.

**Cómo explicarlo:**

La solicitud de cambio transforma una petición informal en un trabajo que podemos evaluar. Debe explicar el problema, la justificación, el alcance y los criterios de aceptación. Para la transferencia, la necesidad es ceder una entrada sin comprar otra. El criterio principal establece que el nuevo titular puede ingresar y el código anterior deja de ser válido. También excluimos reventa, devolución y cambio de asiento. Así evitamos que cada participante imagine una función diferente. Una plantilla de solicitud ayuda a registrar esta información, pero el valor está en su precisión. Si el criterio no permite decidir si el resultado es correcto, debemos aclararlo antes de implementar.

## 09. Análisis de impacto

**Tiempo:** 07:15–08:05 (50 s).

**Idea para recordar:** Identifica qué puede verse afectado, qué riesgo introduce el cambio y cuánto esfuerzo exige.

**Ejemplo concreto:** Una transferencia puede afectar datos y validación de acceso aunque el cambio visible sea un botón.

**Cómo explicarlo:**

El análisis de impacto identifica las consecuencias directas e indirectas de una modificación. En nuestro caso cambian el titular y el estado de la entrada, y el lector debe reconocer únicamente el código vigente. El cobro original se conserva porque esta propuesta no añade una compra. También aparece un riesgo de concurrencia: dos peticiones podrían intentar transferir la misma entrada al mismo tiempo. Necesitamos decidir cómo actualizar sus datos de forma coherente y aceptar una sola operación. Además estimamos el esfuerzo para modificar, probar y publicar los componentes relacionados. Este análisis permite comparar alternativas y detectar cuándo una petición aparentemente pequeña tiene efectos importantes sobre el sistema.

## 10. Roles y decisión del cambio

**Tiempo:** 08:05–08:55 (50 s).

**Idea para recordar:** La responsabilidad de decidir se apoya en información de negocio, tecnología y calidad.

**Ejemplo concreto:** La decisión puede aplazar la función cuando el riesgo de admitir dos códigos todavía no tiene respuesta comprobable.

**Cómo explicarlo:**

Los roles reparten responsabilidades. El solicitante explica la necesidad, negocio establece su prioridad, desarrollo evalúa la solución y calidad define cómo comprobarla. La autoridad responsable decide si procede y deja una justificación. En un equipo pequeño puede ser una persona asignada; en contextos de mayor criticidad puede intervenir un comité. La prioridad indica qué conviene atender primero, la urgencia expresa el plazo y el riesgo combina la posibilidad de un problema con sus consecuencias. Por ejemplo, la transferencia puede ser prioritaria y aun así aplazarse si permite dos accesos. Revisar pruebas aporta información a la decisión, pero no sustituye la responsabilidad de autorizarla.

## 11. Planificación de la implementación

**Tiempo:** 08:55–09:45 (50 s).

**Idea para recordar:** Convierte una decisión aprobada en trabajo ordenado con responsables, dependencias y contingencia.

**Ejemplo concreto:** Preparar el validador antes de habilitar transferencias reduce el riesgo de publicar componentes incompatibles.

**Cómo explicarlo:**

Planificar significa ordenar el trabajo antes de modificar el producto. Debemos asignar responsables, identificar dependencias, estimar esfuerzo y fijar condiciones de publicación y recuperación. En el ejemplo, primero preparamos un lector compatible con el estado vigente de la entrada. Después implementamos la transferencia y la actualización coherente de titular y código. La función se activa cuando los componentes necesarios están listos y comprobados. El desarrollo puede aislarse en una rama y organizarse en cambios pequeños con mensajes claros. Una revisión del código ayuda a detectar efectos inesperados. Este orden evita entregar por separado partes que solamente funcionan correctamente cuando se utilizan juntas.

## 12. Verificación y pruebas

**Tiempo:** 09:45–10:45 (60 s).

**Idea para recordar:** Comprueba la nueva necesidad y los comportamientos anteriores que deben conservarse.

**Ejemplo concreto:** La prueba incluye transferencia, validación de acceso y dos peticiones concurrentes, además de la compra habitual.

**Cómo explicarlo:**

La verificación contrasta el resultado con los criterios acordados. Las pruebas de una regla pueden revisar qué estados permiten transferir. Una prueba de integración comprueba que los componentes y sus datos se actualicen de forma coherente. Una prueba de concurrencia envía dos solicitudes sobre la misma entrada y comprueba que solamente una se acepte. También repetimos compra y acceso habituales para buscar regresiones. Cada prueba debe expresar su entrada, el resultado esperado y la evidencia obtenida. Un flujo de integración continua puede automatizar comprobaciones si está configurado. Que una herramienta indique éxito no elimina la necesidad de revisar si realmente evaluamos los riesgos y condiciones de aceptación.

## 13. Publicación y plan de reversión

**Tiempo:** 10:45–11:35 (50 s).

**Idea para recordar:** Publicar pone el cambio en servicio y la contingencia debe proteger también los datos ya modificados.

**Ejemplo concreto:** Pausar nuevas transferencias no debe reactivar códigos anteriores de entradas ya transferidas o utilizadas.

**Cómo explicarlo:**

Publicar significa poner la modificación a disposición de los usuarios. Integrar un cambio en el repositorio es una acción distinta del despliegue y la activación del servicio. Podemos planificar una activación gradual y observar errores de transferencia o rechazo de entradas. Si aparece un problema, una contingencia razonable podría pausar nuevas transferencias mientras se investiga, conservando las ya confirmadas. No debemos reactivar códigos anteriores de entradas transferidas o utilizadas. Revertir código mediante Git registra otra modificación, pero no restaura automáticamente los datos ni corrige cada efecto operativo. El plan de recuperación debe respetar los derechos de acceso y ser compatible con el estado que ya existe.

## 14. Trazabilidad y artefactos

**Tiempo:** 11:35–12:30 (55 s).

**Idea para recordar:** Los enlaces entre solicitud, decisión, código y pruebas permiten explicar la historia de una entrega.

**Ejemplo concreto:** Ante un rechazo de QR, el equipo puede localizar qué entrega cambió la regla y qué pruebas respaldaron esa decisión.

**Cómo explicarlo:**

La trazabilidad permite reconstruir por qué existe una modificación y qué comprobaciones la respaldan. La solicitud conserva necesidad, alcance y aceptación. La Issue organiza el seguimiento y el Pull Request presenta el código para revisión. Los commits identifican cambios concretos y el registro de cambios explica el contenido de la entrega. Las evidencias enlazadas muestran qué se comprobó. Si un código QR falla, esta relación ayuda a localizar la versión y la decisión que modificaron la regla. Las plantillas y mensajes claros facilitan la lectura. Las reglas de rama pueden exigir revisiones y pruebas cuando estén configuradas. Las herramientas apoyan el proceso, pero los enlaces deben representar trabajo y decisiones reales.

## 15. Una transferencia gestionada

**Tiempo:** 12:30–13:15 (45 s).

**Idea para recordar:** El resultado de gestionar el cambio es una decisión justificada y una entrega comprobable.

**Ejemplo concreto:** La capacidad nueva debe permitir transferir la entrada sin duplicar titulares, acceso ni aforo.

**Cómo explicarlo:**

Volvamos a la petición inicial: una persona quiere transferir su entrada. Ahora sabemos que gestionar esa petición implica definir las condiciones de aceptación, evaluar datos y dependencias, decidir el alcance y planificar una publicación compatible. Después implementamos, comprobamos estados y concurrencia, y conservamos el vínculo entre la necesidad y su evidencia. La condición que guía todo el caso es mantener un único derecho de acceso por entrada. Las cuatro categorías nos ayudaron a reconocer distintos motivos para modificar software y las ocho etapas ordenaron las decisiones. Con este enfoque podemos explicar cualquier cambio mediante preguntas concretas: qué necesidad atiende, qué debe conservar y cómo comprobamos su resultado.

## Preguntas para defender la teoría

1. **¿Qué diferencia hay entre hacer un cambio y gestionarlo?** Gestionarlo incluye justificarlo, evaluar impacto, decidir, planificar, implementar, verificar y registrar su cierre.
2. **¿Cómo identificamos el tipo?** Por su motivo principal: reparar un defecto, responder al entorno, mejorar una capacidad o reducir un riesgo futuro. Usamos los cuatro tipos solicitados por el curso.
3. **¿Prioridad y riesgo significan lo mismo?** La prioridad ordena el trabajo. El riesgo combina la posibilidad de un problema con sus consecuencias. Un cambio prioritario puede necesitar más controles.
4. **¿Quién autoriza?** La persona o autoridad asignada por la organización. Desarrollo analiza y propone; calidad aporta evidencia. Un equipo pequeño puede reunir roles, conservando sus responsabilidades.
5. **¿Integrar en el repositorio ya pone la función en servicio?** Integrar, desplegar y activar son acciones diferentes. Deben coordinarse con versiones compatibles y verificación.
6. **¿Revertir código devuelve los datos al estado anterior?** No lo hace automáticamente. En el ejemplo hay que conservar las transferencias confirmadas y evitar reactivar códigos antiguos; el plan operativo debe respetar esos estados.
7. **¿Qué demuestra el ejemplo de conciertos?** Explica el proceso y sus decisiones bajo supuestos explícitos. No representa un sistema implementado ni cifras reales.

---

A continuación comienza el caso práctico del proyecto del curso. Sus once páginas, explicaciones y preguntas se conservan respecto del guion anterior.

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
