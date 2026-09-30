"""Recupera los archivos de la descompilacion v1 en un destino privado."""
import argparse
import json
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from restaurar_legado import HEADER, ROOT, digest, safe_path


def restore(key_path, destination):
    destination = destination.resolve()
    if destination.is_relative_to(ROOT) and not destination.is_relative_to((ROOT / ".local").resolve()):
        raise ValueError("Dentro del repositorio, restaura unicamente en .local/.")
    key = key_path.read_bytes()
    if len(key) != 32:
        raise ValueError("La clave debe tener 32 bytes.")
    manifest = json.loads((ROOT / "evidencia/ingenieria_inversa/recuperacion_v1.json").read_text(encoding="utf-8"))
    assembly = safe_path(ROOT, manifest["source_assembly"])
    if digest(assembly.read_bytes()) != manifest["source_assembly_sha256"]:
        raise ValueError("El ensamblado de procedencia no coincide con la recuperacion.")
    count = 0
    for entry in manifest["files"]:
        payload = safe_path(ROOT, entry["repository_path"]).read_bytes()
        if digest(payload) != entry["repository_sha256"]:
            raise ValueError("Archivo recuperado alterado: " + entry["recovered_path"])
        if entry["storage"] == "aes256_gcm":
            if not payload.startswith(HEADER):
                raise ValueError("Cabecera de cifrado invalida.")
            start = len(HEADER)
            payload = AESGCM(key).decrypt(payload[start:start + 12], payload[start + 12:], entry["associated_data"].encode("utf-8"))
        elif entry["storage"] != "unchanged":
            raise ValueError("Almacenamiento desconocido.")
        if digest(payload) != entry["recovered_sha256"] or len(payload) != entry["recovered_size"]:
            raise ValueError("La fuente no coincide con la salida del descompilador.")
        output = safe_path(destination, entry["recovered_path"])
        if output.exists():
            if not output.is_file() or digest(output.read_bytes()) != entry["recovered_sha256"]:
                raise ValueError("Se rechaza sobrescribir un archivo diferente: " + str(output))
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(payload)
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clave", type=Path, default=ROOT / ".local/clave_legado.key")
    parser.add_argument("--destino", type=Path, default=ROOT / ".local/v1_src")
    args = parser.parse_args()
    try:
        count = restore(args.clave, args.destino)
    except Exception:
        raise SystemExit("No se pudo restaurar v1. Revisa la clave, integridad y destino sin sobrescribir archivos distintos.") from None
    print(f"Archivos de descompilacion restaurados/verificados: {count}. No se ejecuto codigo del legado.")


if __name__ == "__main__":
    main()
