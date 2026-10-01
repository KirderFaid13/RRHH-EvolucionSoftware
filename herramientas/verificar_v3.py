"""Verifica alcance, contratos, extensión y conservación de las etapas anteriores."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

from verificar_v2 import remove_bodies

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_method(text, name):
    match = re.search(r"(?m)^[ \t]*public ([^\n]+?\b"+name+r"\([^\n]*\))[ \t]*\n[ \t]*\{", text)
    start = match.end()-1
    end, depth = start+1, 1
    while depth:
        depth += (text[end] == "{")-(text[end] == "}")
        end += 1
    return match.group(1), text[start:end]


def main():
    folder = ROOT / "evidencia/semanas/semana05"
    contracts = json.loads((folder / "contratos_v1.json").read_text(encoding="utf-8"))
    compilation = json.loads((folder / "compilacion_y_pruebas.json").read_text(encoding="utf-8"))
    archive = json.loads((folder / "antecedentes.json").read_text(encoding="utf-8"))
    previous = (ROOT / contracts["baseline"]).read_text(encoding="utf-8-sig")
    original = (ROOT / contracts["source"]).read_text(encoding="utf-8-sig")
    new = (ROOT / "src/v3/caso_reportes/RRHHClass.cs").read_text(encoding="utf-8-sig")
    names = [row["method"] for row in contracts["methods"]]
    failures = []
    if sha(ROOT / contracts["source"]) != contracts["source_sha256"] or sha(ROOT / contracts["baseline"]) != contracts["baseline_sha256"]:
        failures.append("Fuente de procedencia modificada")
    preserved = remove_bodies(previous, names) == remove_bodies(new, names)
    if not preserved:
        failures.append("Firmas o código fuera de los dos cuerpos autorizados alterados")
    for row in contracts["methods"]:
        signature, body = get_method(original, row["method"])
        if (signature != row["signature"] or get_method(previous, row["method"])[1] != body
            or hashlib.sha256(body.encode("utf-8")).hexdigest() != row["original_method_sha256"]
            or f'new SqlCommand("{row["command"]}", ObjCnn)' not in body
            or f'Fill(dataSet, "{row["table_name"]}")' not in body
            or f'Parameters.Add("{row["parameter"]["name"]}", SqlDbType.{row["parameter"]["sql_type"]}).Value = {row["parameter"]["argument"]}' not in body):
            failures.append("Contrato extraído no corresponde a v1: " + row["method"])
    expected_diff = "".join(difflib.unified_diff(previous.splitlines(keepends=True), new.splitlines(keepends=True),
                         fromfile=contracts["baseline"], tofile="src/v3/caso_reportes/RRHHClass.cs"))
    if (folder / "antes_despues.diff").read_text(encoding="utf-8") != expected_diff:
        failures.append("Diff no corresponde a la fachada")
    for row in archive["files"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            failures.append("Antecedente alterado: " + row["path"])
    changed = subprocess.run(["git", "diff", "--name-only", "a5849d9", "--", "legado/", "src/v1/", "src/v2/",
                  "evidencia/baseline/", "evidencia/ingenieria_inversa/", "evidencia/semanas/semana04/",
                  "docs/semanas/semana04/", "referencias/", "datos/"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    if changed:
        failures.append("Contenido de etapas anteriores alterado")
    for row in compilation["case_and_reused_source_hashes"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            failures.append("Fuente distinta de la compilada: " + row["path"])
    tests = compilation["contract_tests"]
    proof = compilation["extension_proof"]
    if (compilation["library"]["exit_code"] != 0 or compilation["library"]["source_count"] != 20
        or not tests or tests["exit_code"] != 0 or tests["scenarios_passed"] != 11 or not tests["external_extension_accepted"]):
        failures.append("Compilación o pruebas no aprobadas")
    if (not proof["core_unchanged"] or proof["core_recompiled_for_extension"]
        or proof["core_sha256_before"] != proof["core_sha256_after"]
        or proof["core_source_files_before"] != proof["core_source_files_after"]):
        failures.append("No se demuestra núcleo estable al añadir extensión")
    for row in proof["core_source_files_before"]:
        if sha(ROOT / row["path"]) != row["sha256"]:
            failures.append("Núcleo modificado después de la prueba")
    executor = (ROOT / "src/v3/caso_reportes/EjecutorReportesSql.cs").read_text(encoding="utf-8")
    if (executor.count(".Open()") != 1 or executor.count(".Close()") != 1
        or "new DataSet()" not in executor or ".Fill(resultado, reporte.NombreTabla)" not in executor):
        failures.append("Mecánica de DataSet no conservada")
    files = [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p), "size": p.stat().st_size}
             for p in sorted((ROOT / "src/v3/caso_reportes").glob("*.cs"))]
    result = {"stage": "C04", "ok": not failures, "modified_methods": names,
              "all_other_facade_code_and_public_signatures_preserved": preserved,
              "previous_stage_files_changed": bool(changed), "antecedents_hashes_verified": len(archive["files"]),
              "library_compiled": compilation["library"]["exit_code"] == 0,
              "contract_scenarios_passed": tests["scenarios_passed"] if tests else 0,
              "external_extension_without_rebuilding_core": proof["core_unchanged"] and not proof["core_recompiled_for_extension"],
              "active_case_files": files, "received_code_executed": False, "database_connected": False,
              "whole_system_equivalence_verified": False, "failures": failures}
    (folder / "verificacion_v3.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
