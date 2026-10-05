"""Auditoría de configuración C06: objetos Git C05 y alcance del cambio S08.

No ejecuta RRHH, no descifra originales y no lee contenido de .local/.
Un PASS verifica integridad y alcance; la revisión humana continúa pendiente.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = "6d82f9fa6aa608a0d7d71c14fb2fc661e9d21fa2"
TREE = "a6b85aad0d6ab119297cd4ffd37c8ef5421a383e"
COUNT = 531
MUTABLE_BASE = {
    "README.md", ".context/ROADMAP.md", ".context/03_course_context.md",
    "docs/README.md", "docs/semanas/README.md", "evidencia/README.md",
    "evidencia/semanas/README.md", "herramientas/README.md", "prompts/README.md",
    "specs/README.md", "referencias/README.md",
}
NEW_PREFIXES = (
    "configuracion/", "docs/semanas/semana08/", "evidencia/semanas/semana08/",
    "referencias/semanas/semana08/", "herramientas/presentacion_semana08/",
)
NEW_FILES = {
    "specs/c06_gestion_configuracion.json", "prompts/05_gestion_configuracion.md",
    "herramientas/auditar_configuracion.py", "herramientas/verificar_configuracion.py",
}
PRIVATE_PROBES = [
    ".local/clave_legado.key", ".local/RRHH/RecursosHumanos.exe.config",
    ".local/RRHH/CMI_Backup_QA.bak", ".local/c06/compilacion/PruebasIoC.exe",
    "src/v4/bin/diagnostico.dll", "prueba.key", "prueba.bak", ".env",
]


def git(root, *args, data=None):
    return subprocess.run(
        ["git", "-c", "safe.directory=" + root.resolve().as_posix(), *args],
        cwd=root, input=data, capture_output=True, check=True,
    ).stdout


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def safe_path(root, name):
    """Rechaza rutas ambiguas, escapes y enlaces que cambien el archivo auditado."""
    p = PurePosixPath(name)
    if (not name or p.is_absolute() or "\\" in name or ":" in name
            or any(part in ("", ".", "..") for part in name.split("/"))):
        raise ValueError("Ruta no permitida: " + name)
    dest = root / name
    current = root
    for part in p.parts:
        current = current / part
        if current.is_symlink() or current.is_junction():
            raise ValueError("Enlace no permitido: " + name)
    if not dest.resolve().is_relative_to(root.resolve()):
        raise ValueError("Ruta fuera del repositorio: " + name)
    return dest


def group_for(name):
    if name.startswith("legado/"):
        return "SCI-LEGADO"
    for version in ("v1", "v2", "v3", "v4"):
        if name.startswith("src/" + version + "/"):
            return "SCI-" + version.upper()
    for prefix, group in (("herramientas/", "SCI-HERRAMIENTAS"),
                          ("referencias/", "SCI-CURSO"), ("evidencia/", "SCI-EVIDENCIA"),
                          ("datos/", "SCI-DATOS"), ("docs/ingenieria_inversa/", "SCI-ARQUITECTURA"),
                          ("docs/", "SCI-DISENO"), ("specs/", "SCI-REQUISITOS"),
                          (".context/", "SCI-REQUISITOS")):
        if name.startswith(prefix):
            return group
    return "SCI-CONTROL"


def read_base(root):
    """Calcula SHA-256 desde objetos del commit fijo, sin confiar en el manifiesto."""
    tree = git(root, "rev-parse", BASE + "^{tree}").decode().strip()
    if tree != TREE:
        raise ValueError("El árbol de la base no coincide con C05")
    entries = []
    for raw in git(root, "ls-tree", "-r", "-z", BASE).split(b"\0"):
        if not raw:
            continue
        meta, name = raw.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        if kind != "blob" or mode != "100644":
            raise ValueError("Elemento Git no admitido en C05")
        entries.append((name.decode("utf-8"), oid))
    if len(entries) != COUNT:
        raise ValueError("La base C05 debe contener 531 archivos")
    names = [name for name, _ in entries]
    attr = git(root, "check-attr", "--source=" + BASE, "-z", "--stdin", "text",
               data=b"\0".join(n.encode("utf-8") for n in names) + b"\0").split(b"\0")
    text_files = {attr[i].decode("utf-8") for i in range(0, len(attr) - 1, 3)
                  if attr[i + 2] == b"set"}
    proc = subprocess.Popen(
        ["git", "-c", "safe.directory=" + root.resolve().as_posix(), "cat-file", "--batch"],
        cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    rows = []
    try:
        for name, oid in entries:
            proc.stdin.write((oid + "\n").encode())
            proc.stdin.flush()
            header = proc.stdout.readline().decode().strip().split()
            if len(header) != 3 or header[1] != "blob":
                raise ValueError("No se pudo leer un objeto de C05")
            size = int(header[2])
            remaining, digest = size, hashlib.sha256()
            while remaining:
                chunk = proc.stdout.read(min(remaining, 1024 * 1024))
                if not chunk:
                    raise ValueError("Objeto Git incompleto")
                digest.update(chunk)
                remaining -= len(chunk)
            if proc.stdout.read(1) != b"\n":
                raise ValueError("Separador de objeto Git inválido")
            rows.append({"ruta": name, "bytes": size, "sha256": digest.hexdigest(),
                         "git_blob": oid, "normalizar_lf": name in text_files,
                         "grupo": group_for(name)})
    finally:
        proc.stdin.close()
        proc.stdout.close()
        proc.wait(timeout=10)
    return {"id": "BASE-C05", "commit": BASE, "tree": TREE, "archivos_versionados": COUNT,
            "origen": "Objetos Git del quinto commit, no una nueva entrega de software",
            "sha256_bytes": "Contenido Git. Solo texto declarado se compara normalizando CRLF a LF.",
            "archivos": rows}


def validate_inventory(inventory, expected):
    if any(inventory.get(k) != expected[k] for k in ("commit", "tree", "archivos_versionados")):
        raise ValueError("Metadatos del inventario distintos de C05")
    if inventory.get("archivos") != expected["archivos"]:
        raise ValueError("Inventario incompleto, duplicado o alterado respecto de los objetos Git")


def audit_files(root, rows, mutable):
    seen, unchanged, modified, failures = set(), [], [], []
    for row in rows:
        name = row["ruta"]
        if name.casefold() in seen:
            failures.append("Ruta duplicada: " + name)
            continue
        seen.add(name.casefold())
        try:
            file = safe_path(root, name)
            if not file.is_file():
                failures.append("Archivo ausente: " + name)
                continue
            data = file.read_bytes()
            if row.get("normalizar_lf", False):
                data = data.replace(b"\r\n", b"\n")
            match = len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"]
            if match:
                unchanged.append(name)
            elif name in mutable:
                modified.append(name)
            else:
                failures.append("Cambio fuera del alcance S08: " + name)
        except (OSError, ValueError) as exc:
            failures.append(str(exc))
    return {"iguales": unchanged, "autorizados": modified, "fallos": failures}


def new_allowed(name):
    low = name.lower()
    if low.startswith((".local/", ".git/")) or low.endswith(
            (".key", ".pem", ".bak", ".mdf", ".ldf", ".exe", ".dll", ".exe.config", ".dll.config")):
        return False
    return name in NEW_FILES or any(name.startswith(prefix) for prefix in NEW_PREFIXES)


def audit(root=ROOT):
    expected = read_base(root)
    inventory = json.loads((root / "configuracion/inventario_c05.json").read_text(encoding="utf-8"))
    validate_inventory(inventory, expected)
    contract = json.loads((root / "specs/c06_gestion_configuracion.json").read_text(encoding="utf-8"))
    if (set(contract["cambios_permitidos_base"]) != MUTABLE_BASE
            or tuple(contract["nuevos_prefijos_permitidos"]) != NEW_PREFIXES
            or set(contract["nuevos_archivos_permitidos"]) != NEW_FILES
            or contract["base"]["commit"] != BASE):
        raise ValueError("El contrato debe mantener el alcance explícito C06")
    checked = audit_files(root, inventory["archivos"], MUTABLE_BASE)
    baseline_paths = {row["ruta"] for row in inventory["archivos"]}
    candidates = set(git(root, "ls-files", "-z", "--cached").decode("utf-8").split("\0"))
    candidates.update(git(root, "ls-files", "-z", "--others", "--exclude-standard").decode("utf-8").split("\0"))
    new_files = sorted(candidates - baseline_paths - {""})
    for name in new_files:
        try:
            file = safe_path(root, name)
            if not new_allowed(name) or not file.is_file():
                checked["fallos"].append("Archivo nuevo fuera del alcance S08: " + name)
        except ValueError as exc:
            checked["fallos"].append(str(exc))
    exclusions = []
    for name in PRIVATE_PROBES:
        ignored = subprocess.run(
            ["git", "-c", "safe.directory=" + root.resolve().as_posix(), "check-ignore", "--no-index", "-q", name],
            cwd=root, capture_output=True, check=False,
        ).returncode == 0
        tracked = bool(git(root, "ls-files", "--", name).strip())
        exclusions.append({"ruta": name, "ignorada": ignored, "versionada": tracked})
        if not ignored or tracked:
            checked["fallos"].append("Exclusión de Git incorrecta: " + name)
    result = {"id": "C06-S08", "fecha_preparacion": contract["fecha_preparacion"],
              "fecha_verificacion_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "ok": not checked["fallos"],
              "base": {k: expected[k] for k in ("commit", "tree", "archivos_versionados")},
              "resumen": {"archivos_verificados": len(inventory["archivos"]),
                          "iguales_a_base": len(checked["iguales"]),
                          "cambios_autorizados": len(checked["autorizados"]),
                          "nuevos_en_alcance": len(new_files), "fallos": len(checked["fallos"])},
              "cambios_autorizados": checked["autorizados"], "nuevos_autorizados": [n for n in new_files if new_allowed(n)],
              "exclusiones_git": exclusions, "fallos": checked["fallos"],
              "revision_humana": "El PASS automático no acredita revisión humana; consulte CAM-S08-001 y la decisión del responsable",
              "publicacion": "Se comprueba en Git y el PR. Esta auditoría no certifica su resultado.",
              "head_observado": git(root, "rev-parse", "HEAD").decode().strip(),
              "limite": "Compara contenido de trabajo, no blobs del índice o futuro commit. No certifica ejecución RRHH, integración SQL, datos, seguridad completa ni equivalencia funcional."}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crear-inventario", action="store_true", help="Crear snapshot C05 desde objetos Git inmutables")
    args = parser.parse_args()
    if args.crear_inventario:
        inventory = read_base(ROOT)
        write_json(ROOT / "configuracion/inventario_c05.json", inventory)
        output = io.StringIO(newline="")
        columns = ["ruta", "bytes", "sha256", "git_blob", "normalizar_lf", "grupo"]
        writer = csv.DictWriter(output, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(inventory["archivos"])
        (ROOT / "configuracion/inventario_c05.csv").write_text(output.getvalue(), encoding="utf-8", newline="\n")
        print("Inventario C05: 531 archivos, creado desde Git.")
    try:
        result = audit()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        result = {"id": "C06-S08", "ok": False, "fallos": [str(exc)]}
    write_json(ROOT / "evidencia/semanas/semana08/auditoria_configuracion.json", result)
    print(json.dumps({k: result[k] for k in ("id", "ok", "resumen", "fallos") if k in result}, ensure_ascii=False))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
