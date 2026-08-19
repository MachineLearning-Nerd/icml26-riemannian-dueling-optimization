# Environment and reproduction contract

## Fixed commands

```bash
uv sync --locked
uv run --locked python repro/src/verify.py
uv run --locked python repro/src/publication_gate.py
```

Independent package checks:

```bash
python reproduction/verify_claims.py
python reproduction/verify_claim4.py
cd reproduction
uv run --locked python cumulative_verify.py
uv run --locked python publication_gate.py
```

## Recorded run

The winning cumulative evidence run is `c7711be1-ba38-4dce-af0d-503b167f27d8`
with evidence Git SHA `73c4b84239cbcc71549f64c22ce0dcd7700c64e5`. It used a
Hugging Face `cpu-upgrade` environment, estimated 8 compute cores, 64 logical
CPUs, PyTorch capped at 8 threads, BLAS at one thread, and no GPU. The
scientific runtime was about 1339.44 seconds.

The lockfiles are authoritative. This cleanup records the existing accepted
evidence and its limitations; it does not silently substitute an untracked
rerun or claim that finite tests prove universal theorems.
