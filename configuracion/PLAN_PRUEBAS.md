# Plan inicial de pruebas vinculadas a la configuración

**Ámbito:** C06/S08, preparación local. Objetivo: reconocer la configuración usada, detectar diferencias fuera de alcance y preservar las comprobaciones aisladas disponibles. El plan incluye propuestas futuras; no las presenta como ejecuciones realizadas.

## Enfoques y objetivos

Caja negra observa entradas y salidas sin usar el interior del componente; caja blanca usa conocimiento de su implementación; caja gris combina observación externa con conocimiento parcial. Funcionalidad, rendimiento, seguridad y detección de defectos describen objetivos. Una prueba puede combinar un enfoque y un objetivo.

## Comprobaciones disponibles

| ID | Comprobación y objetivo | Procedimiento | Resultado esperado y límite |
| --- | --- | --- | --- |
| PC-01 | Integridad y alcance de configuración | `python herramientas/auditar_configuracion.py` compara la base C05 de 531 archivos con el estado local y el contrato C06. | Identificar iguales, cambios permitidos, faltantes, cambios no permitidos y altas dentro/fuera del alcance. Integridad no acredita funcionamiento. |
| PC-02 | Detección de fallos del auditor | `python herramientas/verificar_configuracion.py` utiliza muestras temporales controladas. | Detectar alteración, ausencia, ruta fuera del repositorio, inventario alterado y archivo nuevo no permitido, sin tocar el legado real. Ver resultados concretos en evidencia C06. |
| PC-03 | Exclusión de material privado | Auditoría de reglas Git para `.local/`, clave, respaldo y compilados generados. | Confirmar que las rutas representativas están ignoradas. No mostrar contenidos, descifrar archivos ni atribuir seguridad completa a `.gitignore`. |
| PC-04 | Compilación de v4 diagnóstica | El verificador C06 repite la compilación con el entorno y dependencias ya documentados; conserva salida nueva solo en evidencia semana 08. | Biblioteca acumulativa de 22 fuentes y harness de 10 fuentes compilables. No sustituye la DLL original en producción. |
| PC-05 | Regresión aislada de reportes v4 | El mismo verificador C06 ejecuta los 16 escenarios de C05, con sustitutos y datos sintéticos, sin reemplazar evidencia C05. | Conservar comandos y comprobar llamadas, resultado sintético, composición sin abrir conexión y propagación de fallos. No se ejecuta SQL ni interfaz. |
| PC-06 | Coherencia documental y presentación | Comparar contrato, informe, planes, registro, guion y diapositivas; renderizar y revisar ocho diapositivas y comprobar notas/texto editable. | Evitar afirmar pruebas o publicaciones pendientes como realizadas; el registro de presentación declara el estado real de cada entregable. |

Los casos del auditor y del harness usan conocimiento del componente y estados controlados: aportan comprobaciones funcionales y estructurales de componentes aislados. No se describen como cobertura total de caja negra del RRHH original.

Los 16 escenarios de v4 ya constan en evidencia C05. Una repetición para C06 conserva su resultado nuevo por separado, sin reemplazar la evidencia anterior ni modificar fuentes. Una comprobación se marca ejecutada únicamente cuando existe resultado verificable en `evidencia/semanas/semana08/`.

Resultado de esta preparación: 14 escenarios del auditor y 16 de v4 aprobados, biblioteca de 22 fuentes y harness de 10 fuentes compilados. Se verifican las seis columnas de JSON/CSV. El harness necesitó ejecución fuera de AppContainer para inicializar contadores locales de SqlClient; no abrió SQL. El auditor verifica el contenido de trabajo. Los bytes del índice y del commit se revisarán por separado antes y después de la futura incorporación.

## Pruebas propuestas, todavía pendientes

| ID | Enfoque u objetivo | Propuesta para el RRHH | Condición previa |
| --- | --- | --- | --- |
| PF-01 | Funcionalidad con caja negra | Comprobar desde la aplicación una consulta o reporte acordado, sus entradas, salida y mensajes. | Entorno autorizado, pantalla real identificada, datos sintéticos y resultado esperado sustentado. |
| PF-02 | Integración con caja gris | Observar el comportamiento del reporte y su conexión usando los contratos recuperados. | CMI de prueba y procedimientos/esquema verificados; no usar credenciales o datos reales publicados. |
| PF-03 | Rendimiento | Medir tiempo de una operación con volumen sintético y entorno conocidos; comparar versiones equivalentes. | Acordar operación, volumen, entorno y criterio antes de medir. No existe aún umbral ni medición aceptados. |
| PF-04 | Seguridad | Revisar autenticación y autorizaciones reales; probar accesos válidos e inválidos en entorno controlado. | Roles, permisos y flujos observados y autorizados. No se inventa matriz de permisos. |
| PF-05 | Defectos y fallos de integración | Examinar fallos de conexión, datos inesperados o errores del proveedor cuando se conozca su comportamiento. | Acordar resultados esperados y aislamiento; el manejo SQL heredado no se considera corregido por IoC. |

## Registro y criterio de aceptación

Cada resultado identifica fecha, base, entradas sintéticas o metadatos permitidos, comando, código de salida y alcance. Los archivos generados y temporales permanecen en `.local/`; se publica evidencia que no contenga secretos.

Un fallo de alcance bloquea la aceptación de la preparación hasta que se explique y resuelva. Una prueba propuesta pendiente se informa como tal. El éxito de PC-01 a PC-06 no acredita instalación, interfaz completa, rendimiento, autenticación, SQL ni equivalencia con el original.

Este plan responde a la [consigna de semana 08](../referencias/semanas/semana08/Semana08_EVO_TG.pdf), páginas 13 y 16. KirderFaid13 revisa resultados y límites antes de decidir la incorporación de la etapa.
