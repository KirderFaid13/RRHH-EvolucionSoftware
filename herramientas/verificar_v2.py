"""Verifica la procedencia y el alcance del caso SRP/DRY, sin ejecutar SQL."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def remove_bodies(text, names):
    for name in names:
        match=re.search(r"(?m)^[ \t]*public [^\n]+?\b"+name+r"\([^\n]*\)[ \t]*\n[ \t]*\{",text)
        if not match:
            raise ValueError("Falta firma de metodo: "+name)
        start=match.end()-1
        depth,end=1,start+1
        while depth:
            depth+=(text[end]=="{")-(text[end]=="}")
            end+=1
        text=text[:start]+"{BODY_REMOVED:"+name+"}"+text[end:]
    return text


def main():
    folder=ROOT / "evidencia/semanas/semana04"
    contracts=json.loads((folder / "contratos_v1.json").read_text(encoding="utf-8"))
    names=[m["method"] for m in contracts["methods"]]
    original=ROOT / contracts["source"]
    previous=original.read_text(encoding="utf-8-sig")
    new=(ROOT / "src/v2/caso_empleados/RRHHClass.cs").read_text(encoding="utf-8-sig")
    failures=[]
    if sha(original.read_bytes())!=contracts["source_sha256"]:
        failures.append("Fuente de procedencia diferente")
    preserved=remove_bodies(previous,names)==remove_bodies(new,names)
    if not preserved:
        failures.append("Cambios fuera de los tres cuerpos autorizados o en firmas publicas")
    audit=json.loads((folder / "antecedentes.json").read_text(encoding="utf-8"))
    for row in audit["files"]:
        if sha((ROOT / row["path"]).read_bytes())!=row["sha256"]:
            failures.append("Antecedente modificado: "+row["path"])
    untouched=subprocess.run(["git","diff","--name-only","9e18ca4","--","legado/","src/v1/","evidencia/baseline/","evidencia/ingenieria_inversa/"],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    if untouched:
        failures.append("Material de C01/C02 alterado")
    compile_result=json.loads((folder / "compilacion_y_pruebas.json").read_text(encoding="utf-8"))
    tests=compile_result["contract_tests"]
    if compile_result["library"]["exit_code"] or tests["exit_code"] or tests["scenarios_passed"]!=11:
        failures.append("Compilacion o pruebas no aprobadas")
    files=[]
    for p in sorted((ROOT / "src/v2/caso_empleados").glob("*.cs")):
        files.append({"path":p.relative_to(ROOT).as_posix(),"sha256":sha(p.read_bytes()),"size":p.stat().st_size})
    text=(ROOT / "src/v2/caso_empleados/EjecutorConsultasSql.cs").read_text(encoding="utf-8")
    if text.count(".Fill(")!=1 or text.count(".Open()")!=1 or text.count(".Close()")!=1:
        failures.append("Mecanica comun no centralizada")
    result={"stage":"C03","ok":not failures,"modified_methods":names,
            "all_other_facade_code_and_public_signatures_preserved":preserved,
            "previous_stage_files_changed":bool(untouched),"antecedents_hashes_verified":len(audit["files"]),
            "library_compiled":compile_result["library"]["exit_code"]==0,
            "contract_scenarios_passed":tests["scenarios_passed"],"received_code_executed":False,"database_connected":False,
            "whole_system_equivalence_verified":False,"execution_sequences_in_three_original_methods":3,
            "execution_sequence_in_shared_helper":1,"active_case_files":files,"failures":failures}
    (folder / "verificacion_v2.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    if failures:
        raise SystemExit(1)


if __name__=="__main__":
    main()
