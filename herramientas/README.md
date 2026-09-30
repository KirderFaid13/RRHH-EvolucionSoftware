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
