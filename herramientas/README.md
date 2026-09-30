# Herramientas del baseline

Requisitos: Python 3.10 o posterior. Instalar dependencias, si faltan:

```powershell
python -m pip install -r .\herramientas\requirements.txt
```

- `verificar_baseline.py`: verifica inventarios, archivos directos/cifrados, referencias, JSON, enlaces y, con `--indice`, exclusiones y bytes del índice Git. No modifica el paquete ni ejecuta RRHH.
- `restaurar_legado.py`: recupera los originales en un destino privado y comprueba su integridad antes de escribir. Necesita la clave del responsable; no sobrescribe archivos diferentes ni restaura el BAK.

Los comandos se ejecutan desde la raíz. Consulta [evidencia](../evidencia/baseline/README.md) y [restauración](../legado/README.md).
