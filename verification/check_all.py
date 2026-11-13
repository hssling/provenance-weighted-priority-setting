"""Run every test module and the D1 demo; exit 1 on ANY failure, 0 only if everything passed.

Standard library only. A checker that prints FAILED and exits 0 verifies nothing, so every
failure path here sets the exit code, and "FAILED"/"Traceback" in a child's output fails it even if
the child returned 0. A test module that collects no tests (pytest exit 5) is a failure too.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BAD_MARKERS = ("FAILED", "Traceback (most recent call last)")


def run(label: str, cmd: list[str]) -> bool:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    out = proc.stdout + proc.stderr
    marker = next((m for m in BAD_MARKERS if m in out), None)
    ok = proc.returncode == 0 and marker is None
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    print(f"[{'ok' if ok else 'FAIL'}] {label}: {tail}")
    if not ok:
        why = f"exit code {proc.returncode}" if proc.returncode else f"output contains {marker!r}"
        print(f"       {why}\n" + "\n".join("       " + ln for ln in out.strip().splitlines()[-25:]))
    return ok


def main() -> int:
    modules = sorted((ROOT / "tests").glob("test_*.py"))
    if not modules:
        print("[FAIL] no test modules found")
        return 1
    results = [run(m.name, [sys.executable, "-m", "pytest", str(m), "-q", "-p", "no:cacheprovider"])
               for m in modules]
    results.append(run("demos/d1_tb.py", [sys.executable, str(ROOT / "demos" / "d1_tb.py")]))
    results.append(run("demos/d2_who_data_screen.py",
                       [sys.executable, str(ROOT / "demos" / "d2_who_data_screen.py")]))
    # Self-similarity gates on a factual condition (a long verbatim run), not a
    # percentage, so it is safe in the suite. It skips cleanly if a comparison
    # document is missing from this machine.
    results.append(run("verification/check_language.py",
                       [sys.executable, str(ROOT / "verification" / "check_language.py")]))
    results.append(run("verification/check_references.py",
                       [sys.executable, str(ROOT / "verification" / "check_references.py")]))
    results.append(run("verification/check_cross_references.py",
                       [sys.executable, str(ROOT / "verification" / "check_cross_references.py")]))
    results.append(run("verification/check_exhibit_order.py",
                       [sys.executable, str(ROOT / "verification" / "check_exhibit_order.py")]))
    results.append(run("verification/check_data_manifest.py",
                       [sys.executable, str(ROOT / "verification" / "check_data_manifest.py")]))
    results.append(run("verification/check_manuscript_numbers.py",
                       [sys.executable, str(ROOT / "verification" / "check_manuscript_numbers.py")]))
    results.append(run("verification/check_self_similarity.py",
                       [sys.executable, str(ROOT / "verification" / "check_self_similarity.py")]))
    failed = results.count(False)
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
