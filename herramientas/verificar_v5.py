"""Verifica el cambio mínimo S09, su evidencia y la conservación de etapas previas."""
from datetime import datetime, timezone
import json
import subprocess

from compilar_v5 import BASE, EVIDENCE, GENERATOR, LIFECYCLE, OUTPUT, ROOT, EXPECTED_FAILURES
from compilar_v5 import checked_inputs, hashes, read_json, relative, sha, write_json


def git(*args, data=None):
    return subprocess.run(["git", "-c", "safe.directory=" + ROOT.as_posix(), *args], cwd=ROOT,
                          input=data, capture_output=True, check=True).stdout


def protected(name):
    prefixes = ("legado/", "src/v1/", "src/v2/", "src/v3/", "src/v4/", "datos/",
                "evidencia/baseline/", "evidencia/ingenieria_inversa/",
                "evidencia/semanas/semana04/", "evidencia/semanas/semana05/",
                "evidencia/semanas/semana07/", "evidencia/semanas/semana08/",
                "docs/ingenieria_inversa/", "docs/semanas/semana04/", "docs/semanas/semana05/",
                "docs/semanas/semana07/", "docs/semanas/semana08/", "referencias/semanas/")
    return (name.startswith(prefixes)
            or name in ("configuracion/inventario_c05.json", "configuracion/inventario_c05.csv")
            or (name.startswith("herramientas/") and not name.endswith("README.md")))


def preserve_history():
    """Compara blobs de trabajo normalizados por atributos Git, no solo el HEAD."""
    checked, failures, candidates = [], [], []
    for raw in git("ls-tree", "-r", "-z", BASE).split(b"\0"):
        if not raw:
            continue
        meta, encoded = raw.split(b"\t", 1)
        name = encoded.decode("utf-8")
        if not protected(name):
            continue
        expected = meta.decode().split()[2]
        path = ROOT / name
        if not path.is_file() or path.is_symlink() or path.is_junction():
            failures.append("Archivo histórico ausente/enlazado: " + name)
            continue
        if any(character in name for character in ('\n', '\r', '"', '\\')):
            raise ValueError("Nombre histórico no admitido para lectura por lotes")
        candidates.append((name, expected))
    encoded = ("\n".join(name for name, _ in candidates) + "\n").encode("utf-8")
    observed_hashes = git("hash-object", "--stdin-paths", data=encoded).decode().splitlines()
    if len(observed_hashes) != len(candidates):
        raise ValueError("La lectura por lotes devolvió una cantidad de blobs inesperada")
    for (name, expected), observed in zip(candidates, observed_hashes):
        if observed != expected:
            failures.append("Blob histórico modificado: " + name)
        else:
            checked.append(name)
    return checked, failures


def main():
    inputs = checked_inputs()
    evidence = read_json(EVIDENCE / "compilacion_y_pruebas.json")
    provenance = read_json(EVIDENCE / "procedencia_codigo.json")
    failures = []
    old = (ROOT / "src/v4/caso_ioc/GeneradorReportes.cs").read_text(encoding="utf-8-sig")
    expected = old.replace("        return _sql.Ejecutar(Preparar(reporte));",
                           "        using (var comando = Preparar(reporte))\n"
                           "        {\n            return _sql.Ejecutar(comando);\n        }")
    minimal = expected != old and GENERATOR.read_text(encoding="utf-8-sig") == expected
    if not minimal:
        failures.append("El generador cambia fuera del using autorizado en Generar")
    history, problems = preserve_history()
    failures.extend(problems)
    if evidence["active_and_reused_source_hashes"] != hashes(inputs["active"]):
        failures.append("Fuentes activas diferentes de las compiladas")
    if (evidence["lifecycle_test_source_sha256"] != sha(LIFECYCLE)
            or evidence["regression_test_source_sha256"] != sha(inputs["regression"])
            or evidence["generated_contract_source_sha256"] != sha(OUTPUT / "ContratosRecuperados.cs")):
        failures.append("Harness o contratos diferentes de los compilados")
    sources = inputs["active"] + [LIFECYCLE, inputs["regression"]]
    if (provenance["source_files"] != hashes(sources)
            or provenance["private_v1_sources"] != hashes(inputs["base"])
            or provenance["original_compile_references"] != hashes(inputs["business_refs"])
            or provenance["compiler_script_sha256"] != sha(ROOT / "herramientas/compilar_v5.py")):
        failures.append("Procedencia distinta de las fuentes o herramientas actuales")
    library = evidence["library"]
    if library["exit_code"] != 0 or library["source_count"] != 22:
        failures.append("Biblioteca diagnóstica no aprobada o selección inesperada")
    if (not (OUTPUT / "ClassRRHH.v5.diagnostico.dll").is_file()
            or sha(OUTPUT / "ClassRRHH.v5.diagnostico.dll") != library["output_sha256"]):
        failures.append("Biblioteca distinta de la compilada")
    observed = {}
    for name, passed, code, failed, count in (("rojo_v4", 4, 1, EXPECTED_FAILURES, 9),
                                             ("verde_v5", 6, 0, [], 9),
                                             ("regresion_v5", 16, 0, [], 10)):
        suite = evidence["suites"][name]
        compilation, tests = suite["compilation"], suite["tests"]
        executable = OUTPUT / (name + ".exe")
        if (compilation["exit_code"] != 0 or compilation["source_count"] != count
                or not executable.is_file() or sha(executable) != compilation["output_sha256"]
                or not tests or tests["exit_code"] != code or tests["scenarios_passed"] != passed
                or len(tests["scenarios"]) != passed or tests["failures"] != failed):
            failures.append("Suite no reproducida con el resultado esperado: " + name)
        observed[name] = {"approved": tests["scenarios_passed"] if tests else None,
                          "expected_failure_count": len(failed), "compiled_sources": count}
    if not evidence["ok"] or evidence["failures"]:
        failures.append("La evidencia de compilación no está aprobada")
    probes = (".local/c07/verde_v5.exe", ".local/clave_legado.key", "prueba.bak", ".env")
    exclusions = []
    for name in probes:
        ignored = subprocess.run(["git", "-c", "safe.directory=" + ROOT.as_posix(), "check-ignore",
                                  "--no-index", "-q", name], cwd=ROOT, capture_output=True).returncode == 0
        tracked = bool(git("ls-files", "--", name).strip())
        exclusions.append({"path": name, "ignored": ignored, "tracked": tracked})
        if not ignored or tracked:
            failures.append("Material privado/generado no excluido: " + name)
    result = {"stage": "C07-S09", "ok": not failures, "solicitud": "CAM-S09-001", "issue": 10,
              "verification_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "base_commit": BASE, "head_observed": git("rev-parse", "HEAD").decode().strip(),
              "branch_observed": git("branch", "--show-current").decode().strip(),
              "generator_only_using_changed": minimal, "active_implementation": relative(GENERATOR),
              "historical_blobs_preserved": len(history), "historical_changes": problems,
              "library_sources": library["source_count"], "suites": observed,
              "private_exclusions": exclusions, "source_sha256": sha(GENERATOR),
              "received_code_executed": False, "database_connected": False,
              "whole_system_equivalence_verified": False, "failures": failures,
              "limits": ["Compara archivos de trabajo con blobs Git de la base; no certifica el índice futuro.",
                         "El fallo rojo es intencional y esperado; las seis pruebas v5 y dieciséis regresiones deben aprobar.",
                         "No certifica revisión humana, publicación, SQL, interfaz ni liberación de conexiones."]}
    write_json(EVIDENCE / "verificacion_v5.json", result)
    print(json.dumps({"ok": result["ok"], "historical_blobs_preserved": len(history),
                      "suites": observed, "failures": failures}, ensure_ascii=False))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
