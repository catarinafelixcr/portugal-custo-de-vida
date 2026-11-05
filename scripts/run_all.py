"""
Runs every data script in order. Usage (from the project folder):
    .venv\Scripts\activate
    python scripts/run_all.py
"""
import runpy
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SCRIPTS = [
    "01_populacao.py",
    "02_dim_municipio.py",
    "03_salarios.py",
    "04_habitacao.py",
    "05_salario_minimo.py",
]

start = time.time()
for name in SCRIPTS:
    print(f"\n=== {name} ===")
    runpy.run_path(str(HERE / name), run_name="__main__")

print(f"\nDone in {time.time() - start:.0f}s. Files are in data/clean/")
