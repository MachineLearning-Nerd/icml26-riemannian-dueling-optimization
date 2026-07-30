from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[3] / ".trackio/logbook/reproduction/verify_claims.py"))
