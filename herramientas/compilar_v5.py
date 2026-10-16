"""C07/S09: compila v5, reproduce el defecto v4 y prueba sin SQL.

Solo escribe .local/c07/ y evidencia nueva S09. No restaura ni ejecuta el legado.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

from compilar_v2 import compile_sources

ROOT = Path(__file__).resolve().parents[1]
BASE = "6c13e74482563cc158c4329852753f7f1eb2effd"
OUTPUT = ROOT / ".local/c07"
EVIDENCE = ROOT / "evidencia/semanas/semana09"
GENERATOR = ROOT / "src/v5/caso_cambio/GeneradorReportes.cs"
LIFECYCLE = ROOT / "src/v5/pruebas/PruebasCicloVida.cs"
EXPECTED_FAILURES = ["comando_liberado_tras_exito", "comando_liberado_tras_error"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def relative(path):
    return path.relative_to(ROOT).as_posix()


def hashes(paths):
    return [{"path": relative(path), "sha256": sha(path)} for path in sorted(paths)]


def checked_inputs():
    """Comprueba dependencias ya restauradas sin leer claves ni ejecutar originales."""
    contract = read_json(ROOT / "specs/c07_gestion_cambio.json")
    if (contract["base"]["commit"] != BASE
            or contract["implementacion"]["nuevas_fuentes"] != [relative(GENERATOR)]
            or contract["solicitudes"][0]["id"] != "CAM-S09-001"
            or contract["solicitudes"][0]["issue"] != 10):
        raise ValueError("Contrato distinto del alcance CAM-S09-001")
    prior = read_json(ROOT / "evidencia/semanas/semana07/compilacion_y_pruebas.json")
    for row in prior["active_and_reused_source_hashes"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            raise ValueError("Fuente histórica diferente de C05: " + row["path"])
    recovery = read_json(ROOT / "evidencia/ingenieria_inversa/recuperacion_v1.json")
    private = ROOT / ".local/v1_src"
    base = []
    for row in recovery["files"]:
        if not row["recovered_path"].endswith(".cs"):
            continue
        source = private / row["recovered_path"]
        if not source.is_file() or sha(source) != row["recovered_sha256"]:
            raise ValueError("Falta v1 privada verificada; consulte herramientas/restaurar_v1.py")
        if row["recovered_path"] != "ClassRRHH/RRHHClass.cs":
            base.append(source)
    original = read_json(ROOT / "evidencia/baseline/inventario_original.json")
    references = []
    for name, file in (("GRLL.dll", ROOT / ".local/RRHH/GRLL.dll"),
                       ("Seguridad.dll", ROOT / "legado/RRHH/Seguridad.dll")):
        row = next(row for row in original["files"] if row["original_path"] == name)
        if not file.is_file() or sha(file) != row["original_sha256"]:
            raise ValueError("Falta dependencia original verificada: " + name)
        references.append(file)
    generated = ROOT / ".local/c05/ContratosRecuperados.cs"
    regression = ROOT / "src/v4/pruebas/PruebasIoC.cs"
    if not generated.is_file() or sha(generated) != prior["generated_contract_source_sha256"]:
        raise ValueError("Falta el contrato diagnóstico S07 verificado en .local/c05/")
    if sha(regression) != prior["test_source_sha256"]:
        raise ValueError("El harness S07 debe conservarse intacto")
    employees = sorted(path for path in (ROOT / "src/v2/caso_empleados").glob("*.cs")
                       if path.name != "RRHHClass.cs")
    reports = [ROOT / "src/v3/caso_reportes" / name for name in
               ("ComandoReporte.cs", "IDefinicionReporte.cs", "ReporteOficina.cs", "ReporteOficinaPorSigla.cs")]
    reused = [ROOT / "src/v4/caso_ioc" / name for name in
              ("RRHHClass.cs", "IEjecutorReportes.cs", "ComposicionReportes.cs", "EjecutorReportesSql.cs")]
    active = employees + reports + reused + [GENERATOR]
    library = sorted(base) + active
    if len(base) != 11 or len(library) != 22:
        raise ValueError("La selección diagnóstica debe mantener once fuentes v1 y 22 en total")
    core_v5 = [path for path in reused if path.name != "RRHHClass.cs"] + [GENERATOR]
    core_v4 = [path for path in core_v5 if path != GENERATOR] + [ROOT / "src/v4/caso_ioc/GeneradorReportes.cs"]
    framework = Path(os.environ.get("WINDIR", "C:/Windows")) / "Microsoft.NET/Framework/v4.0.30319"
    framework_refs = [framework / name for name in
                      ("mscorlib.dll", "System.dll", "System.Core.dll", "System.Data.dll", "System.Xml.dll",
                       "System.Xml.Linq.dll", "System.Configuration.dll", "Microsoft.VisualBasic.dll")]
    return {"contract": contract, "prior": prior, "library": library, "active": active,
            "base": sorted(base), "business_refs": references, "framework_refs": framework_refs,
            "core_v4": core_v4, "core_v5": core_v5, "reports": reports,
            "regression": regression, "generated": generated}


def run_suite(executable, marker, log_name):
    run = subprocess.run([str(executable)], capture_output=True, text=True, timeout=30)
    (OUTPUT / log_name).write_text(run.stdout + run.stderr, encoding="utf-8", newline="\n")
    passed = [name.strip() for name in re.findall(r"(?m)^PASS:(.+)$", run.stdout)]
    failed = [name.strip() for name in re.findall(r"(?m)^FAIL:(.+)$", run.stdout)]
    count = re.search(re.escape(marker) + r"=(\d+)", run.stdout)
    return {"exit_code": run.returncode, "scenarios_passed": int(count.group(1)) if count else 0,
            "scenarios": passed, "failures": failed, "connection_opened": False,
            "sql_executor_ejecutar_executed": False, "synthetic_data_only": True}


def main():
    inputs = checked_inputs()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    generated = OUTPUT / "ContratosRecuperados.cs"
    shutil.copyfile(inputs["generated"], generated)
    library = compile_sources(inputs["library"], OUTPUT / "ClassRRHH.v5.diagnostico.dll",
                              inputs["framework_refs"] + inputs["business_refs"])
    suites = {}
    for name, core in (("rojo_v4", inputs["core_v4"]), ("verde_v5", inputs["core_v5"])):
        executable = OUTPUT / (name + ".exe")
        compilation = compile_sources(core + inputs["reports"] + [LIFECYCLE], executable,
                                      inputs["framework_refs"], "exe")
        execution = (run_suite(executable, "LIFECYCLE_SCENARIOS_PASSED", name + ".pruebas.log")
                     if compilation["exit_code"] == 0 else None)
        suites[name] = {"compilation": compilation, "tests": execution}
    executable = OUTPUT / "regresion_v5.exe"
    compilation = compile_sources(inputs["core_v5"] + inputs["reports"]
                                  + [inputs["regression"], generated], executable,
                                  inputs["framework_refs"], "exe")
    execution = (run_suite(executable, "IOC_SCENARIOS_PASSED", "regresion_v5.pruebas.log")
                 if compilation["exit_code"] == 0 else None)
    suites["regresion_v5"] = {"compilation": compilation, "tests": execution}
    failures = []
    if library["exit_code"] != 0:
        failures.append("Biblioteca diagnóstica no compilada")
    for name, expected_passed, expected_code, expected_failed in (
            ("rojo_v4", 4, 1, EXPECTED_FAILURES), ("verde_v5", 6, 0, []),
            ("regresion_v5", 16, 0, [])):
        suite = suites[name]
        tests = suite["tests"]
        if (suite["compilation"]["exit_code"] != 0 or not tests
                or tests["scenarios_passed"] != expected_passed
                or len(tests["scenarios"]) != expected_passed
                or tests["exit_code"] != expected_code or tests["failures"] != expected_failed):
            failures.append("Resultado diferente del esperado: " + name)
    source_files = inputs["active"] + [LIFECYCLE, inputs["regression"]]
    provenance = {"stage": "C07-S09", "base_commit": BASE, "solicitud": "CAM-S09-001", "issue": 10,
                  "new_implementation": relative(GENERATOR), "source_files": hashes(source_files),
                  "private_v1_sources": hashes(inputs["base"]),
                  "original_compile_references": hashes(inputs["business_refs"]),
                  "regression_harness_sha256": sha(inputs["regression"]),
                  "generated_contract_source_sha256": sha(generated),
                  "compiler_script_sha256": sha(Path(__file__)),
                  "historical_evidence_rewritten": False,
                  "received_code_executed": False, "database_connected": False}
    result = {"stage": "C07-S09", "solicitud": "CAM-S09-001", "issue": 10, "base_commit": BASE,
              "verification_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "ok": not failures, "sdk": "10.0.103", "reference_profile": "installed Framework v4.0.30319",
              "library": library, "suites": suites, "active_and_reused_source_hashes": hashes(inputs["active"]),
              "lifecycle_test_source_sha256": sha(LIFECYCLE),
              "regression_test_source_sha256": sha(inputs["regression"]),
              "generated_contract_source_sha256": sha(generated),
              "received_code_executed": False, "database_connected": False,
              "whole_system_equivalence_verified": False, "historical_evidence_rewritten": False,
              "failures": failures,
              "limits": ["El rojo v4 es esperado: reproduce dos ausencias de Dispose, no una fuga medida en producción.",
                         "Solo ejecución síncrona con sustitutos; no se ejecutan fachada ni Fill ni SQL.",
                         "Se libera el comando; no se prueba cierre de conexión ni integración CMI.",
                         "El PASS automático no acredita revisión humana ni estado de publicación."]}
    write_json(EVIDENCE / "procedencia_codigo.json", provenance)
    write_json(EVIDENCE / "compilacion_y_pruebas.json", result)
    print(json.dumps({"ok": result["ok"], "library_sources": library["source_count"],
                      "rojo_v4": suites["rojo_v4"]["tests"], "verde_v5": suites["verde_v5"]["tests"],
                      "regresion_v5": suites["regresion_v5"]["tests"], "failures": failures}, ensure_ascii=False))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
