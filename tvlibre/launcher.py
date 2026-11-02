"""Instalación verificada y activación reversible de dumbtv."""

from pathlib import Path
import hashlib
import os
import re
import time
import urllib.request

from .adb import TVLibreError
from . import core


def catalog():
    return core.read_json(core.ROOT / "integrations/launchers.json")


def checksum(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def download(identifier, destination):
    entries = {entry["id"]: entry for entry in catalog()}
    entry = entries.get(identifier)
    if not entry or "sha256" not in entry:
        raise TVLibreError("Esa integración solo tiene guía manual o no está en el catálogo.")
    target = Path(destination)
    if target.exists():
        raise TVLibreError("El destino ya existe. Elige otro para no sobrescribirlo.")
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".part")
    try:
        request = urllib.request.Request(entry["apk_url"], headers={"User-Agent": "TVLibre/0.1"})
        with urllib.request.urlopen(request, timeout=45) as response, partial.open("wb") as f:
            count = 0
            while True:
                block = response.read(65536)
                if not block:
                    break
                count += len(block)
                if count > 30 * 1024 * 1024:
                    raise TVLibreError("Descarga inesperadamente grande; se ha detenido.")
                f.write(block)
        if checksum(partial) != entry["sha256"]:
            raise TVLibreError("SHA-256 incorrecto. El APK descargado no se instalará.")
        os.replace(partial, target)
    finally:
        partial.unlink(missing_ok=True)
    return {"path": str(target), "sha256": entry["sha256"], "id": identifier}


def install(adb, apk, sha256, directory="state", experimental=False):
    if not re.fullmatch(r"[0-9a-fA-F]{64}", sha256) or checksum(apk) != sha256.lower():
        raise TVLibreError("El SHA-256 esperado no coincide con el APK.")
    device = adb.device()
    core.supported(device, experimental)
    # Solo APK fijados del catálogo: no se usa un archivo desconocido como integración.
    if sha256.lower() not in {x.get("sha256") for x in catalog()}:
        raise TVLibreError("APK fuera del catálogo. Compilaciones propias: usa adb install -r tras revisar su manifiesto.")
    path = core.journal_path(directory, "launcher-install")
    info = {"schema": 1, "device": device, "action": "install-apk", "sha256": sha256.lower(),
            "note": "Este registro no desinstala apps ni revierte versiones. Lee docs/RESTAURACION.md."}
    previous = adb.run("shell", "pm path " + core.PACKAGE, check=False)
    paths = [s[8:] for s in previous.stdout.splitlines() if s.startswith("package:")]
    if paths:
        adb.run("pull", paths[0], str(path.parent / "previous.apk"), timeout=90)
        info["previous_apk"] = "previous.apk"
    core.write_json(path, info)
    print(f"Registro de instalación: {path}")
    result = adb.run("install", "-r", str(Path(apk).resolve()), check=False, timeout=120)
    if result.returncode or "Success" not in result.stdout:
        raise TVLibreError("No se instaló el APK. Si la firma es distinta, conserva la app y revisa la guía de migración.\n" + result.stdout + result.stderr)
    if core.PACKAGE not in adb.packages():
        raise TVLibreError("La instalación no corresponde al launcher esperado.")
    print("dumbtv instalado. La activación de Home es un paso separado.")


def bound_guard(dump, user=0):
    """Solo acepta el servicio en la sección de servicios vinculados del usuario."""
    active_user, inside = None, False
    for line in dump.splitlines():
        if "User state[" in line:
            active_user, inside = None, False
        match = re.search(r"attributes:\{id=(\d+)[,}]", line)
        if match:
            active_user = int(match.group(1))
        if active_user == user and re.match(r"\s*(Bound services|services):\s*\{", line):
            inside = True
        if inside:
            if ("Service[label=dumbtv home button," in line
                    or "Service[label=tv.dumbtv.home.Guard," in line):
                return True
            if "}" in line:
                inside = False
    return False


def activation_plan(adb, experimental=False):
    device = adb.device()
    core.supported(device, experimental)
    if device["sdk"] < 28:
        raise TVLibreError("Fire OS 6 requiere Keeper. TVLibre no automatiza esa ruta; consulta el proyecto dumbtv.")
    if core.PACKAGE not in adb.packages():
        raise TVLibreError("Instala dumbtv antes de activar Home.")
    secure, global_ = adb.settings("secure"), adb.settings("global")
    services = [x for x in secure.get("enabled_accessibility_services", "").split(":") if x]
    if any("com.spocky.projengmenu" in x for x in services):
        raise TVLibreError("Projectivy ya controla Home. Desactiva su redirección en sus ajustes antes de activar dumbtv.")
    operations = []
    if core.GUARD not in services and core.PACKAGE + "/.Guard" not in services:
        operations.append({"kind": "setting", "namespace": "secure", "key": "enabled_accessibility_services",
                           "before": secure.get("enabled_accessibility_services"),
                           "after": ":".join(services + [core.GUARD])})
    if secure.get("accessibility_enabled") != "1":
        operations.append({"kind": "setting", "namespace": "secure", "key": "accessibility_enabled",
                           "before": secure.get("accessibility_enabled"), "after": "1"})
    before = global_.get("alarm_manager_constants")
    parts = [x for x in (before or "").split(",") if x and not x.startswith("min_futurity=")]
    after = ",".join(parts + ["min_futurity=0"])
    if before != after:
        operations.append({"kind": "setting", "namespace": "global", "key": "alarm_manager_constants",
                           "before": before, "after": after})
    op = {"kind": "whitelist", "package": core.PACKAGE, "before": False, "after": True}
    if not core.current(adb, op):
        operations.append(op)
    return {"schema": 1, "purpose": "launcher", "device": device, "experimental": experimental,
            "operations": operations}


def activate(adb, directory="state", experimental=False):
    plan = activation_plan(adb, experimental)
    path = core.apply(adb, plan, directory)
    for _ in range(15):
        if bound_guard(adb.shell("dumpsys", "accessibility")):
            break
        time.sleep(1)
    else:
        raise TVLibreError(f"Fire OS no vinculó Guard. No se da Home por configurado. Restaura con --backup {path}")
    adb.shell("input", "keyevent", "KEYCODE_WAKEUP")
    adb.shell("am", "start", "-n", core.PACKAGE + "/.Home")
    return path


def verify(adb, test_home=False, experimental=False):
    if test_home:
        core.supported(adb.device(), experimental)
    secure = adb.settings("secure")
    services = secure.get("enabled_accessibility_services", "").split(":")
    enabled = secure.get("accessibility_enabled") == "1" and any(
        x in services for x in (core.GUARD, core.PACKAGE + "/.Guard"))
    result = {"enabled": enabled, "bound": bound_guard(adb.shell("dumpsys", "accessibility")),
              "foreground": adb.foreground(), "home_key": "no probado", "physical_remote": "pendiente de comprobar por la persona"}
    if test_home:
        adb.shell("input", "keyevent", "KEYCODE_WAKEUP")
        adb.shell("am", "start", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.LEANBACK_SETTINGS")
        time.sleep(2)
        away = adb.foreground()
        if not away or away.startswith(core.PACKAGE + "/"):
            raise TVLibreError("No se pudo salir del launcher; no se puede probar Home desde otra app.")
        adb.shell("input", "keyevent", "KEYCODE_HOME")
        result["home_key"] = False
        for _ in range(8):
            time.sleep(1)
            result["foreground"] = adb.foreground()
            if (result["foreground"] or "").startswith(core.PACKAGE + "/"):
                result["home_key"] = True
                break
    result["ok"] = enabled and result["bound"] and (not test_home or result["home_key"] is True)
    return result


def reboot_check(adb, experimental=False):
    core.supported(adb.device(), experimental)
    previous = adb.shell("cat", "/proc/sys/kernel/random/boot_id")
    # Se espera a que Android guarde los ajustes antes del reinicio directo de ADB.
    adb.shell("sync")
    time.sleep(12)
    adb.run("reboot", check=False, timeout=20)
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        time.sleep(3)
        try:
            adb.connect()
            if adb.shell("getprop", "sys.boot_completed") != "1":
                continue
            if adb.shell("cat", "/proc/sys/kernel/random/boot_id") == previous:
                continue
            # Primero se observa: no se abre Home ni se inyecta ninguna tecla.
            first = adb.foreground()
            foreground = first
            for _ in range(10):
                if foreground and foreground.startswith(core.PACKAGE + "/"):
                    break
                time.sleep(2)
                foreground = adb.foreground()
            return {"boot_changed": True, "first_foreground_observed": first,
                    "foreground_before_any_launch": foreground,
                    "autostart": bool(foreground and foreground.startswith(core.PACKAGE + "/"))}
        except TVLibreError:
            continue
    raise TVLibreError("No se ha podido comprobar el arranque en 180 segundos. Revisa el TV; no se reiniciará otra vez.")
