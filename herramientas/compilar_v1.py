"""Compila la recuperacion v1 como biblioteca diagnostica, sin ejecutarla."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from restaurar_v1 import ROOT, restore


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", default="10.0.103")
    parser.add_argument("--dotnet", type=Path, default=Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "dotnet/dotnet.exe")
    parser.add_argument("--framework", type=Path, default=Path(os.environ.get("WINDIR", "C:/Windows")) / "Microsoft.NET/Framework/v4.0.30319")
    args = parser.parse_args()
    sources_root = ROOT / ".local/v1_src"
    restore(ROOT / ".local/clave_legado.key", sources_root)
    compiler = args.dotnet.parent / "sdk" / args.sdk / "Roslyn/bincore/csc.dll"
    references = [args.framework / name for name in (
        "mscorlib.dll", "System.dll", "System.Core.dll", "System.Data.dll", "System.Xml.dll",
        "System.Xml.Linq.dll", "System.Configuration.dll", "Microsoft.VisualBasic.dll")]
    references.extend([ROOT / "legado/RRHH/Seguridad.dll", ROOT / ".local/RRHH/GRLL.dll"])
    for required in [args.dotnet, compiler, *references]:
        if not required.is_file():
            raise SystemExit("Falta herramienta o referencia: " + str(required) + ". Restaura el legado y revisa el entorno.")
    source_files = sorted(sources_root.rglob("*.cs"))
    if len(source_files) != 12:
        raise SystemExit("La compilacion requiere exactamente las 12 fuentes de la recuperacion.")
    output_root = ROOT / ".local/c02/compilacion_reproducida"
    output_root.mkdir(parents=True, exist_ok=True)
    output = output_root / "ClassRRHH.v1.diagnostico.dll"
    rsp = output_root / "compilar.rsp"
    lines = ["-nologo", "-target:library", "-platform:x86", "-langversion:14.0", "-nostdlib+", f'-out:"{output}"']
    lines += [f'-r:"{path}"' for path in references]
    lines += [f'"{path}"' for path in source_files]
    rsp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    run = subprocess.run([str(args.dotnet), str(compiler), "@" + str(rsp)], capture_output=True, text=True)
    log = run.stdout + run.stderr
    (output_root / "compilacion.log").write_text(log, encoding="utf-8")
    result = {"exit_code": run.returncode, "source_files": len(source_files), "sdk": args.sdk,
              "compilation_target": "library_x86", "reference_profile": "installed_.NET_Framework_v4.0.30319",
              "error_codes": sorted(set(re.findall(r"error (CS\d+)", log))),
              "warning_codes": sorted(set(re.findall(r"warning (CS\d+)", log))),
              "output_size": output.stat().st_size if run.returncode == 0 else None,
              "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest() if run.returncode == 0 else None,
              "application_executed": False, "database_connected": False,
              "functional_equivalence_verified": False,
              "limits": "Diagnostic compilation with installed framework references; does not verify original target framework, resources, signing, deployment or runtime equivalence."}
    (output_root / "resultado.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if run.returncode:
        raise SystemExit(run.returncode)


if __name__ == "__main__":
    main()
