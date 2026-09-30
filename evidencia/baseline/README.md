# Evidencia del primer commit

- [Inventario original](inventario_original.json): 348 rutas, tamaños y SHA-256; modo de almacenamiento de cada archivo.
- [Inventario de documentos](inventario_referencias.json): ocho PDF y sus hashes.
- [Revisión para almacenamiento](revision_credenciales.json): alcance y archivos protegidos, sin valores de credenciales.
- [Resultado de verificación](verificacion_baseline.json): comprobaciones realizadas al preparar el contenido.

Ejecutar desde la raíz:

```powershell
python .\herramientas\verificar_baseline.py
```

El resultado de cada ejecución se muestra en terminal; para guardarlo:

```powershell
python .\herramientas\verificar_baseline.py --salida .local\verificacion_actual.json
```

Con clave local, se verifica también el contenido original de los archivos cifrados. Para cotejar el paquete completo disponible en otro directorio, se puede usar `--origen 'RUTA_DEL_RRHH_ORIGINAL'`. `--indice` comprueba las exclusiones y que Git almacene los mismos bytes de los archivos registrados.

Las comprobaciones acreditan la conservación de contenido y el orden de esta entrega. No se ejecutó el programa ni se restauró su base.
