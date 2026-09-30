import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parents[1]
sha = lambda b: hashlib.sha256(b).hexdigest()
failures = []
counts = {"recovered_files": 0, "antecedent_files": 0, "public_text_files_scanned": 0}
key = (ROOT / ".local/clave_legado.key").read_bytes()
manifest = json.loads((ROOT / "evidencia/ingenieria_inversa/recuperacion_v1.json").read_text(encoding="utf-8"))
for entry in manifest["files"]:
    path = ROOT / entry["repository_path"]
    data = path.read_bytes()
    if sha(data) != entry["repository_sha256"]:
        failures.append("Hash almacenado: " + entry["repository_path"])
    if entry["storage"] == "aes256_gcm":
        offset = len(b"RRHH-AESGCM-v1\n")
        data = AESGCM(key).decrypt(data[offset:offset + 12], data[offset + 12:], entry["associated_data"].encode())
    if sha(data) != entry["recovered_sha256"]:
        failures.append("Hash decompilacion: " + entry["recovered_path"])
    counts["recovered_files"] += 1
audit = json.loads((ROOT / "evidencia/ingenieria_inversa/auditoria_antecedente.json").read_text(encoding="utf-8"))
for entry in audit["files"]:
    if sha((ROOT / entry["repository_path"]).read_bytes()) != entry["sha256"]:
        failures.append("Antecedente diferente: " + entry["repository_path"])
    counts["antecedent_files"] += 1
for entry in audit["pdf_inventory"]:
    if sha((ROOT / entry["path"]).read_bytes()) != entry["sha256"]:
        failures.append("PDF diferente: " + entry["path"])
changed_baseline = subprocess.run(["git", "diff", "--name-only", "e1ead41", "--", "legado/", "evidencia/baseline/", "datos/", ".gitignore", ".env.example"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
if changed_baseline:
    failures.append("Baseline modificado")
source_text = (ROOT / ".local/v1_src/ClassRRHH.My/MySettings.cs").read_text(encoding="utf-8-sig")
encoded = re.findall(r'DefaultSettingValue\("([^"\n]+)"\)', source_text)
passwords = []
for config in (ROOT / ".local/RRHH").rglob("*.config"):
    document = ET.fromstring(config.read_bytes())
    for node in document.iter():
        for value in [node.text or "", *node.attrib.values()]:
            passwords.extend(re.findall(r"(?:Password|Pwd)\s*=\s*([^;\s]+)", value, re.I))
names = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.relative_to(ROOT).parts[0] not in {'.git', '.local', 'legado'}}
for name in names:
    file = ROOT / name
    if not file.is_file() or file.suffix not in {".py", ".cs", ".vb", ".md", ".json", ".txt"}:
        continue
    text = file.read_text(encoding="utf-8-sig")
    if any(value in text for value in encoded):
        failures.append("Default codificado expuesto: " + name)
    for value in passwords:
        if len(value) >= 6 and value in text:
            failures.append("Credencial conocida expuesta: " + name)
    if "\ufffd" in text:
        failures.append("Caracter de reemplazo en texto nuevo: " + name)
    counts["public_text_files_scanned"] += 1
compilation = json.loads((ROOT / "evidencia/ingenieria_inversa/compilacion_v1.json").read_text(encoding="utf-8"))
if compilation["exit_code"] != 0 or compilation["source_files"] != 12 or compilation["error_codes"]:
    failures.append("Compilacion no verificada")
api = json.loads((ROOT / "evidencia/ingenieria_inversa/comparacion_api.json").read_text(encoding="utf-8"))
if not api["all_match"]:
    failures.append("API diferente")
result = {"stage":"C02", "ok": not failures, "counts": counts,
          "baseline_changed": bool(changed_baseline), "compilation_passed": compilation["exit_code"] == 0,
          "api_four_business_classes_match": api["all_match"], "encoded_settings_count_withheld": len(encoded),
          "secret_scan_scope": "Archivos publicos de texto contra contrasenas conocidas de al menos seis caracteres y seis defaults codificados; no certifica ausencia de secretos desconocidos.",
          "application_executed": False, "database_connected":False, "functional_equivalence_verified":False,
          "failures":failures}
(ROOT / "evidencia/ingenieria_inversa/verificacion_c02.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
if failures:
    raise SystemExit(1)
