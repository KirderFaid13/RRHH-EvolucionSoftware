"""Compila v3 y demuestra extensión de reportes sin abrir SQL ni ejecutar legado."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import re

from compilar_v2 import compile_sources, cs_string
from restaurar_v1 import ROOT, restore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_hashes(paths):
    return [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p)} for p in sorted(paths)]


def main():
    restore(ROOT / ".local/clave_legado.key", ROOT / ".local/v1_src")
    output = ROOT / ".local/c04"
    output.mkdir(parents=True, exist_ok=True)
    folder = ROOT / "evidencia/semanas/semana05"
    contracts = json.loads((folder / "contratos_v1.json").read_text(encoding="utf-8"))
    if sha(ROOT / contracts["source"]) != contracts["source_sha256"]:
        raise SystemExit("Los contratos no corresponden al hash de v1.")
    framework = Path(os.environ.get("WINDIR", "C:/Windows")) / "Microsoft.NET/Framework/v4.0.30319"
    refs = [framework / n for n in ("mscorlib.dll", "System.dll", "System.Core.dll", "System.Data.dll", "System.Xml.dll", "System.Xml.Linq.dll", "System.Configuration.dll", "Microsoft.VisualBasic.dll")]
    case = sorted((ROOT / "src/v3/caso_reportes").glob("*.cs"))
    employees = sorted(p for p in (ROOT / "src/v2/caso_empleados").glob("*.cs") if p.name != "RRHHClass.cs")
    base = sorted(p for p in (ROOT / ".local/v1_src").rglob("*.cs") if p.relative_to(ROOT / ".local/v1_src").as_posix() != "ClassRRHH/RRHHClass.cs")
    result = {"stage": "C04", "sdk": "10.0.103", "reference_profile": "installed Framework v4.0.30319",
              "library": compile_sources(base + employees + case, output / "ClassRRHH.v3.diagnostico.dll",
                                         refs + [ROOT / "legado/RRHH/Seguridad.dll", ROOT / ".local/RRHH/GRLL.dll"]),
              "case_and_reused_source_hashes": file_hashes(case + employees)}
    old = sorted((ROOT / "src/v3/antecedentes/src").rglob("*.cs"))
    result["antecedent_compilation"] = compile_sources(old, output / "v3.antecedente.dll", refs)

    # Núcleo con un reporte. La segunda definición no participa en esta compilación.
    core_sources = [p for p in case if p.name not in {"RRHHClass.cs", "ReporteOficinaPorSigla.cs"}]
    core = output / "Reportes.Core.dll"
    result["core_compilation"] = compile_sources(core_sources, core, refs)
    before_sources = file_hashes(core_sources)
    before_binary = sha(core) if result["core_compilation"]["exit_code"] == 0 else None
    extension = output / "Reportes.PorSigla.dll"
    result["extension_compilation"] = None
    result["test_compilation"] = None
    result["contract_tests"] = None
    if before_binary:
        result["extension_compilation"] = compile_sources(
            [ROOT / "src/v3/caso_reportes/ReporteOficinaPorSigla.cs"], extension, refs + [core])
        if result["extension_compilation"]["exit_code"] == 0:
            expected = {row["method"]: row for row in contracts["methods"]}
            calls = []
            for method, definition, values in [
                ("Generar_Report_oficina", "ReporteOficina", ["int.MinValue", "-1", "0", "42", "int.MaxValue"]),
                ("Generar_Report_oficina_Dep", "ReporteOficinaPorSigla", ["null", cs_string(""), cs_string("AREA"), cs_string("área/ñ"), cs_string(" O'NEIL "), cs_string("X" * 1000)]),
            ]:
                row = expected[method]
                for value in values:
                    calls.append(f'Check(generator,new {definition}({value}),{cs_string(row["command"])},CommandType.{row["command_type"]},{cs_string(row["table_name"])},{cs_string(row["parameter"]["name"])},SqlDbType.{row["parameter"]["sql_type"]},{value},connection,adapter);')
            source = output / "PruebasReportes.cs"
            source.write_text('''using System;
using System.Data;
using System.Data.SqlClient;
using ClassRRHH;
class PruebasReportes {
 static int scenarios;
 static void Require(bool ok) { if(!ok) throw new Exception("Contrato de reporte diferente de v1"); }
 static void Check(GeneradorReportes g,IDefinicionReporte definition,string sql,CommandType commandType,
                   string table,string parameter,SqlDbType sqlType,object value,SqlConnection connection,SqlDataAdapter adapter) {
  using(var plan=g.Preparar(definition)) {
   var c=plan.Comando;
   Require(plan.NombreTabla==table && c.CommandText==sql && c.CommandType==commandType);
   Require(Object.ReferenceEquals(c.Connection,connection));
   Require(connection.State==ConnectionState.Closed && adapter.SelectCommand==null);
   Require(c.Parameters.Count==1 && c.Parameters[0].ParameterName==parameter);
   Require(c.Parameters[0].SqlDbType==sqlType && c.Parameters[0].Direction==ParameterDirection.Input);
   Require(Object.Equals(c.Parameters[0].Value,value));
   Require(c.Parameters[0].Size==(value is string ? ((string)value).Length : 0));
   scenarios++;
  }
 }
 static void Main() {
  Require(typeof(ReporteOficina).Assembly==typeof(GeneradorReportes).Assembly);
  Require(typeof(ReporteOficinaPorSigla).Assembly!=typeof(GeneradorReportes).Assembly);
  using(var connection=new SqlConnection()) using(var adapter=new SqlDataAdapter()) {
   var generator=new GeneradorReportes(connection,adapter);
''' + "\n".join(calls) + '''
   Require(connection.State==ConnectionState.Closed && adapter.SelectCommand==null);
  }
  Console.WriteLine("REPORT_CONTRACT_SCENARIOS_PASSED="+scenarios);
  Console.WriteLine("EXTERNAL_EXTENSION_ACCEPTED=True");
 }
}
''', encoding="utf-8", newline="\n")
            harness = output / "PruebasReportes.exe"
            result["test_compilation"] = compile_sources([source], harness, refs + [core, extension], "exe")
            if result["test_compilation"]["exit_code"] == 0:
                run = subprocess.run([str(harness)], capture_output=True, text=True, timeout=30)
                (output / "pruebas.log").write_text(run.stdout + run.stderr, encoding="utf-8")
                count = re.search(r"REPORT_CONTRACT_SCENARIOS_PASSED=(\d+)", run.stdout)
                result["contract_tests"] = {"exit_code": run.returncode, "scenarios_passed": int(count.group(1)) if count else 0,
                    "external_extension_accepted": "EXTERNAL_EXTENSION_ACCEPTED=True" in run.stdout,
                    "connection_opened": False, "scope": "Only authored report preparation via the unchanged generator; no Fill or received code execution."}
    result["extension_proof"] = {"core_source_files_before": before_sources,
        "core_source_files_after": file_hashes(core_sources), "core_sha256_before": before_binary,
        "core_sha256_after": sha(core) if before_binary else None,
        "core_recompiled_for_extension": False,
        "core_unchanged": before_binary is not None and before_binary == sha(core) and before_sources == file_hashes(core_sources)}
    result.update(received_code_executed=False, database_connected=False, whole_system_equivalence_verified=False)
    (folder / "compilacion_y_pruebas.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    tests = result["contract_tests"]
    print(json.dumps({"stage": "C04", "library": result["library"], "antecedent_compilation": result["antecedent_compilation"],
                      "core_compilation": result["core_compilation"], "extension_compilation": result["extension_compilation"],
                      "test_compilation": result["test_compilation"], "contract_tests": tests,
                      "core_unchanged": result["extension_proof"]["core_unchanged"]}, indent=2))
    if (result["library"]["exit_code"] or not tests or tests["exit_code"] or tests["scenarios_passed"] != 11
        or not tests["external_extension_accepted"] or not result["extension_proof"]["core_unchanged"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
