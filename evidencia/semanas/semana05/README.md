# Evidencias C04 — v3 OCP

| Archivo | Qué acredita |
| --- | --- |
| [contratos_v1.json](contratos_v1.json) | Fuente y hashes de v1/v2; firmas, procedimientos, parámetros y nombres suministrados a `Fill` en los dos métodos. No contiene esquema SQL verificado. |
| [antes_despues.diff](antes_despues.diff) | Comparación v2/v3 de la fachada: únicamente los dos cuerpos del caso, con finales de línea normalizados para lectura. |
| [compilacion_y_pruebas.json](compilacion_y_pruebas.json) | Compilaciones, 11 escenarios de preparación y demostración de extensión externa con hashes del núcleo antes/después. |
| [verificacion_v3.json](verificacion_v3.json) | Resultado `ok: true`, firmas y resto de fachada conservados, etapas anteriores intactas y 18 hashes de antecedentes comprobados. |
| [antecedentes.json](antecedentes.json) | Procedencia, tamaño y SHA-256 de los 18 archivos recibidos. |

## Resultados registrados

Con Roslyn SDK 10.0.103 y referencias instaladas Framework v4.0.30319 se compilan, sin errores ni advertencias:

- Biblioteca acumulativa x86: 20 fuentes, compuestas por 11 de v1 sin su fachada, dos helpers reutilizados de v2 y siete C# de v3.
- Antecedente separado: 17 C#; su compilación no corrige sus diferencias de contrato.
- Núcleo: cinco fuentes, con `ReporteOficina` como única definición inicial.
- Extensión: una fuente, `ReporteOficinaPorSigla`, en otra DLL referenciando el núcleo ya compilado.
- Harness: una fuente, referenciando ambas DLL.

La ejecución del harness termina con código 0 y 11 escenarios aprobados. Usa `GeneradorReportes.Preparar` con cinco valores de oficina (`int.MinValue`, `-1`, `0`, `42`, `int.MaxValue`) y seis siglas (`null`, vacío, texto ordinario, Unicode, texto con espacios/apóstrofo y 1000 caracteres). Comprueba comando, `StoredProcedure`, parámetro, tipo SQL, dirección, tamaño inferido, valor recibido, identidad de la conexión cerrada, adaptador sin modificación y nombre de tabla preparado. Esos valores prueban conservación del cliente, no reglas de aceptación del servidor.

El harness confirma que la definición por sigla proviene de otro ensamblado. Es la segunda definición de un reporte que ya existía en v1, no una funcionalidad empresarial nueva. El hash de la DLL del núcleo y los hashes de sus cinco fuentes coinciden antes/después; el núcleo no se modifica ni recompila para esa extensión.

## Reproducción y alcance

Desde la raíz, con Python, SDK/referencias indicados, clave local y legado restaurado:

```powershell
python herramientas/compilar_v3.py
python herramientas/verificar_v3.py
```

Las fuentes privadas de v1 se restauran en `.local/v1_src/`. Logs, respuestas del compilador, fuente del harness y DLL/EXE de diagnóstico quedan en `.local/c04/`, ignorada por Git. Las DLL recibidas se usan como referencias de compilación de la biblioteca acumulativa; no se ejecutan en las pruebas.

Solo se ejecuta código nuevo de preparación de comandos. No se llama `Generar`, `Fill`, `RRHHClass`, GRLL ni código recibido; no se conecta o restaura CMI. `DataSet`, `Fill` y apertura/cierre incondicionales se contrastan en la fuente y mediante compilación. Preparar ocurre antes de `Open`, sin acreditar equivalencia de todos los fallos. No se comprueban resultados SQL, esquema, permisos, UI, despliegue, framework original ni equivalencia funcional completa. Los hashes diagnósticos tampoco acreditan equivalencia binaria con el legado.

[Código v3](../../../src/v3/README.md), [informe](../../../docs/semanas/semana05/01_ocp.md) y [contrato C04](../../../specs/c04_ocp.json).
