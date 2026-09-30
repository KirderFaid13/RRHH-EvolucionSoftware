# Evidencia de ingeniería inversa C02

| Archivo | Qué acredita |
| --- | --- |
| [inventario_tecnico.json](inventario_tecnico.json) | 347 archivos cotejados con baseline, 250 PE CLR, XML y formatos PDB; BAK excluido. |
| [ensamblados_propios.json](ensamblados_propios.json) | Referencias, tipos y firmas seleccionadas sin ejecutar métodos ni extraer secretos. |
| [despliegue.json](despliegue.json) | Archivos ausentes y diferencias de tamaño/digest declaradas en manifiestos. |
| [duplicados.json](duplicados.json) | Grupos de SHA-256 iguales dentro de los 348 originales; no se eliminaron copias. |
| [recuperacion_v1.json](recuperacion_v1.json) | Procedencia y hashes de 12 C# y un icono, cifrado de settings y exclusión del proyecto inferido. |
| [procedimiento_recuperacion.json](procedimiento_recuperacion.json) | Herramienta, versión, comandos y referencias de compilación. |
| [contratos_observados.json](contratos_observados.json) | Inventario heurístico de llamadas del cliente; los casos citados se cotejaron con el código. |
| [compilacion_v1.json](compilacion_v1.json) | Compilación reproducida con script público: 12 fuentes, cero errores/advertencias; DLL no ejecutada. |
| [comparacion_api.json](comparacion_api.json) | Coincidencia de firmas y campos públicos de cuatro clases en el primer ensamblado diagnóstico. |
| [auditoria_antecedente.json](auditoria_antecedente.json) | Hashes del antecedente histórico y revisión de ocho PDF/119 páginas. |
| [verificacion_c02.json](verificacion_c02.json) | Comprobaciones de entrega y exclusiones del segundo commit. |

Los recuentos de duplicados corresponden únicamente al paquete RRHH de 348 archivos; no se mezclan con el inventario anterior de todo el directorio. Los faltantes de despliegue son ocurrencias en manifiestos y pueden repetirse.

Para reproducir metadatos: instalar `herramientas/requirements_ir.txt`, restaurar el legado en `.local/RRHH/` y ejecutar `python herramientas/inspeccionar_legado.py`. Para compilar: `python herramientas/compilar_v1.py`. [Procedimiento completo](../../docs/ingenieria_inversa/03_procedencia_v1.md).

La compilación utiliza referencias instaladas Framework4 y no valida el objetivo inferido `net35`. Coincidencia de API no acredita equivalencia funcional. La segunda compilación genera un nombre/hash distinto; ambos resultados provienen de las mismas fuentes verificadas. No se ejecutó la aplicación ni se conectó o restauró una base.
