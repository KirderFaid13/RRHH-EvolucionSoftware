# Guion de exposición: semana 08, GCS del RRHH

Este guion y las diapositivas conservan la exposición del caso durante su preparación. La autorización posterior para incorporar el sexto commit se registra en [la guía de incorporación](03_preparacion_sexto_commit.md). Si se expone después de la publicación, se describe el estado que realmente muestre GitHub al mencionar la integración.

**Ocho diapositivas; duración orientativa: seis minutos.** El docente no fija una duración en la guía. Este guion se centra en la gestión de configuración aplicada al proyecto. La distribución entre integrantes la decide el equipo; no se asignan nombres ni participaciones ficticias.

## 1. Gestión de la configuración aplicada al RRHH — 0:30

“Nuestro proyecto estudia y mejora un sistema de Recursos Humanos del año 2008. En esta semana aplicamos gestión de la configuración: identificar qué archivos forman parte del proyecto, conocer su versión y controlar los cambios antes de integrarlos.

El código más reciente continúa siendo v4. La mejora de esta semana consiste en inventario, coordinación, registro de cambios, planes iniciales y una herramienta funcional que audita la configuración. Todo está preparado localmente; el sexto commit todavía está pendiente.”

## 2. Por qué necesitamos GCS — 0:45

“Nuestro repositorio reúne originales, código recuperado, propuestas anteriores, versiones refactorizadas y documentación. Si no distinguimos esos materiales, podríamos compilar una propuesta equivocada, mezclar versiones o sobrescribir un archivo recibido.

La GCS nos ayuda a mantener orden, control y trazabilidad. Orden significa localizar cada componente; control significa acordar y revisar sus cambios; trazabilidad significa relacionar un archivo con la versión, la decisión y la evidencia que lo justifican.

Así, un integrante puede continuar el trabajo sin adivinar qué está activo ni qué se ha probado. Estos son riesgos que queremos prevenir; no estamos afirmando que todos hayan ocurrido.”

## 3. Elementos de configuración — 0:55

“Identificamos los elementos que pondremos bajo control. La diapositiva los resume en seis grupos: código fuente; binarios y datos; herramientas; requisitos y diseño, incluida la arquitectura; pruebas y calidad; y documentos del curso y de la exposición.

El informe contiene la tabla completa con los diez tipos que menciona la guía, además de la documentación del curso. Cada grupo tiene ubicación, procedencia, estado y regla de conservación. El inventario individual identifica los 531 archivos de la base C05 mediante ruta, tamaño y hash.

También distinguimos lo que permanece privado. El respaldo SQL, claves, configuraciones restauradas y compilados nuevos quedan fuera de Git. Controlar su ubicación no significa publicar su contenido.”

## 4. Organización del repositorio — 0:40

“Aprovechamos las carpetas ya organizadas. `src` contiene el código; `legado` conserva los archivos recibidos; `docs` explica decisiones y `evidencia` guarda lo comprobado. `specs` delimita cada tarea y `.context` conserva el contexto y las dudas.

Añadimos `configuracion` para el inventario, los elementos, el registro de cambios y los planes iniciales. Los archivos de esta semana se guardan en carpetas de semana 08. `.local` permanece ignorada por Git.

Con esta separación podemos ubicar el código activo y su documentación sin confundirlos con un antecedente o un resultado temporal.”

## 5. Git, GitHub y base de referencia — 0:45

“Usamos Git para controlar versiones y GitHub para alojar y compartir el repositorio. Git registra estados de los archivos; GitHub nos permite proponer cambios mediante ramas y revisarlos antes de integrarlos.

Nuestra referencia es C05, el commit `6d82f9f`, que ya está publicado en `main` y contiene 531 archivos. Los cinco commits permiten ubicar las etapas del proyecto; los usamos como ejemplo de trazabilidad.

Para semana 08 trabajamos en `semana-08-gcs`. La regla propuesta es preparar una rama por semana y conservar una entrega integrada por commit. La auditoría separa los archivos de esa base de los nuevos entregables C06.”

## 6. Control de cambios y responsable — 0:50

“Registramos esta preparación como `CAM-S08-001`. Allí explicamos qué cambia, por qué, qué rutas afecta, sus validaciones y lo que sigue pendiente.

El flujo es registrar el cambio, coordinar las rutas, prepararlo, comprobarlo y revisarlo antes de integrarlo. KirderFaid13 confirmó que revisará e integrará los cambios. El autor debe comunicar el alcance antes de editar para evitar que varias personas modifiquen el mismo archivo sin acuerdo.

La autorización para preparar esta semana no significa que su revisión ya esté aprobada. Después de la revisión y la indicación de incorporación, crearemos el sexto commit y la solicitud de cambios hacia `main`. No afirmamos tener protección de ramas o pruebas automáticas remotas configuradas.”

## 7. Pruebas iniciales — 0:55

“Primero distinguimos enfoques y objetivos. Caja negra, blanca y gris indican cuánto conocemos del interior del componente. Funcionalidad, rendimiento y seguridad indican qué queremos comprobar.

En esta preparación aprobaron las 14 pruebas del auditor con muestras temporales. Comprobamos integridad, alcance y exclusiones de archivos privados. También repetimos las comprobaciones aisladas de v4: compilación diagnóstica y 16 escenarios con sustitutos y datos sintéticos.

Eso no demuestra que toda la aplicación funcione. Las pruebas de interfaz, SQL, rendimiento y autenticación quedan propuestas para un entorno autorizado. Sus entradas, resultados esperados y criterios deberán definirse antes de ejecutarlas. El plan separa claramente comprobaciones disponibles y pendientes.”

## 8. Demostración y aporte de esta semana — 0:40

“Como ejemplo funcional, ejecutamos el auditor de configuración. Compara el estado local con la base congelada y el alcance del contrato. Identifica archivos iguales, cambios permitidos, ausencias y diferencias que requieren explicación.

El verificador demuestra que puede detectar fallos con muestras temporales; no alteramos el legado real para provocar un error. Los resultados quedan en la evidencia de semana 08.

El aporte es contar con una configuración reconocible y verificable antes de integrar cambios. La entrega está preparada para que KirderFaid13 la revise; el sexto commit sigue pendiente.”

## Preparación de la demostración

Desde la raíz del repositorio, ejecutar previamente:

```powershell
python herramientas/verificar_configuracion.py
python herramientas/auditar_configuracion.py
```

Para la exposición basta mostrar el inventario, `CAM-S08-001` y el resultado de auditoría. Si se repite el comando en vivo, explicar el resultado que realmente muestre; no leer una cantidad prevista como si fuera la salida actual. Las pruebas del verificador usan muestras aisladas y la repetición de v4 no abre SQL.

Antes de exponer, comprobar que los archivos de evidencia C06 confirmen las ejecuciones mencionadas en las diapositivas 7 y 8. Si faltara una ejecución, describirla como pendiente y ajustar el guion. No mostrar `.local/`, claves, conexiones restauradas ni datos reales.
