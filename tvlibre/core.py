"""Planes verificables y diario de restauración del estado anterior."""

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import re
import uuid

from .adb import TVLibreError

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "tv.dumbtv.home"
GUARD = PACKAGE + "/" + PACKAGE + ".Guard"
PROFILES = ("conservador", "equilibrado")


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise TVLibreError(f"No se puede leer el JSON {path}: {error}") from error


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", encoding="utf-8") as f:
        if os.name != "nt":
            os.chmod(temp, 0o600)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


def profile(name):
    if name not in PROFILES:
        raise TVLibreError("Perfil desconocido.")
    return read_json(ROOT / "profiles" / (name + ".json"))


def supported(device, experimental=False):
    if not device.get("identity") or device.get("user") != 0:
        raise TVLibreError("Se necesita identidad estable y usuario principal 0 para cambiar el TV.")
    if not device["manufacturer"].lower().startswith("amazon") or device["sdk"] not in (25, 28, 29, 30):
        raise TVLibreError("Esta plataforma solo permite diagnóstico en TVLibre 0.1. Lee Compatibilidad.")
    if (device["model"], device["sdk"]) != ("AFTSSS", 28) and not experimental:
        raise TVLibreError("Modelo pendiente de validar. Solo diagnóstico; --experimental habilita una prueba explícita.")


def same_device(expected, actual):
    for key in ("identity", "model", "sdk", "build", "user"):
        if expected.get(key) != actual.get(key):
            raise TVLibreError(f"El dispositivo o firmware ha cambiado ({key}). No se aplicará este archivo.")


def protected_packages():
    return set(read_json(ROOT / "profiles/protegidos.json")["packages"])


def inventory(adb):
    device = adb.device()
    return {"schema": 1, "device": device, "packages": adb.packages(),
            "disabled": adb.shell("pm", "list", "packages", "-d", "--user", "0").splitlines(),
            "scope": "Inventario local. No mide tráfico ni prueba reproducción de vídeo."}


def make_plan(adb, name="equilibrado", keep=(), experimental=False):
    device = adb.device()
    supported(device, experimental)
    rules = profile(name)
    installed = set(adb.packages())
    blocked = protected_packages() | set(keep)
    operations, skipped = [], []
    for item in rules["packages"]:
        pkg = item["id"]
        if pkg in blocked:
            skipped.append({"package": pkg, "reason": "Protegido o conservado expresamente"})
        elif pkg not in installed:
            skipped.append({"package": pkg, "reason": "No instalado para el usuario 0"})
        else:
            before = adb.package_state(pkg)
            if before in (2, 3, 4):
                skipped.append({"package": pkg, "reason": "Ya estaba deshabilitado"})
            elif before in (0, 1):
                operations.append({"kind": "package", "package": pkg, "before": before,
                                   "after": 3, "reason": item["reason"]})
            else:
                raise TVLibreError(f"Estado de paquete desconocido: {pkg}: {before}")
    namespaces = {n: adb.settings(n) for n in ("secure", "global")}
    for item in rules["settings"]:
        before = namespaces[item["namespace"]].get(item["key"])
        if before != item["value"]:
            operations.append({"kind": "setting", "namespace": item["namespace"],
                               "key": item["key"], "before": before, "after": item["value"],
                               "reason": item["reason"]})
    return {"schema": 1, "purpose": "cleanup", "profile": name, "device": device,
            "experimental": experimental, "operations": operations, "skipped": skipped,
            "notes": ["Alexa, casting, apps personales y actualizaciones se conservan.",
                      "Los interruptores de privacidad sincronizados con Amazon se revisan también con el mando."]}


def validate(document):
    if not isinstance(document, dict) or document.get("schema") != 1 or document.get("purpose") not in ("cleanup", "launcher"):
        raise TVLibreError("Esquema o propósito de archivo desconocido.")
    if not isinstance(document.get("experimental"), bool):
        raise TVLibreError("Falta el indicador de compatibilidad experimental.")
    device = document.get("device", {})
    if not isinstance(device, dict) or not device.get("identity") or device.get("user") != 0:
        raise TVLibreError("El archivo no identifica un dispositivo.")
    operations = document.get("operations")
    if not isinstance(operations, list):
        raise TVLibreError("Falta la lista de operaciones.")
    rules = profile(document["profile"]) if document["purpose"] == "cleanup" else None
    packages = {p["id"] for p in rules["packages"]} if rules else set()
    settings = {(s["namespace"], s["key"]): s["value"] for s in rules["settings"]} if rules else {}
    seen = set()
    for op in operations:
        kind = op.get("kind")
        if kind == "package":
            pkg = op.get("package", "")
            if pkg not in packages or pkg in protected_packages() or op.get("before") not in (0, 1) or op.get("after") != 3:
                raise TVLibreError("El plan intenta cambiar un paquete fuera del perfil permitido.")
            key = (kind, pkg)
        elif kind == "setting":
            ns, name, value = op.get("namespace"), op.get("key"), op.get("after")
            if op.get("before") is not None and not isinstance(op["before"], str):
                raise TVLibreError("Valor anterior de ajuste inválido.")
            allowed = (ns, name) in settings and settings[(ns, name)] == value
            if document["purpose"] == "launcher":
                before = op.get("before")
                if (ns, name) == ("secure", "enabled_accessibility_services"):
                    services = [s for s in (before or "").split(":") if s]
                    allowed = value == ":".join(services + ([GUARD] if GUARD not in services else []))
                elif (ns, name) == ("secure", "accessibility_enabled"):
                    allowed = value == "1"
                elif (ns, name) == ("global", "alarm_manager_constants"):
                    parts = [s for s in (before or "").split(",") if s and not s.startswith("min_futurity=")]
                    allowed = value == ",".join(parts + ["min_futurity=0"])
            if not allowed:
                raise TVLibreError("El plan intenta cambiar un ajuste fuera de la política.")
            key = (kind, ns, name)
        elif kind == "whitelist" and document["purpose"] == "launcher":
            if op.get("package") != PACKAGE or not isinstance(op.get("before"), bool) or op.get("after") is not True:
                raise TVLibreError("Exención de batería inválida.")
            key = (kind, PACKAGE)
        else:
            raise TVLibreError("Tipo de operación desconocido.")
        if key in seen:
            raise TVLibreError("Operación duplicada en el plan.")
        seen.add(key)


def current(adb, op):
    if op["kind"] == "package":
        return adb.package_state(op["package"])
    if op["kind"] == "setting":
        return adb.settings(op["namespace"]).get(op["key"])
    if op["kind"] == "whitelist":
        raw = adb.shell("dumpsys", "deviceidle", "whitelist")
        return any(line.split(",")[1:2] == [op["package"]] for line in raw.splitlines())
    raise TVLibreError("Operación desconocida.")


def set_value(adb, op, value):
    if op["kind"] == "package":
        command = {0: "default-state", 1: "enable", 3: "disable-user"}[value]
        adb.shell("pm", command, "--user", "0", op["package"])
    elif op["kind"] == "setting":
        if value is None:
            if adb.device()["user"] != 0:
                raise TVLibreError("El usuario activo cambió; no se eliminará el ajuste.")
            adb.shell("settings", "delete", op["namespace"], op["key"])
        else:
            adb.shell("settings", "--user", "0", "put", op["namespace"], op["key"], value)
    else:
        adb.shell("dumpsys", "deviceidle", "whitelist", ("+" if value else "-") + op["package"])


def journal_path(directory, purpose):
    path = Path(directory) / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + purpose + "-" + uuid.uuid4().hex[:8])
    path.mkdir(parents=True, exist_ok=False)
    if os.name != "nt":
        path.chmod(0o700)
    return path / "backup.json"


def apply(adb, plan, directory="state"):
    validate(plan)
    actual = adb.device()
    supported(actual, plan["experimental"])
    same_device(plan["device"], actual)
    for op in plan["operations"]:
        if current(adb, op) != op["before"]:
            raise TVLibreError("El estado ha cambiado desde el plan. Genera otro antes de continuar.")
    path = journal_path(directory, plan["purpose"])
    backup = {**plan, "status": "applying", "operations": [dict(op, attempted=False) for op in plan["operations"]]}
    write_json(path, backup)
    print(f"Copia de restauración: {path}", flush=True)
    try:
        for op in backup["operations"]:
            if current(adb, op) != op["before"]:
                raise TVLibreError("El estado cambió durante la sesión; no se sobrescribirá ese cambio.")
            op["attempted"] = True
            write_json(path, backup)  # Primero se registra; después se cambia el dispositivo.
            set_value(adb, op, op["after"])
            if current(adb, op) != op["after"]:
                raise TVLibreError(f"El sistema no aceptó el cambio: {op.get('package', op.get('key'))}")
            op["applied"] = True
            write_json(path, backup)
            print("Aplicado:", op.get("package", op.get("key")), flush=True)
        backup["status"] = "applied"
        write_json(path, backup)
    except BaseException as error:
        backup["status"] = "interrupted"
        backup["error"] = str(error)
        write_json(path, backup)
        print(f"Operación interrumpida. Para deshacer usa restore --backup {path}", flush=True)
        raise
    return path


def restore(adb, backup, path):
    validate(backup)
    require_journal(backup)
    same_device(backup["device"], adb.device())
    conflicts = []
    for op in reversed(backup["operations"]):
        if not op.get("attempted"):
            continue
        actual = current(adb, op)
        if actual == op["before"]:
            op["restored"] = True
        elif actual != op["after"]:
            conflicts.append(op.get("package", op.get("key")))
            continue
        else:
            try:
                set_value(adb, op, op["before"])
                if current(adb, op) != op["before"]:
                    raise TVLibreError("El valor restaurado no coincide.")
                op["restored"] = True
            except TVLibreError as error:
                conflicts.append(op.get("package", op.get("key")))
                op["restore_error"] = str(error)
        write_json(path, backup)
    backup["status"] = "restore-conflicts" if conflicts else "restored"
    write_json(path, backup)
    if conflicts:
        raise TVLibreError("Restauración parcial; hay cambios posteriores o errores en: " + ", ".join(conflicts))
    return backup


def verify(adb, backup):
    validate(backup)
    require_journal(backup)
    same_device(backup["device"], adb.device())
    result = []
    for op in backup["operations"]:
        if not op.get("attempted"):
            continue
        expected = op["before"] if op.get("restored") else op["after"]
        value = current(adb, op)
        result.append({"item": op.get("package", op.get("key")), "expected": expected,
                       "actual": value, "ok": value == expected})
    return {"ok": all(r["ok"] for r in result), "checks": result,
            "scope": "Comprueba estados ADB, no ausencia de telemetría, reproducción ni cuentas."}


def require_journal(backup):
    if backup.get("status") not in ("applying", "applied", "interrupted", "restored", "restore-conflicts"):
        raise TVLibreError("Se necesita un diario backup.json generado al aplicar, no un plan sin ejecutar.")
    if any(not isinstance(op.get("attempted"), bool) for op in backup["operations"]):
        raise TVLibreError("El diario no registra correctamente las operaciones intentadas.")
