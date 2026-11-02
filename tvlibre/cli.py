"""Interfaz de línea de órdenes en español."""

import argparse
import json
import sys
from . import __version__, core, launcher
from .adb import ADB, TVLibreError


def parser():
    p = argparse.ArgumentParser(description="TVLibre — diagnóstico Android TV y herramientas reversibles para Fire TV")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--serial", help="IP:5555 o identificador ADB. Obligatorio para acceder al TV.")
    p.add_argument("--adb", default="adb", help="Ruta de Android Platform Tools/adb")
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("doctor", "inventory"):
        item = sub.add_parser(name, help="Diagnóstico o inventario sin cambiar el TV")
        item.add_argument("--out", help="Guardar JSON local")
    plan = sub.add_parser("plan", help="Generar un plan sin aplicar cambios")
    plan.add_argument("--profile", choices=core.PROFILES, default="equilibrado")
    plan.add_argument("--keep", nargs="*", default=[], help="Paquetes que deseas conservar")
    plan.add_argument("--out", required=True)
    plan.add_argument("--experimental", action="store_true")
    apply = sub.add_parser("apply", help="Aplicar el plan revisado y guardar un diario de restauración")
    apply.add_argument("--plan", required=True)
    apply.add_argument("--backup-dir", default="state")
    apply.add_argument("--yes", action="store_true")
    for name in ("verify", "restore"):
        item = sub.add_parser(name)
        item.add_argument("--backup", required=True, help="Ruta exacta a backup.json")
        if name == "restore":
            item.add_argument("--yes", action="store_true")
    item = sub.add_parser("launcher", help="Descarga, instalación y control de Home")
    commands = item.add_subparsers(dest="action", required=True)
    commands.add_parser("list")
    fetch = commands.add_parser("download")
    fetch.add_argument("--id", choices=("dumbtv-es", "dumbtv-oficial"), default="dumbtv-es")
    fetch.add_argument("--out", required=True)
    install = commands.add_parser("install")
    install.add_argument("--apk", required=True)
    install.add_argument("--sha256", required=True)
    install.add_argument("--backup-dir", default="state")
    install.add_argument("--experimental", action="store_true")
    install.add_argument("--yes", action="store_true")
    activate = commands.add_parser("activate")
    activate.add_argument("--backup-dir", default="state")
    activate.add_argument("--experimental", action="store_true")
    activate.add_argument("--yes", action="store_true")
    check = commands.add_parser("verify")
    check.add_argument("--test-home", action="store_true", help="Abre Ajustes y envía Home por ADB")
    check.add_argument("--experimental", action="store_true")
    reboot = commands.add_parser("reboot-check")
    reboot.add_argument("--yes", action="store_true")
    reboot.add_argument("--experimental", action="store_true")
    return p


def emit(value, out=None):
    if out:
        core.write_json(out, value)
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    try:
        if args.command == "launcher" and args.action == "list":
            emit(launcher.catalog())
            return 0
        if args.command == "launcher" and args.action == "download":
            emit(launcher.download(args.id, args.out))
            return 0
        if not args.serial:
            p.error("indica --serial antes del comando; no se elige un dispositivo por defecto")
        if hasattr(args, "yes") and not args.yes:
            raise TVLibreError("Revisa el plan o la guía y añade --yes para ejecutar esta operación.")
        adb = ADB(args.serial, args.adb)
        adb.connect()
        if args.command == "doctor":
            device = adb.device()
            try:
                core.supported(device)
                status = "Modelo de referencia AFTSSS; consulta la cobertura de pruebas en docs/COMPATIBILIDAD.md"
            except TVLibreError as error:
                status = str(error)
            emit({"device": device, "compatibility": status, "mode": "solo lectura"}, args.out)
        elif args.command == "inventory":
            emit(core.inventory(adb), args.out)
        elif args.command == "plan":
            emit(core.make_plan(adb, args.profile, args.keep, args.experimental), args.out)
        elif args.command == "apply":
            path = core.apply(adb, core.read_json(args.plan), args.backup_dir)
            print(f"Terminado. Verifica con: verify --backup {path}")
        elif args.command == "restore":
            core.restore(adb, core.read_json(args.backup), args.backup)
            print("Se ha restaurado el estado anterior de las operaciones registradas.")
        elif args.command == "verify":
            result = core.verify(adb, core.read_json(args.backup))
            emit(result)
            return 0 if result["ok"] else 1
        elif args.action == "install":
            launcher.install(adb, args.apk, args.sha256, args.backup_dir, args.experimental)
        elif args.action == "activate":
            path = launcher.activate(adb, args.backup_dir, args.experimental)
            print(f"Guard vinculado. Restauración de esta activación: {path}")
        elif args.action == "verify":
            result = launcher.verify(adb, args.test_home, args.experimental)
            emit(result)
            return 0 if result["ok"] else 1
        elif args.action == "reboot-check":
            result = launcher.reboot_check(adb, args.experimental)
            emit(result)
            return 0 if result["autostart"] else 1
        return 0
    except (TVLibreError, OSError, ValueError, KeyError, TypeError) as error:
        print("Error:", error, file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrumpido. Conserva el backup.json impreso antes del primer cambio.", file=sys.stderr)
        return 130
