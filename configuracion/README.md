# Control inicial de configuración: semana 08

La base de software es C05, commit `6d82f9f`, con 531 archivos versionados. C06 añade control de configuración y conserva las fuentes v4. Esta carpeta contiene:

- [Catálogo de elementos](elementos.json): identificadores, tipos, rutas, estado y política de almacenamiento.
- [Inventario completo C05 en CSV](inventario_c05.csv) y [JSON](inventario_c05.json): una fila por archivo de la base con tamaño, SHA-256 y objeto Git. Los nuevos entregables C06 se identifican en el contrato y la auditoría, por separado.
- [Plan de configuración](PLAN_CONFIGURACION.md): organización, versiones, cambios, auditoría y recuperación.
- [Cambio CAM-S08-001](cambios.json): motivo, alcance, comprobaciones y decisión de incorporación por KirderFaid13 y resultado verificable en GitHub.
- [Plan de pruebas](PLAN_PRUEBAS.md) y [plan de calidad](PLAN_CALIDAD.md): procedimientos disponibles y pruebas futuras sin resultados inventados.

Desde la raíz, `python herramientas/auditar_configuracion.py` comprueba el estado de los archivos de trabajo. `python herramientas/verificar_configuracion.py` prueba el auditor y repite v4 de forma aislada, con nuevas salidas en semana 08. Las entradas privadas de compilación se preparan siguiendo semana 07; nunca se incorporan a Git. [Informe y exposición](../docs/semanas/semana08/01_gestion_configuracion.md).

El PASS del auditor no aprueba una revisión humana ni verifica el contenido del índice o de un futuro commit. Antes del sexto commit se revisarán los archivos agregados y, después de integrar, se comprobará el árbol publicado.
