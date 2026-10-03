# Herramientas del baseline

Requisitos: Python 3.10 o posterior. Instalar dependencias, si faltan:

```powershell
python -m pip install -r .\herramientas\requirements.txt
```

- `verificar_baseline.py`: verifica inventarios, archivos directos/cifrados, referencias, JSON, enlaces y, con `--indice`, exclusiones y bytes del índice Git. No modifica el paquete ni ejecuta RRHH.
- `restaurar_legado.py`: recupera los originales en un destino privado y comprueba su integridad antes de escribir. Necesita la clave del responsable; no sobrescribe archivos diferentes ni restaura el BAK.

Los comandos se ejecutan desde la raíz. Consulta [evidencia](../evidencia/baseline/README.md) y [restauración](../legado/README.md).

## Ingeniería inversa C02

- `inspeccionar_legado.py`: inventario PE/.NET, XML, manifiestos y duplicados desde la copia privada restaurada. Dependencias: `requirements_ir.txt`; no ejecuta ensamblados ni extrae valores secretos.
- `restaurar_v1.py`: restaura las fuentes recuperadas, incluido el settings cifrado, en `.local/v1_src/`.
- `compilar_v1.py`: compila esas 12 fuentes como biblioteca diagnóstica; no la ejecuta. Requiere el SDK y referencias descritos en [procedencia](../docs/ingenieria_inversa/03_procedencia_v1.md).
- `verificar_c02.py`: tras restaurar v1, coteja hashes de fuentes/antecedentes, conservación del baseline y exposición de valores conocidos; registra el alcance de la búsqueda en la evidencia. No reemplaza pruebas funcionales ni repite la comparación IL.

```powershell
python -m pip install -r .\herramientas\requirements_ir.txt
python .\herramientas\inspeccionar_legado.py
python .\herramientas\compilar_v1.py
```

Las evidencias de compilación y API deben interpretarse con sus límites. [Resultados C02](../evidencia/ingenieria_inversa/README.md).

## SRP/DRY C03

- `compilar_v2.py`: combina las fuentes verificadas de v1 con el caso de empleados, compila 14 C# y ejecuta 11 escenarios del código nuevo sin abrir SQL. Diagnostica aparte el antecedente original.
- `verificar_v2.py`: comprueba que solo cambien tres cuerpos, que el resto de la fachada y etapas anteriores se conserven y que los ocho antecedentes mantengan sus hashes.

```powershell
python herramientas/compilar_v2.py
python herramientas/verificar_v2.py
```

[Informe](../docs/semanas/semana04/01_srp_dry.md) y [evidencias](../evidencia/semanas/semana04/README.md). Necesita el entorno Windows/Framework descrito para v1; no sustituye pruebas de integración.

## OCP C04

- `compilar_v3.py`: compila la biblioteca acumulativa de 20 fuentes y el antecedente de 17 fuentes por separado. Compila un núcleo con un reporte y después la segunda definición como biblioteca externa contra ese núcleo. Ejecuta 11 escenarios de preparación de comandos con ambas definiciones y conserva los hashes del núcleo.
- `verificar_v3.py`: compara v3 con v2 excluyendo solo los dos cuerpos autorizados, coteja contratos con v1 y comprueba fuentes compiladas, extensión estable, antecedentes y conservación de C01/C02/C03.

```powershell
python herramientas/compilar_v3.py
python herramientas/verificar_v3.py
```

Los binarios, logs y harness permanecen en `.local/c04/`. Se ejecuta solo la preparación del código nuevo, sin `Fill`, conexión SQL o binarios recibidos. [Informe](../docs/semanas/semana05/01_ocp.md) y [evidencias](../evidencia/semanas/semana05/README.md). Requiere el mismo entorno Windows/Framework y restauración privada que las etapas anteriores.

## IoC C05/S07

- `compilar_v4.py`: compila 22 fuentes acumulativas y 10 del harness. Las llamadas de caracterización se generan desde contratos recuperados de v1 y se combinan con [PruebasIoC.cs](../src/v4/pruebas/PruebasIoC.cs). Ejecuta 16 escenarios con sustitutos; no ejecuta el método SQL real.
- `verificar_v4.py`: comprueba que el cambio del generador se limite a campo/constructor, SQL conserve su constructor y cuerpo, la fachada cambie solo dos cuerpos, las fuentes coincidan con la compilación y C01-C04 permanezcan intactos.

```powershell
python herramientas/compilar_v4.py
python herramientas/verificar_v4.py
```

Los binarios, logs y contratos de prueba generados permanecen en `.local/c05/`. El caso y sus pruebas requieren el mismo entorno Windows/SDK10.0.103/Framework que v3. [Informe](../docs/semanas/semana07/01_ioc.md) y [evidencias](../evidencia/semanas/semana07/README.md).
