#!/usr/bin/env python3
"""Overlay the candidate text files on a fresh exact judged-Space clone."""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST = (
    ROOT / ".openresearch/artifacts/release/upload_allowlist.txt"
).read_text().splitlines()
SOURCE_MAP = {
    "reproduction/dense_spd.py": ROOT / "repro/src/dense_spd.py",
    "reproduction/empirical_algorithms.py": ROOT / "repro/src/empirical_algorithms.py",
    "reproduction/real_applications.py": ROOT / "repro/src/real_applications.py",
    "reproduction/theorem_audit.py": ROOT / "repro/src/theorem_audit.py",
    "reproduction/verify_claim4_source.py": ROOT / "repro/src/verify_claim4.py",
    "reproduction/cumulative_verify.py": ROOT / "repro/src/verify.py",
    "reproduction/publication_gate.py": ROOT / "repro/src/publication_gate.py",
    "reproduction/pyproject.toml": ROOT / "pyproject.toml",
    "reproduction/uv.lock": ROOT / "uv.lock",
}


def source_for(destination: str) -> Path:
    if destination in SOURCE_MAP:
        return SOURCE_MAP[destination]
    return ROOT / ".trackio/logbook" / destination


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: package_space.py JUDGED_CLONE CANDIDATE_DIR")
    judged = Path(sys.argv[1]).resolve()
    candidate = Path(sys.argv[2]).resolve()
    assert judged.is_dir()
    assert not candidate.exists()
    shutil.copytree(judged, candidate, ignore=shutil.ignore_patterns(".git"))
    for destination in ALLOWLIST:
        source = source_for(destination)
        assert source.is_file(), source
        target = candidate / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        target.read_text()
    manifest = "\n".join(
        f"{digest(candidate / path)}  {path}" for path in ALLOWLIST
    )
    (candidate / "CANDIDATE_MANIFEST.sha256").write_text(manifest + "\n")
    print(f"candidate_files={len(ALLOWLIST)}")
    print(f"candidate_manifest={candidate / 'CANDIDATE_MANIFEST.sha256'}")


if __name__ == "__main__":
    main()
