"""Pruebas de fallos y recuperación. Ninguna accede a un dispositivo real."""

import copy
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from firelibre.adb import ADB, FireLibreError
from firelibre import core, launcher
from firelibre.cli import main


class FakeTV:
    def __init__(self):
        self.info = {"manufacturer": "Amazon", "model": "AFTSSS", "sdk": 28,
                     "device": "sheldonp", "android": "9", "build": "TEST.1",
                     "identity": "synthetic-device-id", "user": 0}
        self.states = {p["id"]: 0 for p in core.profile("equilibrado")["packages"]}
        self.states[core.PACKAGE] = 0
        self.values = {"secure": {"other_service": "unrelated", "enabled_accessibility_services": "org.example.reader/.Service"},
                       "global": {"window_animation_scale": "1.0", "alarm_manager_constants": "other=200,min_futurity=5000"}}
        self.white = False
        self.fail_key = None
        self.mutations = []

    def device(self):
        return copy.deepcopy(self.info)

    def packages(self):
        return sorted(self.states)

    def package_state(self, package):
        return self.states[package]

    def settings(self, namespace):
        return self.values[namespace].copy()

    def shell(self, *args):
        self.mutations.append(args)
        if args[:2] == ("pm", "list"):
            return "\n".join("package:" + p for p, state in self.states.items() if state == 3)
        if args[0] == "pm":
            self.states[args[-1]] = {"default-state": 0, "enable": 1, "disable-user": 3}[args[1]]
            return "ok"
        if args[0] == "settings":
            offset = 3 if args[1] == "--user" else 1
            command, namespace, key = args[offset:offset + 3]
            if command == "delete":
                self.values[namespace].pop(key, None)
            else:
                self.values[namespace][key] = args[offset + 3]
            if key == self.fail_key:
                self.fail_key = None
                raise FireLibreError("Corte de conexión después de escribir")
            return ""
        if args[:3] == ("dumpsys", "deviceidle", "whitelist"):
            if len(args) > 3:
                self.white = args[3].startswith("+")
            return "user," + core.PACKAGE + ",10000" if self.white else ""
        raise AssertionError(args)


class Plans(unittest.TestCase):
    def setUp(self):
        self.tv = FakeTV()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

    def test_keep_and_already_disabled_are_preserved(self):
        self.tv.states["com.amazon.tv.acr"] = 3
        plan = core.make_plan(self.tv, keep=["com.amazon.dp.logger"])
        packages = [o["package"] for o in plan["operations"] if o["kind"] == "package"]
        self.assertNotIn("com.amazon.tv.acr", packages)
        self.assertNotIn("com.amazon.dp.logger", packages)

    def test_exact_roundtrip_default_explicit_and_missing_settings(self):
        self.tv.states["com.amazon.dp.logger"] = 1
        before = copy.deepcopy((self.tv.states, self.tv.values))
        plan = core.make_plan(self.tv)
        path = core.apply(self.tv, plan, self.temp.name)
        backup = core.read_json(path)
        self.assertTrue(core.verify(self.tv, backup)["ok"])
        core.restore(self.tv, backup, path)
        self.assertEqual((self.tv.states, self.tv.values), before)
        self.assertTrue(core.verify(self.tv, core.read_json(path))["ok"])

    def test_interruption_after_write_can_be_recovered(self):
        before = copy.deepcopy((self.tv.states, self.tv.values))
        self.tv.fail_key = "amz_limit_ad_tracking"
        with self.assertRaises(FireLibreError):
            core.apply(self.tv, core.make_plan(self.tv), self.temp.name)
        path = next(Path(self.temp.name).glob("*/backup.json"))
        backup = core.read_json(path)
        self.assertEqual(backup["status"], "interrupted")
        self.assertTrue(backup["operations"][-1].get("attempted") is False)
        core.restore(self.tv, backup, path)
        self.assertEqual((self.tv.states, self.tv.values), before)

    def test_different_tv_or_firmware_is_rejected_before_mutation(self):
        plan = core.make_plan(self.tv)
        self.tv.info["identity"] = "another-device"
        with self.assertRaises(FireLibreError):
            core.apply(self.tv, plan, self.temp.name)
        self.assertFalse(self.tv.mutations)

    def test_drift_is_rejected_before_any_change(self):
        plan = core.make_plan(self.tv)
        self.tv.values["global"]["window_animation_scale"] = "0.75"
        with self.assertRaises(FireLibreError):
            core.apply(self.tv, plan, self.temp.name)
        self.assertFalse(self.tv.mutations)

    def test_tampered_plan_cannot_disable_launcher_or_ota(self):
        for package in ("com.amazon.tv.launcher", "com.amazon.device.software.ota", "com.netflix.ninja"):
            plan = core.make_plan(self.tv)
            plan["operations"][0]["package"] = package
            with self.assertRaises(FireLibreError):
                core.apply(self.tv, plan, self.temp.name)
        self.assertFalse(self.tv.mutations)

    def test_tampered_plan_cannot_write_arbitrary_setting(self):
        plan = core.make_plan(self.tv)
        plan["operations"].append({"kind": "setting", "namespace": "global", "key": "adb_enabled", "before": "1", "after": "0"})
        with self.assertRaises(FireLibreError):
            core.apply(self.tv, plan, self.temp.name)

    def test_conflicting_later_change_is_not_overwritten(self):
        path = core.apply(self.tv, core.make_plan(self.tv), self.temp.name)
        self.tv.values["global"]["window_animation_scale"] = "0.75"
        with self.assertRaises(FireLibreError):
            core.restore(self.tv, core.read_json(path), path)
        self.assertEqual(self.tv.values["global"]["window_animation_scale"], "0.75")
        self.assertTrue(all(s == 0 for s in self.tv.states.values()))

    def test_unknown_platform_never_mutates(self):
        for manufacturer, sdk in [("Amazon", 22), ("Amazon", 34), ("Google", 28), ("Amazon", 0)]:
            self.tv.info.update(manufacturer=manufacturer, sdk=sdk)
            with self.assertRaises(FireLibreError):
                core.make_plan(self.tv, experimental=True)

    def test_untested_model_requires_explicit_flag(self):
        self.tv.info["model"] = "SYNTHETIC-UNTESTED"
        with self.assertRaises(FireLibreError):
            core.make_plan(self.tv)
        self.assertTrue(core.make_plan(self.tv, experimental=True)["experimental"])

    def test_other_user_is_read_only(self):
        self.tv.info["user"] = 10
        with self.assertRaises(FireLibreError):
            core.make_plan(self.tv)

    def test_unexecuted_plan_is_not_a_successful_verification(self):
        with self.assertRaises(FireLibreError):
            core.verify(self.tv, core.make_plan(self.tv))

    def test_non_object_json_is_rejected(self):
        with self.assertRaises(FireLibreError):
            core.validate([])

    def test_mid_session_drift_is_preserved(self):
        plan = core.make_plan(self.tv)
        original = core.set_value

        def write_and_drift(adb, op, value):
            original(adb, op, value)
            adb.values["secure"]["amz_limit_ad_tracking"] = "new-user-choice"

        with patch.object(core, "set_value", side_effect=write_and_drift):
            with self.assertRaises(FireLibreError):
                core.apply(self.tv, plan, self.temp.name)
        self.assertEqual(self.tv.values["secure"]["amz_limit_ad_tracking"], "new-user-choice")

    def test_launcher_roundtrip_preserves_reader_alarm_and_battery_state(self):
        before = copy.deepcopy(self.tv.values)
        plan = launcher.activation_plan(self.tv)
        self.assertIn("org.example.reader/.Service:", next(o["after"] for o in plan["operations"] if o.get("key") == "enabled_accessibility_services"))
        path = core.apply(self.tv, plan, self.temp.name)
        self.assertTrue(self.tv.white)
        core.restore(self.tv, core.read_json(path), path)
        self.assertEqual(self.tv.values, before)
        self.assertFalse(self.tv.white)

    def test_projectivy_conflict_is_not_overridden(self):
        self.tv.values["secure"]["enabled_accessibility_services"] = "com.spocky.projengmenu/.Service"
        with self.assertRaises(FireLibreError):
            launcher.activation_plan(self.tv)

    def test_already_active_launcher_has_no_redundant_writes(self):
        self.tv.values["secure"].update(enabled_accessibility_services=core.GUARD, accessibility_enabled="1")
        self.tv.values["global"]["alarm_manager_constants"] = "other=200,min_futurity=0"
        self.tv.white = True
        self.assertEqual(launcher.activation_plan(self.tv)["operations"], [])


class ParsingAndTransport(unittest.TestCase):
    def test_binding_is_not_inferred_from_enabled_list(self):
        wrong = "User state[attributes:{id=0, x}\n services:{}\n Enabled services:{Service[label=dumbtv home button, x]}"
        right = "User state[attributes:{id=0, x}\n services:{Service[label=dumbtv home button, x]}"
        other_user = right.replace("id=0", "id=10")
        self.assertFalse(launcher.bound_guard(wrong))
        self.assertTrue(launcher.bound_guard(right))
        self.assertFalse(launcher.bound_guard(other_user))
        self.assertFalse(launcher.bound_guard(right.replace("button,", "button extra,")))

    def test_selected_device_and_remote_shell_quoting(self):
        with patch("shutil.which", return_value="/test/adb"), patch("subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "ok\n", "")
            adb = ADB("192.0.2.10:5555")
            adb.shell("settings", "put", "secure", "example", "a;$(touch nope)")
            command = run.call_args.args[0]
            self.assertEqual(command[:4], ["/test/adb", "-s", "192.0.2.10:5555", "shell"])
            self.assertIn("'a;$(touch nope)'", command[-1])

    def test_invalid_serial(self):
        with self.assertRaises(FireLibreError):
            ADB("-H other-device")

    def test_legacy_fire_os_settings_list_has_no_user_flag(self):
        with patch("shutil.which", return_value="/test/adb"), patch("subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "sample=value\n", "")
            adb = ADB("192.0.2.10:5555")
            self.assertEqual(adb.settings("secure"), {"sample": "value"})
            self.assertEqual(run.call_args.args[0][-1], "settings list secure")

    def test_mutating_cli_without_yes_never_connects(self):
        with patch("firelibre.cli.ADB") as adb, patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(main(["--serial", "192.0.2.10:5555", "apply", "--plan", "fake.json"]), 1)
            adb.assert_not_called()

    def test_checksum_failure_keeps_no_download(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "launcher.apk"
            entry = {"id": "dumbtv-es", "apk_url": "https://example.invalid/apk", "sha256": "0" * 64}
            with patch.object(launcher, "catalog", return_value=[entry]), patch("urllib.request.urlopen", return_value=io.BytesIO(b"unexpected")):
                with self.assertRaises(FireLibreError):
                    launcher.download("dumbtv-es", target)
            self.assertFalse(target.exists())
            self.assertFalse(target.with_suffix(".apk.part").exists())

    def test_unrecognized_operation_is_rejected(self):
        plan = core.make_plan(FakeTV())
        plan["operations"].append({"kind": "arbitrary-shell", "command": "rm -rf /"})
        with self.assertRaises(FireLibreError):
            core.validate(plan)

    def test_reboot_observes_autostart_without_launching_or_pressing_home(self):
        tv = FakeTV()
        tv.connect = lambda: None
        tv.run = lambda *args, **kwargs: None
        tv.foreground = unittest.mock.Mock(side_effect=["com.amazon.tv.launcher/.Home", core.PACKAGE + "/.Home"])
        tv.shell = unittest.mock.Mock(side_effect=["boot-before", "", "1", "boot-after"])
        with patch("time.sleep"):
            result = launcher.reboot_check(tv)
        self.assertTrue(result["autostart"])
        self.assertEqual(result["first_foreground_observed"], "com.amazon.tv.launcher/.Home")
        self.assertFalse(any(c.args[0] in ("am", "input") for c in tv.shell.call_args_list))


if __name__ == "__main__":
    unittest.main()
