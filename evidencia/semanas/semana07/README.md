# Evidencias C05: v4 IoC

| Archivo | Qué acredita |
| --- | --- |
| [procedencia.json](procedencia.json) | Commit base, hashes de los siete archivos v3 y de los contratos v1 reutilizados; identifica las cuatro fuentes de reportes que se conservan. |
| [antes_despues.diff](antes_despues.diff) | Comparación v3/v4: dos cuerpos de la fachada, campo/constructor del generador y declaración de interfaz del ejecutor. |
| [compilacion_y_pruebas.json](compilacion_y_pruebas.json) | Biblioteca de 22 fuentes, harness de 10 y 16 escenarios aprobados del flujo con sustitutos, sin ejecución SQL. |
| [verificacion_v4.json](verificacion_v4.json) | Resultado `ok: true`; conservación de contratos, firmas, cuerpos seleccionados, etapas previas y ocho hashes de antecedentes. |
| [antecedentes.json](antecedentes.json) | Procedencia, tamaño y SHA-256 de los ocho archivos del borrador recibido. |
| [presentacion.json](presentacion.json) | Hashes de la entrega local, seis diapositivas y notas, revisión de renders y estado separado de Canva. |
| [preparacion.json](preparacion.json) | Integridad de los 348 originales, referencias y enlaces; búsqueda de secretos conocidos, rama local y cuatro commits en el remoto público confirmado por el responsable. |

`preparacion.json` conserva la comprobación anterior a la creación del quinto commit. Los indicadores `fifth_commit_created` y `published` de `presentacion.json` también describen su revisión previa. Son evidencia histórica; el estado actual del commit y de su incorporación se consulta en Git y en el PR, según el [detalle de incorporación](../../../docs/semanas/semana07/03_preparacion_quinto_commit.md).

## Resultados registrados

Con Roslyn SDK 10.0.103 y referencias instaladas Framework v4.0.30319, las dos compilaciones registran salida 0, sin errores ni advertencias:

- Biblioteca acumulativa x86: 22 fuentes, compuestas por 11 de v1 sin su fachada, dos helpers de empleados v2, cuatro fuentes de reportes v3 reutilizadas y cinco fuentes v4.
- Harness: 10 fuentes, compuestas por ocho componentes del caso de reportes, [PruebasIoC.cs](../../../src/v4/pruebas/PruebasIoC.cs) y `ContratosRecuperados.cs`, generado desde los contratos v1.

El harness termina con salida 0 y 16 escenarios aprobados. El verificador registra `ok: true` y `failures: []`: conserva firmas y resto de fachada, comprueba el cambio mínimo de campo/constructor del generador, el constructor y cuerpo SQL y los ocho antecedentes; no detecta cambios en las etapas C01-C04.

Las pruebas de comandos reutilizan los [contratos observados en v1](../semana05/contratos_v1.json): cinco enteros de oficina y seis siglas, incluidos `null`, vacío, Unicode, espacios/apóstrofo y 1000 caracteres. Comprueban procedimiento, tipo de comando, nombre/tipo/dirección/tamaño/valor del parámetro, nombre de tabla y referencia de conexión cerrada. Se llama `Generar` con un sustituto y se verifica una llamada y el mismo `DataSet` sintético devuelto por identidad. Las entradas comprueban conservación del cliente, sin acreditar que el servidor las acepte.

Los cinco escenarios adicionales aprobados son:

| Escenario | Comprobación ejecutada |
| --- | --- |
| `sustitucion_de_ejecutor_y_resultado` | Dos instancias de la misma clase de generador reciben ejecutores diferentes y devuelven el resultado correspondiente por identidad, sin mezclar sus llamadas. |
| `preparar_no_ejecuta_dependencia` | `Preparar` conserva conexión cerrada y no llama al sustituto. |
| `excepcion_del_ejecutor_se_propaga` | `Generar` propaga la misma excepción del sustituto, que recibe una llamada. |
| `composicion_sql_solo_prepara_sin_abrir` | La composición crea la ruta SQL; `Preparar` conserva conexión cerrada, adaptador sin `SelectCommand` y parámetro esperado. No ejecuta el ejecutor SQL. |
| `fallo_de_preparacion_no_llama_ejecutor` | Un fallo al crear el comando propaga la misma excepción y no incrementa las llamadas al sustituto. |

## Reproducción y límites

Desde la raíz, con Python, SDK .NET 10.0.103 y referencias Framework v4.0.30319 instaladas, clave local y legado restaurado:

```powershell
python herramientas/compilar_v4.py
python herramientas/verificar_v4.py
```

Las fuentes privadas restauradas permanecen en `.local/v1_src/`. El harness, sus llamadas generadas, logs, respuestas del compilador y DLL/EXE diagnósticos quedan en `.local/c05/`, ignorada por Git. Los ensamblados recibidos se utilizan como referencias para compilar la biblioteca acumulativa; no se ejecutan en el harness. Los ocho archivos del antecedente v4 se preservan y verifican por hash, sin compilarlos o activarlos.

La ejecución con sustitutos demuestra la entrega externa de la dependencia y el flujo del generador. No llama al ejecutor SQL real, `Fill`, la fachada, GRLL o la UI; no conecta ni restaura CMI. El cuerpo SQL se compara con v3 y se compila. Se mantienen conexión/comando `SqlClient`, apertura/cierre manuales y ciclo de vida actual de comandos. No se comprueban resultados SQL, esquema, permisos, despliegue, framework original o equivalencia funcional completa. Compilar y conservar hashes son evidencias diferentes de ejecutar el sistema.

[Código v4](../../../src/v4/README.md), [informe](../../../docs/semanas/semana07/01_ioc.md), [contrato C05](../../../specs/c05_ioc.json) y [descripción del quinto commit](../../../docs/semanas/semana07/03_preparacion_quinto_commit.md). La entrega se incorpora mediante la rama semanal y un PR con squash hacia `main`.
