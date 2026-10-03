"""Compila v4 y ejecuta el flujo IoC con sustitutos, sin abrir SQL."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from compilar_v2 import compile_sources, cs_string
from restaurar_v1 import ROOT, restore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes(paths):
    return [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p)} for p in sorted(paths)]


def main():
    restore(ROOT / ".local/clave_legado.key", ROOT / ".local/v1_src")
    output = ROOT / ".local/c05"
    output.mkdir(parents=True, exist_ok=True)
    folder = ROOT / "evidencia/semanas/semana07"
    provenance = json.loads((folder / "procedencia.json").read_text(encoding="utf-8"))
    contract_path = ROOT / provenance["contracts"]
    if sha(contract_path) != provenance["contracts_sha256"]:
        raise SystemExit("Los contratos de procedencia cambiaron")
    contracts = json.loads(contract_path.read_text(encoding="utf-8"))
    if sha(ROOT / contracts["source"]) != contracts["source_sha256"]:
        raise SystemExit("Los contratos no corresponden al hash de v1")
    framework = Path(os.environ.get("WINDIR", "C:/Windows")) / "Microsoft.NET/Framework/v4.0.30319"
    refs = [framework / n for n in ("mscorlib.dll", "System.dll", "System.Core.dll", "System.Data.dll", "System.Xml.dll", "System.Xml.Linq.dll", "System.Configuration.dll", "Microsoft.VisualBasic.dll")]
    case = sorted((ROOT / "src/v4/caso_ioc").glob("*.cs"))
    reports = [ROOT / "src/v3/caso_reportes" / n for n in provenance["reused_v3_sources"]]
    employees = sorted(p for p in (ROOT / "src/v2/caso_empleados").glob("*.cs") if p.name != "RRHHClass.cs")
    base = sorted(p for p in (ROOT / ".local/v1_src").rglob("*.cs") if p.relative_to(ROOT / ".local/v1_src").as_posix() != "ClassRRHH/RRHHClass.cs")
    result = {"stage": "C05_S07", "sdk": "10.0.103", "reference_profile": "installed Framework v4.0.30319",
              "library": compile_sources(base + employees + reports + case,
                  output / "ClassRRHH.v4.diagnostico.dll",
                  refs + [ROOT / "legado/RRHH/Seguridad.dll", ROOT / ".local/RRHH/GRLL.dll"]),
              "active_and_reused_source_hashes": source_hashes(case + reports + employees)}
    expected = {row["method"]: row for row in contracts["methods"]}
    calls = []
    for method, definition, values in [
        ("Generar_Report_oficina", "ReporteOficina", ["int.MinValue", "-1", "0", "42", "int.MaxValue"]),
        ("Generar_Report_oficina_Dep", "ReporteOficinaPorSigla", ["null", cs_string(""), cs_string("AREA"), cs_string("área/ñ"), cs_string(" O'NEIL "), cs_string("X"*1000)]),
    ]:
        row = expected[method]
        for i, value in enumerate(values):
            label = method + "_valor_" + str(i+1)
            calls.append(f'Check(generator,fake,new {definition}({value}),{cs_string(row["command"])},{cs_string(row["table_name"])},{cs_string(row["parameter"]["name"])},SqlDbType.{row["parameter"]["sql_type"]},{value},connection,{cs_string(label)});')
    expected_source = output / "ContratosRecuperados.cs"
    expected_source.write_text('''using System.Data;
using System.Data.SqlClient;
using ClassRRHH;
internal partial class PruebasIoC {
 private static void ProbarContratosRecuperados(GeneradorReportes generator,EjecutorSimulado fake,SqlConnection connection) {
''' + "\n".join(calls) + "\n }\n}\n", encoding="utf-8", newline="\n")
    test_source = ROOT / "src/v4/pruebas/PruebasIoC.cs"
    harness = output / "PruebasIoC.exe"
    test_sources = [p for p in case if p.name != "RRHHClass.cs"] + reports + [test_source, expected_source]
    result["test_compilation"] = compile_sources(test_sources, harness, refs, "exe")
    result["test_source_sha256"] = sha(test_source)
    result["generated_contract_source_sha256"] = sha(expected_source)
    result["tests"] = None
    if result["test_compilation"]["exit_code"] == 0:
        run = subprocess.run([str(harness)], capture_output=True, text=True, timeout=30)
        (output / "pruebas.log").write_text(run.stdout+run.stderr, encoding="utf-8")
        count = re.search(r"IOC_SCENARIOS_PASSED=(\d+)", run.stdout)
        names = re.findall(r"(?m)^PASS:(.+)$", run.stdout)
        result["tests"] = {"exit_code": run.returncode, "scenarios_passed": int(count.group(1)) if count else 0,
            "scenarios": [name.strip() for name in names], "original_contract_scenarios": 11,
            "generator_generar_executed_with_substitute": True, "sql_executor_ejecutar_executed": False,
            "connection_opened": False, "synthetic_data_only": True}
    result.update(received_code_executed=False, database_connected=False, whole_system_equivalence_verified=False)
    (folder / "compilacion_y_pruebas.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps({"stage": result["stage"], "library": result["library"],
                      "test_compilation": result["test_compilation"], "tests": result["tests"]}, ensure_ascii=False, indent=2))
    if result["library"]["exit_code"] or not result["tests"] or result["tests"]["exit_code"] or result["tests"]["scenarios_passed"] != 16:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
