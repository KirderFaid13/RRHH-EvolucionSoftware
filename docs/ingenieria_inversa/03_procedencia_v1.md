# Procedencia, recuperación y compilación de v1

La v1 de esta revisión corresponde a la descompilación estática de `legado/RRHH/ClassRRHH.dll`, tamaño 55.808 bytes, SHA-256 `39c2b11a6f8f1181f2f9fe061ece9638f57bfa599e94e937e7998e179123c42c`.

Herramienta: **ILSpyCMD 11.1.0.9782**. Se recuperaron 12 C# y un icono; el proyecto generado queda excluido porque contiene rutas de referencia del equipo y un objetivo `net35` que no fue validado. Las fuentes preservan los bytes producidos por el descompilador. [Manifiesto de recuperación](../../evidencia/ingenieria_inversa/recuperacion_v1.json).

ILSpy ofrece descompilación de ensamblados .NET a C#. Esto permite inspeccionar código derivado de IL; no devuelve necesariamente el lenguaje, comentarios, nombres locales ni estructura de proyecto originales. [Documentación oficial de ILSpy](https://github.com/icsharpcode/ILSpy).

## Repetir la descompilación

Desde la raíz, con un SDK compatible con la herramienta y acceso a NuGet:

```powershell
dotnet tool install ilspycmd --version 11.1.0.9782 --tool-path .local/tools
.\.local\tools\ilspycmd.exe --disable-updatecheck --project --outputdir .local/c02/repeticion --referencepath legado/RRHH legado/RRHH/ClassRRHH.dll
```

Usar un destino nuevo; el comando genera archivos privados, incluidos settings. La salida de referencia se generó con estos argumentos, y sus hashes figuran en el manifiesto. El entorno de resolución de referencias puede afectar la salida; comparar diferencias antes de sustituir fuentes.

## Restaurar y compilar la copia publicada

```powershell
python -m pip install -r .\herramientas\requirements.txt
python .\herramientas\restaurar_legado.py
python .\herramientas\restaurar_v1.py
python .\herramientas\compilar_v1.py
```

Se requiere la clave local del primer commit. El legado se restaura en `.local/RRHH/`; las fuentes en `.local/v1_src/`; los logs y la DLL diagnóstica en `.local/c02/compilacion_reproducida/`. Los destinos permanecen fuera de Git.

`MySettings.cs` contiene seis defaults codificados, dos usados como contraseñas Jet. Su salida original se guarda con AES-256-GCM y la misma clave local; los valores no se descifran ni se imprimen. Once C# e icono quedan visibles; la restauración recupera el archivo restante sin editarlo. El cifrado protege la fuente publicada, no sustituye el mecanismo interno del programa original.

La compilación utiliza las 12 fuentes, Roslyn del SDK 10.0.103, `-target:library`, `-platform:x86`, `-langversion:14.0` y referencias Framework instaladas en `C:/Windows/Microsoft.NET/Framework/v4.0.30319`, además de `Seguridad.dll` y `GRLL.dll` originales. El script permite indicar SDK, ubicación de dotnet y directorio Framework; no instala ni migra el framework del producto.

## Resultado y alcance

- Compilación de biblioteca: código de salida 0, cero errores y advertencias, DLL de 52.224 bytes.
- Comparación estática: coinciden firmas y campos públicos de las cuatro clases de negocio. Incluye constructores y accesores; no compara comportamiento ni todos los tipos de soporte.
- Originales y fuentes: SHA-256 cotejados; el baseline sigue sin cambios.
- Ejecución y datos: no se ejecutaron métodos del legado, no se abrieron SQL/Access ni se restauró CMI.

[Procedimiento registrado](../../evidencia/ingenieria_inversa/procedimiento_recuperacion.json), [compilación reproducida](../../evidencia/ingenieria_inversa/compilacion_v1.json) y [comparación de API](../../evidencia/ingenieria_inversa/comparacion_api.json).

El objetivo `net35` procede del proyecto inferido por ILSpy. La compilación con referencias Framework4 acredita resolución de tipos y sintaxis en este entorno; no verifica ese objetivo, firma, recursos, instalación ni equivalencia funcional. La DLL no reemplaza el ejecutable original.
