# Evidencia C06/S08: gestión de configuración

Base publicada: C05 `6d82f9fa6aa608a0d7d71c14fb2fc661e9d21fa2`, árbol `a6b85aad0d6ab119297cd4ffd37c8ef5421a383e`, 531 archivos. Los JSON y diapositivas registran la preparación de C06 en `semana-08-gcs`. Después de esa entrega, el responsable indicó realizar el sexto commit; [incorporación y publicación verificable](../../../docs/semanas/semana08/03_preparacion_sexto_commit.md).

| Archivo | Qué acredita | Límite |
| --- | --- | --- |
| [procedencia.json](procedencia.json) | Copia exacta del PDF docente, páginas de práctica y rúbrica. | Las ocho referencias del inventario inicial permanecen separadas. |
| [auditoria_configuracion.json](auditoria_configuracion.json) | 531 archivos comparados con objetos Git de C05, guías modificadas dentro del alcance, nuevos archivos C06 y ocho exclusiones Git. | Compara archivos de trabajo; no certifica índice, futuro commit ni funcionamiento. |
| [verificacion_configuracion.json](verificacion_configuracion.json) | 14 escenarios aislados del auditor, equivalencia de las seis columnas JSON/CSV, compilación de 22 fuentes y 16 escenarios v4. | Sin SQL, interfaz, rendimiento, autenticación ni binarios recibidos. |
| [presentacion.json](presentacion.json) | Ocho diapositivas locales, notas y tabla editables, hashes y revisión del PPTX renderizado. | Creación independiente de Canva. La edición Canva tiene estado propio. |
| [canva.json](canva.json) | Identificador y estado de la presentación Canva. | Los enlaces de edición, borradores y tokens se conservan solo localmente. |

Las 14 pruebas cubren archivo conservado, modificación no permitida, cambio autorizado, ausencia, CRLF/LF, escape y ruta absoluta, duplicados, inventario alterado o incompleto, alta fuera del alcance, secreto por extensión y CSV incompleto. Utilizan muestras propias temporales; nunca alteran el legado.

La compilación v4 reutiliza fuentes verificadas de C05. Nuevos DLL/EXE, respuesta del compilador y logs quedan en `.local/c06/compilacion/`. Windows bloqueó la inicialización local de contadores de SqlClient en AppContainer; la ejecución elevada autorizada del harness aislado aprobó. No se abrió una conexión SQL. Los hashes de compilados nuevos pueden diferir de C05; no se atribuye una compilación determinista.

Para repetir, ejecutar desde la raíz:

```powershell
python herramientas/auditar_configuracion.py
python herramientas/verificar_configuracion.py
```

Requiere Python 3.12 o posterior y Git compatible con `check-attr --source`; v4 requiere las fuentes privadas restauradas, contratos generados verificados, SDK10.0.103 y referencias Windows/.NET Framework descritos en semana 07. Estas verificaciones escriben exclusivamente evidencia nueva S08. Antes del futuro commit se comprobará el índice y después el árbol integrado; la indicación de incorporación por KirderFaid13 consta en CAM-S08-001; no se presume una revisión formal.
