"""Comprueba la integridad del baseline y las exclusiones, sin ejecutar RRHH."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HEADER = b"RRHH-AESGCM-v1\n"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(base, relative):
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError("Ruta fuera del directorio permitido.")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origen", type=Path)
    parser.add_argument("--clave", type=Path, default=ROOT / ".local/clave_legado.key")
    parser.add_argument("--salida", type=Path)
    parser.add_argument("--indice", action="store_true")
    args = parser.parse_args()
    failures = []
    counts = {"original_inventory": 0, "unchanged_verified": 0, "encrypted_storage_verified": 0,
              "encrypted_original_verified": 0, "excluded_backup": 0, "source_original_verified": 0,
              "configuration_examples": 0, "reference_pdfs": 0, "json_documents": 0,
              "markdown_documents": 0, "git_inventory_files_verified": 0}
    manifest = json.loads((ROOT / "evidencia/baseline/inventario_original.json").read_text(encoding="utf-8"))
    references = json.loads((ROOT / "evidencia/baseline/inventario_referencias.json").read_text(encoding="utf-8"))
    cipher = None
    if args.clave.is_file():
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        key = args.clave.read_bytes()
        if len(key) != 32:
            raise SystemExit("Clave invalida: se requieren 32 bytes.")
        cipher = AESGCM(key)
    repository_paths = []
    originals = set()
    for entry in manifest["files"]:
        relative = entry["original_path"]
        if relative in originals:
            failures.append("Ruta duplicada: " + relative)
        originals.add(relative)
        counts["original_inventory"] += 1
        if args.origen:
            source = safe_path(args.origen, relative)
            if not source.is_file() or sha(source.read_bytes()) != entry["original_sha256"] or source.stat().st_size != entry["original_size"]:
                failures.append("Original local diferente o ausente: " + relative)
            else:
                counts["source_original_verified"] += 1
        mode = entry["storage"]
        if mode == "local_only":
            if entry["repository_path"] is not None or entry["repository_sha256"] is not None:
                failures.append("El respaldo excluido declara un archivo de repositorio.")
            counts["excluded_backup"] += 1
            continue
        stored = safe_path(ROOT, entry["repository_path"])
        repository_paths.append(entry["repository_path"])
        if not stored.is_file():
            failures.append("Archivo almacenado ausente: " + relative)
            continue
        payload = stored.read_bytes()
        if sha(payload) != entry["repository_sha256"]:
            failures.append("Hash almacenado diferente: " + relative)
        if mode == "unchanged":
            if sha(payload) != entry["original_sha256"] or len(payload) != entry["original_size"]:
                failures.append("Archivo directo alterado: " + relative)
            else:
                counts["unchanged_verified"] += 1
        elif mode == "aes256_gcm":
            if not payload.startswith(HEADER):
                failures.append("Formato cifrado invalido: " + relative)
                continue
            counts["encrypted_storage_verified"] += 1
            if cipher:
                start = len(HEADER)
                try:
                    plain = cipher.decrypt(payload[start:start + 12], payload[start + 12:], relative.encode("utf-8"))
                    if sha(plain) != entry["original_sha256"] or len(plain) != entry["original_size"]:
                        failures.append("Contenido descifrado diferente: " + relative)
                    else:
                        counts["encrypted_original_verified"] += 1
                except Exception:
                    failures.append("Autenticacion del cifrado fallida: " + relative)
        else:
            failures.append("Modo de almacenamiento desconocido: " + relative)
        if entry.get("configuration_example"):
            example = safe_path(ROOT, entry["configuration_example"])
            try:
                tree = ET.fromstring(example.read_bytes())
                for node in tree.iter():
                    values = [node.text or "", *node.attrib.values()]
                    if any(re.search(r"(?:password|pwd)\s*=\s*[^;\s]+", value, re.I) for value in values):
                        failures.append("Asignacion de password en ejemplo: " + entry["configuration_example"])
                counts["configuration_examples"] += 1
            except (OSError, ET.ParseError):
                failures.append("Ejemplo XML ausente o invalido: " + entry["configuration_example"])
    for entry in references["files"]:
        file = safe_path(ROOT, entry["path"])
        if not file.is_file() or sha(file.read_bytes()) != entry["sha256"] or file.stat().st_size != entry["size"]:
            failures.append("Referencia PDF diferente o ausente: " + entry["path"])
        else:
            counts["reference_pdfs"] += 1
        repository_paths.append(entry["path"])
    for file in ROOT.rglob("*"):
        if not file.is_file():
            continue
        relative = file.relative_to(ROOT)
        if relative.parts[0] in {".git", ".local", "legado"}:
            continue
        if file.suffix == ".json":
            try:
                json.loads(file.read_text(encoding="utf-8"))
                counts["json_documents"] += 1
            except (UnicodeError, json.JSONDecodeError):
                failures.append("JSON invalido: " + relative.as_posix())
        if file.suffix == ".md":
            counts["markdown_documents"] += 1
            for target in re.findall(r"\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
                if re.match(r"(?:https?://|mailto:|#)", target):
                    continue
                target = unquote(target.strip("<>").split("#", 1)[0])
                if target and not (file.parent / target).exists():
                    failures.append("Enlace inexistente: " + relative.as_posix() + " -> " + target)
    expected = {"original_inventory": 348, "unchanged_verified": 335,
                "encrypted_storage_verified": 12, "excluded_backup": 1,
                "configuration_examples": 6, "reference_pdfs": 8}
    for name, value in expected.items():
        if counts[name] != value:
            failures.append("Conteo inesperado: " + name)
    if cipher and counts["encrypted_original_verified"] != 12:
        failures.append("No se verificaron todos los originales cifrados.")
    if args.indice:
        run = lambda command, **kwargs: subprocess.run(command, cwd=ROOT, capture_output=True, check=True, **kwargs)
        tracked = run(["git", "ls-files", "--stage"], text=True).stdout
        index = {}
        for line in tracked.splitlines():
            metadata, path = line.split("\t", 1)
            index[path] = metadata.split()[1]
            if (path.startswith(".local/") or path.endswith((".key", ".bak", ".exe.config", ".dll.config"))):
                failures.append("Archivo privado en indice Git: " + path)
        input_paths = "\n".join(repository_paths) + "\n"
        hashes = run(["git", "hash-object", "--no-filters", "--stdin-paths"], input=input_paths, text=True).stdout.splitlines()
        for path, git_hash in zip(repository_paths, hashes):
            if index.get(path) != git_hash:
                failures.append("Git no conserva los bytes registrados: " + path)
            else:
                counts["git_inventory_files_verified"] += 1
        if len(hashes) != len(repository_paths):
            failures.append("Conteo incompleto de hashes Git.")
        ignored = run(["git", "check-ignore", ".local/clave_legado.key"], text=True).stdout.strip()
        if ignored != ".local/clave_legado.key":
            failures.append("La clave local no esta ignorada por Git.")
    result = {"scope": "commit_01_rrhh_original", "ok": not failures, "counts": counts,
              "encrypted_original_check": "verified_with_local_key" if cipher else "not_checked_key_unavailable",
              "source_original_check": "verified" if args.origen else "not_requested",
              "git_index_check": "verified" if args.indice else "not_requested",
              "application_executed": False, "database_restored": False, "failures": failures}
    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
