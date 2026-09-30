"""Compila v2 y prueba contratos del codigo nuevo sin abrir conexiones SQL."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from restaurar_v1 import ROOT, restore


def compile_sources(sources, output, references, target="library"):
    dotnet = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "dotnet/dotnet.exe"
    csc = dotnet.parent / "sdk/10.0.103/Roslyn/bincore/csc.dll"
    if not all(p.is_file() for p in [dotnet, csc, *references]):
        raise SystemExit("Falta SDK10.0.103 o referencias. Restaura el legado y revisa el entorno Windows.")
    response = output.with_suffix(".rsp")
    args = ["-nologo", "-nostdlib+", "-platform:x86", "-langversion:14.0", "-target:" + target, f'-out:"{output}"']
    args += [f'-r:"{p}"' for p in references] + [f'"{p}"' for p in sources]
    response.write_text("\n".join(args)+"\n", encoding="utf-8")
    result = subprocess.run([str(dotnet), str(csc), "@"+str(response)], capture_output=True, text=True)
    log = result.stdout + result.stderr
    output.with_suffix(".log").write_text(log, encoding="utf-8")
    return {"exit_code":result.returncode,"source_count":len(sources),
            "errors":re.findall(r"error (CS\d+)",log),"warnings":re.findall(r"warning (CS\d+)",log),
            "output_sha256":hashlib.sha256(output.read_bytes()).hexdigest() if result.returncode == 0 else None}


def cs_string(text):
    return '@"'+text.replace('"','""')+'"'


def main():
    restore(ROOT / ".local/clave_legado.key", ROOT / ".local/v1_src")
    output_dir = ROOT / ".local/c03"
    output_dir.mkdir(parents=True,exist_ok=True)
    framework = Path(os.environ.get("WINDIR","C:/Windows")) / "Microsoft.NET/Framework/v4.0.30319"
    refs = [framework / name for name in ("mscorlib.dll","System.dll","System.Core.dll","System.Data.dll","System.Xml.dll","System.Xml.Linq.dll","System.Configuration.dll","Microsoft.VisualBasic.dll")]
    business_refs = refs + [ROOT / "legado/RRHH/Seguridad.dll", ROOT / ".local/RRHH/GRLL.dll"]
    case_sources = sorted((ROOT / "src/v2/caso_empleados").glob("*.cs"))
    base_sources = sorted(p for p in (ROOT / ".local/v1_src").rglob("*.cs") if p.relative_to(ROOT / ".local/v1_src").as_posix() != "ClassRRHH/RRHHClass.cs")
    result = {"stage":"C03","sdk":"10.0.103","reference_profile":"installed Framework v4.0.30319","library":compile_sources(base_sources+case_sources,output_dir / "ClassRRHH.v2.diagnostico.dll",business_refs)}
    # Diagnostico del antecedente sin editar ni ejecutar sus fuentes.
    old_sources = sorted((ROOT / "src/v2/antecedentes/src").rglob("*.cs"))
    result["antecedent_compilation"] = compile_sources(old_sources,output_dir / "v2.antecedente.dll",refs)
    contracts = json.loads((ROOT / "evidencia/semanas/semana04/contratos_v1.json").read_text(encoding="utf-8"))
    expected = {row["method"]:row for row in contracts["methods"]}
    if hashlib.sha256((ROOT / contracts["source"]).read_bytes()).hexdigest() != contracts["source_sha256"]:
        raise SystemExit("Los contratos no corresponden al hash de v1.")
    checks = []
    noargs=expected["ObtenerEmpleados"]
    checks.append(f'Check(repo.CrearComandoObtenerEmpleados(),{cs_string(noargs["command"])},CommandType.{noargs["command_type"]},null,0,connection);')
    for method,builder in [("BuscarEmpleado_Codigo","CrearComandoBuscarEmpleado"),("spRRHH_ListarTrabajadores","CrearComandoListarTrabajadores")]:
        row=expected[method]
        parameter=row["parameters"][0]
        checks.append(f'foreach(int value in new[]{{int.MinValue,-1,0,42,int.MaxValue}}) Check(repo.{builder}(value),{cs_string(row["command"])},CommandType.{row["command_type"]},{cs_string(parameter["name"])},value,connection);')
    test_source=output_dir / "PruebasContratos.cs"
    test_source.write_text('''using System;
using System.Data;
using System.Data.SqlClient;
using ClassRRHH;
class PruebasContratos {
 static int scenarios=0;
 static void Require(bool condition) { if(!condition) throw new Exception("Contrato de consulta diferente de v1"); }
 static void Check(SqlCommand c,string text,CommandType type,string parameter,int value,SqlConnection connection) {
  using(c) {
   Require(c.CommandText==text && c.CommandType==type);
   Require(Object.ReferenceEquals(c.Connection,connection));
   Require(connection.State==ConnectionState.Closed);
   Require(c.Parameters.Count==(parameter==null ? 0 : 1));
   if(parameter!=null) {
    Require(c.Parameters[0].ParameterName==parameter);
    Require(c.Parameters[0].SqlDbType==SqlDbType.Int && c.Parameters[0].Direction==ParameterDirection.Input);
    Require(c.Parameters[0].Value is int && (int)c.Parameters[0].Value==value);
   }
   scenarios++;
  }
 }
 static void Main() {
  using(var connection=new SqlConnection()) using(var adapter=new SqlDataAdapter()) {
   var repo=new EmpleadoConsultas(connection,adapter);
''' + "\n".join(checks) + '''
   Require(connection.State==ConnectionState.Closed);
  }
  Console.WriteLine("CONTRACT_SCENARIOS_PASSED="+scenarios);
 }
}
''',encoding="utf-8")
    # Solo dos clases nuevas y el harness; no se ejecutan RRHHClass ni dependencias propias recibidas.
    harness=output_dir / "PruebasContratos.exe"
    result["contract_test_compilation"]=compile_sources([p for p in case_sources if p.name!="RRHHClass.cs"]+[test_source],harness,refs,"exe")
    test=None
    if result["contract_test_compilation"]["exit_code"]==0:
        run=subprocess.run([str(harness)],capture_output=True,text=True,timeout=30)
        match=re.search(r"CONTRACT_SCENARIOS_PASSED=(\d+)",run.stdout)
        test={"exit_code":run.returncode,"scenarios_passed":int(match.group(1)) if match else 0,"connection_opened":False,"scope":"Only command construction in new authored code; no query execution or received assembly execution."}
        (output_dir / "pruebas.log").write_text(run.stdout+run.stderr,encoding="utf-8")
    result["contract_tests"]=test
    result.update(received_code_executed=False,database_connected=False,whole_system_equivalence_verified=False)
    (ROOT / "evidencia/semanas/semana04/compilacion_y_pruebas.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    if result["library"]["exit_code"] or not test or test["exit_code"] or test["scenarios_passed"]!=11:
        raise SystemExit(1)


if __name__=="__main__":
    main()
