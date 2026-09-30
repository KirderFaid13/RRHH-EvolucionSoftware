"""Restaura la distribución recibida sin modificar ni ejecutar los originales."""
import argparse
import hashlib
import json
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parents[1]
HEADER = b"RRHH-AESGCM-v1\n"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(base, relative):
    target = (base / relative).resolve()
    if not target.is_relative_to(base.resolve()):
        raise ValueError("Ruta fuera del directorio permitido.")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clave", type=Path, default=ROOT / ".local/clave_legado.key")
    parser.add_argument("--destino", type=Path, default=ROOT / ".local/RRHH")
    args = parser.parse_args()
    destination = args.destino.resolve()
    local_root = (ROOT / ".local").resolve()
    if destination.is_relative_to(ROOT) and not destination.is_relative_to(local_root):
        raise SystemExit("Dentro del repositorio, restaura unicamente en .local/ (ignorada por Git).")
    if not args.clave.is_file():
        raise SystemExit("Falta la clave local. Solicitala al responsable por un medio privado; no la subas a Git.")
    key = args.clave.read_bytes()
    if len(key) != 32:
        raise SystemExit("La clave debe tener exactamente 32 bytes.")
    manifest = json.loads((ROOT / "evidencia/baseline/inventario_original.json").read_text(encoding="utf-8"))
    restored = 0
    excluded = 0
    for entry in manifest["files"]:
        if entry["storage"] == "local_only":
            excluded += 1
            continue
        payload = safe_path(ROOT, entry["repository_path"]).read_bytes()
        if digest(payload) != entry["repository_sha256"]:
            raise SystemExit("Integridad del archivo almacenado incorrecta: " + entry["original_path"])
        if entry["storage"] == "aes256_gcm":
            if not payload.startswith(HEADER):
                raise SystemExit("Formato de cifrado desconocido.")
            start = len(HEADER)
            try:
                payload = AESGCM(key).decrypt(
                    payload[start:start + 12], payload[start + 12:],
                    entry["original_path"].encode("utf-8"),
                )
            except Exception:
                raise SystemExit("No se pudo autenticar el archivo cifrado: " + entry["original_path"]) from None
        if digest(payload) != entry["original_sha256"] or len(payload) != entry["original_size"]:
            raise SystemExit("El contenido restaurado no coincide con el original.")
        output = safe_path(destination, entry["original_path"])
        if output.exists():
            if not output.is_file() or digest(output.read_bytes()) != entry["original_sha256"]:
                raise SystemExit("No se sobrescribe un archivo diferente: " + str(output))
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(payload)
        restored += 1
    print(f"Restaurados/verificados: {restored}. Respaldos solo locales: {excluded}.")
    print("La aplicacion no fue ejecutada. Destino: " + str(destination))


if __name__ == "__main__":
    main()
