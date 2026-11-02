"""Puente ADB limitado al dispositivo elegido explícitamente."""

import hashlib
import re
import shlex
import shutil
import subprocess
import time


class FireLibreError(RuntimeError):
    pass


class ADB:
    def __init__(self, serial, binary="adb"):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:\[\]-]*", serial):
            raise FireLibreError("Identificador ADB inválido.")
        self.serial = serial
        self.binary = shutil.which(binary)
        if not self.binary:
            raise FireLibreError("No se encuentra adb. Instala Android Platform Tools.")

    def run(self, *args, check=True, timeout=40):
        try:
            p = subprocess.run([self.binary, "-s", self.serial, *args],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise FireLibreError(f"ADB no ha completado la operación: {error}") from error
        if check and p.returncode:
            raise FireLibreError((p.stderr or p.stdout).strip())
        return p.stdout.strip() if check else p

    def shell(self, *args):
        return self.run("shell", shlex.join([str(a) for a in args]))

    def connect(self):
        if ":" in self.serial:
            self.run("connect", self.serial, check=False, timeout=15)
        state = self.run("get-state", check=False)
        if "unauthorized" in state.stderr + state.stdout:
            raise FireLibreError("Acepta «Permitir depuración USB» en el televisor y repite.")
        if state.stdout.strip() == "offline" or "offline" in state.stderr:
            self.run("reconnect", check=False)
            time.sleep(1)
            state = self.run("get-state", check=False)
        if state.returncode or state.stdout.strip() != "device":
            raise FireLibreError("El dispositivo no está conectado. Revisa IP, alimentación y ADB.")

    def device(self):
        names = {
            "manufacturer": "ro.product.manufacturer", "model": "ro.product.model",
            "device": "ro.product.device", "sdk": "ro.build.version.sdk",
            "android": "ro.build.version.release", "build": "ro.build.display.id",
        }
        result = {k: self.shell("getprop", v) for k, v in names.items()}
        result["sdk"] = int(result["sdk"] or 0)
        raw = self.shell("getprop", "ro.serialno")
        if not raw or raw == "unknown":
            raw = self.shell("settings", "--user", "0", "get", "secure", "android_id")
        result["identity"] = hashlib.sha256(raw.encode()).hexdigest() if raw and raw != "null" else None
        result["user"] = int(self.shell("am", "get-current-user"))
        return result

    def settings(self, namespace):
        # Fire OS 7 admite --user en get/put, pero lo rechaza en list/delete.
        # El motor exige usuario activo 0 antes de planificar o modificar ajustes.
        raw = self.shell("settings", "list", namespace)
        return dict(line.split("=", 1) for line in raw.splitlines() if "=" in line)

    def packages(self):
        text = self.shell("pm", "list", "packages", "--user", "0")
        return sorted(line[8:] for line in text.splitlines() if line.startswith("package:"))

    def package_state(self, package):
        dump = self.shell("dumpsys", "package", package)
        match = re.search(r"User 0:[^\n]*\benabled=(\d+)", dump)
        if not match:
            raise FireLibreError(f"No se puede leer el estado de {package}.")
        return int(match.group(1))

    def foreground(self):
        dump = self.shell("dumpsys", "activity", "activities")
        match = re.search(r"m(?:Top)?ResumedActivity:.*?\bu\d+ ([\w.]+/[\w.$]+)", dump)
        return match.group(1) if match else None
