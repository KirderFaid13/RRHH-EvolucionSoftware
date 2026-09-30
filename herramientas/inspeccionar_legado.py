"""Inspección estática reproducible: archivos, metadatos CLR y manifiestos.

No carga ni ejecuta ensamblados. No extrae #US, cuerpos IL, recursos, cadenas
de conexión, rutas de depuración ni contenido de configuraciones o respaldos.
Las firmas de métodos se conservan como blobs ECMA-335 hex, sin traducirlas
automáticamente a declaraciones de código fuente.
"""
from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import json
import logging
from pathlib import Path
import sys
import urllib.parse
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
# Instalación alternativa local y excluida de Git; la instalación normal en un
# entorno virtual mediante requirements_ir.txt también es compatible.
LOCAL_DEPS = ROOT / ".local" / "c02" / "pydeps"
if LOCAL_DEPS.is_dir():
    sys.path.insert(0, str(LOCAL_DEPS))
try:
    import dnfile
    import pefile
except ImportError:
    raise SystemExit("Instale herramientas/requirements_ir.txt en su entorno Python.")

logging.getLogger("dnfile").setLevel(logging.CRITICAL)
logging.getLogger("pefile").setLevel(logging.CRITICAL)

RELATED_NAMES = {
    "ClassRRHH.dll", "RecursosHumanos.exe", "GRLL.dll",
    "GRLL.Common.Rutinas.dll", "Seguridad.dll", "ClsCtrls.dll", "TabStrip.dll",
    "Custom Featured MessageBox.dll",
}
MAIN_SELECTED_TYPES = {
    "MainMDI", "FrmImportarAsistencia", "FrmImportarAsistenciaBio",
    "FrmImportarAsistenciaCONSEJO", "FrmImportarAsistenciaFueraSEDE",
    "FrmImportarAsistenciaPROIND",
}
GRLL_SELECTED_TYPES = {
    "ClsExcel", "ClsFunciones", "clsLogin", "clsConexion", "SQLConfiguracion",
    "clsVariables", "ClsTipoDatos",
}
IDENTITY = "urn:schemas-microsoft-com:HashTransforms.Identity"
HASH_ALGORITHMS = {
    "http://www.w3.org/2000/09/xmldsig#sha1": "sha1",
    "http://www.w3.org/2001/04/xmlenc#sha256": "sha256",
}


def digest(data: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, data).hexdigest()


def text(value) -> str:
    return str(value) if value is not None else ""


def version(row) -> str:
    return ".".join(str(getattr(row, field)) for field in
                    ("MajorVersion", "MinorVersion", "BuildNumber", "RevisionNumber"))


def rows(tables, name: str):
    table = getattr(tables, name, None)
    return table.rows if table else []


def type_name(row) -> str | None:
    if row is None:
        return None
    name = text(getattr(row, "TypeName", ""))
    namespace = text(getattr(row, "TypeNamespace", ""))
    return f"{namespace}.{name}" if namespace else name


def enabled_flags(flags, prefix: str) -> list[str]:
    return sorted(key for key, value in vars(flags).items()
                  if key.startswith(prefix) and value is True)


def inspect_pe(data: bytes) -> tuple[dict, dict | None]:
    pe = dnfile.dnPE(data=data)
    info = {
        "machine": pefile.MACHINE_TYPE.get(pe.FILE_HEADER.Machine,
                                           hex(pe.FILE_HEADER.Machine)),
        "managed": bool(pe.net),
    }
    detail = None
    if pe.net:
        tables = pe.net.mdtables
        assembly_rows = rows(tables, "Assembly")
        assembly = assembly_rows[0] if assembly_rows else None
        info.update({
            "assembly_name": text(assembly.Name) if assembly else None,
            "assembly_version": version(assembly) if assembly else None,
            "runtime_metadata_version": pe.net.metadata.struct.Version.rstrip(b"\0").decode("ascii"),
            "clr_flags": enabled_flags(pe.net.Flags, "CLR_"),
            "module_mvid": text(rows(tables, "Module")[0].Mvid) if rows(tables, "Module") else None,
            "type_definition_count": len(rows(tables, "TypeDef")),
            "method_definition_count": len(rows(tables, "MethodDef")),
            "field_definition_count": len(rows(tables, "Field")),
            "manifest_resource_count": len(rows(tables, "ManifestResource")),
            "assembly_references": sorted([
                {"name": text(r.Name), "version": version(r), "culture": text(r.Culture)}
                for r in rows(tables, "AssemblyRef")
            ], key=lambda r: (r["name"], r["version"])),
        })
        if info["assembly_name"] in {
            "ClassRRHH", "RecursosHumanos", "GRLL", "GRLL.Common.Rutinas",
            "Seguridad", "ClsCtrls", "TabStrip", "Custom Featured MessageBox",
        }:
            detail = {"types": [], "selected_method_signatures": []}
            method_indices = {id(m): i for i, m in enumerate(rows(tables, "MethodDef"), start=1)}
            nested = {id(n.NestedClass.row): type_name(n.EnclosingClass.row)
                      for n in rows(tables, "NestedClass")}
            for t in rows(tables, "TypeDef"):
                name = type_name(t)
                extends = getattr(t.Extends, "row", None)
                detail["types"].append({
                    "name": name, "enclosing_type": nested.get(id(t)),
                    "base_type": type_name(extends),
                    "method_count": len(t.MethodList),
                    "field_count": len(t.FieldList),
                    "is_public": bool(t.Flags.tdPublic or t.Flags.tdNestedPublic),
                    "is_interface": bool(t.Flags.tdInterface),
                })
                simple_name = text(t.TypeName)
                if info["assembly_name"] == "RecursosHumanos":
                    selected = simple_name in MAIN_SELECTED_TYPES
                elif info["assembly_name"] == "GRLL":
                    selected = simple_name in GRLL_SELECTED_TYPES
                else:
                    selected = (simple_name != "<Module>" and ".My" not in (name or ""))
                if not selected:
                    continue
                for ref in t.MethodList:
                    method = ref.row
                    detail["selected_method_signatures"].append({
                        "type": name, "name": text(method.Name),
                        "metadata_token": f"0x{0x06000000 | method_indices[id(method)]:08x}",
                        "signature_blob_hex": method.Signature.value.hex(),
                        "is_public": bool(method.Flags.mdPublic),
                        "is_static": bool(method.Flags.mdStatic),
                        "parameters": [
                            {"sequence": p.row.Sequence, "name": text(p.row.Name)}
                            for p in method.ParamList
                        ],
                    })
    pe.close()
    return info, detail


def local_tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def inspect_manifest(path: Path, source: Path, file_index: dict[str, Path]) -> dict:
    xml = ET.fromstring(path.read_bytes())
    item = {"path": path.relative_to(source).as_posix(), "xml_well_formed": True,
            "file_references": [], "prerequisite_assemblies": []}
    for node in xml.iter():
        tag = local_tag(node.tag)
        if tag not in ("dependentAssembly", "file"):
            continue
        relative = node.attrib.get("codebase") if tag == "dependentAssembly" else node.attrib.get("name")
        if not relative:
            identity = next((n for n in node if local_tag(n.tag) == "assemblyIdentity"), None)
            if identity is not None:
                item["prerequisite_assemblies"].append({
                    "name": identity.attrib.get("name"), "version": identity.attrib.get("version"),
                    "architecture": identity.attrib.get("processorArchitecture"),
                })
            continue
        uri = urllib.parse.urlparse(relative)
        if uri.scheme or uri.netloc:
            item["file_references"].append({"reference": "[ubicacion externa omitida]",
                                             "status": "external_location_not_read"})
            continue
        candidate = (path.parent / Path(relative.replace("\\", "/"))).resolve()
        try:
            relative_candidate = candidate.relative_to(source.resolve()).as_posix()
        except ValueError:
            item["file_references"].append({"reference": "[fuera del directorio del legado]",
                                             "status": "outside_source_not_read"})
            continue
        actual_path = file_index.get(relative_candidate.casefold())
        storage_suffix = None
        if actual_path is None:
            actual_path = file_index.get((relative_candidate + ".deploy").casefold())
            if actual_path:
                storage_suffix = ".deploy"
        ref = {"reference": relative.replace("\\", "/"), "resolved_path": relative_candidate,
               "status": "present" if actual_path else "missing",
               "declared_size": int(node.attrib["size"]) if "size" in node.attrib else None}
        if storage_suffix:
            ref["storage_suffix"] = storage_suffix
        if actual_path:
            raw = actual_path.read_bytes()
            ref["actual_size"] = len(raw)
            ref["size_matches"] = (len(raw) == ref["declared_size"]) if ref["declared_size"] is not None else None
            digest_method = next((n for n in node.iter() if local_tag(n.tag) == "DigestMethod"), None)
            digest_value = next((n for n in node.iter() if local_tag(n.tag) == "DigestValue"), None)
            transforms = [n.attrib.get("Algorithm") for n in node.iter() if local_tag(n.tag) == "Transform"]
            if digest_method is not None and digest_value is not None:
                algorithm_uri = digest_method.attrib.get("Algorithm")
                algorithm = HASH_ALGORITHMS.get(algorithm_uri)
                ref["digest_algorithm"] = algorithm_uri
                ref["digest_transforms"] = transforms
                if algorithm and all(t == IDENTITY for t in transforms):
                    try:
                        declared = base64.b64decode("".join((digest_value.text or "").split()), validate=True)
                        actual = hashlib.new(algorithm, raw).digest()
                        ref["digest_status"] = "matches" if declared == actual else "mismatch"
                        ref["declared_digest_hex"] = declared.hex()
                        ref["actual_digest_hex"] = actual.hex()
                    except ValueError:
                        ref["digest_status"] = "invalid_base64"
                else:
                    ref["digest_status"] = "unsupported_algorithm_or_transform"
        item["file_references"].append(ref)
    refs = item["file_references"]
    item["summary"] = {
        "references": len(refs),
        "missing": sum(r["status"] == "missing" for r in refs),
        "size_mismatches": sum(r.get("size_matches") is False for r in refs),
        "digest_mismatches": sum(r.get("digest_status") == "mismatch" for r in refs),
    }
    return item


def write_json(output: Path, name: str, value: dict) -> None:
    (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / ".local" / "RRHH")
    parser.add_argument("--output", type=Path, default=ROOT / "evidencia" / "ingenieria_inversa")
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.is_dir():
        raise SystemExit("No existe la copia restaurada. Ejecute primero herramientas/restaurar_legado.py.")
    manifest_path = ROOT / "evidencia" / "baseline" / "inventario_original.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    originals = manifest["files"]
    expected = {row["original_path"]: row for row in originals}
    paths = sorted((p for p in source.rglob("*") if p.is_file()), key=lambda p: p.relative_to(source).as_posix())
    file_index = {p.relative_to(source).as_posix().casefold(): p for p in paths}
    files = []
    hashes = collections.defaultdict(list)
    pe_cache = {}
    related = {}
    failures = []
    xml_files = []
    xml_errors = []
    pds = []
    for path in paths:
        relative = path.relative_to(source).as_posix()
        raw = path.read_bytes()
        sha = digest(raw)
        row = {"path": relative, "size": len(raw), "sha256": sha,
               "extension": path.suffix.lower() or "[sin extension]"}
        baseline = expected.get(relative)
        row["matches_baseline"] = bool(baseline and baseline["original_sha256"] == sha
                                        and baseline["original_size"] == len(raw))
        hashes[sha].append(relative)
        if raw.startswith(b"MZ"):
            try:
                if sha not in pe_cache:
                    pe_cache[sha] = inspect_pe(raw)
                info, detail = pe_cache[sha]
                row["pe"] = info
                if detail and path.name in RELATED_NAMES:
                    if sha not in related:
                        related[sha] = {"paths": [], "sha256": sha, "metadata": info, **detail}
                    related[sha]["paths"].append(relative)
            except Exception as exc:
                row["pe_error"] = type(exc).__name__
                failures.append({"path": relative, "error_type": type(exc).__name__})
        if path.suffix.lower() in (".manifest", ".application", ".xml", ".config"):
            # Las configuraciones se validan sintácticamente; nunca se exportan valores.
            try:
                ET.fromstring(raw)
                xml_files.append(relative)
            except ET.ParseError:
                xml_errors.append(relative)
        if path.suffix.lower() == ".pdb":
            header = raw[:32]
            fmt = "MSF 7.00" if header.startswith(b"Microsoft C/C++ MSF 7.00") else "formato no identificado"
            pds.append({"path": relative, "size": len(raw), "sha256": sha, "format": fmt,
                        "symbols_or_source_paths_exported": False})
        files.append(row)
    if any(not f["matches_baseline"] for f in files):
        raise SystemExit("La copia inspeccionada contiene diferencias con el inventario original; no se generan evidencias.")
    missing = [{"path": row["original_path"], "size": row["original_size"],
                "sha256": row["original_sha256"], "storage": row["storage"]}
               for row in originals if row["original_path"].casefold() not in file_index]
    pe_files = [f for f in files if "pe" in f]
    data = {
        "schema_version": 1,
        "scope": "Inspeccion estatica de copia restaurada; sin ejecucion ni acceso a CMI",
        "baseline_manifest": "evidencia/baseline/inventario_original.json",
        "baseline_manifest_sha256": digest(manifest_path.read_bytes()),
        "tools": {"dnfile": dnfile.__version__, "pefile": pefile.__version__},
        "summary": {
            "original_files_in_manifest": len(originals), "files_inspected": len(files),
            "inspected_bytes": sum(f["size"] for f in files),
            "files_matching_baseline": sum(f["matches_baseline"] for f in files),
            "files_not_available_in_restored_copy": len(missing),
            "portable_executable_files": len(pe_files),
            "managed_files": sum(f["pe"]["managed"] for f in pe_files),
            "unique_portable_executable_contents": len(pe_cache),
            "metadata_parse_failures": len(failures),
            "xml_well_formed_files": len(xml_files), "xml_parse_failures": len(xml_errors),
            "extensions": dict(sorted(collections.Counter(f["extension"] for f in files).items())),
            "runtime_metadata_versions": dict(sorted(collections.Counter(
                f["pe"].get("runtime_metadata_version", "no administrado") for f in pe_files).items())),
        },
        "not_available": missing, "metadata_errors": failures,
        "xml_errors": xml_errors, "pdb_headers": pds, "files": files,
        "limits": [
            "Version CLR de metadatos no determina por si sola todo el framework requerido.",
            "Los PDB se identifican por cabecera; no se recupero ni verifico codigo fuente con ellos.",
            "El inventario incluye el respaldo local, pero esta inspeccion no lee su contenido ni obtiene su esquema.",
            "Los conteos incluyen tipos y metodos generados por compiladores y disenadores.",
        ],
    }
    own = {"schema_version": 1,
           "scope": "Ensamblados asociados al proyecto en la distribucion; autoria no acreditada por metadatos",
           "signature_format": "Blob de firma ECMA-335 en hexadecimal, no codigo descompilado",
           "method_selection": {
               "RecursosHumanos": sorted(MAIN_SELECTED_TYPES),
               "GRLL": sorted(GRLL_SELECTED_TYPES),
               "other_related_assemblies": "Tipos distintos de <Module> y sin .My en nombre; catalogo completo de tipos en todos los casos",
           },
           "assemblies": sorted(related.values(), key=lambda r: r["paths"][0]),
           "limits": ["No se analizan cuerpos IL ni se afirma un grafo completo de llamadas.",
                      "Los nombres de metodos y parametros no acreditan reglas funcionales ni firmas SQL."]}
    manifests = [inspect_manifest(path, source, file_index) for path in paths
                 if path.suffix.lower() in (".manifest", ".application")]
    deploy = {"schema_version": 1,
              "scope": "Comprobacion estatica de referencias, tamano y digest en manifiestos",
              "execution_performed": False, "deployment_verified": False,
              "summary": {
                  "manifest_files": len(manifests),
                  "file_references": sum(m["summary"]["references"] for m in manifests),
                  "missing_reference_occurrences": sum(m["summary"]["missing"] for m in manifests),
                  "size_mismatch_occurrences": sum(m["summary"]["size_mismatches"] for m in manifests),
                  "digest_mismatch_occurrences": sum(m["summary"]["digest_mismatches"] for m in manifests),
              },
              "manifests": manifests,
              "limits": ["Una referencia ausente impide acreditar la integridad del despliegue, no demuestra por si sola que todas las funciones fallen.",
                         "No se verifico firma de ClickOnce, instalacion, prerequisitos instalados ni ejecucion.",
                         "DigestValue se decodifica de base64; se compara el algoritmo declarado sobre bytes cuando la transformacion es Identity."]}
    all_groups = collections.defaultdict(list)
    for row in originals:
        all_groups[row["original_sha256"]].append(row)
    duplicate_groups = [{"sha256": sha, "size_per_file": group[0]["original_size"],
                         "copies": len(group), "redundant_bytes": (len(group) - 1) * group[0]["original_size"],
                         "paths": sorted(r["original_path"] for r in group)}
                        for sha, group in all_groups.items() if len(group) > 1]
    duplicates = {"schema_version": 1, "scope": "Los 348 originales inventariados, incluido respaldo local",
                  "criterion": "Igualdad SHA-256 y tamano del inventario baseline; no similitud por nombre",
                  "summary": {"original_files": len(originals), "unique_contents": len(all_groups),
                              "duplicate_groups": len(duplicate_groups),
                              "redundant_bytes": sum(g["redundant_bytes"] for g in duplicate_groups)},
                  "groups": sorted(duplicate_groups, key=lambda g: g["paths"][0]),
                  "changes_applied": "Ninguno: las copias originales se conservan"}
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name, result in [("inventario_tecnico.json", data), ("ensamblados_propios.json", own),
                         ("despliegue.json", deploy), ("duplicados.json", duplicates)]:
        write_json(output, name, result)
    print(json.dumps({"inventory": data["summary"], "deployment": deploy["summary"],
                      "duplicates": duplicates["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
