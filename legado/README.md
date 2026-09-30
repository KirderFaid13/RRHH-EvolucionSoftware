# RRHH recibido

`RRHH/` conserva la estructura interna del paquete original, incluidas sus carpetas `Reportes/` y `temp/`, dependencias, XML y símbolos PDB. No se deduplicó el paquete ni se aplicaron refactorizaciones.

El [inventario original](../evidencia/baseline/inventario_original.json) registra todos sus archivos. `storage` identifica cómo se conserva cada uno:

- `unchanged`: contenido original disponible directamente.
- `aes256_gcm`: contenido original cifrado; el nombre añade `.aesgcm`.
- `local_only`: respaldo registrado que no se incorporó a Git.

Las seis configuraciones tienen también una variante `.config.example`. Estos ejemplos reemplazan las cadenas de conexión por marcadores; no son las configuraciones originales y no se garantiza que permitan ejecutar la aplicación.

## Restauración

Requisitos: Python 3.10 o posterior, dependencias de `herramientas/requirements.txt` y clave del responsable del proyecto. La clave no se incluye en GitHub.

Desde la raíz:

```powershell
python -m pip install -r .\herramientas\requirements.txt
python .\herramientas\restaurar_legado.py
```

Con la clave en `.local/clave_legado.key`, el programa restaura/verifica 347 archivos en `.local/RRHH/`. Autentica el contenido cifrado y coteja SHA-256 y tamaño antes de escribirlo. Si encuentra un archivo diferente en el destino, se detiene sin sobrescribirlo. Repetirlo con archivos idénticos es válido.

Para usar otras ubicaciones:

```powershell
python .\herramientas\restaurar_legado.py --clave 'RUTA_PRIVADA\clave_legado.key' --destino 'RUTA_FUERA_DEL_REPOSITORIO\RRHH'
```

Dentro del repositorio, la herramienta solo permite restaurar en `.local/`, ignorada por Git. No ejecutes la copia ni la conectes a sistemas reales como parte de una comprobación de hashes.

El respaldo `CMI_Backup_QA.bak` se conserva aparte; consulta [datos/respaldos](../datos/respaldos/README.md). Las configuraciones restauradas siguen conteniendo sus credenciales originales, por lo que la copia debe mantenerse privada.

La carpeta del repositorio no está preparada para ejecución directa: sus archivos sensibles están cifrados. La verificación de funcionamiento se documentará cuando realmente se efectúe.
