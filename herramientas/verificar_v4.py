"""Verifica el cambio de dependencia y contratos preservados de semana 07."""
import difflib
import hashlib
import json
from pathlib import Path
import subprocess

from verificar_v2 import remove_bodies

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folder = ROOT / "evidencia/semanas/semana07"
    provenance = json.loads((folder / "procedencia.json").read_text(encoding="utf-8"))
    compilation = json.loads((folder / "compilacion_y_pruebas.json").read_text(encoding="utf-8"))
    archive = json.loads((folder / "antecedentes.json").read_text(encoding="utf-8"))
    failures = []
    for row in provenance["source_files"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            failures.append("Fuente v3 modificada: " + row["path"])
    if sha(ROOT / provenance["contracts"]) != provenance["contracts_sha256"]:
        failures.append("Contratos de procedencia alterados")
    previous = (ROOT / "src/v3/caso_reportes/RRHHClass.cs").read_text(encoding="utf-8-sig")
    new = (ROOT / "src/v4/caso_ioc/RRHHClass.cs").read_text(encoding="utf-8-sig")
    names = ["Generar_Report_oficina", "Generar_Report_oficina_Dep"]
    preserved = remove_bodies(previous, names) == remove_bodies(new, names)
    if not preserved:
        failures.append("Firma o código fuera del caso alterado")
    old_generator = (ROOT / "src/v3/caso_reportes/GeneradorReportes.cs").read_text(encoding="utf-8")
    generator = (ROOT / "src/v4/caso_ioc/GeneradorReportes.cs").read_text(encoding="utf-8")
    generator_expected = old_generator.replace("private readonly EjecutorReportesSql _sql;", "private readonly IEjecutorReportes _sql;")
    generator_expected = generator_expected.replace("GeneradorReportes(SqlConnection conexion, SqlDataAdapter adaptador)", "GeneradorReportes(SqlConnection conexion, IEjecutorReportes sql)")
    generator_expected = generator_expected.replace("_sql = new EjecutorReportesSql(conexion, adaptador);", "_sql = sql;")
    minimal_generator = generator == generator_expected
    if not minimal_generator:
        failures.append("El generador cambia fuera de campo/constructor autorizados")
    old_executor = (ROOT / "src/v3/caso_reportes/EjecutorReportesSql.cs").read_text(encoding="utf-8")
    executor = (ROOT / "src/v4/caso_ioc/EjecutorReportesSql.cs").read_text(encoding="utf-8")
    executor_body_preserved = (old_executor.replace("// Dependencia concreta conservada. La entrega IoC queda para semana 07.", "// Semana 07: implementación SQL del contrato inyectado.")
        .replace("public sealed class EjecutorReportesSql", "public sealed class EjecutorReportesSql : IEjecutorReportes") == executor)
    if not executor_body_preserved:
        failures.append("Mecánica SQL alterada")
    comparisons = [("RRHHClass.cs", previous, new), ("GeneradorReportes.cs", old_generator, generator),
                   ("EjecutorReportesSql.cs", old_executor, executor)]
    expected_diff = "".join("".join(difflib.unified_diff(a.splitlines(keepends=True), b.splitlines(keepends=True),
                              fromfile="src/v3/caso_reportes/"+name, tofile="src/v4/caso_ioc/"+name))
                            for name, a, b in comparisons)
    if (folder / "antes_despues.diff").read_text(encoding="utf-8") != expected_diff:
        failures.append("Diff no corresponde al código")
    for row in archive["files"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            failures.append("Antecedente alterado: " + row["path"])
    for row in compilation["active_and_reused_source_hashes"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            failures.append("Fuente distinta de la compilada: " + row["path"])
    if sha(ROOT / "src/v4/pruebas/PruebasIoC.cs") != compilation["test_source_sha256"]:
        failures.append("Prueba distinta de la compilada")
    generated = ROOT / ".local/c05/ContratosRecuperados.cs"
    if not generated.is_file() or sha(generated) != compilation["generated_contract_source_sha256"]:
        failures.append("Fuente generada de contratos distinta de la compilada")
    changed = subprocess.run(["git", "diff", "--name-only", "7bd215a", "--", "legado/", "src/v1/", "src/v2/", "src/v3/",
        "evidencia/baseline/", "evidencia/ingenieria_inversa/", "evidencia/semanas/semana04/", "evidencia/semanas/semana05/",
        "docs/semanas/semana04/", "docs/semanas/semana05/", "referencias/", "datos/"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    if changed:
        failures.append("Etapas anteriores alteradas")
    tests = compilation["tests"]
    if (compilation["library"]["exit_code"] or compilation["library"]["source_count"] != 22
        or compilation["test_compilation"]["exit_code"] or compilation["test_compilation"]["source_count"] != 10
        or not tests or tests["exit_code"] or tests["scenarios_passed"] != 16 or len(tests["scenarios"]) != 16):
        failures.append("Compilación o pruebas no aprobadas")
    files = [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p), "size": p.stat().st_size}
             for p in sorted((ROOT / "src/v4/caso_ioc").glob("*.cs"))]
    result = {"stage": "C05_S07", "ok": not failures, "modified_facade_methods": names,
        "all_other_facade_code_and_public_signatures_preserved": preserved,
        "generator_only_field_and_constructor_changed": minimal_generator,
        "sql_executor_body_and_constructor_preserved": executor_body_preserved,
        "previous_stage_files_changed": bool(changed), "antecedents_hashes_verified": len(archive["files"]),
        "library_compiled": compilation["library"]["exit_code"] == 0,
        "ioc_scenarios_passed": tests["scenarios_passed"] if tests else 0,
        "generated_contract_source_hash_verified": generated.is_file() and sha(generated) == compilation["generated_contract_source_sha256"],
        "active_case_files": files, "received_code_executed": False, "database_connected": False,
        "whole_system_equivalence_verified": False, "failures": failures}
    (folder / "verificacion_v4.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
