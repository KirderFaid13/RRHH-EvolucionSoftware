"""Prueba la auditoría S08 con muestras aisladas y repite v4 sin SQL.

Las fuentes/evidencias de semanas anteriores permanecen intactas. Los nuevos
compilados y los archivos temporales quedan en .local/c06/.
"""
import copy
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from auditar_configuracion import ROOT, audit, audit_files, new_allowed, validate_inventory, write_json
from compilar_v2 import compile_sources


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(call):
    try:
        call()
    except ValueError:
        return True
    return False


def csv_matches(text, rows):
    columns = ["ruta", "bytes", "sha256", "git_blob", "normalizar_lf", "grupo"]
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != columns:
        return False
    return list(reader) == [{k: str(row[k]) for k in columns} for row in rows]


def test_auditor():
    tests = []
    def check(name, result):
        tests.append({"nombre": name, "ok": bool(result)})
    temporary_parent = ROOT / ".local/c06/pruebas_temporales"
    temporary_parent.mkdir(parents=True, exist_ok=True)
    if not temporary_parent.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("El directorio temporal debe estar dentro del workspace")
    # Solo esta muestra creada por la prueba se modifica o elimina al salir.
    with tempfile.TemporaryDirectory(prefix="auditoria_", dir=temporary_parent) as folder:
        root = Path(folder)
        name = "src/caso.cs"
        file = root / name
        file.parent.mkdir()
        original = b"contenido conocido\n"
        file.write_bytes(original)
        row = {"ruta": name, "bytes": len(original), "sha256": hashlib.sha256(original).hexdigest(), "normalizar_lf": True}
        check("archivo_conservado", not audit_files(root, [row], set())["fallos"])
        file.write_bytes(b"cambio sin autorizar\n")
        check("cambio_protegido_detectado", bool(audit_files(root, [row], set())["fallos"]))
        check("cambio_autorizado_identificado", audit_files(root, [row], {name})["autorizados"] == [name])
        file.unlink()
        check("archivo_ausente_detectado", bool(audit_files(root, [row], set())["fallos"]))
        file.write_bytes(original.replace(b"\n", b"\r\n"))
        check("texto_crlf_equivalente_a_lf", not audit_files(root, [row], set())["fallos"])
        file.write_bytes(original)
        escape = dict(row, ruta="../fuera.cs")
        check("escape_de_ruta_rechazado", bool(audit_files(root, [escape], set())["fallos"]))
        absolute = dict(row, ruta="C:/Windows/archivo.cs")
        check("ruta_absoluta_rechazada", bool(audit_files(root, [absolute], set())["fallos"]))
        check("ruta_duplicada_rechazada", bool(audit_files(root, [row, row], set())["fallos"]))
        expected = {"commit": "base", "tree": "arbol", "archivos_versionados": 1, "archivos": [row]}
        tampered = copy.deepcopy(expected)
        tampered["archivos"][0]["sha256"] = "0" * 64
        check("hash_del_inventario_alterado_rechazado", rejected(lambda: validate_inventory(tampered, expected)))
        incomplete = dict(expected, archivos=[])
        check("inventario_incompleto_rechazado", rejected(lambda: validate_inventory(incomplete, expected)))
        check("archivo_nuevo_fuera_de_alcance_rechazado", not new_allowed("src/v4/nuevo.cs"))
        check("secreto_en_carpeta_permitida_rechazado", not new_allowed("configuracion/secreto.key"))
        check("entregable_nuevo_en_alcance_aceptado", new_allowed("docs/semanas/semana08/01_gestion_configuracion.md"))
        check("csv_sin_hash_ni_esquema_rechazado", not csv_matches("ruta\nsrc/caso.cs\n", [row]))
    return {"aprobadas": sum(t["ok"] for t in tests), "total": len(tests), "escenarios": tests,
            "muestras": "Archivos temporales propios, nunca originales RRHH"}


def repeat_v4():
    prior = json.loads((ROOT / "evidencia/semanas/semana07/compilacion_y_pruebas.json").read_text(encoding="utf-8"))
    recovered = json.loads((ROOT / "evidencia/ingenieria_inversa/recuperacion_v1.json").read_text(encoding="utf-8"))
    private_base = ROOT / ".local/v1_src"
    for row in recovered["files"]:
        if row["recovered_path"].endswith(".cs"):
            file = private_base / row["recovered_path"]
            if not file.is_file() or sha(file) != row["recovered_sha256"]:
                raise ValueError("Restaure v1 de forma privada siguiendo herramientas/restaurar_v1.py antes de repetir la compilación")
    for row in prior["active_and_reused_source_hashes"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            raise ValueError("Fuente v4 diferente de C05: " + row["path"])
    source = ROOT / "src/v4/pruebas/PruebasIoC.cs"
    generated = ROOT / ".local/c05/ContratosRecuperados.cs"
    if not generated.is_file() or sha(generated) != prior["generated_contract_source_sha256"]:
        raise ValueError("Falta la fuente diagnóstica de contratos de C05 verificada; consulte el procedimiento de semana 07")
    if sha(source) != prior["test_source_sha256"]:
        raise ValueError("El harness de v4 fue modificado")
    output = ROOT / ".local/c06/compilacion"
    output.mkdir(parents=True, exist_ok=True)
    generated_copy = output / "ContratosRecuperados.cs"
    shutil.copyfile(generated, generated_copy)
    framework = Path(os.environ.get("WINDIR", "C:/Windows")) / "Microsoft.NET/Framework/v4.0.30319"
    refs = [framework / name for name in ("mscorlib.dll", "System.dll", "System.Core.dll", "System.Data.dll", "System.Xml.dll", "System.Xml.Linq.dll", "System.Configuration.dll", "Microsoft.VisualBasic.dll")]
    case = sorted((ROOT / "src/v4/caso_ioc").glob("*.cs"))
    reports = [ROOT / "src/v3/caso_reportes" / name for name in ("IDefinicionReporte.cs", "ReporteOficina.cs", "ReporteOficinaPorSigla.cs", "ComandoReporte.cs")]
    employees = sorted(p for p in (ROOT / "src/v2/caso_empleados").glob("*.cs") if p.name != "RRHHClass.cs")
    base = sorted(p for p in private_base.rglob("*.cs") if p.relative_to(private_base).as_posix() != "ClassRRHH/RRHHClass.cs")
    library = compile_sources(base + employees + reports + case, output / "ClassRRHH.v4.diagnostico.dll", refs + [ROOT / "legado/RRHH/Seguridad.dll", ROOT / ".local/RRHH/GRLL.dll"])
    harness = output / "PruebasIoC.exe"
    compiled = compile_sources([p for p in case if p.name != "RRHHClass.cs"] + reports + [source, generated_copy], harness, refs, "exe")
    tests = {"exit_code": None, "scenarios_passed": 0, "connection_opened": False}
    if compiled["exit_code"] == 0:
        result = subprocess.run([str(harness)], capture_output=True, text=True, timeout=30)
        (output / "pruebas.log").write_text(result.stdout + result.stderr, encoding="utf-8")
        names = [s.strip() for s in re.findall(r"(?m)^PASS:(.+)$", result.stdout)]
        count = re.search(r"IOC_SCENARIOS_PASSED=(\d+)", result.stdout)
        tests = {"exit_code": result.returncode, "scenarios_passed": int(count.group(1)) if count else 0,
                 "scenarios": names, "connection_opened": False,
                 "sql_executor_ejecutar_executed": False, "synthetic_data_only": True}
    return {"library": library, "test_compilation": compiled, "tests": tests,
            "sources_checked_against_c05": True, "received_code_executed": False,
            "database_connected": False, "whole_system_equivalence_verified": False,
            "resultados_anteriores_modificados": False}


def main():
    tests = test_auditor()
    problems = [t["nombre"] for t in tests["escenarios"] if not t["ok"]]
    current = audit()
    problems.extend(current["fallos"])
    inventory = json.loads((ROOT / "configuracion/inventario_c05.json").read_text(encoding="utf-8"))
    csv_ok = csv_matches((ROOT / "configuracion/inventario_c05.csv").read_text(encoding="utf-8"), inventory["archivos"])
    if not csv_ok:
        problems.append("El CSV no coincide con el inventario JSON")
    try:
        v4 = repeat_v4()
        if (v4["library"]["exit_code"] != 0 or v4["library"]["source_count"] != 22
                or v4["test_compilation"]["exit_code"] != 0 or v4["test_compilation"]["source_count"] != 10
                or v4["tests"]["exit_code"] != 0 or v4["tests"]["scenarios_passed"] != 16
                or len(v4["tests"].get("scenarios", [])) != 16):
            problems.append("Compilación o escenarios v4 no aprobados")
    except (OSError, ValueError, subprocess.SubprocessError, SystemExit) as exc:
        v4 = {"estado": "no_comprobado", "motivo": str(exc)}
        problems.append("Repetición v4 no comprobada")
    result = {"id": "C06-S08", "fecha_preparacion": "2026-10-05",
              "fecha_verificacion_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "ok": not problems,
              "pruebas_auditor": tests, "inventario_json_csv_coinciden": csv_ok,
              "auditoria_resumen": current["resumen"], "v4": v4, "fallos": problems,
              "limites": ["Pruebas aisladas de configuración e IoC, sin aplicación original ni SQL",
                          "Sin medición de rendimiento ni verificación completa de autenticación",
                          "Las pruebas automáticas no acreditan revisión humana. La publicación se comprueba en Git y el PR."]}
    write_json(ROOT / "evidencia/semanas/semana08/verificacion_configuracion.json", result)
    write_json(ROOT / "evidencia/semanas/semana08/auditoria_configuracion.json", current)
    print(json.dumps({"ok": result["ok"], "pruebas_auditor": tests["aprobadas"],
                      "pruebas_v4": v4.get("tests", {}).get("scenarios_passed"), "fallos": problems}, ensure_ascii=False))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
