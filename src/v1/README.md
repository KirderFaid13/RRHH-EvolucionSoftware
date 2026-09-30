# v1: base recuperada mediante ingeniería inversa

Esta v1 permite inspeccionar el ensamblado propio `ClassRRHH.dll` con procedencia verificable. Es una recuperación parcial del sistema; no incorpora toda la interfaz ni constituye una aplicación completa.

- `recuperado/`: 12 archivos C# producidos por ILSpyCMD 11.1.0.9782 y un icono. Once fuentes son visibles y `MySettings.cs` se conserva cifrada por sus valores codificados de configuración. Las cuatro clases de negocio están en `recuperado/ClassRRHH/`.
- [antecedentes](antecedentes/README.md): los dos VB y la descripción histórica del grupo, conservados sin editar para su auditoría. Son una reconstrucción esquemática y no forman parte de la compilación recuperada.

Las fuentes C# conservan su salida de descompilación; no se reorganizaron métodos ni se implementaron principios SOLID en esta etapa. Las carpetas `.My` contienen soporte generado del programa VB, no módulos nuevos del negocio.

## Consulta y reproducción

1. Lee el [informe](../../docs/ingenieria_inversa/01_informe.md) y la [arquitectura](../../docs/ingenieria_inversa/02_arquitectura.md).
2. Consulta [procedencia y comandos](../../docs/ingenieria_inversa/03_procedencia_v1.md).
3. Restaura el legado y v1 mediante las herramientas de la raíz; después ejecuta `python herramientas/compilar_v1.py` para la comprobación diagnóstica.

La compilación de las 12 fuentes pasó como biblioteca x86 con referencias instaladas Framework4. No acredita el framework original, equivalencia del producto ni operación de CMI. El [manifiesto](../../evidencia/ingenieria_inversa/recuperacion_v1.json) distingue fuente generada, cifrado y procedencia.

Las mejoras v2/v3 se incorporarán cuando el equipo indique continuar. El próximo contrato debe identificar si modifica este código recuperado o utiliza un demostrador académico y justificar expresamente la elección.
